"""Phase 2 class signatures for the 10-real-class Tiny ImageNet split.

Each signature computes a continuous confidence score based on how well
the image's color/texture stats match the class prototype. No hard
binary thresholds — the scorer ranks classes by soft similarity.
"""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.registry import get_feature, register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


def _stats(graph: SceneGraph) -> dict[str, float]:
    image = graph.raw_image
    if image is None:
        return {}
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    hue = hsv[:, :, 0]
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]
    warm = (((hue >= 5) & (hue <= 45)) | (hue <= 5)) & (sat > 50) & (val > 50)
    yellow = (hue >= 15) & (hue <= 45) & (sat > 70) & (val > 70)
    blue_purple = (hue >= 75) & (hue <= 145) & (sat > 45) & (val > 45)
    green = (hue >= 35) & (hue <= 85) & (sat > 30) & (val > 40)
    bw = ((gray < 60) | (gray > 200)) | (sat < 35)
    edges = cv2.Canny(gray, 50, 150)
    lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    warm_aspect = 1.0
    warm_coverage = float(warm.sum()) / (h * w)
    if warm_coverage > 0.02:
        num_labels, labels = cv2.connectedComponents((warm * 255).astype(np.uint8))
        if num_labels > 1:
            largest = 1 + np.argmax([(labels == i).sum() for i in range(1, num_labels)])
            ys, xs = np.where(labels == largest)
            if len(xs) and len(ys):
                bw_box = xs.max() - xs.min() + 1
                bh_box = ys.max() - ys.min() + 1
                warm_aspect = max(bw_box / max(bh_box, 1), bh_box / max(bw_box, 1))

    center = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
    border_mean = (
        gray[:h // 4, :].mean()
        + gray[3 * h // 4:, :].mean()
        + gray[:, :w // 4].mean()
        + gray[:, 3 * w // 4:].mean()
    ) / 4

    # LBP entropy (texture complexity)
    center_px = gray[1:-1, 1:-1].astype(np.int16)
    lbp_code = np.zeros_like(center_px, dtype=np.uint8)
    for bit, (dy, dx) in enumerate([(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]):
        neighbor = gray[1+dy:h-1+dy, 1+dx:w-1+dx].astype(np.int16)
        lbp_code |= ((neighbor >= center_px).astype(np.uint8) << bit)
    lbp_hist, _ = np.histogram(lbp_code, bins=64, range=(0, 256))
    lbp_hist = lbp_hist / (lbp_hist.sum() + 1e-9)
    lbp_entropy = float(-np.sum(lbp_hist[lbp_hist > 0] * np.log2(lbp_hist[lbp_hist > 0])))

    # Symmetry (left-right pixel similarity)
    left_half = gray[:, :w//2]
    right_half = gray[:, w//2:][:, ::-1]
    min_half = min(left_half.shape[1], right_half.shape[1])
    symmetry = 1.0 - float(np.mean(np.abs(left_half[:, :min_half].astype(float) - right_half[:, :min_half].astype(float)))) / 255

    # Gradient magnitude mean (overall texture strength)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(gx**2 + gy**2)
    grad_mean = float(grad_mag.mean()) / 100

    # Gradient direction entropy (low = strong directional structure like vehicles)
    angles = np.arctan2(gy, gx + 1e-9)
    strong_mask = grad_mag > grad_mag.mean()
    if strong_mask.sum() > 10:
        angle_hist, _ = np.histogram(angles[strong_mask], bins=16, range=(-np.pi, np.pi))
        angle_hist = angle_hist / (angle_hist.sum() + 1e-9)
        grad_dir_entropy = float(-np.sum(angle_hist[angle_hist > 0] * np.log2(angle_hist[angle_hist > 0]))) / 4
    else:
        grad_dir_entropy = 1.0

    # Color channel std (high = colorful/diverse hues)
    b_ch, g_ch, r_ch = cv2.split(graph.raw_image)
    color_std = float(np.std([r_ch.mean(), g_ch.mean(), b_ch.mean()])) / 100

    # Center-surround brightness ratio
    center_region = gray[h//4:3*h//4, w//4:3*w//4]
    total_sum = float(gray.sum())
    center_sum = float(center_region.sum())
    center_area = (h//2) * (w//2)
    surround_area = h * w - center_area
    surround_mean = (total_sum - center_sum) / max(surround_area, 1)
    center_surround = float(center_region.mean()) / max(surround_mean, 1)

    # --- Spatial profiles ---
    warm_bands = np.array_split(warm, 4, axis=0)
    gray_bands = np.array_split(gray, 4, axis=0)
    warm_band_top = float(warm_bands[0].mean())
    warm_band_bot = float(warm_bands[3].mean())
    bright_band_top = float(gray_bands[0].mean()) / 255
    bright_band_bot = float(gray_bands[3].mean()) / 255

    # Radial profile: inner circle vs outer ring
    Y, X = np.ogrid[:h, :w]
    cy, cx = h // 2, w // 2
    r = min(h, w) // 4
    inner_mask = (Y - cy)**2 + (X - cx)**2 < r**2
    inner_warm = float(warm[inner_mask].mean()) if inner_mask.sum() > 0 else 0
    outer_warm = float(warm[~inner_mask].mean()) if (~inner_mask).sum() > 0 else 0

    # --- Hue histogram (12 bins, only saturated pixels) ---
    sat_mask = sat > 50
    sat_pixels_ratio = float(sat_mask.sum()) / (h * w)
    if sat_mask.sum() > 100:
        hue_masked = hue[sat_mask]
        hue_hist, _ = np.histogram(hue_masked, bins=12, range=(0, 180))
        hue_hist = hue_hist / (hue_hist.sum() + 1e-9)
    else:
        hue_hist = np.zeros(12)
    hue_spread = float(np.sum(hue_hist > 0.05))

    return {
        "sat": float(sat.mean()) / 255,
        "val": float(val.mean()) / 255,
        "warm": warm_coverage,
        "yellow": float(yellow.sum()) / (h * w),
        "blue_purple": float(blue_purple.sum()) / (h * w),
        "green": float(green.sum()) / (h * w),
        "bw": float(bw.sum()) / (h * w),
        "edge": float(edges.sum() / 255) / (h * w),
        "lap_var": lap_var,
        "warm_aspect": warm_aspect,
        "bg_contrast": abs(float(center.mean()) - float(border_mean)),
        "lbp_entropy": lbp_entropy,
        "symmetry": symmetry,
        "grad_mean": grad_mean,
        "grad_dir_entropy": grad_dir_entropy,
        "color_std": color_std,
        "center_surround": center_surround,
        # Spatial
        "warm_band_top": warm_band_top,
        "warm_band_bot": warm_band_bot,
        "bright_top_minus_bot": bright_band_top - bright_band_bot,
        "radial_warm_diff": inner_warm - outer_warm,
        # Hue histogram
        "hue_red": float(hue_hist[0]),
        "hue_orange": float(hue_hist[1]),
        "hue_yellow": float(hue_hist[2]),
        "hue_green": float(hue_hist[4]),
        "hue_cyan_blue": float(hue_hist[7]),
        "hue_blue": float(hue_hist[8]),
        "hue_spread": hue_spread,
        "sat_pixels_ratio": sat_pixels_ratio,
    }


def _feature_conf(name: str, graph: SceneGraph) -> float:
    feat = get_feature(name)
    if feat is None:
        return 0.0
    try:
        return feat.evaluate(graph).confidence
    except Exception:
        return 0.0


def _clamp(x: float) -> float:
    return max(0.0, min(x, 1.0))


def _sigmoid(x: float, center: float, scale: float) -> float:
    """Soft threshold: returns ~0 below center, ~1 above, smooth transition."""
    z = (x - center) * scale
    z = max(-10, min(10, z))
    return 1.0 / (1.0 + np.exp(-z))


def _detected(score: float, evidence: str) -> FeatureValue:
    return FeatureValue.detected(confidence=_clamp(score), evidence=[evidence])


@register_feature(name="phase2_jellyfish_signature", tags=["phase2", "class"], description="Blue/purple translucent, low-edge, low-warm")
class Phase2JellyfishSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("blue_purple", 0), 0.15, 8) * 0.25
            + _sigmoid(s.get("hue_orange", 1), 0.20, -8) * 0.20
            + _sigmoid(s.get("grad_mean", 1), 0.80, -4) * 0.15
            + _sigmoid(s.get("yellow", 1), 0.10, -10) * 0.15
            + _sigmoid(s.get("edge", 1), 0.18, -12) * 0.15
            + _sigmoid(s.get("warm", 1), 0.15, -6) * 0.10
        )
        if score > 0.25:
            return _detected(score, f"bp={s.get('blue_purple',0):.2f}, hue_o={s.get('hue_orange',0):.2f}, grad={s.get('grad_mean',0):.2f}")
        return FeatureValue.absent("no jellyfish signature")


@register_feature(name="phase2_king_penguin_signature", tags=["phase2", "class"], description="Low-sat, low-warm, low-color-std, desaturated body")
class Phase2KingPenguinSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("sat", 1), 0.35, -10) * 0.20
            + _sigmoid(s.get("color_std", 1), 0.12, -8) * 0.20
            + _sigmoid(s.get("sat_pixels_ratio", 1), 0.60, -5) * 0.15
            + _sigmoid(s.get("radial_warm_diff", 1), 0.05, -6) * 0.15
            + _sigmoid(s.get("warm", 1), 0.30, -8) * 0.15
            + _sigmoid(s.get("val", 1), 0.52, -5) * 0.15
        )
        if score > 0.25:
            return _detected(score, f"sat={s.get('sat',0):.2f}, cstd={s.get('color_std',0):.2f}, warm={s.get('warm',0):.2f}")
        return FeatureValue.absent("no penguin signature")


@register_feature(name="phase2_orange_signature", tags=["phase2", "class"], description="High-sat, high-color-std, low-texture warm fruit")
class Phase2OrangeSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("sat", 0), 0.50, 8) * 0.20
            + _sigmoid(s.get("color_std", 0), 0.25, 5) * 0.20
            + _sigmoid(s.get("lap_var", 99999), 5000, -0.0003) * 0.15
            + _sigmoid(s.get("warm", 0), 0.40, 4) * 0.15
            + _sigmoid(s.get("grad_mean", 1), 1.0, -4) * 0.15
            + _sigmoid(s.get("sat_pixels_ratio", 0), 0.80, 5) * 0.15
        )
        if score > 0.25:
            return _detected(score, f"sat={s.get('sat',0):.2f}, cstd={s.get('color_std',0):.2f}, lap={s.get('lap_var',0):.0f}")
        return FeatureValue.absent("no orange signature")


@register_feature(name="phase2_banana_signature", tags=["phase2", "class"], description="Yellow-dominant warm fruit with orange hue peak")
class Phase2BananaSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("yellow", 0), 0.25, 5) * 0.25
            + _sigmoid(s.get("warm", 0), 0.40, 4) * 0.20
            + _sigmoid(s.get("hue_orange", 0), 0.40, 5) * 0.15
            + _sigmoid(s.get("warm_band_bot", 0), 0.45, 4) * 0.15
            + _sigmoid(s.get("hue_cyan_blue", 1), 0.05, -15) * 0.15
            + _sigmoid(s.get("sat", 0), 0.65, -6) * 0.10
        )
        if score > 0.25:
            return _detected(score, f"yellow={s.get('yellow',0):.2f}, warm={s.get('warm',0):.2f}, hue_o={s.get('hue_orange',0):.2f}")
        return FeatureValue.absent("no banana signature")


@register_feature(name="phase2_brown_bear_signature", tags=["phase2", "class"], description="High LBP/edge, dark center, low color-std nature animal")
class Phase2BrownBearSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("lbp_entropy", 0), 5.20, 6) * 0.20
            + _sigmoid(s.get("edge", 0), 0.27, 10) * 0.20
            + _sigmoid(s.get("center_surround", 1), 0.95, -5) * 0.20
            + _sigmoid(s.get("color_std", 1), 0.15, -6) * 0.15
            + _sigmoid(s.get("sat", 1), 0.40, -5) * 0.15
            + _sigmoid(s.get("grad_dir_entropy", 0), 0.97, 10) * 0.10
        )
        if score > 0.25:
            return _detected(score, f"lbp={s.get('lbp_entropy',0):.2f}, edge={s.get('edge',0):.2f}, cs={s.get('center_surround',0):.2f}")
        return FeatureValue.absent("no brown bear signature")


