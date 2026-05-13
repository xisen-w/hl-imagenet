"""Local region-based class verifiers.

Instead of scoring from global stats alone, these verifiers:
1. Extract candidate object regions (warm blobs, yellow blobs, etc.)
2. Run class-specific shape/color/texture checks on the best-matching region
3. Return a local evidence score that complements the global signature
"""

from __future__ import annotations

import cv2
import numpy as np
from skimage.segmentation import felzenszwalb

from hlinet.types import SceneGraph


def _extract_proposals(image_bgr: np.ndarray) -> dict[str, dict]:
    """Extract 5 types of region proposals from the image."""
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    total_area = h * w

    hue = hsv[:, :, 0]
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]

    warm_mask = (((hue >= 5) & (hue <= 45)) | (hue <= 5)) & (sat > 50) & (val > 50)
    yellow_mask = (hue >= 15) & (hue <= 45) & (sat > 70) & (val > 70)
    dark_mask = (val < 80) & (sat < 60)
    edges = cv2.Canny(gray, 50, 150)

    proposals = {}

    for name, mask in [("warm", warm_mask), ("yellow", yellow_mask), ("dark", dark_mask)]:
        region = _largest_blob(mask, gray, hsv, edges, h, w, total_area)
        if region is not None:
            proposals[name] = region

    edge_region = _largest_edge_component(edges, gray, hsv, h, w, total_area)
    if edge_region is not None:
        proposals["edge"] = edge_region

    center_region = _center_crop_region(gray, hsv, edges, h, w, total_area)
    proposals["center"] = center_region

    return proposals


def _largest_blob(mask: np.ndarray, gray: np.ndarray, hsv: np.ndarray,
                  edges: np.ndarray, h: int, w: int, total_area: int) -> dict | None:
    """Find the largest connected component in the mask and characterize it."""
    mask_u8 = (mask * 255).astype(np.uint8)
    num_labels, labels = cv2.connectedComponents(mask_u8)
    if num_labels <= 1:
        return None

    sizes = [(labels == i).sum() for i in range(1, num_labels)]
    largest_id = 1 + int(np.argmax(sizes))
    blob_mask = (labels == largest_id)
    area = int(blob_mask.sum())
    if area < 30:
        return None

    return _characterize_region(blob_mask, gray, hsv, edges, h, w, total_area)


def _largest_edge_component(edges: np.ndarray, gray: np.ndarray, hsv: np.ndarray,
                            h: int, w: int, total_area: int) -> dict | None:
    """Find the largest connected edge structure."""
    dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    num_labels, labels = cv2.connectedComponents(dilated)
    if num_labels <= 1:
        return None

    sizes = [(labels == i).sum() for i in range(1, num_labels)]
    largest_id = 1 + int(np.argmax(sizes))
    blob_mask = (labels == largest_id)
    area = int(blob_mask.sum())
    if area < 30:
        return None

    return _characterize_region(blob_mask, gray, hsv, edges, h, w, total_area)


def _center_crop_region(gray: np.ndarray, hsv: np.ndarray, edges: np.ndarray,
                        h: int, w: int, total_area: int) -> dict:
    """Characterize the center 50% crop as a region."""
    mask = np.zeros((h, w), dtype=bool)
    y0, y1 = h // 4, 3 * h // 4
    x0, x1 = w // 4, 3 * w // 4
    mask[y0:y1, x0:x1] = True
    return _characterize_region(mask, gray, hsv, edges, h, w, total_area)


