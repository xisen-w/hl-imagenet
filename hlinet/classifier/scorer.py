"""Score classes by evaluating features along the hierarchy tree."""

from __future__ import annotations

from hlinet.classifier.hierarchy import ClassNode
from hlinet.registry import registry
from hlinet.types import FeatureValue, SceneGraph


def score_node(node: ClassNode, graph: SceneGraph, cache: dict[str, FeatureValue]) -> float:
    """Score a leaf class node against a scene graph."""
    required_score = _eval_feature_list(node.required_features, graph, cache)
    if required_score < 0.1:
        return 0.0

    supporting_score = _eval_feature_list(node.supporting_features, graph, cache)
    excluding_score = _eval_feature_list(node.excluding_features, graph, cache)

    # Required features are mandatory, supporting boost, excluding penalize
    score = required_score * 0.6 + supporting_score * 0.3 - excluding_score * 0.2
    return max(0.0, min(score, 1.0))


def score_gate(node: ClassNode, graph: SceneGraph, cache: dict[str, FeatureValue]) -> float:
    """Score a branch gate to decide whether to expand children."""
    if not node.gate_features:
        return 0.5  # no gate = always expand
    # Gate uses MAX of its features (any one can open the gate)
    scores = []
    for fname in node.gate_features:
        if fname in cache:
            val = cache[fname]
        else:
            try:
                feat = registry.get_feature(fname)
                val = feat.evaluate(graph)
                cache[fname] = val
            except (KeyError, Exception):
                val = FeatureValue.absent(f"feature {fname} unavailable")
                cache[fname] = val
        scores.append(val.confidence)
    return max(scores) if scores else 0.0


def _eval_feature_list(feature_names: list[str], graph: SceneGraph, cache: dict[str, FeatureValue]) -> float:
    if not feature_names:
        return 0.0

    scores = []
    for fname in feature_names:
        if fname in cache:
            val = cache[fname]
        else:
            try:
                feat = registry.get_feature(fname)
                val = feat.evaluate(graph)
                cache[fname] = val
            except (KeyError, Exception):
                val = FeatureValue.absent(f"feature {fname} unavailable")
                cache[fname] = val
        scores.append(val.confidence)

    return sum(scores) / len(scores) if scores else 0.0
