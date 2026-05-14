"""Structural part features: wheels, legs, handles, screens, keyboards."""

from __future__ import annotations

import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(name="wheel_like", tags=["part", "vehicle"], description="Circular components in lower region suggesting wheels")
class WheelLike:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        h, w = graph.image_shape[:2]
        lower_half_y = h * 0.4

        wheel_candidates = []
        for atom in graph.atoms:
            if atom.kind == "circle":
                _, cy = atom.region.center
                if cy > lower_half_y and atom.region.area_fraction > 0.04:
                    wheel_candidates.append(atom)
            elif atom.kind == "contour" and atom.metadata.get("circularity", 0) > 0.65:
                _, cy = atom.region.center
                if cy > lower_half_y and atom.region.area_fraction > 0.04:
                    wheel_candidates.append(atom)

        if len(wheel_candidates) >= 2:
            return FeatureValue.detected(
                confidence=min(len(wheel_candidates) * 0.4, 1.0),
                evidence=[f"{len(wheel_candidates)} wheel-like circles in lower region"],
            )
        elif len(wheel_candidates) == 1:
            return FeatureValue.detected(
                confidence=0.3,
                evidence=["1 wheel-like circle in lower region"],
            )
        return FeatureValue.absent("no wheel-like components")


@register_feature(name="keyboard_pattern", tags=["part", "electronics", "instrument"], description="Regular grid of rectangular keys/buttons")
class KeyboardPattern:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        # Look for many small rectangular shapes in a row
        small_rects = []
        for atom in graph.atoms:
            if atom.kind == "contour":
                solidity = atom.metadata.get("solidity", 0)
                if solidity > 0.8 and 0.001 < atom.region.area_fraction < 0.03:
                    ar = atom.region.aspect_ratio
                    if 0.3 < ar < 3.0:
                        small_rects.append(atom)

        if len(small_rects) < 5:
            return FeatureValue.absent("too few small rectangles for keyboard")

        # Check if they're aligned horizontally
        ys = [a.region.center[1] for a in small_rects]
        y_groups = {}
        for i, y in enumerate(ys):
            placed = False
            for key in y_groups:
                if abs(y - key) < graph.image_shape[0] * 0.05:
                    y_groups[key].append(i)
                    placed = True
                    break
            if not placed:
                y_groups[y] = [i]

        max_row = max(len(v) for v in y_groups.values()) if y_groups else 0

        if max_row >= 5:
            return FeatureValue.detected(
                confidence=min(max_row / 10, 1.0),
                evidence=[f"keyboard-like row of {max_row} aligned rectangles"],
            )
        return FeatureValue.absent(f"max aligned row: {max_row}")


@register_feature(name="screen_rectangle", tags=["part", "electronics"], description="Large central rectangle suggesting a screen/display")
class ScreenRectangle:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        h, w = graph.image_shape[:2]

        for atom in graph.atoms:
            if atom.kind == "contour":
                solidity = atom.metadata.get("solidity", 0)
                circularity = atom.metadata.get("circularity", 1)
                af = atom.region.area_fraction
                ar = atom.region.aspect_ratio
                # Large, rectangular, in upper-center
                if (solidity > 0.85 and circularity < 0.5
                        and af > 0.1 and 0.8 < ar < 2.5):
                    cx, cy = atom.region.center
                    if 0.2 < cx / w < 0.8 and 0.1 < cy / h < 0.7:
                        return FeatureValue.detected(
                            confidence=min(af * 3, 1.0),
                            region=atom.region,
                            evidence=[f"screen-like rectangle: area={af:.2f}, aspect={ar:.1f}"],
                        )

        return FeatureValue.absent("no screen-like rectangle found")


@register_feature(name="handle_spout", tags=["part", "container"], description="Loop/protrusion suggesting handle or spout")
class HandleSpout:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        # Handle/spout: a SMALL elongated protrusion attached to a ROUND/compact body
        # The body should be compact (not elongated like a vehicle)
        segments = sorted(
            [a for a in graph.atoms if a.kind == "segment"],
            key=lambda a: a.region.area_fraction,
            reverse=True,
        )

        if len(segments) < 3:
            return FeatureValue.absent("too few segments")

        # Body must be somewhat compact (aspect ratio near 1)
        body = segments[0]
        body_ar = body.region.aspect_ratio
        if body_ar > 2.5 or body_ar < 0.4:
            return FeatureValue.absent("body too elongated for teapot/container")

        # Look for thin protrusions on the sides (not above/below)
        h, w = graph.image_shape[:2]
        body_cx, body_cy = body.region.center
        protrusions = []

        for seg in segments[1:8]:
            af = seg.region.area_fraction
            # Protrusion should be small relative to body
            if 0.01 < af < body.region.area_fraction * 0.3:
                seg_ar = seg.region.aspect_ratio
                # Must be elongated
                if seg_ar > 2.0 or seg_ar < 0.5:
                    seg_cx, seg_cy = seg.region.center
                    # Should be roughly at same height (side protrusion)
                    if abs(seg_cy - body_cy) < h * 0.2:
                        protrusions.append(seg)

        if len(protrusions) >= 1:
            conf = min(len(protrusions) * 0.35 + 0.2, 0.8)
            return FeatureValue.detected(
                confidence=conf,
                evidence=[f"{len(protrusions)} side protrusions on compact body"],
            )
        return FeatureValue.absent("no handle/spout protrusions")


@register_feature(name="leg_like_vertical", tags=["part", "animal"], description="Multiple thin vertical components below body (legs)")
class LegLikeVertical:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        h, w = graph.image_shape[:2]
        lower_region_y = h * 0.5

        vertical_thin = []
        for atom in graph.atoms:
            if atom.kind in ("contour", "segment", "edge"):
                ar = atom.region.aspect_ratio
                _, cy = atom.region.center
                # Tall and thin, in lower half
                if ar < 0.5 and cy > lower_region_y and atom.region.area_fraction > 0.005:
                    vertical_thin.append(atom)

        if len(vertical_thin) >= 3:
            return FeatureValue.detected(
                confidence=min(len(vertical_thin) / 4, 1.0),
                evidence=[f"{len(vertical_thin)} leg-like vertical components"],
            )
        return FeatureValue.absent(f"only {len(vertical_thin)} vertical components")
