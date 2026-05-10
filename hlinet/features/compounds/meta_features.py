"""Meta-features: compose existing feature outputs into higher-order signals."""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.registry import register_feature, get_feature
from hlinet.types import FeatureValue, Region, SceneGraph


def _eval_feature(name: str, graph: SceneGraph) -> FeatureValue:
    feat = get_feature(name)
    if feat is None:
        return FeatureValue.absent(f"feature {name} not found")
    return feat.evaluate(graph)


@register_feature(name="teapot_on_table", tags=["meta", "container"], description="top_textured_bottom_plain AND distinct_background (teapot on tabletop)")
class TeapotOnTable:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        ttbp = _eval_feature("top_textured_bottom_plain", graph)
        db = _eval_feature("distinct_background", graph)

        if ttbp.present and db.present:
            score = min(ttbp.confidence * 0.5 + db.confidence * 0.5, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"teapot_on_table: ttbp={ttbp.confidence:.2f}, bg={db.confidence:.2f}"],
            )
        return FeatureValue.absent("needs both top_textured AND distinct_bg")


@register_feature(name="indoor_still_object", tags=["meta", "container", "food"], description="distinct_background AND NOT outdoor_animal_scene (indoor tabletop object)")
class IndoorStillObject:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        db = _eval_feature("distinct_background", graph)
        oas = _eval_feature("outdoor_animal_scene", graph)

        if db.present and not oas.present:
            return FeatureValue.detected(
                confidence=db.confidence,
                evidence=[f"indoor_still: bg={db.confidence:.2f}, no_outdoor"],
            )
        return FeatureValue.absent("not indoor still object")


@register_feature(name="nature_animal_composite", tags=["meta", "animal"], description="outdoor_animal_scene AND (blob_smoothness OR golden_fur_in_nature)")
class NatureAnimalComposite:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        oas = _eval_feature("outdoor_animal_scene", graph)
        bs = _eval_feature("blob_smoothness", graph)
        gfn = _eval_feature("golden_fur_in_nature", graph)

        if not oas.present:
            return FeatureValue.absent("no outdoor scene")

        animal_signal = max(
            bs.confidence if bs.present else 0.0,
            gfn.confidence if gfn.present else 0.0,
        )
        if animal_signal > 0.2:
            score = min(oas.confidence * 0.4 + animal_signal * 0.6, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"nature_animal: outdoor={oas.confidence:.2f}, animal={animal_signal:.2f}"],
            )
        return FeatureValue.absent("outdoor but no animal signal")
