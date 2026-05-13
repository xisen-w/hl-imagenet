"""Local region-based features via Felzenszwalb segmentation.

Extracts per-region shape, color, texture features and computes
compositional object descriptors (e.g. "elongated smooth yellow region exists").
"""

from __future__ import annotations

import cv2
import numpy as np
from skimage.segmentation import felzenszwalb

from hlinet.types import SceneGraph


def _extract_regions(image_bgr: np.ndarray, scale: int = 50, sigma: float = 0.5,
                     min_size: int = 20) -> list[dict[str, float]]:
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    total_area = h * w

    segments = felzenszwalb(rgb, scale=scale, sigma=sigma, min_size=min_size)
    n_regions = segments.max() + 1

    edges = cv2.Canny(gray, 50, 150)

    regions = []
    for rid in range(n_regions):
        mask = (segments == rid)
        area = int(mask.sum())
        if area < 10:
            continue

        ys, xs = np.where(mask)
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        bbox_w, bbox_h = x1 - x0 + 1, y1 - y0 + 1

        aspect = max(bbox_w, bbox_h) / max(min(bbox_w, bbox_h), 1)
        fill_ratio = area / max(bbox_w * bbox_h, 1)

        cy, cx = float(ys.mean()) / h, float(xs.mean()) / w

        hue_vals = hsv[:, :, 0][mask]
        sat_vals = hsv[:, :, 1][mask]
        val_vals = hsv[:, :, 2][mask]

        warm_frac = float(((hue_vals <= 45) & (sat_vals > 50) & (val_vals > 50)).sum()) / area
        yellow_frac = float(((hue_vals >= 15) & (hue_vals <= 45) & (sat_vals > 70) & (val_vals > 70)).sum()) / area
        blue_frac = float(((hue_vals >= 75) & (hue_vals <= 145) & (sat_vals > 45) & (val_vals > 45)).sum()) / area
        green_frac = float(((hue_vals >= 35) & (hue_vals <= 85) & (sat_vals > 30) & (val_vals > 40)).sum()) / area

        edge_density = float(edges[mask].sum() / 255) / area
        gray_std = float(gray[mask].std()) / 128

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

        regions.append({
            "area_frac": area / total_area,
            "aspect": aspect,
            "fill_ratio": fill_ratio,
            "cx": cx, "cy": cy,
            "mean_sat": float(sat_vals.mean()) / 255,
            "mean_val": float(val_vals.mean()) / 255,
            "warm_frac": warm_frac,
            "yellow_frac": yellow_frac,
            "blue_frac": blue_frac,
            "green_frac": green_frac,
            "edge_density": edge_density,
            "gray_std": gray_std,
            "circularity": circularity,
            "convexity": convexity,
        })

    regions.sort(key=lambda r: r["area_frac"], reverse=True)
    return regions


