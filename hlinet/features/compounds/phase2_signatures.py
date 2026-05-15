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
    warm_blob_count = 0.0
    warm_coverage = float(warm.sum()) / (h * w)
    if warm_coverage > 0.02:
        num_labels, labels = cv2.connectedComponents((warm * 255).astype(np.uint8))
        warm_blob_count = min(num_labels - 1, 20) / 20.0
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

    # Horizontal gradient dominance (vehicles have strong horizontal lines)
    horiz_dominance = float(np.abs(gy).sum()) / max(float(np.abs(gx).sum()), 1)

    # Edge spatial autocorrelation (repetitive structures like windows)
    edge_f = edges.astype(np.float32) / 255
    shifted_r = np.zeros_like(edge_f)
    shifted_r[:, 2:] = edge_f[:, :-2]
    autocorr_flat = edge_f.ravel()
    shifted_flat = shifted_r.ravel()
    denom = np.std(autocorr_flat) * np.std(shifted_flat)
    autocorr_h = float(np.corrcoef(autocorr_flat, shifted_flat)[0, 1]) if denom > 1e-9 else 0.0
    if np.isnan(autocorr_h):
        autocorr_h = 0.0

    # DCT frequency band energy (expands representation space orthogonally)
    gray_f = gray.astype(np.float32)
    dct_img = cv2.dct(gray_f if h == w else cv2.resize(gray_f, (64, 64)))
    dct_abs = np.abs(dct_img)
    total_energy = float(dct_abs.sum()) + 1e-9
    dct_low = float(dct_abs[:8, :8].sum()) / total_energy
    dct_mid = float(dct_abs[8:24, 8:24].sum()) / total_energy
    dct_high = float(dct_abs[24:, 24:].sum()) / total_energy

    # Vertical edge regularity (how evenly spaced are vertical edges)
    vert_edge_profile = (np.abs(gx) > grad_mag.mean()).sum(axis=0).astype(np.float32)
    vert_edge_profile = vert_edge_profile / (vert_edge_profile.max() + 1e-9)
    if len(vert_edge_profile) > 4:
        vert_fft = np.abs(np.fft.rfft(vert_edge_profile - vert_edge_profile.mean()))
        vert_regularity = float(vert_fft[1:6].max()) / max(float(vert_fft[1:].mean()), 1e-9)
    else:
        vert_regularity = 0.0

    # Gabor filter bank — texture at specific orientations/frequencies
    gabor_0_04_var = float(cv2.filter2D(gray, cv2.CV_64F,
        cv2.getGaborKernel((9, 9), 3, 0, 2.5, 0.5, 0)).var()) / 10000
    gabor_45_04_var = float(cv2.filter2D(gray, cv2.CV_64F,
        cv2.getGaborKernel((9, 9), 3, np.pi/4, 2.5, 0.5, 0)).var()) / 10000
    gabor_90_01_mean = float(np.abs(cv2.filter2D(gray, cv2.CV_64F,
        cv2.getGaborKernel((9, 9), 3, np.pi/2, 10.0, 0.5, 0))).mean()) / 100
    orient_energies = []
    for theta in [0, np.pi/4, np.pi/2, 3*np.pi/4]:
        k = cv2.getGaborKernel((9, 9), 3, theta, 5.0, 0.5, 0)
        orient_energies.append(float(np.abs(cv2.filter2D(gray, cv2.CV_64F, k)).mean()))
    gabor_dominant_orient = float(np.argmax(orient_energies)) / 4.0

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

    # --- 2x2 spatial pyramid ---
    mid_y, mid_x = h // 2, w // 2
    quads = {
        "tl": (slice(0, mid_y), slice(0, mid_x)),
        "tr": (slice(0, mid_y), slice(mid_x, w)),
        "bl": (slice(mid_y, h), slice(0, mid_x)),
        "br": (slice(mid_y, h), slice(mid_x, w)),
    }
    quad_warm = {}
    quad_edge = {}
    quad_green = {}
    quad_sat = {}
    for qname, (ys, xs) in quads.items():
        qarea = max((ys.stop - ys.start) * (xs.stop - xs.start), 1)
        quad_warm[qname] = float(warm[ys, xs].sum()) / qarea
        quad_edge[qname] = float(edges[ys, xs].sum() / 255) / qarea
        quad_green[qname] = float(green[ys, xs].sum()) / qarea
        quad_sat[qname] = float(sat[ys, xs].mean()) / 255

    # Sky detection (Phase 1 heuristic): blue or bright uniform top quarter
    top_q = gray[:h // 4, :]
    top_sat = sat[:h // 4, :]
    top_hue = hue[:h // 4, :]
    sky_blue = ((top_hue >= 85) & (top_hue <= 130) & (top_sat > 30) & (top_q > 80))
    sky_bright = (top_q > 180) & (top_sat < 40)
    sky_ratio = float((sky_blue | sky_bright).sum()) / max(top_q.size, 1)
    top_uniformity = 1.0 - float(top_q.std()) / 128

    # Blob interior texture (Phase 1: blob_smooth vs blob_textured)
    blob_lap_var = 0.0
    blob_coverage = 0.0
    if warm_coverage > 0.12:
        num_labels_b, labels_b = cv2.connectedComponents((warm * 255).astype(np.uint8))
        if num_labels_b > 1:
            largest_b = 1 + np.argmax([(labels_b == i).sum() for i in range(1, num_labels_b)])
            blob_mask = (labels_b == largest_b)
            blob_coverage = float(blob_mask.sum()) / (h * w)
            if blob_coverage > 0.08:
                lap = cv2.Laplacian(gray, cv2.CV_64F)
                blob_lap_var = float(lap[blob_mask].var()) / 10000

    # Contour shape: circularity of largest contour
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circularity = 0.0
    contour_solidity = 0.0
    if contours:
        largest_c = max(contours, key=cv2.contourArea)
        area_c = cv2.contourArea(largest_c)
        peri_c = cv2.arcLength(largest_c, True)
        if peri_c > 0 and area_c > 50:
            circularity = 4 * np.pi * area_c / (peri_c * peri_c)
            hull = cv2.convexHull(largest_c)
            hull_area = cv2.contourArea(hull)
            if hull_area > 0:
                contour_solidity = area_c / hull_area

    # Top vs bottom edge density (Phase 1: mushroom cap = top textured, bottom detailed)
    top_edge = float(edges[:mid_y, :].sum() / 255) / max(mid_y * w, 1)
    bot_edge = float(edges[mid_y:, :].sum() / 255) / max((h - mid_y) * w, 1)

    result = {
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
        "warm_blob_count": warm_blob_count,
        "bg_contrast": abs(float(center.mean()) - float(border_mean)),
        "lbp_entropy": lbp_entropy,
        "symmetry": symmetry,
        "grad_mean": grad_mean,
        "grad_dir_entropy": grad_dir_entropy,
        "color_std": color_std,
        "center_surround": center_surround,
        # Spatial bands
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
        # --- NEW: spatial pyramid (2x2) ---
        "warm_tl": quad_warm["tl"],
        "warm_tr": quad_warm["tr"],
        "warm_bl": quad_warm["bl"],
        "warm_br": quad_warm["br"],
        "edge_tl": quad_edge["tl"],
        "edge_tr": quad_edge["tr"],
        "edge_bl": quad_edge["bl"],
        "edge_br": quad_edge["br"],
        "green_tl": quad_green["tl"],
        "green_tr": quad_green["tr"],
        "green_bl": quad_green["bl"],
        "green_br": quad_green["br"],
        "sat_tl": quad_sat["tl"],
        "sat_tr": quad_sat["tr"],
        "sat_bl": quad_sat["bl"],
        "sat_br": quad_sat["br"],
        # --- NEW: sky / scene context ---
        "sky_ratio": sky_ratio,
        "top_uniformity": top_uniformity,
        # --- NEW: blob interior ---
        "blob_lap_var": blob_lap_var,
        "blob_coverage": blob_coverage,
        # --- NEW: shape ---
        "circularity": circularity,
        "contour_solidity": contour_solidity,
        # --- NEW: vertical edge asymmetry ---
        "top_edge": top_edge,
        "bot_edge": bot_edge,
        "edge_top_minus_bot": top_edge - bot_edge,
        # --- Derived conjunctive features ---
        "smooth_yellow": float(yellow.sum()) / (h * w) * max(0, 1.0 - float(edges.sum() / 255) / (h * w) * 3),
        "smooth_warm": warm_coverage * max(0, 1.0 - float(edges.sum() / 255) / (h * w) * 3),
        "textured_decentered": float(edges.sum() / 255) / (h * w) * max(0, 1.0 - center_surround / 1.5),
        "warm_val_mean": float(val[warm].mean()) / 255 if warm.sum() > 100 else 0.5,
        "dark_warm_ratio": float(((warm) & (val < 120)).sum()) / max(float(((warm) & (val >= 120)).sum()), 1),
        "sat_color_std": float(sat.mean()) / 255 * color_std,
        "sat_smooth_warm": float(sat.mean()) / 255 * warm_coverage * max(0, 1.0 - float(edges.sum() / 255) / (h * w) * 3),
        "warm_hue_mean": float(hue[warm].mean()) / 45 if warm.sum() > 100 else 0.5,
        "warm_hue_median": float(np.median(hue[warm])) if warm.sum() > 100 else 15.0,
        "warm_sat_cv": float(sat[warm].std() / max(sat[warm].mean(), 1)) if warm.sum() > 100 else 0.3,
        "horiz_dominance": horiz_dominance,
        "autocorr_h": autocorr_h,
        "autocorr_x_warm_bl": autocorr_h * quad_warm["bl"],
        "horiz_x_warm_bl": horiz_dominance * quad_warm["bl"],
        "autocorr_x_mid_wider": 0.0,
        "dct_low": dct_low,
        "dct_mid": dct_mid,
        "dct_high": dct_high,
        "dct_mid_over_low": dct_mid / max(dct_low, 1e-9),
        "vert_regularity": vert_regularity,
        "gabor_0_04_var": gabor_0_04_var,
        "gabor_45_04_var": gabor_45_04_var,
        "gabor_90_01_mean": gabor_90_01_mean,
        "gabor_dominant_orient": gabor_dominant_orient,
    }

    # Width profile: is the middle third wider than top/bottom in edge spread?
    widths = np.zeros(h)
    for row_y in range(h):
        edge_cols = np.where(edges[row_y, :] > 0)[0]
        if len(edge_cols) >= 2:
            widths[row_y] = edge_cols[-1] - edge_cols[0]
    max_width = max(widths.max(), 1)
    widths_norm = widths / max_width
    third = h // 3
    top_width = float(widths_norm[:third].mean())
    mid_width = float(widths_norm[third:2*third].mean())
    bot_width = float(widths_norm[2*third:].mean())
    result["mid_wider"] = 1.0 if (mid_width > top_width and mid_width > bot_width) else 0.0
    result["mid_width_ratio"] = mid_width / max(0.5 * (top_width + bot_width), 0.01)
    result["autocorr_x_mid_wider"] = autocorr_h * result["mid_wider"]

    from hlinet.features.compounds.local_regions import _region_stats
    local = _region_stats(graph)
    result.update(local)

    hist_scores = _color_hist_scores(image)
    result.update(hist_scores)

    if hist_scores:
        hb = hist_scores.get("hist_banana", 0)
        ho = hist_scores.get("hist_orange", 0)
        hs = hist_scores.get("hist_sports_car", 0)
        hsb = hist_scores.get("hist_school_bus", 0)
        hg = hist_scores.get("hist_golden_retriever", 0)
        hbb = hist_scores.get("hist_brown_bear", 0)
        hm = hist_scores.get("hist_mushroom", 0)
        ht = hist_scores.get("hist_teapot", 0)
        hk = hist_scores.get("hist_king_penguin", 0)
        hj = hist_scores.get("hist_jellyfish", 0)
        result["hist_orange_minus_banana"] = ho - hb
        result["hist_sports_minus_bus"] = hs - hsb
        result["hist_bear_minus_gr"] = hbb - hg
        result["hist_mushroom_minus_bear"] = hm - hbb
        result["hist_gr_minus_banana"] = hg - hb
        result["hist_teapot_minus_kp"] = ht - hk
        result["hist_teapot_minus_banana"] = ht - hb
        result["hist_banana_minus_mushroom"] = hb - hm
        result["hist_gr_minus_teapot"] = hg - ht
        result["hist_bear_minus_kp"] = hbb - hk
        result["hist_jelly_minus_kp"] = hj - hk
        result["hist_orange_minus_teapot"] = ho - ht
        result["hist_bear_minus_teapot"] = hbb - ht
        result["hist_gr_minus_kp"] = hg - hk
        result["hist_gr_minus_mushroom"] = hg - hm

    return result


_COLOR_PROTOS = None

def _color_hist_scores(image_bgr: np.ndarray) -> dict[str, float]:
    global _COLOR_PROTOS
    if _COLOR_PROTOS is None:
        import pathlib
        proto_path = pathlib.Path(__file__).parent / "color_prototypes.npz"
        if proto_path.exists():
            _COLOR_PROTOS = dict(np.load(str(proto_path)))
        else:
            return {}
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [12, 8], [0, 180, 0, 256])
    hist = cv2.normalize(hist, hist).flatten().astype(np.float32)
    scores = {}
    for cls_name, proto in _COLOR_PROTOS.items():
        score = cv2.compareHist(hist, proto.astype(np.float32), cv2.HISTCMP_INTERSECT)
        scores[f"hist_{cls_name}"] = float(score)
    return scores


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


def _guarded_score(pos: float, guards: list[float]) -> float:
    """Positive core modulated by min-guard: if any guard fires 0, score halves."""
    guard = min(guards) if guards else 1.0
    return pos * (0.5 + 0.5 * guard)


@register_feature(name="phase2_jellyfish_signature", tags=["phase2", "class"], description="Blue/purple translucent, low-edge, low-warm")
class Phase2JellyfishSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("blue_region_area", 0), 0.10, 8) * 0.25
            + _sigmoid(s.get("blue_purple", 0), 0.13, 6) * 0.20
            + _sigmoid(s.get("hue_cyan_blue", 0), 0.10, 5) * 0.15
            + _sigmoid(s.get("color_std", 0), 0.25, 5) * 0.10
            + _sigmoid(s.get("edge", 1), 0.20, -8) * 0.10
            + _sigmoid(s.get("lbp_entropy", 1), 5.0, -5) * 0.10
            + _sigmoid(s.get("r0_area", 0), 0.15, 6) * 0.10
        )
        guards = [
            _sigmoid(s.get("warm", 1), 0.43, -4),
            _sigmoid(s.get("hue_orange", 1), 0.47, -3),
            _sigmoid(s.get("yellow", 1), 0.22, -5),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"bp={s.get('blue_purple',0):.2f}, hcb={s.get('hue_cyan_blue',0):.2f}, cstd={s.get('color_std',0):.2f}")
        return FeatureValue.absent("no jellyfish signature")


