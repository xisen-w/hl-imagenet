"""Spatial attention features: find region → analyze within region."""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


def _find_warm_blob(image):
    """Find the largest warm-colored connected component. Returns blob_mask or None."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    warm = ((hsv[:, :, 0] >= 8) & (hsv[:, :, 0] <= 35) &
            (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 50))
    if warm.sum() / (h * w) < 0.15:
        return None
    warm_uint8 = (warm * 255).astype(np.uint8)
    num_labels, labels = cv2.connectedComponents(warm_uint8)
    if num_labels <= 1:
        return None
    largest_label = 1 + np.argmax([(labels == i).sum() for i in range(1, num_labels)])
    blob_mask = (labels == largest_label).astype(np.uint8)
    if blob_mask.sum() / (h * w) < 0.10:
        return None
    return blob_mask


@register_feature(name="blob_smooth_interior", tags=["compound", "spatial_attention", "animal"], description="Low Laplacian variance within warm blob (smooth fur, not textured cap)")
class BlobSmoothInterior:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        blob_mask = _find_warm_blob(graph.raw_image)
        if blob_mask is None:
            return FeatureValue.absent("no warm blob found")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap_var = float(lap[blob_mask == 1].var())

        # Dogs: median lap_var=2635, mushrooms: 11164, teapots: 5191
        # Threshold at 4000: dogs=27/46 fire, mushrooms=7/34, teapots=11/32
        if lap_var < 4000:
            score = min((4000 - lap_var) / 3000, 1.0)
            return FeatureValue.detected(
                confidence=max(0.3, score),
                evidence=[f"smooth_blob: lap_var={lap_var:.0f}"],
            )
        return FeatureValue.absent(f"blob not smooth: lap_var={lap_var:.0f}")


@register_feature(name="blob_textured_interior", tags=["compound", "spatial_attention", "food"], description="High Laplacian variance within warm blob (gilled/textured surface)")
class BlobTexturedInterior:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        blob_mask = _find_warm_blob(graph.raw_image)
        if blob_mask is None:
            return FeatureValue.absent("no warm blob found")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap_var = float(lap[blob_mask == 1].var())

        # Mushrooms: median=11164. Threshold at 7000: mushrooms=22/34, dogs=16/46, teapots=6/32
        if lap_var > 7000:
            score = min((lap_var - 5000) / 10000, 1.0)
            return FeatureValue.detected(
                confidence=max(0.3, score),
                evidence=[f"textured_blob: lap_var={lap_var:.0f}"],
            )
        return FeatureValue.absent(f"blob not textured enough: lap_var={lap_var:.0f}")


@register_feature(name="blob_hue_uniform", tags=["compound", "spatial_attention", "animal"], description="Low hue variance within warm blob (uniform golden coat)")
class BlobHueUniform:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        blob_mask = _find_warm_blob(graph.raw_image)
        if blob_mask is None:
            return FeatureValue.absent("no warm blob found")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        blob_hue = hsv[:, :, 0][blob_mask == 1]
        hue_std = float(blob_hue.std())

        # Dogs: mean hue_std=3.6, mushrooms=5.3, teapots=3.9
        # Dogs have very uniform golden hue
        if hue_std < 3.5:
            score = min((3.5 - hue_std) / 2.0, 1.0)
            return FeatureValue.detected(
                confidence=max(0.3, score),
                evidence=[f"uniform_hue_blob: hue_std={hue_std:.1f}"],
            )
        return FeatureValue.absent(f"blob hue not uniform: std={hue_std:.1f}")


@register_feature(name="blob_compact_coverage", tags=["compound", "spatial_attention"], description="Warm blob covers large fraction of frame (animal body fills frame)")
class BlobCompactCoverage:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        blob_mask = _find_warm_blob(graph.raw_image)
        if blob_mask is None:
            return FeatureValue.absent("no warm blob found")

        h, w = graph.raw_image.shape[:2]
        coverage = float(blob_mask.sum()) / (h * w)

        # Dogs/mushrooms: coverage ~0.53, teapots: ~0.40
        if coverage > 0.48:
            score = min((coverage - 0.40) / 0.25, 1.0)
            return FeatureValue.detected(
                confidence=max(0.3, score),
                evidence=[f"large_blob: coverage={coverage:.2f}"],
            )
        return FeatureValue.absent(f"blob too small: coverage={coverage:.2f}")
