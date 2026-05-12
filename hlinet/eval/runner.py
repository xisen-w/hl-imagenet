"""Evaluation runner: orchestrates full evaluation and produces reports."""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

import cv2

from hlinet.classifier.predict import predict
from hlinet.eval.dataset import load_dataset, PHASE2_CLASSES
from hlinet.eval.metrics import EvalResult

LOGS_ROOT = Path(__file__).parent.parent.parent / "logs"


def _logs_dir_for_tag(tag: str) -> Path:
    """Route reports into phase-specific log folders."""
    return LOGS_ROOT / "phase2" if tag.startswith("phase2") else LOGS_ROOT / "phase1"


def run_evaluation(
    data_dir: Path | None = None,
    classes: list[str] | None = None,
    max_per_class: int | None = None,
    verbose: bool = True,
    auto_save: bool = True,
    tag: str = "phase1",
) -> EvalResult:
    """Run full evaluation on the dataset. Always saves a log unless auto_save=False."""
    classes = classes or PHASE2_CLASSES
    samples = load_dataset(data_dir=data_dir, classes=classes, max_per_class=max_per_class)

    if not samples:
        print("No samples found. Ensure data is in data/imagenet_10/<class_name>/")
        return EvalResult()

    result = EvalResult()

    for i, sample in enumerate(samples):
        image = cv2.imread(str(sample.path))
        if image is None:
            continue

        start = time.time()
        prediction = predict(image)
        latency = (time.time() - start) * 1000

        result.record(sample.label, prediction, latency)

        if verbose and (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(samples)}] acc={result.top1_accuracy:.3f} "
                  f"latency={result.mean_latency_ms:.0f}ms")

    if auto_save:
        save_report(result, tag=tag)

    return result


def save_report(result: EvalResult, tag: str = "phase1") -> Path:
    """Save evaluation report to logs directory."""
    logs_dir = _logs_dir_for_tag(tag)
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = logs_dir / f"eval_{tag}_{timestamp}.json"

    report = result.to_dict()
    report["tag"] = tag
    report["timestamp"] = timestamp

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    # Also save a human-readable markdown log
    md_path = logs_dir / f"eval_{tag}_{timestamp}.md"
    with open(md_path, "w") as f:
        f.write(f"# Eval Run: {timestamp}\n\n")
        f.write(f"**Tag:** {tag}\n")
        f.write(f"**Samples:** {result.n_samples}\n")
        f.write(f"**Top-1 Accuracy:** {result.top1_accuracy:.3f}\n")
        f.write(f"**Top-3 Accuracy:** {result.top3_accuracy:.3f}\n")
        f.write(f"**Mean Latency:** {result.mean_latency_ms:.0f} ms\n\n")
        f.write("## Per-Class Accuracy\n\n")
        f.write("| Class | Accuracy | Correct/Total |\n")
        f.write("|-------|----------|---------------|\n")
        for cls, acc in sorted(result.per_class_accuracy.items()):
            f.write(f"| {cls} | {acc:.3f} | {result.per_class_correct[cls]}/{result.per_class_total[cls]} |\n")
        f.write("\n## Top Confusions\n\n")
        sorted_confusion = sorted(
            [(k, v) for k, v in result.confusion.items() if k[0] != k[1]],
            key=lambda x: -x[1],
        )
        for (true, pred), count in sorted_confusion[:10]:
            f.write(f"- {true} → {pred}: {count}\n")
        f.write("\n## Feature Reuse\n\n")
        for fname, count in sorted(result.feature_reuse.items(), key=lambda x: -x[1])[:10]:
            f.write(f"- {fname}: used by {count} classes\n")

    return report_path


def main():
    """CLI entry point for evaluation."""
    import argparse
    parser = argparse.ArgumentParser(description="Run HL-Image-Net evaluation")
    parser.add_argument("--data-dir", type=Path, default=None)
    parser.add_argument("--max-per-class", type=int, default=None)
    parser.add_argument("--tag", default="phase1")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    print("Running HL-Image-Net evaluation...")
    print(f"Classes: {PHASE2_CLASSES}")
    print()

    result = run_evaluation(
        data_dir=args.data_dir,
        max_per_class=args.max_per_class,
        verbose=not args.quiet,
        auto_save=False,
    )

    print()
    print(result.summary())

    report_path = save_report(result, tag=args.tag)
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
