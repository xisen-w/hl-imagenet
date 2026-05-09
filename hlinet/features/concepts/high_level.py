"""High-level concept features that compose lower-level features."""

from __future__ import annotations

import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(name="quadruped_like", tags=["concept", "animal"], description="Four-legged animal body plan")
class QuadrupedLike:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        from hlinet.registry import registry
        scores = {}

        # Check for fur/organic texture (animals have complex non-smooth texture)
        fur_feat = registry.get_feature("fur_texture")
        organic_feat = registry.get_feature("organic_texture")
        fur_val = fur_feat.evaluate(graph)
        organic_val = organic_feat.evaluate(graph)
        scores["texture"] = max(fur_val.confidence, organic_val.confidence * 0.6)

        # Check for a dominant body region that is NOT the whole image
        body_score = 0.0
        segments = sorted(
            [a for a in graph.atoms if a.kind == "segment"],
            key=lambda a: a.region.area_fraction, reverse=True,
        )
        for seg in segments[:5]:
            af = seg.region.area_fraction
            if 0.08 < af < 0.7:
                body_score = max(body_score, af * 2)
        scores["body"] = min(body_score, 1.0)

        # Exclude if strong vehicle or keyboard features
        wheel_feat = registry.get_feature("wheel_like")
        keyboard_feat = registry.get_feature("keyboard_pattern")
        if wheel_feat.evaluate(graph).confidence > 0.4:
            return FeatureValue.absent("excluded: wheels detected")
        if keyboard_feat.evaluate(graph).confidence > 0.4:
            return FeatureValue.absent("excluded: keyboard detected")

        # Non-uniform color distribution (animals aren't solid colored like vehicles)
        color_atoms = [a for a in graph.atoms if a.kind == "color_region"]
        unique_colors = set(a.metadata.get("color") for a in color_atoms)
        scores["color_variety"] = min(len(unique_colors) / 3, 1.0)

        weights = {"texture": 0.4, "body": 0.35, "color_variety": 0.25}
        total = sum(scores[k] * weights[k] for k in weights)

        if total > 0.25:
            evidence = [f"{k}: {v:.2f}" for k, v in scores.items()]
            return FeatureValue.detected(confidence=min(total, 1.0), evidence=evidence)
        return FeatureValue.absent(f"quadruped score too low: {total:.2f}")


@register_feature(name="vehicle_like", tags=["concept", "vehicle"], description="Vehicle body plan (wheels + body + road context)")
class VehicleLike:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        from hlinet.registry import registry
        scores = {}

        wheel_feat = registry.get_feature("wheel_like")
        scores["wheels"] = wheel_feat.evaluate(graph).confidence

        rect_feat = registry.get_feature("rectangular_shape")
        scores["rect_body"] = rect_feat.evaluate(graph).confidence

        # Large dominant segment (vehicle bodies are big in frame)
        large_body = 0.0
        for atom in graph.atoms:
            if atom.kind == "segment" and atom.region.area_fraction > 0.15:
                large_body = max(large_body, atom.region.area_fraction * 2)
        scores["large_body"] = min(large_body, 1.0)

        # Exclude if fur/organic (not a vehicle)
        fur_feat = registry.get_feature("fur_texture")
        if fur_feat.evaluate(graph).confidence > 0.4:
            return FeatureValue.absent("excluded: fur detected (not vehicle)")

        weights = {"wheels": 0.35, "rect_body": 0.3, "large_body": 0.35}
        total = sum(scores[k] * weights[k] for k in weights)

        if total > 0.2:
            evidence = [f"{k}: {v:.2f}" for k, v in scores.items()]
            return FeatureValue.detected(confidence=min(total, 1.0), evidence=evidence)
        return FeatureValue.absent(f"vehicle score too low: {total:.2f}")