@register_feature(name="phase2_king_penguin_signature", tags=["phase2", "class"], description="Low-sat, low-color-std, low warm, bw dominant")
class Phase2KingPenguinSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("sat", 1), 0.35, -8) * 0.20
            + _sigmoid(s.get("bw", 0), 0.55, 5) * 0.15
            + _sigmoid(s.get("color_std", 1), 0.13, -8) * 0.15
            + _sigmoid(s.get("warm", 1), 0.30, -8) * 0.15
            + _sigmoid(s.get("has_dark_bright_contrast", 0), 0.5, 5) * 0.10
            + _sigmoid(s.get("sat_bl", 1), 0.35, -8) * 0.10
            + _sigmoid(s.get("sat_br", 1), 0.35, -8) * 0.15
        )
        guards = [
            _sigmoid(s.get("lap_var", 99999), 20000, -0.0001),
            _sigmoid(s.get("blob_coverage", 1), 0.62, -3),
            _sigmoid(s.get("edge", 1), 0.35, -5),
            _sigmoid(s.get("yellow", 1), 0.52, -3),
            _sigmoid(s.get("hue_red", 1), 0.57, -3),
            _sigmoid(s.get("grad_mean", 1), 2.00, -2),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"sat={s.get('sat',0):.2f}, cstd={s.get('color_std',0):.2f}, hcb={s.get('hue_cyan_blue',0):.2f}")
        return FeatureValue.absent("no penguin signature")


