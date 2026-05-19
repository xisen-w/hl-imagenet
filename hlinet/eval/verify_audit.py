"""Verify rule audit: measures per-class impact of verify stage on train vs val.

Compares base_rerank predictions against full predictions to identify
which classes benefit from verify (transfer) vs which are hurt (overfit).
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import cv2

from hlinet.classifier.predict import predict
from hlinet.eval.dataset import PHASE2_CLASSES, load_dataset
from hlinet.eval.splits import load_inner_split

LOGS_ROOT = Path(__file__).parent.parent.parent / "logs" / "generalization"


def audit_verify_impact(verbose: bool = True) -> dict:
    """Compare base_rerank vs full predictions per image to measure verify impact.

    For each image, records whether verify changed the prediction and whether
    the change was correct (helped) or incorrect (hurt).
    """
    splits = {
        "inner_train": load_inner_split("inner_train"),
        "inner_dev": load_inner_split("inner_dev"),
        "val": load_dataset(split="val"),
    }

    results = {}

    for split_name, samples in splits.items():
        if verbose:
            print(f"\n[{split_name}] Auditing verify impact ({len(samples)} images)...")

        stats = {
            "total": 0,
            "verify_changed": 0,
            "verify_helped": 0,
            "verify_hurt": 0,
            "verify_neutral_change": 0,
            "per_class_helped": defaultdict(int),
            "per_class_hurt": defaultdict(int),
            "per_class_total": defaultdict(int),
            "pair_helped": defaultdict(int),
            "pair_hurt": defaultdict(int),
        }

        for sample in samples:
            image = cv2.imread(str(sample.path))
            if image is None:
                continue

            pred_base = predict(image, mode="base_rerank")
            pred_full = predict(image, mode="full")

            stats["total"] += 1
            stats["per_class_total"][sample.label] += 1

            if pred_base.label != pred_full.label:
                stats["verify_changed"] += 1
                base_correct = pred_base.label == sample.label
                full_correct = pred_full.label == sample.label

                if full_correct and not base_correct:
                    stats["verify_helped"] += 1
                    stats["per_class_helped"][sample.label] += 1
                    pair_key = f"{pred_base.label}->{sample.label}"
                    stats["pair_helped"][pair_key] += 1
                elif base_correct and not full_correct:
                    stats["verify_hurt"] += 1
                    stats["per_class_hurt"][sample.label] += 1
                    pair_key = f"{sample.label}->{pred_full.label}"
                    stats["pair_hurt"][pair_key] += 1
                else:
                    stats["verify_neutral_change"] += 1

        results[split_name] = stats

        if verbose:
            pct_changed = stats["verify_changed"] / max(stats["total"], 1) * 100
            print(f"  Changed: {stats['verify_changed']}/{stats['total']} ({pct_changed:.1f}%)")
            print(f"  Helped: {stats['verify_helped']}, Hurt: {stats['verify_hurt']}, "
                  f"Neutral swap: {stats['verify_neutral_change']}")
            print(f"  Net impact: {stats['verify_helped'] - stats['verify_hurt']:+d}")

    if verbose:
        _print_report(results)

    _save_report(results)
    return results


def _print_report(results: dict) -> None:
    print("\n" + "=" * 70)
    print("VERIFY AUDIT: Per-class help/hurt")
    print("=" * 70)

    print(f"\n{'Class':<20} {'train_help':>10} {'train_hurt':>10} "
          f"{'dev_help':>9} {'dev_hurt':>9} {'val_help':>9} {'val_hurt':>9}")
    print("-" * 70)

    for cls in PHASE2_CLASSES:
        row = f"{cls:<20}"
        for split in ("inner_train", "inner_dev", "val"):
            h = results[split]["per_class_helped"].get(cls, 0)
            hu = results[split]["per_class_hurt"].get(cls, 0)
            row += f" {h:>9d} {hu:>9d}"
        print(row)

    print("\n--- Top verify-hurt patterns on val ---")
    val_hurt = results["val"]["pair_hurt"]
    for pair, count in sorted(val_hurt.items(), key=lambda x: -x[1])[:10]:
        print(f"  {pair}: {count}")

    print("\n--- Top verify-helped patterns on val ---")
    val_helped = results["val"]["pair_helped"]
    for pair, count in sorted(val_helped.items(), key=lambda x: -x[1])[:10]:
        print(f"  {pair}: {count}")

    print("\n--- Transfer ratio (dev_net / train_net) ---")
    for split in ("inner_train", "inner_dev", "val"):
        net = results[split]["verify_helped"] - results[split]["verify_hurt"]
        total = results[split]["total"]
        print(f"  {split}: net={net:+d} ({net/total*100:+.1f}%)")


def _save_report(results: dict) -> None:
    LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = LOGS_ROOT / f"verify_audit_{timestamp}.json"

    serializable = {}
    for split_name, stats in results.items():
        serializable[split_name] = {
            "total": stats["total"],
            "verify_changed": stats["verify_changed"],
            "verify_helped": stats["verify_helped"],
            "verify_hurt": stats["verify_hurt"],
            "verify_neutral_change": stats["verify_neutral_change"],
            "per_class_helped": dict(stats["per_class_helped"]),
            "per_class_hurt": dict(stats["per_class_hurt"]),
            "per_class_total": dict(stats["per_class_total"]),
            "pair_helped": dict(stats["pair_helped"]),
            "pair_hurt": dict(stats["pair_hurt"]),
        }

    with open(path, "w") as f:
        json.dump(serializable, f, indent=2)
    print(f"\nReport saved: {path}")


if __name__ == "__main__":
    audit_verify_impact()
