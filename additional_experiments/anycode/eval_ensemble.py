"""Evaluate ensemble of main forest + HOG forest on val."""
import sys
import time
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2"

CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]

# Import both forests' feature extractors
from predict import _extract_features
from build_hog_forest import extract_hog_features

# Build both forests' tree functions by importing the compiled code
# For main forest, we use predict.py's tree functions
import predict as main_forest

# For HOG forest, load the tree code
import hog_trees


def get_main_forest_trees():
    """Get all tree functions from main forest."""
    trees = []
    i = 0
    while True:
        fname = f"_tree_{i}"
        if hasattr(main_forest, fname):
            trees.append(getattr(main_forest, fname))
            i += 1
        else:
            break
    return trees


def ensemble_predict(image, main_trees):
    """Combine votes from both forests."""
    # Main forest votes
    main_feats = _extract_features(image)
    main_votes = [t(main_feats) for t in main_trees]

    # HOG forest votes
    hog_feats = extract_hog_features(image)
    hog_vote = hog_trees._hog_vote(hog_feats)

    # Combined: main forest gets weight proportional to accuracy ratio
    # main=64.4% vs hog=40.7%, so weight main ~1.6x more
    # Simple: give main forest 101 votes, HOG 40 votes (proportional to accuracy)
    votes = Counter(main_votes)
    votes[hog_vote] += 40  # HOG gets 40 effective votes vs 101 main votes

    return CLASSES[votes.most_common(1)[0][0]]


def evaluate(split="val"):
    data_root = DATA_ROOT / split
    main_trees = get_main_forest_trees()
    print(f"Loaded {len(main_trees)} main forest trees")

    correct = 0
    total = 0
    per_class = defaultdict(lambda: [0, 0])

    # Also track where they disagree
    main_only = 0
    hog_helps = 0
    hog_hurts = 0

    t0 = time.time()
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
            per_class[cls][1] += 1

            # Main forest prediction
            main_feats = _extract_features(img)
            main_votes = Counter([t(main_feats) for t in main_trees])
            main_pred = main_votes.most_common(1)[0][0]

            # HOG forest prediction
            hog_feats = extract_hog_features(img)
            hog_pred = hog_trees._hog_vote(hog_feats)

            # Ensemble
            combined = Counter(main_votes)
            combined[hog_pred] += 40
            ensemble_pred = combined.most_common(1)[0][0]

            if ensemble_pred == cls_idx:
                correct += 1
                per_class[cls][0] += 1

            # Track disagreements
            if main_pred == cls_idx and ensemble_pred != cls_idx:
                hog_hurts += 1
            elif main_pred != cls_idx and ensemble_pred == cls_idx:
                hog_helps += 1

    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"ENSEMBLE {split.upper()} ACCURACY: {correct/total:.1%} ({correct}/{total}) in {elapsed:.1f}s")
    print(f"{'='*60}")
    print(f"  HOG helps (flips wrong→correct): {hog_helps}")
    print(f"  HOG hurts (flips correct→wrong): {hog_hurts}")
    print(f"  Net from HOG: {hog_helps - hog_hurts:+d}")

    for cls in CLASSES:
        cc, ct = per_class[cls]
        print(f"  {cls:20s} {cc/ct:.1%} ({cc}/{ct})")


if __name__ == "__main__":
    split = sys.argv[1] if len(sys.argv) > 1 else "val"
    evaluate(split)