@register_feature(name="phase2_orange_signature", tags=["phase2", "class"], description="High-sat, high-color-std, warm, smooth fruit with red hue")
class Phase2OrangeSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("sat", 0), 0.50, 8) * 0.20
            + _sigmoid(s.get("sat_color_std", 0), 0.15, 8) * 0.15
            + _sigmoid(s.get("smooth_warm", 0), 0.15, 5) * 0.15
            + _sigmoid(s.get("warm", 0), 0.40, 4) * 0.15
            + _sigmoid(s.get("blob_coverage", 0), 0.38, 4) * 0.10
            + _sigmoid(s.get("smooth_warm_blob_area", 0), 0.05, 10) * 0.10
            + _sigmoid(s.get("hue_red", 0), 0.25, 5) * 0.15
        )
        guards = [
            _sigmoid(s.get("edge", 1), 0.32, -8),
            _sigmoid(s.get("grad_mean", 1), 1.55, -3),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"sat={s.get('sat',0):.2f}, cstd={s.get('color_std',0):.2f}, hred={s.get('hue_red',0):.2f}")
        return FeatureValue.absent("no orange signature")


@register_feature(name="phase2_banana_signature", tags=["phase2", "class"], description="High yellow, warm, saturated, orange-hue fruit")
class Phase2BananaSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("smooth_yellow", 0), 0.06, 12) * 0.25
            + _sigmoid(s.get("yellow", 0), 0.25, 5) * 0.20
            + _sigmoid(s.get("warm", 0), 0.40, 4) * 0.15
            + _sigmoid(s.get("hue_orange", 0), 0.40, 5) * 0.15
            + _sigmoid(s.get("warm_band_bot", 0), 0.45, 4) * 0.15
            + _sigmoid(s.get("hue_cyan_blue", 1), 0.05, -15) * 0.10
        )
        guards = [
            _sigmoid(s.get("hue_red", 1), 0.55, -4),
            _sigmoid(s.get("edge", 1), 0.35, -8),
            _sigmoid(s.get("blue_purple", 1), 0.38, -3),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"yellow={s.get('yellow',0):.2f}, warm={s.get('warm',0):.2f}, sat={s.get('sat',0):.2f}")
        return FeatureValue.absent("no banana signature")


