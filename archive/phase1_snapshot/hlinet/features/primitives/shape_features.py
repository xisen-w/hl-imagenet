"""Shape-based primitive features."""

from __future__ import annotations

import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(name="circular_components", tags=["shape", "primitive"], description="Presence of circular/wheel-like components")
class CircularComponents:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        circles = [a for a in graph.atoms if a.kind == "circle"]
        count = len(circles)

        if count == 0:
            # Fall back to checking contour circularity
            round_contours = [
                a for a in graph.atoms
                if a.kind == "contour" and a.metadata.get("circularity", 0) > 0.7
            ]
            count = len(round_contours)

        if count > 0:
            return FeatureValue.detected(
                confidence=min(count * 0.3, 1.0),
                evidence=[f"found {count} circular components"],
            )
        return FeatureValue.absent("no circular components")


@register_feature(name="elongated_shape", tags=["shape", "primitive"], description="Presence of elongated (non-compact) shapes")
class ElongatedShape:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        elongated = []
        for atom in graph.atoms:
            if atom.kind in ("contour", "segment"):
                ar = atom.region.aspect_ratio
                if ar > 2.5 or ar < 0.4:
                    elongated.append(atom)

        if elongated:
            max_elongation = max(
                max(a.region.aspect_ratio, 1 / a.region.aspect_ratio) for a in elongated
            )
            return FeatureValue.detected(
                confidence=min(max_elongation / 5.0, 1.0),
                evidence=[f"{len(elongated)} elongated shapes, max ratio: {max_elongation:.1f}"],
            )
        return FeatureValue.absent("no elongated shapes")


@register_feature(name="rectangular_shape", tags=["shape", "primitive"], description="Presence of rectangular/boxy shapes")
class RectangularShape:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        rectangles = []
        for atom in graph.atoms:
            if atom.kind == "contour":
                solidity = atom.metadata.get("solidity", 0)
                circularity = atom.metadata.get("circularity", 1)
                if solidity > 0.85 and circularity < 0.6:
                    rectangles.append(atom)

        if rectangles:
            largest = max(rectangles, key=lambda a: a.region.area_fraction)
            return FeatureValue.detected(
                confidence=min(len(rectangles) * 0.25 + largest.region.area_fraction, 1.0),
                region=largest.region,
                evidence=[f"{len(rectangles)} rectangular shapes"],
            )
        return FeatureValue.absent("no rectangular shapes")


@register_feature(name="bilateral_symmetry", tags=["shape", "primitive"], description="Object exhibits bilateral symmetry")
class BilateralSymmetry:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        h, w = graph.image_shape[:2]

        left_atoms = [a for a in graph.atoms if a.region.center[0] < w / 2 and a.region.area_fraction > 0.01]
        right_atoms = [a for a in graph.atoms if a.region.center[0] >= w / 2 and a.region.area_fraction > 0.01]

        if not left_atoms or not right_atoms:
            return FeatureValue.absent("insufficient atoms for symmetry check")

        left_ys = sorted([a.region.center[1] for a in left_atoms])
        right_ys = sorted([a.region.center[1] for a in right_atoms])

        min_len = min(len(left_ys), len(right_ys))
        if min_len == 0:
            return FeatureValue.absent("no paired regions")

        left_arr = np.array(left_ys[:min_len])
        right_arr = np.array(right_ys[:min_len])
        y_correlation = 1.0 - np.mean(np.abs(left_arr - right_arr)) / h

        count_ratio = min(len(left_atoms), len(right_atoms)) / max(len(left_atoms), len(right_atoms))
        symmetry_score = (y_correlation + count_ratio) / 2

        if symmetry_score > 0.5:
            return FeatureValue.detected(
                confidence=symmetry_score,
                evidence=[f"symmetry score: {symmetry_score:.2f} (y_corr={y_correlation:.2f}, count_ratio={count_ratio:.2f})"],
            )
        return FeatureValue.absent(f"low symmetry: {symmetry_score:.2f}")
