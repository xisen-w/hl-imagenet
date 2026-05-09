"""Score classes by evaluating features along the hierarchy tree."""

from __future__ import annotations

from hlinet.classifier.hierarchy import ClassNode
from hlinet.registry import registry
from hlinet.types import FeatureValue, SceneGraph


def score_node(node: ClassNode, graph: SceneGraph, cache: dict[str, FeatureValue]) -> float:
    """Score a leaf class node against a scene graph."""
    required_score = _eval_required(node.required_features, graph, cache)
    if required_score < 0.1:
        # Fallback: still give a small score based on supporting only
        # This allows classes to compete even without required features firing
        supporting_score = _eval_feature_list(node.supporting_features, graph, cache)
        excluding_score = _eval_feature_list(node.excluding_features, graph, cache)
        fallback = supporting_score * 0.15 - excluding_score * 0.1
        return max(0.0, min(fallback, 0.3))

    supporting_score = _eval_feature_list(node.supporting_features, graph, cache)
    excluding_score = _eval_feature_list(node.excluding_features, graph, cache)

    # Required features are mandatory, supporting boost, excluding penalize
    score = required_score * 0.6 + supporting_score * 0.3 - excluding_score * 0.2
    return max(0.0, min(score, 1.0))


def _eval_required(feature_names: list[str], graph: SceneGraph, cache: dict[str, FeatureValue]) -> float:
    """For required features: ALL must fire (AND logic). Returns average confidence."""
    if not feature_names:
        return 0.5

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
        if val.confidence < 0.1:
            return 0.0  # AND logic: if any required fails, score is 0
        scores.append(val.confidence)

    return sum(scores) / len(scores) if scores else 0.0


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


def _eval_supporting_list(feature_names: list[str], graph: SceneGraph, cache: dict[str, FeatureValue]) -> float:
    """For supporting features: count how many fire above threshold, weighted by confidence."""
    if not feature_names:
        return 0.0

    firing = []
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
        if val.confidence > 0.2:
            firing.append(val.confidence)

    if not firing:
        return 0.0
    # Score based on: what fraction of supporting features fired, weighted by their strength
    fraction_firing = len(firing) / len(feature_names)
    avg_strength = sum(firing) / len(firing)
    return fraction_firing * avg_strength


def _eval_excluding_list(feature_names: list[str], graph: SceneGraph, cache: dict[str, FeatureValue]) -> float:
    """For excluding features, use top-K average — strong exclusions penalize more than weak ones."""
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
        if val.present:
            scores.append(val.confidence)

    if not scores:
        return 0.0
    # Average of top-2 firing exclusions (or just the one if only one fires)
    scores.sort(reverse=True)
    top_k = scores[:2]
    return sum(top_k) / len(top_k)