@register_feature(name="phase2_brown_bear_signature", tags=["phase2", "class"], description="High LBP/edge, dark center, low color-std nature animal")
class Phase2BrownBearSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("textured_decentered", 0), 0.08, 10) * 0.25
            + _sigmoid(s.get("edge", 0), 0.27, 10) * 0.15
            + _sigmoid(s.get("lbp_entropy", 0), 5.20, 6) * 0.10
            + _sigmoid(s.get("center_surround", 1), 0.95, -5) * 0.15
            + _sigmoid(s.get("dark_warm_ratio", 0), 1.0, 1.5) * 0.15
            + _sigmoid(s.get("warm_val_mean", 1), 0.50, -5) * 0.10
            + _sigmoid(s.get("green", 0), 0.08, 5) * 0.10
        )
        guards = [
            _sigmoid(s.get("blue_purple", 1), 0.35, -3),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"td={s.get('textured_decentered',0):.3f}, edge={s.get('edge',0):.2f}, dwr={s.get('dark_warm_ratio',0):.2f}")
        return FeatureValue.absent("no brown bear signature")


@register_feature(name="phase2_sports_car_signature", tags=["phase2", "class"], description="Low grad_dir, high warm_aspect, low warm/blob structured vehicle")
class Phase2SportsCarSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("grad_dir_entropy", 1), 0.94, -10) * 0.20
            + _sigmoid(s.get("horiz_dominance", 0), 1.10, 3) * 0.15
            + _sigmoid(s.get("max_elongation", 0), 4.0, 0.5) * 0.10
            + _sigmoid(s.get("r0_aspect", 0), 2.0, 1.5) * 0.10
            + _sigmoid(s.get("warm_aspect", 0), 1.48, 2) * 0.10
            + _sigmoid(s.get("lap_var", 0), 7000, 0.0002) * 0.10
            + _sigmoid(s.get("grad_mean", 0), 1.18, 3) * 0.10
            + _sigmoid(s.get("autocorr_h", 0), 0.15, 5) * 0.10
            + _sigmoid(s.get("blob_coverage", 1), 0.38, -4) * 0.05
        )
        guards = [
            _sigmoid(s.get("yellow", 1), 0.42, -4),
            _sigmoid(s.get("hue_orange", 1), 0.60, -3),
            _sigmoid(s.get("sat", 1), 0.63, -3),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"gdir={s.get('grad_dir_entropy',0):.2f}, lap={s.get('lap_var',0):.0f}, grad={s.get('grad_mean',0):.2f}")
        return FeatureValue.absent("no sports car signature")


