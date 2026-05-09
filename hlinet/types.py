"""Core types for the Visual Concept Algebra.

Five types form the foundation:
- Region: a spatial extent in the image
- Atom: a primitive visual observation
- FeatureValue: the universal return type of every feature
- SceneGraph: a structured representation of an image
- Prediction: a classification result with proof
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import networkx as nx
import numpy as np


@dataclass(frozen=True)
class Region:
    bbox: tuple[int, int, int, int]  # x, y, w, h
    mask: np.ndarray | None = field(default=None, repr=False, compare=False)
    area_fraction: float = 0.0

    @property
    def center(self) -> tuple[float, float]:
        x, y, w, h = self.bbox
        return (x + w / 2, y + h / 2)

    @property
    def aspect_ratio(self) -> float:
        _, _, w, h = self.bbox
        return w / max(h, 1)

    def overlaps(self, other: Region) -> float:
        x1, y1, w1, h1 = self.bbox
        x2, y2, w2, h2 = other.bbox
        xi = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
        yi = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
        intersection = xi * yi
        union = w1 * h1 + w2 * h2 - intersection
        return intersection / max(union, 1)


@dataclass
class Atom:
    kind: str  # "edge", "blob", "texture_patch", "contour", "keypoint", "segment"
    region: Region
    descriptor: np.ndarray = field(repr=False)
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FeatureValue:
    present: bool
    confidence: float  # [0, 1]
    region: Region | None = None
    evidence: list[str] = field(default_factory=list)
    sub_values: dict[str, FeatureValue] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @staticmethod
    def absent(reason: str = "") -> FeatureValue:
        return FeatureValue(present=False, confidence=0.0, evidence=[reason] if reason else [])

    @staticmethod
    def detected(confidence: float, region: Region | None = None, evidence: list[str] | None = None) -> FeatureValue:
        return FeatureValue(present=True, confidence=confidence, region=region, evidence=evidence or [])


@dataclass
class SceneGraph:
    graph: nx.DiGraph
    image_shape: tuple[int, int, int]
    atoms: list[Atom] = field(default_factory=list)

    @property
    def nodes(self) -> list[dict]:
        return [self.graph.nodes[n] for n in self.graph.nodes]

    @property
    def regions(self) -> list[Region]:
        return [self.graph.nodes[n]["region"] for n in self.graph.nodes if "region" in self.graph.nodes[n]]

    def get_relations(self, rel_type: str | None = None) -> list[tuple[int, int, dict]]:
        edges = list(self.graph.edges(data=True))
        if rel_type:
            edges = [(u, v, d) for u, v, d in edges if d.get("type") == rel_type]
        return edges

    def nodes_with_attr(self, key: str, value: Any = None) -> list[int]:
        results = []
        for n, data in self.graph.nodes(data=True):
            if key in data:
                if value is None or data[key] == value:
                    results.append(n)
        return results


@dataclass
class Prediction:
    label: str
    confidence: float
    alternatives: list[tuple[str, float]] = field(default_factory=list)
    proof: list[str] = field(default_factory=list)
    feature_activations: dict[str, FeatureValue] = field(default_factory=dict)
    route: list[str] = field(default_factory=list)  # path through hierarchy


# --- Protocols ---

@runtime_checkable
class Sensor(Protocol):
    name: str
    output_kinds: list[str]

    def extract(self, image: np.ndarray) -> list[Atom]: ...


@runtime_checkable
class Feature(Protocol):
    name: str
    version: str
    description: str
    tags: list[str]

    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue: ...
