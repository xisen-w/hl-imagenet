"""Pairwise tiebreakers: when two classes are close, use direct discriminators."""

from __future__ import annotations

import cv2
import numpy as np
from pathlib import Path

from hlinet.types import SceneGraph


TIEBREAKER_RULES: dict[tuple[str, str], callable] = {}

_PROTO_FILE = Path(__file__).parent / "prototypes.npz"
_PROTOS = None


def _load_prototypes():
    global _PROTOS
    if _PROTOS is None:
        data = np.load(str(_PROTO_FILE))
        _PROTOS = {"dog": data["dog_proto"], "teapot": data["teapot_proto"]}
    return _PROTOS


def _hist_dog_vs_teapot(image: np.ndarray) -> float:
    """Returns (teapot_corr - dog_corr) using HS histogram prototypes."""
    protos = _load_prototypes()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [18, 8], [0, 180, 0, 256])
    hist = hist.flatten().astype(np.float32)
    hist /= hist.sum() + 1e-10
    dog_corr = float(cv2.compareHist(hist, protos["dog"].astype(np.float32), cv2.HISTCMP_CORREL))
    tea_corr = float(cv2.compareHist(hist, protos["teapot"].astype(np.float32), cv2.HISTCMP_CORREL))
    return tea_corr - dog_corr


def register_tiebreaker(class_a: str, class_b: str):
    def decorator(fn):
        TIEBREAKER_RULES[(class_a, class_b)] = fn
        TIEBREAKER_RULES[(class_b, class_a)] = lambda g: 1.0 - fn(g)
        return fn
    return decorator


def resolve_tie(class_a: str, class_b: str, graph: SceneGraph) -> float | None:
    key = (class_a, class_b)
    if key in TIEBREAKER_RULES:
        return TIEBREAKER_RULES[key](graph)
    return None


