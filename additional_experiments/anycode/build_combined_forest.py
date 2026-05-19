"""Build forest on combined features (90 global + 90 HOG spatial).

Strategy: use higher n_feat_sample to avoid dilution from doubled feature count.
Test multiple n_feat_sample values to find the sweet spot."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import extract_features, CLASSES, gini, Node, find_best_split, build_tree, count_nodes, predict_tree
from build_hog_forest import extract_hog_features

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def load_combined_data(data_root):
    X, y = [], []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = data_root / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            main_feats = extract_features(img)
            hog_feats = extract_hog_features(img)
            X.append(main_feats + hog_feats)
            y.append(cls_idx)
    return np.array(X), np.array(y)


def eval_forest(trees, X, y):
    correct = 0
    for i in range(len(y)):
        votes = Counter()
        for t in trees:
            votes[predict_tree(t, X[i])] += 1
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    return correct / len(y)


def build_forest(X, y, n_trees=101, max_depth=14, min_samples=16, n_feat_sample=18):
    trees = []
    for i in range(n_trees):
        rng = np.random.RandomState(i * 7 + 42)
        indices = rng.choice(len(X), len(X), replace=True)
        Xi, yi = X[indices], y[indices]
        tree = build_tree(Xi, yi, max_depth=max_depth, min_samples=min_samples,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
    return trees


def main():
    print("Loading combined features (main + HOG)...")
    X_train, y_train = load_combined_data(DATA_ROOT)
    X_val, y_val = load_combined_data(VAL_ROOT)
    print(f"Train: {len(X_train)} samples, {X_train.shape[1]} features")
    print(f"Val: {len(X_val)} samples")

    # Test multiple n_feat_sample values
    n_total = X_train.shape[1]  # 180
    for n_feat in [18, 27, 36, 45, 60]:
        print(f"\n--- n_feat_sample={n_feat} (n_trees=51, fast scan) ---")
        trees = build_forest(X_train, y_train, n_trees=51, n_feat_sample=n_feat)
        train_acc = eval_forest(trees, X_train, y_train)
        val_acc = eval_forest(trees, X_val, y_val)
        print(f"  Train: {train_acc:.1%}, Val: {val_acc:.1%}, Gap: {(train_acc-val_acc)*100:.1f}pp")


if __name__ == "__main__":
    main()