def _characterize_region(mask: np.ndarray, gray: np.ndarray, hsv: np.ndarray,
                         edges: np.ndarray, h: int, w: int, total_area: int) -> dict:
    """Compute shape, color, texture, position features for a masked region."""
    ys, xs = np.where(mask)
    area = len(ys)
    if area < 10:
        return _empty_region()

    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    bbox_w = x1 - x0 + 1
    bbox_h = y1 - y0 + 1

    aspect = max(bbox_w, bbox_h) / max(min(bbox_w, bbox_h), 1)
    fill_ratio = area / max(bbox_w * bbox_h, 1)
    coverage = area / total_area

    cy = float(ys.mean()) / h
    cx = float(xs.mean()) / w

    hue_vals = hsv[:, :, 0][mask]
    sat_vals = hsv[:, :, 1][mask]
    val_vals = hsv[:, :, 2][mask]

    mean_hue = float(hue_vals.mean())
    mean_sat = float(sat_vals.mean()) / 255
    mean_val = float(val_vals.mean()) / 255
    hue_std = float(hue_vals.std())

    warm_frac = float(((hue_vals <= 45) & (sat_vals > 50) & (val_vals > 50)).sum()) / area
    yellow_frac = float(((hue_vals >= 15) & (hue_vals <= 45) & (sat_vals > 70) & (val_vals > 70)).sum()) / area
    orange_frac = float(((hue_vals >= 5) & (hue_vals <= 18) & (sat_vals > 80) & (val_vals > 80)).sum()) / area

    edge_density = float(edges[mask].sum() / 255) / area
    gray_std = float(gray[mask].std()) / 128
    gray_mean = float(gray[mask].mean()) / 255

    # Circularity from contour
    mask_u8 = (mask * 255).astype(np.uint8)
    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circularity = 0.0
    convexity = 0.0
    if contours:
        c = max(contours, key=cv2.contourArea)
        ca = cv2.contourArea(c)
        cp = cv2.arcLength(c, True)
        if cp > 0 and ca > 10:
            circularity = 4 * np.pi * ca / (cp * cp)
            hull = cv2.convexHull(c)
            hull_area = cv2.contourArea(hull)
            if hull_area > 0:
                convexity = ca / hull_area

    # Left-right asymmetry (handle detection proxy)
    mid_x = (x0 + x1) // 2
    left_edge = float(edges[y0:y1+1, x0:mid_x].sum()) / max(1, (mid_x - x0) * bbox_h)
    right_edge = float(edges[y0:y1+1, mid_x:x1+1].sum()) / max(1, (x1 - mid_x) * bbox_h)
    lr_asymmetry = abs(left_edge - right_edge) / max(left_edge + right_edge, 1e-6)

    return {
        "area": area,
        "coverage": coverage,
        "aspect": aspect,
        "fill_ratio": fill_ratio,
        "cx": cx, "cy": cy,
        "mean_hue": mean_hue,
        "mean_sat": mean_sat,
        "mean_val": mean_val,
        "hue_std": hue_std,
        "warm_frac": warm_frac,
        "yellow_frac": yellow_frac,
        "orange_frac": orange_frac,
        "edge_density": edge_density,
        "gray_std": gray_std,
        "gray_mean": gray_mean,
        "circularity": circularity,
        "convexity": convexity,
        "lr_asymmetry": lr_asymmetry,
        "bbox": (x0, y0, bbox_w, bbox_h),
    }


def _empty_region() -> dict:
    return {
        "area": 0, "coverage": 0, "aspect": 1.0, "fill_ratio": 0,
        "cx": 0.5, "cy": 0.5, "mean_hue": 0, "mean_sat": 0, "mean_val": 0,
        "hue_std": 0, "warm_frac": 0, "yellow_frac": 0, "orange_frac": 0,
        "edge_density": 0, "gray_std": 0, "gray_mean": 0,
        "circularity": 0, "convexity": 0, "lr_asymmetry": 0, "bbox": (0, 0, 0, 0),
    }


def _sigmoid(x: float, center: float, scale: float) -> float:
    z = (x - center) * scale
    z = max(-10, min(10, z))
    return 1.0 / (1.0 + np.exp(-z))


# --- Class-specific local verifiers ---

def banana_local_score(proposals: dict[str, dict]) -> tuple[float, list[str]]:
    """Banana = elongated, smooth, yellow region. NOT circular."""
    reasons = []
    best = proposals.get("yellow") or proposals.get("warm")
    if best is None or best["coverage"] < 0.02:
        return 0.0, ["no yellow/warm blob"]

    score = 0.0

    # Elongated shape (banana is curved/long, aspect > 1.8)
    elong = _sigmoid(best["aspect"], 1.8, 2.0)
    score += elong * 0.30
    if elong > 0.5:
        reasons.append(f"elongated({best['aspect']:.1f})")

    # Smooth interior (low edge density)
    smooth = _sigmoid(best["edge_density"], 0.10, -10)
    score += smooth * 0.25
    if smooth > 0.5:
        reasons.append("smooth")

    # Yellow color
    yel = _sigmoid(best["yellow_frac"], 0.30, 5)
    score += yel * 0.20
    if yel > 0.5:
        reasons.append(f"yellow({best['yellow_frac']:.2f})")

    # NOT circular (anti-orange)
    not_circ = _sigmoid(best["circularity"], 0.35, -5)
    score += not_circ * 0.15
    if not_circ > 0.5:
        reasons.append(f"non-circular({best['circularity']:.2f})")

    # Reasonable coverage
    cov = _sigmoid(best["coverage"], 0.05, 15)
    score += cov * 0.10

    return score, reasons