def _region_stats(graph: SceneGraph) -> dict[str, float]:
    """Compute local/compositional features from region analysis."""
    image = graph.raw_image
    if image is None:
        return {}

    regions = _extract_regions(image)
    if not regions:
        return {}

    result: dict[str, float] = {}

    # --- Largest region properties ---
    r0 = regions[0]
    result["r0_area"] = r0["area_frac"]
    result["r0_aspect"] = r0["aspect"]
    result["r0_warm"] = r0["warm_frac"]
    result["r0_edge"] = r0["edge_density"]
    result["r0_circularity"] = r0["circularity"]

    # --- Object-like region detection ---
    # Find the most "object-like" region: not too small, not background-like
    # (centered, moderate size, distinct from surroundings)
    min_area = 0.03
    significant = [r for r in regions if r["area_frac"] >= min_area]

    # --- Elongated region features (banana, bus, car) ---
    elongated = [r for r in significant if r["aspect"] > 2.0]
    result["has_elongated"] = 1.0 if elongated else 0.0
    result["max_elongation"] = max((r["aspect"] for r in significant), default=1.0)
    if elongated:
        most_elongated = max(elongated, key=lambda r: r["aspect"])
        result["elong_area"] = most_elongated["area_frac"]
        result["elong_warm"] = most_elongated["warm_frac"]
        result["elong_yellow"] = most_elongated["yellow_frac"]
        result["elong_edge"] = most_elongated["edge_density"]
        result["elong_cy"] = most_elongated["cy"]
    else:
        result["elong_area"] = 0.0
        result["elong_warm"] = 0.0
        result["elong_yellow"] = 0.0
        result["elong_edge"] = 0.0
        result["elong_cy"] = 0.5

    # --- Round region features (orange, teapot body) ---
    round_regions = [r for r in significant if r["circularity"] > 0.25 and r["convexity"] > 0.5]
    result["has_round"] = 1.0 if round_regions else 0.0
    if round_regions:
        roundest = max(round_regions, key=lambda r: r["circularity"])
        result["round_area"] = roundest["area_frac"]
        result["round_warm"] = roundest["warm_frac"]
        result["round_yellow"] = roundest["yellow_frac"]
        result["round_edge"] = roundest["edge_density"]
        result["round_circularity"] = roundest["circularity"]
    else:
        result["round_area"] = 0.0
        result["round_warm"] = 0.0
        result["round_yellow"] = 0.0
        result["round_edge"] = 0.0
        result["round_circularity"] = 0.0

    # --- Sky detection (blue or bright region in top third) ---
    sky_regions = [r for r in regions if r["blue_frac"] > 0.3 and r["cy"] < 0.35 and r["area_frac"] > 0.02]
    bright_sky = [r for r in regions if r["mean_val"] > 0.7 and r["mean_sat"] < 0.15 and r["cy"] < 0.35 and r["area_frac"] > 0.03]
    result["has_sky_region"] = 1.0 if (sky_regions or bright_sky) else 0.0
    result["sky_area"] = sum(r["area_frac"] for r in sky_regions + bright_sky)

    # --- Green surround (nature context for bear, mushroom) ---
    green_regions = [r for r in regions if r["green_frac"] > 0.3 and r["area_frac"] > 0.02]
    result["has_green_surround"] = 1.0 if green_regions else 0.0
    result["green_region_area"] = sum(r["area_frac"] for r in green_regions)

    # --- Large blue region (jellyfish) ---
    blue_regions = [r for r in significant if r["blue_frac"] > 0.5]
    result["blue_region_area"] = sum(r["area_frac"] for r in blue_regions)

    # --- Smooth warm blob (banana, orange) ---
    smooth_warm = [r for r in significant if r["warm_frac"] > 0.5 and r["edge_density"] < 0.10]
    result["smooth_warm_blob_area"] = sum(r["area_frac"] for r in smooth_warm)
    if smooth_warm:
        biggest_sw = max(smooth_warm, key=lambda r: r["area_frac"])
        result["smooth_warm_blob_yellow"] = biggest_sw["yellow_frac"]
        result["smooth_warm_blob_aspect"] = biggest_sw["aspect"]
        result["smooth_warm_blob_circ"] = biggest_sw["circularity"]
    else:
        result["smooth_warm_blob_yellow"] = 0.0
        result["smooth_warm_blob_aspect"] = 1.0
        result["smooth_warm_blob_circ"] = 0.0

    # --- Textured warm blob (bear, dog) ---
    textured_warm = [r for r in significant if r["warm_frac"] > 0.3 and r["edge_density"] > 0.10]
    result["textured_warm_area"] = sum(r["area_frac"] for r in textured_warm)

    # --- Region count and diversity ---
    result["n_significant_regions"] = float(len(significant))
    result["region_area_entropy"] = _entropy([r["area_frac"] for r in significant]) if len(significant) > 1 else 0.0

    # --- Dark-light spatial pattern (penguin: dark body + white belly) ---
    dark_regions = [r for r in significant if r["mean_val"] < 0.35]
    bright_regions = [r for r in significant if r["mean_val"] > 0.65 and r["mean_sat"] < 0.25]
    result["has_dark_bright_contrast"] = 1.0 if (dark_regions and bright_regions) else 0.0

    # --- Compositional: warm object in center, different surround ---
    center_warm = [r for r in significant if r["warm_frac"] > 0.5 and 0.25 < r["cx"] < 0.75 and 0.25 < r["cy"] < 0.75]
    surround_cool = [r for r in significant if r["warm_frac"] < 0.1 and (r["cx"] < 0.2 or r["cx"] > 0.8 or r["cy"] < 0.2 or r["cy"] > 0.8)]
    result["warm_center_cool_surround"] = 1.0 if (center_warm and surround_cool) else 0.0

    return result


def _entropy(probs: list[float]) -> float:
    total = sum(probs)
    if total <= 0:
        return 0.0
    p = np.array(probs) / total
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))
