"""Color-based primitive features."""

from __future__ import annotations

import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(name="yellow_dominant", tags=["color", "primitive"], description="Image has dominant yellow coloring")
class YellowDominant:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        yellow_coverage = 0.0
        for atom in graph.atoms:
            if atom.kind == "color_region" and atom.metadata.get("color") == "yellow":
                yellow_coverage += atom.region.area_fraction

        if yellow_coverage > 0.1:
            return FeatureValue.detected(
                confidence=min(yellow_coverage * 3, 1.0),
                evidence=[f"yellow coverage: {yellow_coverage:.2f}"],
            )
        return FeatureValue.absent("no significant yellow")


@register_feature(name="black_white_dominant", tags=["color", "primitive"], description="Image is primarily black and white")
class BlackWhiteDominant:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        bw_coverage = 0.0
        for atom in graph.atoms:
            if atom.kind == "color_region" and atom.metadata.get("color") in ("black", "white"):
                bw_coverage += atom.region.area_fraction

        color_hist = [a for a in graph.atoms if a.kind == "color_hist"]
        low_saturation = False
        if color_hist:
            sat_mean = color_hist[0].metadata.get("saturation_mean", 0.5)
            low_saturation = sat_mean < 0.3

        present = bw_coverage > 0.3 or low_saturation
        conf = min(bw_coverage * 2, 1.0) if present else 0.0
        return FeatureValue(
            present=present,
            confidence=conf,
            evidence=[f"BW coverage: {bw_coverage:.2f}", f"low saturation: {low_saturation}"],
        )


@register_feature(name="golden_brown_color", tags=["color", "primitive"], description="Golden/brown coloring (fur, wood)")
class GoldenBrownColor:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        coverage = 0.0
        for atom in graph.atoms:
            if atom.kind == "color_region" and atom.metadata.get("color") in ("golden", "brown", "orange"):
                coverage += atom.region.area_fraction

        if coverage > 0.1:
            return FeatureValue.detected(
                confidence=min(coverage * 3, 1.0),
                evidence=[f"golden/brown coverage: {coverage:.2f}"],
            )
        return FeatureValue.absent("no significant golden/brown")


@register_feature(name="green_context", tags=["color", "context", "primitive"], description="Green background suggesting outdoor/nature")
class GreenContext:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        green_coverage = 0.0
        for atom in graph.atoms:
            if atom.kind == "color_region" and atom.metadata.get("color") == "green":
                green_coverage += atom.region.area_fraction

        if green_coverage > 0.05:
            return FeatureValue.detected(
                confidence=min(green_coverage * 4, 1.0),
                evidence=[f"green coverage: {green_coverage:.2f} (outdoor context)"],
            )
        return FeatureValue.absent("no green context")