@register_feature(name="phase2_teapot_signature", tags=["phase2", "class"], description="Low edge, low sat, uniform top, indoor object")
class Phase2TeapotSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("edge_tl", 1), 0.22, -10) * 0.15
            + _sigmoid(s.get("top_edge", 1), 0.22, -10) * 0.10
            + _sigmoid(s.get("edge", 1), 0.23, -10) * 0.10
            + _sigmoid(s.get("sat_tl", 1), 0.43, -5) * 0.10
            + _sigmoid(s.get("color_std", 1), 0.21, -5) * 0.10
            + _sigmoid(s.get("top_uniformity", 0), 0.70, 5) * 0.10
            + _sigmoid(s.get("center_surround", 0), 1.00, 3) * 0.10
            + _sigmoid(s.get("hue_red", 0), 0.15, 5) * 0.15
            + _sigmoid(s.get("warm_br", 0), 0.20, 4) * 0.10
        )
        guards = [
            _sigmoid(s.get("sat", 1), 0.66, -3),
            _sigmoid(s.get("blue_purple", 1), 0.23, -5),
            _sigmoid(s.get("yellow", 1), 0.70, -2),
            _sigmoid(s.get("warm", 1), 0.86, -2),
            _sigmoid(s.get("green", 1), 0.21, -3),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"edge={s.get('edge',0):.2f}, cs={s.get('center_surround',0):.2f}, hred={s.get('hue_red',0):.2f}")
        return FeatureValue.absent("no teapot signature")


