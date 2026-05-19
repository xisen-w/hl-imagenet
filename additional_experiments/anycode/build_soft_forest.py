"""Soft-voting forest: trees emit class distributions, averaged across ensemble.

Hard majority vote: each tree votes for ONE class, majority wins.
Soft probability vote: each tree emits a probability distribution over classes,
the distributions are averaged, and the highest average probability wins.

Soft voting is strictly better than hard voting when trees are uncertain —
a tree that's 60% bear, 40% GR contributes to BOTH classes instead of just bear.
This should help at decision boundaries where the forest is currently fragile.

Also tests: noise-injected trees (add Gaussian noise to features during training
to prevent memorization of exact threshold values)."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import extract_features, CLASSES, gini, find_best_split, count_nodes, load_data

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


class SoftNode:
    def __init__(self):
        self.feat = None
        self.thresh = None
        self.left = None
        self.right = None
        self.probs = None  # class probability distribution at leaf


def build_soft_tree(X, y, depth=0, max_depth=14, min_samples=16, n_feat_sample=18, rng=None, noise_std=0.0):
    node = SoftNode()
    if depth >= max_depth or len(y) < min_samples or gini(y) < 0.05:
        counts = np.bincount(y, minlength=10).astype(float)
        node.probs = counts / counts.sum()
        return node

    n_features = X.shape[1]
    if n_feat_sample and n_feat_sample < n_features:
        feature_subset = rng.choice(n_features, n_feat_sample, replace=False)
    else:
        feature_subset = np.arange(n_features)

    # Optionally add noise to features during split finding
    if noise_std > 0:
        X_noisy = X + rng.normal(0, noise_std, X.shape) * np.std(X, axis=0, keepdims=True)
    else:
        X_noisy = X

    feat, thresh, gain = find_best_split(X_noisy, y, feature_subset)
    if gain <= 0.001:
        counts = np.bincount(y, minlength=10).astype(float)
        node.probs = counts / counts.sum()
        return node

    node.feat = feat
    node.thresh = round(float(thresh), 4)
    # Split on ORIGINAL features (not noisy) for consistency
    left_mask = X[:, feat] <= thresh
    if np.sum(left_mask) < 2 or np.sum(~left_mask) < 2:
        counts = np.bincount(y, minlength=10).astype(float)
        node.probs = counts / counts.sum()
        return node

    node.left = build_soft_tree(X[left_mask], y[left_mask], depth + 1, max_depth, min_samples, n_feat_sample, rng, noise_std)
    node.right = build_soft_tree(X[~left_mask], y[~left_mask], depth + 1, max_depth, min_samples, n_feat_sample, rng, noise_std)
    return node


def predict_soft(node, x):
    """Return class probability distribution."""
    if node.probs is not None:
        return node.probs
    if x[node.feat] <= node.thresh:
        return predict_soft(node.left, x)
    return predict_soft(node.right, x)


def evaluate_hard(trees, X, y, label=""):
    """Standard hard majority vote."""
    correct = 0
    for i in range(len(y)):
        votes = Counter()
        for t in trees:
            probs = predict_soft(t, X[i])
            votes[np.argmax(probs)] += 1
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    acc = correct / len(y)
    print(f"  {label} (hard): {acc:.1%} ({correct}/{len(y)})")
    return acc


def evaluate_soft(trees, X, y, label=""):
    """Soft probability averaging."""
    correct = 0
    for i in range(len(y)):
        avg_probs = np.zeros(10)
        for t in trees:
            avg_probs += predict_soft(t, X[i])
        avg_probs /= len(trees)
        if np.argmax(avg_probs) == y[i]:
            correct += 1
    acc = correct / len(y)
    print(f"  {label} (soft): {acc:.1%} ({correct}/{len(y)})")
    return acc


def load_val_data():
    X, y = [], []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = VAL_ROOT / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            X.append(extract_features(img))
            y.append(cls_idx)
    return np.array(X), np.array(y)


def main():
    print("Loading data...")
    X_train, y_train = load_data()
    X_val, y_val = load_val_data()
    print(f"  Train: {len(X_train)}, Val: {len(X_val)}")

    configs = [
        # (noise_std, max_depth, min_samples, description)
        (0.0, 14, 16, "baseline (no noise, same as current)"),
        (0.05, 14, 16, "light noise (5% of feature std)"),
        (0.10, 14, 16, "moderate noise (10%)"),
        (0.20, 14, 16, "heavy noise (20%)"),
        (0.05, 12, 20, "noise + shallower + more regularized"),
        (0.10, 12, 24, "noise + shallow + regularized"),
    ]

    for noise_std, max_depth, min_samples, desc in configs:
        print(f"\n--- {desc} ---")
        n_trees = 101
        n_feat_sample = 18

        trees = []
        for i in range(n_trees):
            rng = np.random.RandomState(i * 7 + 42)
            indices = rng.choice(len(X_train), len(X_train), replace=True)
            Xi, yi = X_train[indices], y_train[indices]
            tree = build_soft_tree(Xi, yi, max_depth=max_depth, min_samples=min_samples,
                                  n_feat_sample=n_feat_sample, rng=rng, noise_std=noise_std)
            trees.append(tree)

        # Evaluate both hard and soft voting
        evaluate_hard(trees, X_train, y_train, "Train")
        evaluate_soft(trees, X_train, y_train, "Train")
        evaluate_hard(trees, X_val, y_val, "Val")
        val_soft = evaluate_soft(trees, X_val, y_val, "Val")


if __name__ == "__main__":
    main()
