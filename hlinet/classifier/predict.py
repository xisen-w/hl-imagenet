"""Top-level prediction: image → Prediction with proof."""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np

from hlinet.classifier.hierarchy import ClassNode, build_phase1_hierarchy
from hlinet.classifier.scorer import score_node
from hlinet.classifier.tiebreaker import resolve_tie
from hlinet.scene.builder import SceneGraphBuilder
from hlinet.types import FeatureValue, Prediction, SceneGraph

# Force feature/sensor registration on import
import hlinet.sensors  # noqa: F401
import hlinet.features  # noqa: F401


_hierarchy = build_phase1_hierarchy()
_builder = SceneGraphBuilder()


def predict(image: np.ndarray) -> Prediction:
    """Classify an image through the symbolic visual algebra pipeline.

    image: BGR numpy array (as loaded by cv2.imread)
    """
    graph = _builder.build(image)
    cache: dict[str, FeatureValue] = {}
    # Flat scoring: evaluate ALL leaf classes directly (no gate filtering)
    candidates = _score_all_classes_flat(_hierarchy, graph, cache)

    if not candidates:
        return Prediction(
            label="unknown",
            confidence=0.0,
            proof=["no class matched above threshold"],
            feature_activations=cache,
        )

    candidates.sort(key=lambda x: x[1], reverse=True)

    # Phase 1 tiebreaker disabled for Phase 2: soft signatures produce larger
    # margins, making the old pixel-level tiebreaker counterproductive.

    best_label, best_score, best_route = candidates[0]
    alternatives = [(label, score) for label, score, _ in candidates[1:5]]

    proof = _generate_proof(best_label, best_route, cache)

    return Prediction(
        label=best_label,
        confidence=best_score,
        alternatives=alternatives,
        proof=proof,
        feature_activations=cache,
        route=best_route,
    )


def _iterative_refine(
    candidates: list[tuple[str, float, list[str]]],
    graph: SceneGraph,
    cache: dict[str, FeatureValue],
) -> list[tuple[str, float, list[str]]]:
    """Second pass: no-op placeholder for future spatial attention refinement."""
    return candidates


def _score_all_classes_flat(
    root: ClassNode, graph: SceneGraph, cache: dict[str, FeatureValue]
) -> list[tuple[str, float, list[str]]]:
    """Score ALL leaf classes directly, ignoring gate thresholds."""
    results = []
    _collect_leaves(root, graph, cache, [], results)
    return results


def _collect_leaves(
    node: ClassNode, graph: SceneGraph, cache: dict[str, FeatureValue],
    route: list[str], results: list[tuple[str, float, list[str]]]
) -> None:
    current_route = route + [node.name]
    if node.is_leaf:
        score = score_node(node, graph, cache)
        results.append((node.name, score, current_route))
    else:
        for child in node.children:
            _collect_leaves(child, graph, cache, current_route, results)


def _generate_proof(label: str, route: list[str], cache: dict[str, FeatureValue]) -> list[str]:
    """Generate a human-readable proof trace for the prediction."""
    proof = [f"Claim: image contains '{label}'"]
    proof.append(f"Route: {' → '.join(route)}")
    proof.append("Evidence:")

    active_features = [
        (name, val) for name, val in cache.items()
        if val.present and val.confidence > 0.2
    ]
    active_features.sort(key=lambda x: x[1].confidence, reverse=True)

    for name, val in active_features[:8]:
        evidence_str = "; ".join(val.evidence[:2]) if val.evidence else "detected"
        proof.append(f"  {name}: {val.confidence:.2f} ({evidence_str})")

    absent_features = [
        (name, val) for name, val in cache.items()
        if not val.present and val.evidence
    ]
    if absent_features[:3]:
        proof.append("Absent (supporting exclusion):")
        for name, val in absent_features[:3]:
            proof.append(f"  {name}: not detected")

    return proof


def predict_file(image_path: str | Path) -> Prediction:
    """Convenience: predict from a file path."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return predict(image)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: hlinet-predict <image_path>")
        sys.exit(1)

    path = sys.argv[1]
    result = predict_file(path)

    print(f"\nPrediction: {result.label} ({result.confidence:.2f})")
    if result.alternatives:
        print(f"Alternatives: {', '.join(f'{l} ({s:.2f})' for l, s in result.alternatives)}")
    print()
    for line in result.proof:
        print(line)


if __name__ == "__main__":
    main()