@register_tiebreaker("bicycle", "mushroom")
def bicycle_vs_mushroom(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bicycle, <0.5 if more like mushroom."""
    if graph.raw_image is None:
        return 0.5
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Mushroom: bright top + detailed bottom (cap+gills)
    top_bright = float(gray[:h // 2, :].mean())
    bot_bright = float(gray[h // 2:, :].mean())
    bright_diff = top_bright - bot_bright

    bot_edges = cv2.Canny(gray[h // 2:, :], 50, 150)
    bot_edge = float(bot_edges.sum()) / 255 / (h // 2 * w)

    if bright_diff > 15 and bot_edge > 0.15:
        return 0.25  # mushroom signal
    return 0.5  # no strong signal


@register_tiebreaker("bicycle", "school_bus")
def bicycle_vs_bus(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bicycle, <0.5 if more like bus."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]

    # Bus has large yellow mass; bicycle doesn't
    yellow = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
              (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (h * w)

    if yellow_ratio > 0.1:
        return 0.2  # strong bus signal
    return 0.5  # no strong signal, don't flip


@register_tiebreaker("golden_retriever", "school_bus")
def dog_vs_bus(graph: SceneGraph) -> float:
    """Returns >0.5 if more like dog, <0.5 if more like bus."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]

    # Yellow body = bus signal
    yellow = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
              (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (h * w)

    # Sky in top
    top = hsv[:h // 4, :, :]
    blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
    bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)

    if yellow_ratio > 0.25 and sky_ratio > 0.1:
        return 0.15  # strong bus signal (large yellow + sky)
    if yellow_ratio > 0.20:
        return 0.25  # moderate yellow without sky
    return 0.5  # no strong signal


@register_tiebreaker("golden_retriever", "mushroom")
def dog_vs_mushroom(graph: SceneGraph) -> float:
    """Returns >0.5 if more like dog, <0.5 if more like mushroom.
    Uses blob smoothness as dog confirmatory and bottom detail as mushroom signal."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Spatial attention: find warm blob and measure interior texture
    warm = ((hsv[:, :, 0] >= 8) & (hsv[:, :, 0] <= 35) &
            (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 50))
    warm_ratio = float(warm.sum()) / (h * w)

    mean_sat = float(hsv[:, :, 1].mean())
    green_mask = ((hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 85) & (hsv[:, :, 1] > 30))
    green_ratio = float(green_mask.sum()) / (h * w)

    # Dog counter-signal: very green scene + warm animal body (not yellow objects)
    yellow_mask = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
                   (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow_mask.sum()) / (h * w)
    if green_ratio > 0.50 and warm_ratio > 0.34 and yellow_ratio < 0.45:
        return 0.70  # warm animal in very green outdoor scene

    # Mushroom conjunctive signals (checked first — override smooth blob)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(gx**2 + gy**2)
    strong_grad = mag > np.percentile(mag, 70)
    angles = np.arctan2(gy, gx)[strong_grad]
    if len(angles) > 0:
        ghist, _ = np.histogram(angles, bins=8, range=(-np.pi, np.pi))
        ghist = ghist.astype(float) / ghist.sum()
        grad_top_bin = float(ghist.max())
    else:
        grad_top_bin = 0.125

    warm_ok = warm_ratio < 0.68 or (warm_ratio < 0.85 and green_ratio > 0.25)
    if grad_top_bin > 0.18 and green_ratio > 0.089 and warm_ok:
        return 0.30  # mushroom: directional gradients + green context

    if mean_sat > 140 and green_ratio > 0.20 and warm_ratio < 0.50:
        return 0.30  # mushroom: high saturation + green context + not warm-dominated

    yellow_mask = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
                   (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow_mask.sum()) / (h * w)
    rb_bot = float(graph.raw_image[2 * h // 3:, :, 2].mean()) / max(
        float(graph.raw_image[2 * h // 3:, :, 0].mean()), 1)
    if mean_sat > 117 and rb_bot < 1.83 and green_ratio < 0.10 and yellow_ratio < 0.15:
        return 0.30  # mushroom: saturated + cool bottom + no green + not yellow

    blob_lap_var = None
    if warm_ratio >= 0.15:
        warm_uint8 = (warm * 255).astype(np.uint8)
        num_labels, labels = cv2.connectedComponents(warm_uint8)
        if num_labels > 1:
            largest_label = 1 + np.argmax([(labels == i).sum() for i in range(1, num_labels)])
            blob_mask = (labels == largest_label).astype(np.uint8)
            if blob_mask.sum() / (h * w) >= 0.10:
                lap = cv2.Laplacian(gray, cv2.CV_64F)
                blob_lap_var = float(lap[blob_mask == 1].var())

    # Strong dog signal: smooth blob interior
    if blob_lap_var is not None and blob_lap_var < 3000:
        return 0.70  # dog — strong enough to trigger reverse swap

    # Bottom edge density (mushrooms have gills/stem detail in bottom third)
    edges = cv2.Canny(gray, 50, 150)
    bot_edges = float(edges[2 * h // 3:, :].sum() / 255) / (h // 3 * w)
    top_edges = float(edges[:h // 3, :].sum() / 255) / (h // 3 * w)

    if bot_edges > 0.32 and bot_edges > top_edges * 1.05:
        if mean_sat > 155:
            return 0.30  # strong mushroom: high saturation + bottom detail
        return 0.35  # lean mushroom
    if bot_edges > 0.30 and bot_edges > top_edges * 1.05 and mean_sat > 155:
        return 0.30  # relaxed threshold with strong saturation guard

    # Dog signal: detail concentrated in upper region (face/head) + warm body + no sky
    top_quarter = hsv[:h // 4, :, :]
    blue_sky = ((top_quarter[:, :, 0] >= 90) & (top_quarter[:, :, 0] <= 130) &
                (top_quarter[:, :, 1] > 30))
    bright_sky = (top_quarter[:, :, 2] > 180) & (top_quarter[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)
    if top_edges > bot_edges * 1.5 and warm_ratio > 0.30 and sky_ratio < 0.10:
        return 0.70  # top-heavy detail = face close-up (not outdoor bus)

    return 0.55  # slight dog lean


@register_tiebreaker("golden_retriever", "teapot")
def dog_vs_teapot(graph: SceneGraph) -> float:
    """Returns >0.5 if more like dog, <0.5 if more like teapot.
    These classes overlap heavily at 64x64 — only flip on strong signal."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)

    # Guard: if image has yellow AND sky AND window pattern, it's a bus not teapot
    yellow = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
              (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (h * w)
    top = hsv[:h // 4, :, :]
    blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
    bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)

    # Check for horizontal window pattern (bus signature)
    col_means = gray.mean(axis=0)
    crossings = int(np.sum(np.diff(np.sign(col_means - col_means.mean())) != 0))
    has_windows = crossings >= 8

    if yellow_ratio > 0.1 and sky_ratio > 0.1 and has_windows:
        return 0.5  # don't flip — bus territory (yellow + sky + windows)

    teapot_signals = 0.0

    # Signal 1: object with distinct background (tabletop)
    center_reg = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
    border_mean = (gray[:h // 4, :].mean() + gray[3 * h // 4:, :].mean() +
                   gray[:, :w // 4].mean() + gray[:, 3 * w // 4:].mean()) / 4
    bg_contrast = abs(float(center_reg.mean()) - border_mean)
    if bg_contrast > 40:
        teapot_signals += 0.3

    # Signal 2: wide + low solidity = spout/handle shape
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, bw, bh = cv2.boundingRect(largest)
        aspect = bw / max(bh, 1)
        hull = cv2.convexHull(largest)
        hull_area = cv2.contourArea(hull)
        area = cv2.contourArea(largest)
        solidity = area / max(hull_area, 1)
        if aspect > 1.3 and solidity < 0.75:
            teapot_signals += 0.3

    # Signal 3: low edge density in periphery (clean background)
    edges = cv2.Canny(gray, 50, 150)
    periph_mask = np.ones((h, w), dtype=bool)
    periph_mask[h // 4:3 * h // 4, w // 4:3 * w // 4] = False
    periph_edge = float(edges[periph_mask].sum() / 255) / periph_mask.sum()
    if periph_edge < 0.16:
        teapot_signals += 0.2

    # Signal 4: smooth manufactured surface (low gradient regions)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(gx**2 + gy**2)
    smooth_pct = float((mag < 10).sum()) / (h * w)
    if smooth_pct > 0.12:
        teapot_signals += 0.3

    # Dog counter-signal: green outdoor scene with warm animal (no teapot has this)
    green_mask = ((hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 85) & (hsv[:, :, 1] > 30))
    green_ratio = float(green_mask.sum()) / (h * w)
    warm = ((hsv[:, :, 0] >= 5) & (hsv[:, :, 0] <= 25) &
            (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 40))
    warm_ratio = float(warm.sum()) / (h * w)
    if green_ratio > 0.30 and warm_ratio > 0.20:
        return 0.70  # warm animal in green nature scene

    # Dog counter-signal: warm fur + high center edge density = textured animal
    center_edges = cv2.Canny(gray[h // 4:3 * h // 4, w // 4:3 * w // 4], 50, 150)
    center_edge_density = float(center_edges.sum()) / 255 / (h // 2 * w // 2)
    if warm_ratio > 0.50 and center_edge_density > 0.32:
        return 0.5  # warm + textured center = fur, not ceramic

    # For images with yellow but no sky: require stronger evidence
    flip_threshold = 0.6 if yellow_ratio > 0.25 else 0.5
    if teapot_signals >= flip_threshold:
        return 0.25  # strong teapot

    # Histogram prototype matching as supplementary signal
    hist_gap = _hist_dog_vs_teapot(graph.raw_image)
    if hist_gap > 0.12:
        return 0.25  # color distribution matches teapot prototype more than dog
    return 0.5  # no strong signal (need multiple signals to flip)


@register_tiebreaker("piano", "mushroom")
def piano_vs_mushroom(graph: SceneGraph) -> float:
    """Returns >0.5 if more like piano, <0.5 if more like mushroom."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]

    green = ((hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 85) & (hsv[:, :, 1] > 30))
    green_ratio = float(green.sum()) / (h * w)

    if green_ratio > 0.25:
        return 0.30  # green context = outdoor mushroom, not piano
    return 0.5


@register_tiebreaker("bicycle", "teapot")
def bicycle_vs_teapot(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bicycle, <0.5 if more like teapot."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    center_reg = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
    border_mean = (gray[:h // 4, :].mean() + gray[3 * h // 4:, :].mean() +
                   gray[:, :w // 4].mean() + gray[:, 3 * w // 4:].mean()) / 4
    bg_contrast = abs(float(center_reg.mean()) - border_mean)

    warm = ((hsv[:, :, 0] <= 35) | (hsv[:, :, 0] >= 170)) & (hsv[:, :, 1] > 20) & (hsv[:, :, 2] > 30)
    warm_ratio = float(warm.sum()) / (h * w)

    yellow = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
              (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (h * w)

    if bg_contrast > 40 and yellow_ratio > 0.40:
        return 0.30  # yellow object on distinct background = teapot (not bicycle)
    return 0.5


@register_tiebreaker("school_bus", "zebra")
def bus_vs_zebra(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bus, <0.5 if more like zebra."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]

    # Bus: yellow/orange mass, zebra: black+white with green
    yellow = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
              (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (h * w)

    # Black+white dominance (zebra)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    bw = float(((gray < 60) | (gray > 200)).sum()) / (h * w)

    # Clear bus signal: yellow body present
    if yellow_ratio > 0.15:
        return 0.8
    if bw > 0.5 and yellow_ratio < 0.05:
        return 0.2
    return 0.5


@register_tiebreaker("school_bus", "teapot")
def bus_vs_teapot(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bus, <0.5 if more like teapot."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]

    top = hsv[:h // 4, :, :]
    blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
    bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)

    body = hsv[h // 4:, :, :]
    yellow = ((body[:, :, 0] >= 15) & (body[:, :, 0] <= 45) &
              (body[:, :, 1] > 60) & (body[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (3 * h // 4 * w)

    yellow_hi = ((body[:, :, 0] >= 15) & (body[:, :, 0] <= 45) &
                 (body[:, :, 1] > 100) & (body[:, :, 2] > 100))
    yellow_hi_ratio = float(yellow_hi.sum()) / (3 * h // 4 * w)

    if sky_ratio > 0.1 and yellow_hi_ratio > 0.08:
        return 0.8  # strong bus signal (sky + saturated yellow)

    # Sky + strong horizontal banding (bus without visible yellow)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    row_means = gray.mean(axis=1)
    mid_rows = row_means[h // 4:3 * h // 4]
    deviations = mid_rows - mid_rows.mean()
    crossings = int(np.sum(np.diff(np.sign(deviations)) != 0))
    amplitude = float(mid_rows.max() - mid_rows.min())
    if sky_ratio > 0.3 and crossings >= 8 and amplitude > 45:
        return 0.75  # bus: sky + strong window pattern without needing yellow

    if yellow_ratio < 0.02 and sky_ratio < 0.1:
        return 0.30  # no yellow, no sky — unlikely bus
    return 0.5


@register_tiebreaker("school_bus", "mushroom")
def bus_vs_mushroom(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bus, <0.5 if more like mushroom."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = hsv.shape[:2]

    top = hsv[:h // 4, :, :]
    blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
    bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)

    body = hsv[h // 4:, :, :]
    yellow = ((body[:, :, 0] >= 15) & (body[:, :, 0] <= 45) &
              (body[:, :, 1] > 80) & (body[:, :, 2] > 80))
    yellow_ratio = float(yellow.sum()) / (3 * h // 4 * w)

    yellow_hi = ((body[:, :, 0] >= 15) & (body[:, :, 0] <= 45) &
                 (body[:, :, 1] > 100) & (body[:, :, 2] > 100))
    yellow_hi_ratio = float(yellow_hi.sum()) / (3 * h // 4 * w)

    # Mushroom counter-signal: bright top + detailed bottom
    # BUT: if bus signal also present (sky+yellow), override mushroom guard
    top_bright = float(gray[:h // 2, :].mean())
    bot_bright = float(gray[h // 2:, :].mean())
    bright_diff = top_bright - bot_bright
    bot_edges = cv2.Canny(gray[h // 2:, :], 50, 150)
    bot_edge = float(bot_edges.sum()) / 255 / (h // 2 * w)
    if bright_diff > 15 and bot_edge > 0.28:
        if sky_ratio > 0.15 and yellow_hi_ratio > 0.10:
            pass  # bus signal overrides mushroom guard
        elif yellow_ratio < 0.05:
            return 0.30  # strong mushroom: cap+gills pattern, no yellow
        else:
            return 0.5  # ambiguous: mushroom structure but some yellow

    if sky_ratio > 0.15 and yellow_hi_ratio > 0.10:
        return 0.8
    if sky_ratio > 0.8 and yellow_hi_ratio > 0.05:
        return 0.7  # very strong sky + trace yellow
    if yellow_hi_ratio > 0.20:
        return 0.7
    return 0.5


@register_tiebreaker("mushroom", "teapot")
def mushroom_vs_teapot(graph: SceneGraph) -> float:
    """Returns >0.5 if more like mushroom, <0.5 if more like teapot."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = hsv.shape[:2]

    # Teapot counter-signal: BOTH high background contrast AND texture ratio
    center_reg = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
    border_mean = (gray[:h // 4, :].mean() + gray[3 * h // 4:, :].mean() +
                   gray[:, :w // 4].mean() + gray[:, 3 * w // 4:].mean()) / 4
    bg_contrast = abs(float(center_reg.mean()) - border_mean)

    top_var = float(cv2.Laplacian(gray[:h // 2, :], cv2.CV_64F).var())
    bot_var = float(cv2.Laplacian(gray[h // 2:, :], cv2.CV_64F).var())
    texture_ratio = top_var / max(bot_var, 1)

    bot_edges = cv2.Canny(gray[h // 2:, :], 50, 150)
    bot_edge = float(bot_edges.sum()) / 255 / (h // 2 * w)

    # Need strong evidence: high contrast AND texture ratio, or very high contrast alone
    if bg_contrast > 50 and texture_ratio > 1.5:
        return 0.30  # strong teapot signal
    if bg_contrast > 60 and bot_edge < 0.30:
        return 0.30  # very high contrast + smooth bottom (not mushroom gills)

    top_bright = float(gray[:h // 2, :].mean())
    bot_bright = float(gray[h // 2:, :].mean())
    bright_diff = top_bright - bot_bright

    # Teapot: texture concentrated in top, bottom brighter (lit surface below)
    if texture_ratio > 2.5 and bright_diff < 0:
        return 0.30  # teapot: textured top, bright bottom
    if bright_diff < -80:
        return 0.30  # teapot: bottom much brighter (surface reflection)

    # Mushroom signal: high saturation + green context (natural mushroom)
    mean_sat = float(hsv[:, :, 1].mean())
    green_mask = ((hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 85) & (hsv[:, :, 1] > 30))
    green_ratio = float(green_mask.sum()) / (h * w)
    if mean_sat > 150 and green_ratio > 0.30:
        return 0.70  # mushroom: high saturation + green (natural setting)

    if bright_diff > 15 and bot_edge > 0.28:
        return 0.7  # strong mushroom signal (bright cap + detailed bottom)

    center_reg = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
    border_mean2 = (gray[:h // 4, :].mean() + gray[3 * h // 4:, :].mean() +
                    gray[:, :w // 4].mean() + gray[:, 3 * w // 4:].mean()) / 4
    bg_contrast2 = abs(float(center_reg.mean()) - border_mean2)

    if bot_edge > 0.32 and bg_contrast2 < 35:
        mean_sat = float(hsv[:, :, 1].mean())
        green_mask = ((hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 85) & (hsv[:, :, 1] > 30))
        green_ratio = float(green_mask.sum()) / (h * w)
        if mean_sat > 80 or green_ratio > 0.05 or bright_diff > 5:
            return 0.70  # mushroom: detailed bottom + supporting color/structure signal
        return 0.5  # detailed bottom but no mushroom color context

    return 0.5  # no strong signal


@register_tiebreaker("golden_retriever", "laptop")
def dog_vs_laptop(graph: SceneGraph) -> float:
    """Returns >0.5 if more like dog, <0.5 if more like laptop."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    mean_sat = float(hsv[:, :, 1].mean())

    # Laptop: low saturation (screen + muted body)
    # Dog: high saturation (golden fur in nature)
    if mean_sat < 40:
        return 0.25  # laptop signal
    if mean_sat > 70:
        return 0.75  # dog signal
    return 0.5


@register_tiebreaker("bicycle", "piano")
def bicycle_vs_piano(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bicycle, <0.5 if more like piano."""
    if graph.raw_image is None:
        return 0.5
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    col_means = gray.mean(axis=0)
    crossings = int(np.sum(np.diff(np.sign(col_means - col_means.mean())) != 0))

    # Piano has many more vertical crossings (keyboard pattern)
    if crossings > 20:
        return 0.2  # strong piano signal
    if crossings < 14:
        return 0.7  # bicycle signal
    return 0.5


@register_tiebreaker("zebra", "piano")
def zebra_vs_piano(graph: SceneGraph) -> float:
    """Returns >0.5 if more like zebra, <0.5 if more like piano."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    mean_sat = float(hsv[:, :, 1].mean())

    # Zebras have higher saturation (color in stripes/background)
    # Pianos are very low saturation (B&W keys, muted indoor)
    if mean_sat > 50:
        return 0.7  # zebra signal
    if mean_sat < 35:
        return 0.3  # piano signal
    return 0.5


@register_tiebreaker("laptop", "mushroom")
def laptop_vs_mushroom(graph: SceneGraph) -> float:
    """Returns >0.5 if more like laptop, <0.5 if more like mushroom."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    mean_sat = float(hsv[:, :, 1].mean())

    yellow = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
              (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (h * w)
    top = hsv[:h // 4, :, :]
    blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
    bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)
    if yellow_ratio > 0.1 and sky_ratio > 0.1:
        return 0.5  # yellow + sky: likely bus, not laptop or mushroom

    if mean_sat > 80:
        return 0.2  # mushroom: high saturation
    if mean_sat < 45:
        return 0.7  # laptop: low saturation
    return 0.5


@register_tiebreaker("banana", "mushroom")
def banana_vs_mushroom(graph: SceneGraph) -> float:
    """Returns >0.5 if more like banana, <0.5 if more like mushroom."""
    if graph.raw_image is None:
        return 0.5
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    bot_edges = cv2.Canny(gray[h // 2:, :], 50, 150)
    bot_edge = float(bot_edges.sum()) / 255 / (h // 2 * w)
    if bot_edge > 0.25:
        return 0.2  # mushroom signal (detailed bottom)
    return 0.5


@register_tiebreaker("banana", "golden_retriever")
def banana_vs_dog(graph: SceneGraph) -> float:
    """Returns >0.5 if more like banana, <0.5 if more like dog."""
    if graph.raw_image is None:
        return 0.5
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    gray_std = float(gray.std())
    edges = cv2.Canny(gray, 50, 150)
    h, w = gray.shape
    edge_d = float(edges.sum() / 255) / (h * w)

    if gray_std < 15 and edge_d < 0.01:
        return 0.8  # banana: very uniform bright patch
    if gray_std > 30 or edge_d > 0.1:
        return 0.2  # dog: textured
    return 0.5


@register_tiebreaker("banana", "teapot")
def banana_vs_teapot(graph: SceneGraph) -> float:
    """Returns >0.5 if more like banana, <0.5 if more like teapot."""
    if graph.raw_image is None:
        return 0.5
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    gray_std = float(gray.std())

    if gray_std < 15:
        return 0.8  # banana: extremely uniform
    if gray_std > 35:
        return 0.2  # teapot: higher contrast
    return 0.5


@register_tiebreaker("eagle", "teapot")
def eagle_vs_teapot(graph: SceneGraph) -> float:
    """Returns >0.5 if more like eagle, <0.5 if more like teapot."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Teapot guard: high edge density = object with detail (not smooth synthetic eagle)
    edges = cv2.Canny(gray, 50, 150)
    edge_d = float(edges.sum() / 255) / (h * w)
    if edge_d > 0.05:
        return 0.5  # too much detail for eagle synth

    # Eagle: high symmetry + sky + low saturation + low edges
    left = gray[:, :w // 2]
    right = np.flip(gray[:, w // 2:w // 2 * 2], axis=1)
    sym = 1.0 - float(np.abs(left.astype(float) - right.astype(float)).mean()) / 128

    top = hsv[:h // 4, :, :]
    blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
    bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)

    mean_sat = float(hsv[:, :, 1].mean())

    if sym > 0.85 and sky_ratio > 0.3 and mean_sat < 50:
        return 0.8  # strong eagle signal
    if sky_ratio > 0.4 and mean_sat < 40:
        return 0.75  # sky + desaturated
    return 0.5


@register_tiebreaker("eagle", "mushroom")
def eagle_vs_mushroom(graph: SceneGraph) -> float:
    """Returns >0.5 if more like eagle, <0.5 if more like mushroom."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    edges = cv2.Canny(gray, 50, 150)
    edge_d = float(edges.sum() / 255) / (h * w)
    if edge_d > 0.05:
        return 0.5  # too much detail for eagle synth

    top = hsv[:h // 4, :, :]
    blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
    bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)

    mean_sat = float(hsv[:, :, 1].mean())

    if sky_ratio > 0.3 and mean_sat < 50:
        return 0.8  # strong eagle signal
    return 0.5


@register_tiebreaker("bicycle", "golden_retriever")
def bicycle_vs_dog(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bicycle, <0.5 if more like dog."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = hsv.shape[:2]
    warm = ((hsv[:, :, 0] >= 8) & (hsv[:, :, 0] <= 35) &
            (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 50))
    warm_ratio = float(warm.sum()) / (h * w)
    if warm_ratio > 0.50:
        center_reg = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
        border_mean = (gray[:h // 4, :].mean() + gray[3 * h // 4:, :].mean() +
                       gray[:, :w // 4].mean() + gray[:, 3 * w // 4:].mean()) / 4
        bg_contrast = abs(float(center_reg.mean()) - border_mean)
        if bg_contrast > 30:
            return 0.5  # warm but distinct-object-on-background → could be teapot
        return 0.25  # strong dog signal (lots of warm/golden color, no bg contrast)
    return 0.5


@register_tiebreaker("laptop", "school_bus")
def laptop_vs_bus(graph: SceneGraph) -> float:
    """Returns >0.5 if more like laptop, <0.5 if more like bus."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]

    mean_sat = float(hsv[:, :, 1].mean())
    yellow = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
              (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (h * w)

    top = hsv[:h // 4, :, :]
    blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
    bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
    sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)

    if yellow_ratio > 0.15 and sky_ratio > 0.1:
        return 0.2  # strong bus signal (yellow + sky)
    if mean_sat < 50:
        return 0.8  # strong laptop signal
    return 0.5
