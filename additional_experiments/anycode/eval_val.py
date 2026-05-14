"""Evaluate on val split to check generalization."""
import sys
import time
from pathlib import Path
from collections import defaultdict
import cv2

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"

CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]

sys.path.insert(0, str(Path(__file__).parent))
from predict import predict


def main():
    correct = 0
    total = 0
    per_class_correct = defaultdict(int)
    per_class_total = defaultdict(int)
    confusion = defaultdict(int)

    t0 = time.time()
    for cls in CLASSES:
        cls_dir = DATA_ROOT / cls
        if not cls_dir.exists():
            print(f"MISSING: {cls_dir}")
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            pred = predict(img)
            total += 1
            per_class_total[cls] += 1
            if pred == cls:
                correct += 1
                per_class_correct[cls] += 1
            else:
                confusion[(cls, pred)] += 1

    elapsed = time.time() - t0
    acc = correct / total if total else 0

    print(f"\n{'='*60}")
    print(f"VAL ACCURACY: {acc:.1%} ({correct}/{total}) in {elapsed:.1f}s")
    print(f"{'='*60}")

    for cls in CLASSES:
        ct = per_class_total[cls]
        cc = per_class_correct[cls]
        cls_acc = cc / ct if ct else 0
        print(f"  {cls:20s} {cls_acc:6.1%} ({cc}/{ct})")

    sorted_conf = sorted(confusion.items(), key=lambda x: -x[1])[:15]
    for (true, pred), count in sorted_conf:
        print(f"  CONFUSION: {true} -> {pred}: {count}")


if __name__ == "__main__":
    main()
