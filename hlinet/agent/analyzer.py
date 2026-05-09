"""Error analysis: identify worst confusion pairs and missing features."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2

from hlinet.classifier.predict import predict
from hlinet.eval.dataset import Sample
from hlinet.types import Prediction


@dataclass
class ConfusionPair:
    true_class: str
    predicted_class: str
    count: int
    example_paths: list[Path]
    missing_features: list[str]


def analyze_errors(samples: list[Sample], max_examples: int = 5) -> list[ConfusionPair]:
    """Run predictions and identify the worst confusion pairs."""
    from collections import defaultdict

    confusions: dict[tuple[str, str], list[Path]] = defaultdict(list)
    feature_gaps: dict[tuple[str, str], list[str]] = defaultdict(list)

    for sample in samples:
        image = cv2.imread(str(sample.path))
        if image is None:
            continue

        pred = predict(image)

        if pred.label != sample.label:
            key = (sample.label, pred.label)
            confusions[key].append(sample.path)

            # Find features that were expected but absent
            absent = [
                name for name, val in pred.feature_activations.items()
                if not val.present
            ]
            feature_gaps[key].extend(absent)

    # Rank by frequency
    pairs = []
    for (true_cls, pred_cls), paths in sorted(confusions.items(), key=lambda x: -len(x[1])):
        # Most commonly missing features for this pair
        gap_counts: dict[str, int] = defaultdict(int)
        for feat in feature_gaps[(true_cls, pred_cls)]:
            gap_counts[feat] += 1
        top_gaps = sorted(gap_counts.keys(), key=lambda f: -gap_counts[f])[:5]

        pairs.append(ConfusionPair(
            true_class=true_cls,
            predicted_class=pred_cls,
            count=len(paths),
            example_paths=paths[:max_examples],
            missing_features=top_gaps,
        ))

    return pairs


def format_analysis(pairs: list[ConfusionPair]) -> str:
    """Format error analysis for logging."""
    lines = ["Error Analysis", "=" * 50]
    for pair in pairs[:10]:
        lines.append(f"\n{pair.true_class} → {pair.predicted_class} ({pair.count} errors)")
        lines.append(f"  Missing features: {', '.join(pair.missing_features)}")
        lines.append(f"  Examples: {pair.example_paths[:3]}")
    return "\n".join(lines)