@register_feature(name="phase2_mushroom_signature", tags=["phase2", "class"], description="High LBP/edge, high grad, low blue, dark valued")
class Phase2MushroomSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("round_edge", 0), 0.15, 8) * 0.20
            + _sigmoid(s.get("edge", 0), 0.26, 10) * 0.15
            + _sigmoid(s.get("lbp_entropy", 0), 5.20, 6) * 0.10
            + _sigmoid(s.get("center_surround", 0), 1.05, 3) * 0.10
            + _sigmoid(s.get("has_green_surround", 0), 0.5, 5) * 0.15
            + _sigmoid(s.get("green_region_area", 0), 0.03, 10) * 0.10
            + _sigmoid(s.get("bot_edge", 0), 0.26, 8) * 0.10
            + _sigmoid(s.get("grad_mean", 0), 1.3, 3) * 0.10
        )
        guards = [
            _sigmoid(s.get("hue_cyan_blue", 1), 0.11, -8),
            _sigmoid(s.get("blue_purple", 1), 0.12, -8),
            _sigmoid(s.get("smooth_warm_blob_area", 1), 0.19, -3),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"lbp={s.get('lbp_entropy',0):.2f}, edge={s.get('edge',0):.2f}, cs={s.get('center_surround',0):.2f}")
        return FeatureValue.absent("no mushroom signature")


