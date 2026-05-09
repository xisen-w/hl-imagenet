"""Concept router: coarse-to-fine conditional expansion of the feature space.

This is the symbolic analogue of attention — only compute features relevant
to the activated concept branches.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from hlinet.types import FeatureValue, SceneGraph
from hlinet.registry import registry


@dataclass
class Branch:
    name: str
    gate_features: list[str]
    children: list[str] = field(default_factory=list)
    threshold: float = 0.3


class ConceptRouter:
    def __init__(self):
        self.branches: dict[str, Branch] = {}

    def add_branch(self, branch: Branch) -> None:
        self.branches[branch.name] = branch

    def route(self, graph: SceneGraph) -> dict[str, float]:
        """Determine which concept branches to activate.

        Returns dict of branch_name -> activation_score.
        Only branches above threshold are returned.
        """
        activations = {}

        for name, branch in self.branches.items():
            scores = []
            for feat_name in branch.gate_features:
                try:
                    feat = registry.get_feature(feat_name)
                    val = feat.evaluate(graph)
                    scores.append(val.confidence)
                except (KeyError, Exception):
                    scores.append(0.0)

            score = max(scores) if scores else 0.0
            if score >= branch.threshold:
                activations[name] = score

        return activations

    def get_active_classes(self, activations: dict[str, float]) -> list[str]:
        """Given active branches, return the set of candidate classes."""
        classes = []
        for branch_name in activations:
            branch = self.branches[branch_name]
            classes.extend(branch.children)
        return classes
