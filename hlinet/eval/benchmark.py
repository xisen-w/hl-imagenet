"""Phase 2 benchmark harness for HL-ImageNet.

Compares the current HL symbolic classifier against transparent non-neural
baselines on the same split.

This module does not modify classifier behavior.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2

from hlinet.classifier.predict import predict
from hlinet.eval.baselines import BaselinePrediction, make_default_baselines
from hlinet.eval.dataset import PHASE2_CLASSES, Sample, load_dataset


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "logs" / "phase2" / "benchmarks"
DEFAULT_DATA_ROOT = REPO_ROOT / "data" / "phase2"
ACTIVE_DATA_ROOT = DEFAULT_DATA_ROOT


class ModelMetrics:
    def __init__(self, name: str, classes: list[str]):
        self.name = name
        self.classes = classes
        self.n_samples = 0
        self.n_top1 = 0
        self.n_top3 = 0
        self.latencies: list[float] = []
        self.per_class_total: Counter[str] = Counter()
        self.per_class_correct: Counter[str] = Counter()
        self.confusion: Counter[tuple[str, str]] = Counter()

    def add(self, true_label: str, pred: BaselinePrediction) -> None:
        self.n_samples += 1
        self.per_class_total[true_label] += 1
        self.confusion[(true_label, pred.label)] += 1
        self.latencies.append(float(pred.latency_ms))

        if pred.label == true_label:
            self.n_top1 += 1
            self.per_class_correct[true_label] += 1

        if true_label in pred.ranked_labels[:3]:
            self.n_top3 += 1

    @property
    def top1(self) -> float:
        return self.n_top1 / self.n_samples if self.n_samples else 0.0

    @property
    def top3(self) -> float:
        return self.n_top3 / self.n_samples if self.n_samples else 0.0

    @property
    def mean_latency_ms(self) -> float:
        return statistics.mean(self.latencies) if self.latencies else 0.0

    def per_class_recall(self) -> dict[str, float]:
        return {
            cls: self.per_class_correct[cls] / self.per_class_total[cls]
            if self.per_class_total[cls]
            else 0.0
            for cls in self.classes
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "n_samples": self.n_samples,
            "top1_accuracy": self.top1,
            "top3_accuracy": self.top3,
            "mean_latency_ms": self.mean_latency_ms,
            "per_class_recall": self.per_class_recall(),
            "confusion_matrix": {
                f"{true}->{pred}": count
                for (true, pred), count in sorted(self.confusion.items())
            },
        }


def _load_split(split: str, max_per_class: int | None) -> list[Sample]:
    split_dir = ACTIVE_DATA_ROOT / split
    return load_dataset(
        data_dir=split_dir,
        classes=PHASE2_CLASSES,
        split=split,
        max_per_class=max_per_class,
    )


def _prediction_from_hl(image, path: str | None = None) -> BaselinePrediction:
    start = time.perf_counter()
    result = predict(image)
    latency_ms = (time.perf_counter() - start) * 1000.0
    ranked = [result.label] + [label for label, _score in result.alternatives]
    for cls in PHASE2_CLASSES:
        if cls not in ranked:
            ranked.append(cls)
    return BaselinePrediction(result.label, ranked, latency_ms)


def _evaluate_predictor(name: str, samples: list[Sample], predict_fn, classes: list[str]) -> ModelMetrics:
    metrics = ModelMetrics(name, classes)

    for sample in samples:
        image = cv2.imread(str(sample.path))
        if image is None:
            continue

        pred = predict_fn(image, str(sample.path))
        metrics.add(sample.label, pred)

    return metrics


def _top_model_rows(results: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for name, payload in results["models"].items():
        rows.append({
            "name": name,
            "top1_accuracy": payload["top1_accuracy"],
            "top3_accuracy": payload["top3_accuracy"],
            "mean_latency_ms": payload["mean_latency_ms"],
        })
    return sorted(rows, key=lambda row: row["top1_accuracy"], reverse=True)


def run_benchmark(
    split: str = "val",
    train_max_per_class: int | None = None,
    eval_max_per_class: int | None = None,
    include_hl: bool = True,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    data_root: Path = DEFAULT_DATA_ROOT,
) -> dict[str, Any]:
    global ACTIVE_DATA_ROOT
    ACTIVE_DATA_ROOT = Path(data_root)
    train_samples = _load_split("train", train_max_per_class)
    eval_samples = _load_split(split, eval_max_per_class)

    if not train_samples:
        raise FileNotFoundError(
            f"No train samples found under {ACTIVE_DATA_ROOT / 'train'}"
        )

    if not eval_samples:
        raise FileNotFoundError(
            f"No eval samples found under {ACTIVE_DATA_ROOT / split}"
        )

    classes = PHASE2_CLASSES
    models: dict[str, Any] = {}

    baselines = make_default_baselines(classes)

    for baseline in baselines:
        baseline.fit(train_samples)
        metrics = _evaluate_predictor(
            baseline.name,
            eval_samples,
            lambda image, path, b=baseline: b.predict(image, path),
            classes,
        )
        models[baseline.name] = metrics.to_dict()

    if include_hl:
        hl_metrics = _evaluate_predictor(
            "hl_symbolic_classifier",
            eval_samples,
            _prediction_from_hl,
            classes,
        )
        models["hl_symbolic_classifier"] = hl_metrics.to_dict()

    artifact = {
        "schema": "hl_imagenet_phase2_benchmark_harness_v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "split": split,
        "train_samples": len(train_samples),
        "eval_samples": len(eval_samples),
        "classes": classes,
        "data_root": str(ACTIVE_DATA_ROOT),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "models": models,
        "leaderboard": _top_model_rows({"models": models}),
        "baseline_definitions": {
            "random": "Seeded random class ranking.",
            "majority_class": "Ranks classes by train-split frequency.",
            "color_centroid": "Nearest class centroid over simple color features fit on train.",
            "image_stats_centroid": "Nearest class centroid over handcrafted image statistics fit on train.",
            "handcrafted_stats_knn": "kNN over handcrafted image statistics fit on train.",
            "hl_symbolic_classifier": "Current upstream HL symbolic classifier, evaluated without behavior changes.",
        },
        "non_claim_lock": [
            "This benchmark harness does not change classifier behavior.",
            "This benchmark harness does not claim accuracy improvement.",
            "Validation results are not final test results.",
            "Baselines are transparent comparators, not neural-network comparisons.",
            "Do not claim symbolic methods beat neural systems from this artifact.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "latest_phase2_benchmark.json"
    md_path = output_dir / "latest_phase2_benchmark.md"

    json_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    write_markdown_report(artifact, md_path)

    return artifact


def write_markdown_report(artifact: dict[str, Any], path: Path) -> None:
    lines: list[str] = []

    lines.append("# HL-ImageNet Phase 2 Benchmark Harness")
    lines.append("")
    lines.append(f"Generated: `{artifact['generated_at']}`")
    lines.append(f"Split: `{artifact['split']}`")
    lines.append(f"Train samples: `{artifact['train_samples']}`")
    lines.append(f"Eval samples: `{artifact['eval_samples']}`")
    lines.append(f"Data root: `{artifact['data_root']}`")
    lines.append("")
    lines.append("## Leaderboard")
    lines.append("")
    lines.append("| Model | Top-1 | Top-3 | Mean latency ms |")
    lines.append("|---|---:|---:|---:|")

    for row in artifact["leaderboard"]:
        lines.append(
            f"| {row['name']} | {row['top1_accuracy']:.3f} | "
            f"{row['top3_accuracy']:.3f} | {row['mean_latency_ms']:.2f} |"
        )

    lines.append("")
    lines.append("## Per-class recall")
    lines.append("")

    classes = artifact["classes"]
    model_names = list(artifact["models"].keys())

    lines.append("| Class | " + " | ".join(model_names) + " |")
    lines.append("|---" + "|---:" * len(model_names) + "|")

    for cls in classes:
        row = [cls]
        for model in model_names:
            recall = artifact["models"][model]["per_class_recall"].get(cls, 0.0)
            row.append(f"{recall:.3f}")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("## Baseline definitions")
    lines.append("")
    for name, desc in artifact["baseline_definitions"].items():
        lines.append(f"- `{name}`: {desc}")

    lines.append("")
    lines.append("## Non-claim lock")
    lines.append("")
    for lock in artifact["non_claim_lock"]:
        lines.append(f"- {lock}")

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run HL-ImageNet Phase 2 benchmark harness.")
    parser.add_argument("--split", default="val", choices=["train", "val", "test"], help="Evaluation split.")
    parser.add_argument("--train-max-per-class", type=int, default=None)
    parser.add_argument("--eval-max-per-class", type=int, default=None)
    parser.add_argument("--no-hl", action="store_true", help="Skip current HL classifier.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT, help="Root containing train/val/test split folders.")
    args = parser.parse_args()

    artifact = run_benchmark(
        split=args.split,
        train_max_per_class=args.train_max_per_class,
        eval_max_per_class=args.eval_max_per_class,
        include_hl=not args.no_hl,
        output_dir=args.output_dir,
        data_root=args.data_root,
    )

    print("Phase 2 benchmark harness complete.")
    print(f"Models: {', '.join(artifact['models'].keys())}")
    print(f"JSON: {args.output_dir / 'latest_phase2_benchmark.json'}")
    print(f"Markdown: {args.output_dir / 'latest_phase2_benchmark.md'}")


if __name__ == "__main__":
    main()