@register_feature(name="phase2_golden_retriever_signature", tags=["phase2", "class"], description="Warm centered, radial warm, high grad_dir, red hue animal")
class Phase2GoldenRetrieverSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        pos = (
            _sigmoid(s.get("radial_warm_diff", 0), 0.10, 4) * 0.20
            + _sigmoid(s.get("hue_red", 0), 0.23, 4) * 0.20
            + _sigmoid(s.get("warm_val_mean", 0), 0.50, 5) * 0.15
            + _sigmoid(s.get("warm", 0), 0.35, 4) * 0.15
            + _sigmoid(s.get("center_surround", 0), 1.00, 3) * 0.10
            + _sigmoid(s.get("bot_edge", 0), 0.22, 8) * 0.10
            + _sigmoid(s.get("grad_dir_entropy", 0), 0.96, 8) * 0.10
        )
        guards = [
            _sigmoid(s.get("blue_purple", 1), 0.38, -3),
            _sigmoid(s.get("hue_cyan_blue", 1), 0.17, -5),
            _sigmoid(s.get("bw", 1), 0.88, -2),
            _sigmoid(s.get("color_std", 1), 0.25, -4),
        ]
        score = _guarded_score(pos, guards)
        if score > 0.20:
            return _detected(score, f"warm={s.get('warm',0):.2f}, rwd={s.get('radial_warm_diff',0):.2f}, hred={s.get('hue_red',0):.2f}")
        return FeatureValue.absent("no golden retriever signature")


@register_feature(name="phase2_school_bus_signature", tags=["phase2", "class"], description="High blob texture, high grad, structured, warm vehicle")
class Phase2SchoolBusSignature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        s = _stats(graph)
        score = (
            _sigmoid(s.get("grad_mean", 0), 1.4, 3) * 0.15
            + _sigmoid(s.get("grad_dir_entropy", 1), 0.94, -8) * 0.15
            + _sigmoid(s.get("lap_var", 0), 9000, 0.0002) * 0.15
            + _sigmoid(s.get("hue_orange", 0), 0.40, 4) * 0.15
            + _sigmoid(s.get("blob_lap_var", 0), 0.50, 2) * 0.10
            + _sigmoid(s.get("warm_band_bot", 0), 0.35, 4) * 0.10
            + _sigmoid(s.get("autocorr_h", 0), 0.15, 5) * 0.10
            + _sigmoid(s.get("horiz_dominance", 0), 1.05, 3) * 0.10
        )
        if score > 0.20:
            return _detected(score, f"gdir={s.get('grad_dir_entropy',0):.2f}, lap={s.get('lap_var',0):.0f}, hue_o={s.get('hue_orange',0):.2f}")
        return FeatureValue.absent("no school bus signature")