@register_feature(name="phase2_sports_car_signature", tags=["phase2", "class"], description="Low grad_dir, low warm/yellow, high texture")
class Phase2SportsCarSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("grad_dir_entropy", 1), 0.94, -10) * 0.25
            + _sigmoid(s.get("hue_orange", 1), 0.20, -6) * 0.20
            + _sigmoid(s.get("warm", 1), 0.30, -5) * 0.15
            + _sigmoid(s.get("yellow", 1), 0.15, -6) * 0.15
            + _sigmoid(s.get("warm_band_bot", 1), 0.25, -4) * 0.15
            + _sigmoid(s.get("color_std", 1), 0.15, -5) * 0.10
        )
        if score > 0.25:
            return _detected(score, f"gdir={s.get('grad_dir_entropy',0):.2f}, warm={s.get('warm',0):.2f}, hue_o={s.get('hue_orange',0):.2f}")
        return FeatureValue.absent("no sports car signature")


@register_feature(name="phase2_teapot_signature", tags=["phase2", "class"], description="Low-edge, low-color-std, low-texture indoor object")
class Phase2TeapotSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("edge", 1), 0.22, -10) * 0.20
            + _sigmoid(s.get("blue_purple", 1), 0.08, -8) * 0.15
            + _sigmoid(s.get("color_std", 1), 0.15, -5) * 0.15
            + _sigmoid(s.get("grad_mean", 1), 1.0, -4) * 0.15
            + _sigmoid(s.get("lap_var", 99999), 6000, -0.0003) * 0.15
            + _sigmoid(s.get("bw", 0), 0.50, 4) * 0.10
            + _sigmoid(s.get("warm", 0), 0.25, 4) * 0.10
        )
        if score > 0.25:
            return _detected(score, f"edge={s.get('edge',0):.2f}, cstd={s.get('color_std',0):.2f}, grad={s.get('grad_mean',0):.2f}")
        return FeatureValue.absent("no teapot signature")


