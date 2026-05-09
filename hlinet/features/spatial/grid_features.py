"""Grid-based spatial features: WHERE is the color/texture, not just IF it exists."""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(name="yellow_center_mass", tags=["spatial", "color"], description="Yellow/orange concentrated in central body region")
class YellowCenterMass:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        # Yellow/orange: H10-70, S>100, V>80
        mask = ((hsv[:, :, 0] >= 10) & (hsv[:, :, 0] <= 70) &
                (hsv[:, :, 1] > 100) & (hsv[:, :, 2] > 80))

        total_yellow = float(mask.sum())
        if total_yellow < h * w * 0.05:
            return FeatureValue.absent("insufficient yellow pixels")

        # Check concentration in center (middle 60% of image)
        center_mask = np.zeros_like(mask)
        cy, cx = int(h * 0.2), int(w * 0.2)
        center_mask[cy:h - cy, cx:w - cx] = True
        center_yellow = float((mask & center_mask).sum())
        center_ratio = center_yellow / total_yellow

        if center_ratio > 0.5 and total_yellow / (h * w) > 0.08:
            return FeatureValue.detected(
                confidence=min(center_ratio * total_yellow / (h * w) * 5, 1.0),
                evidence=[f"yellow center_ratio={center_ratio:.2f}, coverage={total_yellow/(h*w):.2f}"],
            )
        return FeatureValue.absent(f"yellow not centered: ratio={center_ratio:.2f}")


@register_feature(name="dark_horizontal_band", tags=["spatial", "layout"], description="Dark horizontal band in upper-middle (bus windows, piano keys)")
class DarkHorizontalBand:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Divide into 4 horizontal bands
        band_h = h // 4
        band_means = []
        for i in range(4):
            band = gray[i * band_h:(i + 1) * band_h, :]
            band_means.append(float(band.mean()))

        # Look for a dark band (significantly darker than neighbors)
        for i in range(1, 3):  # middle two bands
            if band_means[i] < 100:  # dark
                neighbors = []
                if i > 0:
                    neighbors.append(band_means[i - 1])
                if i < 3:
                    neighbors.append(band_means[i + 1])
                contrast = np.mean(neighbors) - band_means[i]
                if contrast > 30:
                    return FeatureValue.detected(
                        confidence=min(contrast / 80, 1.0),
                        evidence=[f"dark band at row {i}: mean={band_means[i]:.0f}, contrast={contrast:.0f}"],
                    )

        return FeatureValue.absent("no dark horizontal band")


@register_feature(name="top_heavy_blob", tags=["spatial", "layout"], description="Mass concentrated in upper half (mushroom cap, umbrella)")
class TopHeavyBlob:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Edge density comparison: top half vs bottom half
        edges = cv2.Canny(gray, 50, 150)
        top_edges = float(edges[:h // 2, :].sum())
        bottom_edges = float(edges[h // 2:, :].sum())
        total_edges = top_edges + bottom_edges + 1

        # Also check: darker/more complex top, lighter/simpler bottom (cap over stem)
        top_mean = float(gray[:h // 2, :].mean())
        bottom_mean = float(gray[h // 2:, :].mean())

        # Top-heavy: more edge content in top half AND different brightness
        top_ratio = top_edges / total_edges
        brightness_diff = abs(top_mean - bottom_mean)

        if top_ratio > 0.55 and brightness_diff > 15:
            score = (top_ratio - 0.5) * 4 + brightness_diff / 100
            return FeatureValue.detected(
                confidence=min(score, 1.0),
                evidence=[f"top_heavy: edge_ratio={top_ratio:.2f}, bright_diff={brightness_diff:.0f}"],
            )
        return FeatureValue.absent(f"not top-heavy: ratio={top_ratio:.2f}")


@register_feature(name="vertical_stem_below", tags=["spatial", "layout"], description="Thin vertical structure in bottom half (mushroom stem, lamp post)")
class VerticalStemBelow:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Look at bottom half: check for narrow vertical structure
        bottom = gray[h // 2:, :]
        edges = cv2.Canny(bottom, 50, 150)

        # Vertical edges in center third
        center_third = edges[:, w // 3:2 * w // 3]
        vert_kernel = np.array([[-1, 2, -1]], dtype=np.float32).T
        vert_response = cv2.filter2D(center_third.astype(np.float32), -1, vert_kernel)
        vert_energy = float(np.abs(vert_response).mean())

        # Also check that the center column is narrower (stem-like)
        col_sums = edges.sum(axis=0)
        center_cols = col_sums[w // 3:2 * w // 3]
        side_cols = np.concatenate([col_sums[:w // 3], col_sums[2 * w // 3:]])
        center_density = float(center_cols.mean())
        side_density = float(side_cols.mean())

        if center_density > side_density * 1.5 and vert_energy > 5:
            score = min((center_density / (side_density + 1)) * 0.3 + vert_energy / 20, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"vertical stem: center_density={center_density:.1f}, sides={side_density:.1f}"],
            )
        return FeatureValue.absent("no vertical stem detected")


@register_feature(name="uniform_background", tags=["spatial", "layout"], description="Low-complexity background (object on table/plain surface)")
class UniformBackground:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Check border regions for uniformity
        border_size = max(h // 6, 4)
        top_border = gray[:border_size, :]
        bottom_border = gray[-border_size:, :]
        left_border = gray[:, :border_size]
        right_border = gray[:, -border_size:]

        border_stds = [
            float(top_border.std()),
            float(bottom_border.std()),
            float(left_border.std()),
            float(right_border.std()),
        ]
        mean_border_std = np.mean(border_stds)

        # Center should be more complex than border
        center = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
        center_std = float(center.std())

        if mean_border_std < 30 and center_std > mean_border_std * 1.3:
            score = (1.0 - mean_border_std / 60) * 0.6 + min(center_std / mean_border_std / 5, 0.4)
            return FeatureValue.detected(
                confidence=min(score, 1.0),
                evidence=[f"uniform bg: border_std={mean_border_std:.1f}, center_std={center_std:.1f}"],
            )
        return FeatureValue.absent(f"background not uniform: border_std={mean_border_std:.1f}")