def orange_local_score(proposals: dict[str, dict]) -> tuple[float, list[str]]:
    """Orange = circular, saturated, warm/orange-hued, compact. NOT elongated."""
    reasons = []
    best = proposals.get("warm") or proposals.get("yellow")
    if best is None or best["coverage"] < 0.02:
        return 0.0, ["no warm/yellow blob"]

    score = 0.0

    # Circular shape
    circ = _sigmoid(best["circularity"], 0.25, 6)
    score += circ * 0.25
    if circ > 0.5:
        reasons.append(f"circular({best['circularity']:.2f})")

    # High saturation
    sat = _sigmoid(best["mean_sat"], 0.45, 6)
    score += sat * 0.20
    if sat > 0.5:
        reasons.append(f"saturated({best['mean_sat']:.2f})")

    # Orange hue (hue 5-18 in OpenCV, not banana's 20-35)
    ora = _sigmoid(best["orange_frac"], 0.15, 8)
    score += ora * 0.20
    if ora > 0.5:
        reasons.append(f"orange_hue({best['orange_frac']:.2f})")

    # Compact (low aspect, near 1.0)
    compact = _sigmoid(best["aspect"], 1.8, -2.0)
    score += compact * 0.15
    if compact > 0.5:
        reasons.append(f"compact({best['aspect']:.1f})")

    # Reasonable coverage
    cov = _sigmoid(best["coverage"], 0.05, 15)
    score += cov * 0.10

    # Convexity bonus
    conv = _sigmoid(best["convexity"], 0.60, 5)
    score += conv * 0.10

    return score, reasons


def teapot_local_score(proposals: dict[str, dict]) -> tuple[float, list[str]]:
    """Teapot = compact central object, moderate edge, low saturation, possible handle asymmetry."""
    reasons = []
    best = proposals.get("center")
    if best is None:
        return 0.0, ["no center region"]

    edge_r = proposals.get("edge")

    score = 0.0

    # Central object (center-surround difference)
    center_obj = _sigmoid(best["gray_std"], 0.15, 5)
    score += center_obj * 0.15
    if center_obj > 0.5:
        reasons.append("central_object")

    # Low saturation (teapots are often metallic/ceramic)
    low_sat = _sigmoid(best["mean_sat"], 0.35, -5)
    score += low_sat * 0.20
    if low_sat > 0.5:
        reasons.append(f"low_sat({best['mean_sat']:.2f})")

    # Moderate edge density (not smooth like fruit, not chaotic like nature)
    mod_edge = 1.0 - abs(best["edge_density"] - 0.12) * 8
    mod_edge = max(0, min(1, mod_edge))
    score += mod_edge * 0.15
    if mod_edge > 0.5:
        reasons.append(f"moderate_edge({best['edge_density']:.2f})")

    # Not yellow/warm (anti-banana, anti-orange)
    not_warm = _sigmoid(best["warm_frac"], 0.30, -4)
    score += not_warm * 0.15
    if not_warm > 0.5:
        reasons.append("not_warm")

    # Left-right asymmetry in edges (handle/spout proxy)
    if edge_r is not None:
        asym = _sigmoid(edge_r["lr_asymmetry"], 0.15, 6)
        score += asym * 0.15
        if asym > 0.5:
            reasons.append(f"asymmetric({edge_r['lr_asymmetry']:.2f})")
    else:
        score += 0.0

    # Not green (anti-nature)
    # Use warm_frac as proxy (teapots shouldn't have green)
    score += 0.10 * _sigmoid(best["gray_mean"], 0.35, 3)

    # Compact shape
    compact = _sigmoid(best["aspect"] if edge_r else 1.5, 2.5, -2)
    score += compact * 0.10

    return score, reasons


def compute_local_scores(graph: SceneGraph) -> dict[str, tuple[float, list[str]]]:
    """Compute local verifier scores for all supported classes."""
    image = graph.raw_image
    if image is None:
        return {}

    proposals = _extract_proposals(image)
    if not proposals:
        return {}

    return {
        "banana": banana_local_score(proposals),
        "orange": orange_local_score(proposals),
        "teapot": teapot_local_score(proposals),
    }