@register_feature(name="bird_like", tags=["concept", "animal"], description="Bird body plan (wings, beak, compact body)")
class BirdLike:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        # Very strict: only fires on synthetic eagle images for now.
        # For real bird detection we need wing-spread shape + beak + feather texture.
        # At 64x64 resolution, this is extremely hard to distinguish from other objects.
        # So we use a very conservative heuristic: strong bilateral symmetry
        # + triangular overall shape + no other concept match.
        from hlinet.registry import registry

        # Must have strong bilateral symmetry
        sym_feat = registry.get_feature("bilateral_symmetry")
        sym_val = sym_feat.evaluate(graph)
        if sym_val.confidence < 0.7:
            return FeatureValue.absent("insufficient symmetry for bird")

        # Must NOT match vehicle or food
        vehicle_feat = registry.get_feature("vehicle_like")
        if vehicle_feat.evaluate(graph).confidence > 0.3:
            return FeatureValue.absent("looks more like vehicle")

        # Check for triangular/spread shape: wider at bottom than top
        h, w = graph.image_shape[:2]
        segments = [a for a in graph.atoms if a.kind == "segment" and a.region.area_fraction > 0.02]

        # Bird-specific: body should be compact and centered, with spread
        centered_compact = False
        for seg in segments:
            cx, cy = seg.region.center
            if (0.3 < cx/w < 0.7 and 0.3 < cy/h < 0.7
                    and 0.05 < seg.region.area_fraction < 0.4):
                centered_compact = True
                break

        if not centered_compact:
            return FeatureValue.absent("no centered compact body")

        # Require brown/dark coloring (eagles/hawks)
        golden_feat = registry.get_feature("golden_brown_color")
        golden_val = golden_feat.evaluate(graph)

        score = 0.3 + (golden_val.confidence * 0.3) + (sym_val.confidence - 0.7) * 0.5
        score = max(0, min(score, 0.7))

        if score > 0.35:
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"symmetry={sym_val.confidence:.2f}, golden={golden_val.confidence:.2f}"],
            )
        return FeatureValue.absent(f"bird score too low: {score:.2f}")


@register_feature(name="food_like", tags=["concept", "food"], description="Food-like object (organic, colorful, small, on surface)")
class FoodLike:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        from hlinet.registry import registry
        scores = {}

        # Food should NOT have animal/vehicle characteristics
        quadruped_feat = registry.get_feature("quadruped_like")
        vehicle_feat = registry.get_feature("vehicle_like")
        if quadruped_feat.evaluate(graph).confidence > 0.4:
            return FeatureValue.absent("excluded: looks like animal")
        if vehicle_feat.evaluate(graph).confidence > 0.4:
            return FeatureValue.absent("excluded: looks like vehicle")

        # Food is typically: small/medium object, often on a surface
        # NOT filling the entire frame like an animal close-up
        segments = sorted(
            [a for a in graph.atoms if a.kind == "segment"],
            key=lambda a: a.region.area_fraction, reverse=True,
        )
        compact_object = 0.0
        if len(segments) >= 2:
            main = segments[0]
            # Food object shouldn't dominate the frame
            if 0.05 < main.region.area_fraction < 0.45:
                compact_object = 0.6
        scores["compact_object"] = compact_object

        # Organic texture (non-metallic, non-smooth)
        organic_feat = registry.get_feature("organic_texture")
        scores["organic"] = organic_feat.evaluate(graph).confidence * 0.7

        # Bright/saturated colors
        color_atoms = [a for a in graph.atoms if a.kind == "color_region"]
        food_colors = [a for a in color_atoms if a.metadata.get("color") in ("yellow", "orange", "red", "green", "brown")]
        scores["food_colors"] = min(len(food_colors) / 3, 1.0) if food_colors else 0.0

        weights = {"compact_object": 0.4, "organic": 0.3, "food_colors": 0.3}
        total = sum(scores[k] * weights[k] for k in weights)

        if total > 0.3:
            evidence = [f"{k}: {v:.2f}" for k, v in scores.items()]
            return FeatureValue.detected(confidence=min(total, 1.0), evidence=evidence)
        return FeatureValue.absent(f"food score too low: {total:.2f}")
