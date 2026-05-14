"""Evaluation harness for the anycode experiment.
Loads train split, runs predict() on each image, reports accuracy."""

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import cv2

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"

CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]


def load_train(max_per_class: int | None = None) -> list[tuple[Path, str]]:
    samples = []
    for cls in CLASSES:
        cls_dir = DATA_ROOT / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        if max_per_class:
            images = images[:max_per_class]
        for p in images:
            samples.append((p, cls))
    return samples


def run_eval(max_per_class: int | None = None, verbose: bool = True) -> dict:
    from predict import predict

    samples = load_train(max_per_class)
    if not samples:
        print("ERROR: No samples found. Check data/phase2/train/")
        return {}

    correct = 0
    total = 0
    per_class_correct = defaultdict(int)
    per_class_total = defaultdict(int)
    confusion = defaultdict(int)
    errors = []

    t0 = time.time()
    for path, true_label in samples:
        img = cv2.imread(str(path))
        if img is None:
            continue
        pred = predict(img)
        total += 1
        per_class_total[true_label] += 1
        if pred == true_label:
            correct += 1
            per_class_correct[true_label] += 1
        else:
            confusion[(true_label, pred)] += 1
            errors.append({"path": str(path), "true": true_label, "pred": pred})

    elapsed = time.time() - t0
    acc = correct / total if total else 0

    result = {
        "top1_accuracy": acc,
        "correct": correct,
        "total": total,
        "elapsed_s": round(elapsed, 1),
        "ms_per_image": round(elapsed / total * 1000, 1) if total else 0,
        "per_class": {},
        "top_confusions": [],
        "sample_errors": errors[:30],
    }

    if verbose:
        print(f"\n{'='*60}")
        print(f"ACCURACY: {acc:.1%} ({correct}/{total}) in {elapsed:.1f}s")
        print(f"{'='*60}")

    for cls in CLASSES:
        ct = per_class_total[cls]
        cc = per_class_correct[cls]
        cls_acc = cc / ct if ct else 0
        result["per_class"][cls] = {"accuracy": cls_acc, "correct": cc, "total": ct}
        if verbose:
            print(f"  {cls:20s} {cls_acc:6.1%} ({cc}/{ct})")

    sorted_conf = sorted(confusion.items(), key=lambda x: -x[1])[:15]
    for (true, pred), count in sorted_conf:
        result["top_confusions"].append({"true": true, "pred": pred, "count": count})
        if verbose:
            print(f"  CONFUSION: {true} -> {pred}: {count}")

    return result


if __name__ == "__main__":
    max_pc = int(sys.argv[1]) if len(sys.argv) > 1 else None
    result = run_eval(max_per_class=max_pc)
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    with open(log_dir / f"eval_{ts}.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to logs/eval_{ts}.json")
