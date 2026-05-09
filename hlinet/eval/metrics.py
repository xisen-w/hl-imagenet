"""Evaluation metrics: accuracy, confusion matrix, feature analysis."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

import numpy as np

from hlinet.types import Prediction


@dataclass
class EvalResult:
    n_samples: int = 0
    n_correct: int = 0
    n_top3_correct: int = 0
    per_class_correct: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    per_class_total: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    confusion: dict[tuple[str, str], int] = field(default_factory=lambda: defaultdict(int))
    feature_fires: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    feature_used_by_class: dict[str, set] = field(default_factory=lambda: defaultdict(set))
    latencies_ms: list[float] = field(default_factory=list)

    @property
    def top1_accuracy(self) -> float:
        return self.n_correct / max(self.n_samples, 1)

    @property
    def top3_accuracy(self) -> float:
        return self.n_top3_correct / max(self.n_samples, 1)

    @property
    def per_class_accuracy(self) -> dict[str, float]:
        return {
            cls: self.per_class_correct[cls] / max(self.per_class_total[cls], 1)
            for cls in self.per_class_total
        }

    @property
    def mean_latency_ms(self) -> float:
        return np.mean(self.latencies_ms) if self.latencies_ms else 0.0

    @property
    def feature_reuse(self) -> dict[str, int]:
        return {name: len(classes) for name, classes in self.feature_used_by_class.items()}

    def record(self, true_label: str, prediction: Prediction, latency_ms: float = 0.0) -> None:
        self.n_samples += 1
        self.per_class_total[true_label] += 1
        self.confusion[(true_label, prediction.label)] += 1
        self.latencies_ms.append(latency_ms)

        if prediction.label == true_label:
            self.n_correct += 1
            self.per_class_correct[true_label] += 1

        # Top-3
        all_labels = [prediction.label] + [l for l, _ in prediction.alternatives]
        if true_label in all_labels[:3]:
            self.n_top3_correct += 1

        # Feature usage
        for fname, fval in prediction.feature_activations.items():
            if fval.present:
                self.feature_fires[fname] += 1
                self.feature_used_by_class[fname].add(true_label)

    def summary(self) -> str:
        lines = [
            f"Evaluation Results ({self.n_samples} samples)",
            f"  Top-1 accuracy: {self.top1_accuracy:.3f}",
            f"  Top-3 accuracy: {self.top3_accuracy:.3f}",
            f"  Mean latency:   {self.mean_latency_ms:.0f} ms",
            "",
            "Per-class accuracy:",
        ]
        for cls, acc in sorted(self.per_class_accuracy.items()):
            lines.append(f"  {cls:20s} {acc:.3f} ({self.per_class_correct[cls]}/{self.per_class_total[cls]})")

        lines.append("")
        lines.append("Feature reuse (classes using each feature):")
        for fname, count in sorted(self.feature_reuse.items(), key=lambda x: -x[1])[:10]:
            lines.append(f"  {fname:25s} {count} classes")

        # Worst confusions
        lines.append("")
        lines.append("Top confusions:")
        sorted_confusion = sorted(
            [(k, v) for k, v in self.confusion.items() if k[0] != k[1]],
            key=lambda x: -x[1],
        )
        for (true, pred), count in sorted_confusion[:5]:
            lines.append(f"  {true} → {pred}: {count}")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "n_samples": self.n_samples,
            "top1_accuracy": self.top1_accuracy,
            "top3_accuracy": self.top3_accuracy,
            "mean_latency_ms": self.mean_latency_ms,
            "per_class_accuracy": self.per_class_accuracy,
            "feature_reuse": {k: v for k, v in self.feature_reuse.items()},
            "confusion_matrix": {f"{t}->{p}": c for (t, p), c in self.confusion.items()},
        }