@register_feature(name="phase2_mushroom_signature", tags=["phase2", "class"], description="High LBP/edge, high grad, low blue, dark valued")
class Phase2MushroomSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("edge", 0), 0.26, 10) * 0.20
            + _sigmoid(s.get("lbp_entropy", 0), 5.20, 6) * 0.20
            + _sigmoid(s.get("hue_cyan_blue", 1), 0.04, -15) * 0.15
            + _sigmoid(s.get("lap_var", 0), 8000, 0.0002) * 0.15
            + _sigmoid(s.get("blue_purple", 1), 0.05, -12) * 0.15
            + _sigmoid(s.get("grad_mean", 0), 1.3, 3) * 0.15
        )
        if score > 0.25:
            return _detected(score, f"edge={s.get('edge',0):.2f}, lbp={s.get('lbp_entropy',0):.2f}, hcb={s.get('hue_cyan_blue',0):.2f}")
        return FeatureValue.absent("no mushroom signature")


@register_feature(name="phase2_golden_retriever_signature", tags=["phase2", "class"], description="Warm-centered, high grad_dir, red-hue, low-blue animal")
class Phase2GoldenRetrieverSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("radial_warm_diff", 0), 0.10, 4) * 0.20
            + _sigmoid(s.get("hue_red", 0), 0.25, 4) * 0.20
            + _sigmoid(s.get("warm", 0), 0.35, 4) * 0.15
            + _sigmoid(s.get("blue_purple", 1), 0.08, -8) * 0.15
            + _sigmoid(s.get("lap_var", 99999), 6000, -0.0002) * 0.15
            + _sigmoid(s.get("green", 1), 0.10, -6) * 0.15
        )
        if score > 0.25:
            return _detected(score, f"rwd={s.get('radial_warm_diff',0):.2f}, hred={s.get('hue_red',0):.2f}, warm={s.get('warm',0):.2f}")
        return FeatureValue.absent("no golden retriever signature")


@register_feature(name="phase2_school_bus_signature", tags=["phase2", "class"], description="High grad/lap, low grad_dir, orange-hue dominated vehicle")
class Phase2SchoolBusSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("grad_mean", 0), 1.4, 3) * 0.20
            + _sigmoid(s.get("grad_dir_entropy", 1), 0.94, -8) * 0.20
            + _sigmoid(s.get("lap_var", 0), 9000, 0.0002) * 0.20
            + _sigmoid(s.get("hue_orange", 0), 0.40, 4) * 0.15
            + _sigmoid(s.get("edge", 0), 0.24, 8) * 0.15
            + _sigmoid(s.get("radial_warm_diff", 0), 0.10, 4) * 0.10
        )
        if score > 0.25:
            return _detected(score, f"grad={s.get('grad_mean',0):.2f}, gdir={s.get('grad_dir_entropy',0):.2f}, lap={s.get('lap_var',0):.0f}")
        return FeatureValue.absent("no school bus signature")
