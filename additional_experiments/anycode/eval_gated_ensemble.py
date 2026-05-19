"""Gated ensemble: HOG forest only breaks ties when main forest is uncertain."""
import sys
import time
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from predict import _extract_features
from build_hog_forest import extract_hog_features
import predict as main_forest
import hog_trees

CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2"


def get_main_trees():
    trees = []
    i = 0
    while True:
        if hasattr(main_forest, f"_tree_{i}"):
            trees.append(getattr(main_forest, f"_tree_{i}"))
            i += 1
        else:
            break
    return trees


def evaluate(split="val", margin_threshold=0.15):
    data_root = DATA_ROOT / split
    main_trees = get_main_trees()
    n_trees = len(main_trees)
    print(f"Main trees: {n_trees}, margin threshold: {margin_threshold}")

    correct = 0
    total = 0
    gated_activations = 0
    gated_helps = 0
    gated_hurts = 0

    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = data_root / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            total += 1

            # Main forest
            main_feats = _extract_features(img)
            main_votes = Counter([t(main_feats) for t in main_trees])
            top2 = main_votes.most_common(2)
            main_pred = top2[0][0]
            main_conf = top2[0][1] / n_trees

            # Check margin
            if len(top2) > 1:
                margin = (top2[0][1] - top2[1][1]) / n_trees
            else:
                margin = 1.0

            if margin < margin_threshold:
                # Low confidence — consult HOG
                gated_activations += 1
                hog_feats = extract_hog_features(img)
                hog_pred = hog_trees._hog_vote(hog_feats)

                # HOG gets to break tie between main's top-2
                candidates = [top2[0][0], top2[1][0]] if len(top2) > 1 else [top2[0][0]]
                if hog_pred in candidates:
                    final_pred = hog_pred
                else:
                    final_pred = main_pred  # HOG disagrees with both → trust main
            else:
                final_pred = main_pred

            if final_pred == cls_idx:
                correct += 1
            # Track gating effect
            if margin < margin_threshold:
                if final_pred == cls_idx and main_pred != cls_idx:
                    gated_helps += 1
                elif final_pred != cls_idx and main_pred == cls_idx:
                    gated_hurts += 1

    acc = correct / total
    print(f"\n{split.upper()}: {acc:.1%} ({correct}/{total})")
    print(f"  Gated activations: {gated_activations}/{total} ({gated_activations/total:.1%})")
    print(f"  HOG helps: {gated_helps}, HOG hurts: {gated_hurts}, net: {gated_helps-gated_hurts:+d}")
    return acc


if __name__ == "__main__":
    split = sys.argv[1] if len(sys.argv) > 1 else "val"
    print("Testing margin thresholds...")
    for thresh in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        evaluate(split, margin_threshold=thresh)
        print()
