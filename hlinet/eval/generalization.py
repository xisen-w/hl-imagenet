"""Generalization-aware evaluation: measures stage-by-stage transfer."""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

import cv2

from hlinet.classifier.predict import predict, PIPELINE_MODES
from hlinet.eval.dataset import PHASE2_CLASSES, load_dataset
from hlinet.eval.metrics import EvalResult
from hlinet.eval.splits import load_inner_split

LOGS_ROOT = Path(__file__).parent.parent.parent / "logs" / "generalization"
REPORT_MODE_ORDER = ("base", "base_rerank", "full")


def run_generalization_eval(
    modes: list[str] | None = None,
    tag: str = "gen_audit",
    verbose: bool = True,
) -> dict[str, dict[str, EvalResult]]:
    """Run evaluation across pipeline modes and inner splits.

    Returns: {mode: {"inner_train": EvalResult, "inner_dev": EvalResult, "val": EvalResult}}
    """
    modes = modes or list(PIPELINE_MODES)
    splits = {
        "inner_train": load_inner_split("inner_train"),
        "inner_dev": load_inner_split("inner_dev"),
        "val": load_dataset(split="val"),
    }

    results: dict[str, dict[str, EvalResult]] = {}

    for mode in modes:
        results[mode] = {}
        for split_name, samples in splits.items():
            if verbose:
                print(f"  [{mode}] {split_name} ({len(samples)} samples)...")

            result = EvalResult()
            for sample in samples:
                image = cv2.imread(str(sample.path))
                if image is None:
                    continue
                start = time.time()
                prediction = predict(image, mode=mode)
                latency = (time.time() - start) * 1000
                result.record(sample.label, prediction, latency)

            results[mode][split_name] = result
            if verbose:
                print(f"    top-1={result.top1_accuracy:.3f}  top-3={result.top3_accuracy:.3f}")

    if verbose:
        _print_summary(results)

    _save_report(results, tag)
    return results


def _print_summary(results: dict[str, dict[str, EvalResult]]) -> None:
    print("\n" + "=" * 70)
    print("GENERALIZATION REPORT")
    print("=" * 70)
    print(f"{'Mode':<14} {'inner_train':>12} {'inner_dev':>12} {'val':>12} {'gap(t-v)':>10}")
    print("-" * 70)
    for mode in REPORT_MODE_ORDER:
        if mode not in results:
            continue
        r = results[mode]
        t = r["inner_train"].top1_accuracy
        d = r["inner_dev"].top1_accuracy
        v = r["val"].top1_accuracy
        gap = t - v
        print(f"{mode:<14} {t:>11.1%} {d:>11.1%} {v:>11.1%} {gap:>9.1%}")

    print("\n--- Per-class detail (val, mode=base vs full) ---")
    if "base" in results and "full" in results:
        base_cls = results["base"]["val"].per_class_accuracy
        full_cls = results["full"]["val"].per_class_accuracy
        print(f"{'Class':<20} {'base':>8} {'full':>8} {'delta':>8}")
        for cls in sorted(base_cls.keys()):
            b = base_cls.get(cls, 0)
            f = full_cls.get(cls, 0)
            delta = f - b
            marker = " !!" if delta < -0.05 else ""
            print(f"{cls:<20} {b:>7.1%} {f:>7.1%} {delta:>+7.1%}{marker}")


def _save_report(results: dict[str, dict[str, EvalResult]], tag: str) -> Path:
    LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = LOGS_ROOT / f"{tag}_{timestamp}.json"

    report = {"tag": tag, "timestamp": timestamp, "modes": {}}
    for mode, splits in results.items():
        report["modes"][mode] = {}
        for split_name, result in splits.items():
            report["modes"][mode][split_name] = {
                "top1": result.top1_accuracy,
                "top3": result.top3_accuracy,
                "n_samples": result.n_samples,
                "per_class": result.per_class_accuracy,
            }

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    md_path = report_path.with_suffix(".md")
    with open(md_path, "w") as f:
        f.write(f"# Generalization Audit: {timestamp}\n\n")
        f.write(f"**Tag:** {tag}\n\n")
        f.write("## Summary\n\n")
        f.write(f"| Mode | inner_train | inner_dev | val | gap(t-v) |\n")
        f.write(f"|------|-------------|-----------|-----|----------|\n")
        for mode in REPORT_MODE_ORDER:
            if mode not in results:
                continue
            r = results[mode]
            t = r["inner_train"].top1_accuracy
            d = r["inner_dev"].top1_accuracy
            v = r["val"].top1_accuracy
            f.write(f"| {mode} | {t:.1%} | {d:.1%} | {v:.1%} | {t-v:+.1%} |\n")

        f.write("\n## Per-Class (val)\n\n")
        report_modes = [mode for mode in REPORT_MODE_ORDER if mode in results]
        f.write("| Class " + "".join(f"| {mode} " for mode in report_modes) + "|\n")
        f.write("|-------" + "".join("|------" for _ in report_modes) + "|\n")
        for cls in PHASE2_CLASSES:
            row = f"| {cls} "
            for mode in report_modes:
                acc = results[mode]["val"].per_class_accuracy.get(cls, 0)
                row += f"| {acc:.1%} "
            row += "|\n"
            f.write(row)

    print(f"\nReport saved: {report_path}")
    return report_path


if __name__ == "__main__":
    print("Running generalization audit...")
    print(f"Pipeline modes: {PIPELINE_MODES}")
    print()
    run_generalization_eval()
