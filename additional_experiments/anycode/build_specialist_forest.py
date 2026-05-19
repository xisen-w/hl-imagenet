"""Per-class specialist forests: 10 binary classifiers (1-vs-rest).

Each specialist sees ALL 90 features (no feature subsampling needed since
binary classification with 90 features is well-conditioned).
Final prediction = class with highest specialist confidence.

This avoids the 10-way split problem where rare signal gets diluted."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import extract_features, CLASSES, gini, Node, find_best_split, build_tree, count_nodes, predict_tree, load_data

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def gini_binary(y):
    if len(y) == 0:
        return 0.0
    p = np.mean(y)
    return 2 * p * (1 - p)


def build_binary_tree(X, y, depth=0, max_depth=10, min_samples=20, n_feat_sample=30, rng=None):
    """Build tree for binary classification (class vs rest)."""
    node = Node()
    if depth >= max_depth or len(y) < min_samples or gini_binary(y) < 0.02:
        node.label = 1 if np.mean(y) > 0.5 else 0
        # Store confidence for soft voting
        node.conf = float(np.mean(y))
        return node

    n_features = X.shape[1]
    if n_feat_sample and n_feat_sample < n_features:
        feature_subset = rng.choice(n_features, n_feat_sample, replace=False)
    else:
        feature_subset = np.arange(n_features)

    # Find best binary split
    n = len(y)
    best_gain = -1
    best_feat = 0
    best_thresh = 0.0
    parent_gini = gini_binary(y)
    for f_idx in feature_subset:
        vals = X[:, f_idx]
        thresholds = np.percentile(vals, np.arange(5, 100, 5))
        thresholds = np.unique(thresholds)
        for t in thresholds:
            left_mask = vals <= t
            nl = np.sum(left_mask)
            nr = n - nl
            if nl < 5 or nr < 5:
                continue
            gain = parent_gini - (nl * gini_binary(y[left_mask]) + nr * gini_binary(y[~left_mask])) / n
            if gain > best_gain:
                best_gain = gain
                best_feat = f_idx
                best_thresh = t

    if best_gain <= 0.001:
        node.label = 1 if np.mean(y) > 0.5 else 0
        node.conf = float(np.mean(y))
        return node

    node.feat = best_feat
    node.thresh = round(float(best_thresh), 4)
    left_mask = X[:, best_feat] <= best_thresh
    node.left = build_binary_tree(X[left_mask], y[left_mask], depth + 1, max_depth, min_samples, n_feat_sample, rng)
    node.right = build_binary_tree(X[~left_mask], y[~left_mask], depth + 1, max_depth, min_samples, n_feat_sample, rng)
    return node


def predict_confidence(node, x):
    """Return P(positive class)."""
    if node.label is not None:
        return node.conf
    if x[node.feat] <= node.thresh:
        return predict_confidence(node.left, x)
    return predict_confidence(node.right, x)


def main():
    print("Loading data...")
    X_train, y_train = load_data()

    X_val, y_val = [], []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = VAL_ROOT / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            X_val.append(extract_features(img))
            y_val.append(cls_idx)
    X_val, y_val = np.array(X_val), np.array(y_val)
    print(f"Train: {len(X_train)}, Val: {len(X_val)}")

    # Build specialists
    n_trees_per_class = 31
    specialists = {}  # class_idx -> list of trees
    for cls_idx in range(10):
        print(f"\nBuilding specialist for {CLASSES[cls_idx]}...")
        y_binary = (y_train == cls_idx).astype(int)
        pos_count = np.sum(y_binary)
        neg_count = len(y_binary) - pos_count
        print(f"  Positive: {pos_count}, Negative: {neg_count}")

        trees = []
        for i in range(n_trees_per_class):
            rng = np.random.RandomState(cls_idx * 100 + i * 7 + 42)
            # Balanced bootstrap: oversample positive class
            pos_idx = np.where(y_binary == 1)[0]
            neg_idx = np.where(y_binary == 0)[0]
            boot_pos = rng.choice(pos_idx, pos_count, replace=True)
            boot_neg = rng.choice(neg_idx, pos_count, replace=True)  # balance
            indices = np.concatenate([boot_pos, boot_neg])
            rng.shuffle(indices)
            Xi, yi = X_train[indices], y_binary[indices]

            tree = build_binary_tree(Xi, yi, max_depth=10, min_samples=20,
                                    n_feat_sample=30, rng=rng)
            trees.append(tree)
        specialists[cls_idx] = trees

    # Evaluate
    for split_name, X_eval, y_eval in [("Train", X_train, y_train), ("Val", X_val, y_val)]:
        correct = 0
        for i in range(len(y_eval)):
            # Get confidence from each specialist
            scores = np.zeros(10)
            for cls_idx in range(10):
                confs = [predict_confidence(t, X_eval[i]) for t in specialists[cls_idx]]
                scores[cls_idx] = np.mean(confs)
            pred = np.argmax(scores)
            if pred == y_eval[i]:
                correct += 1
        print(f"\n{split_name}: {correct/len(y_eval):.1%} ({correct}/{len(y_eval)})")


if __name__ == "__main__":
    main()
