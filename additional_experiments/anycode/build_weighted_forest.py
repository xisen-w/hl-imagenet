"""Build forest with feature-importance-weighted sampling.

Instead of uniform random feature subsets, sample features proportional
to their F-ratio. This ensures good features appear in most splits
while still allowing diverse combinations."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import extract_features, CLASSES, FEATURE_NAMES, gini, Node, count_nodes, predict_tree, load_data

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def compute_f_ratios(X, y):
    """Compute F-ratio for each feature."""
    all_means = np.array([np.mean(X[y == c], axis=0) for c in range(10)])
    between_var = np.var(all_means, axis=0) * 10
    within_var = np.array([np.mean([np.var(X[y == c, i]) for c in range(10)]) for i in range(X.shape[1])])
    f_ratios = between_var / np.maximum(within_var, 1e-10)
    return f_ratios


def find_best_split(X, y, feature_subset):
    n = X.shape[0]
    best_gain = -1
    best_feat = 0
    best_thresh = 0.0
    parent_gini = gini(y)
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
            gain = parent_gini - (nl * gini(y[left_mask]) + nr * gini(y[~left_mask])) / n
            if gain > best_gain:
                best_gain = gain
                best_feat = f_idx
                best_thresh = t
    return best_feat, best_thresh, best_gain


def build_tree_weighted(X, y, feat_probs, depth=0, max_depth=14, min_samples=16, n_feat_sample=18, rng=None):
    node = Node()
    if depth >= max_depth or len(y) < min_samples or gini(y) < 0.05:
        node.label = int(np.argmax(np.bincount(y, minlength=10)))
        return node

    n_features = X.shape[1]
    # Weighted sampling without replacement
    feature_subset = rng.choice(n_features, min(n_feat_sample, n_features), replace=False, p=feat_probs)

    feat, thresh, gain = find_best_split(X, y, feature_subset)
    if gain <= 0.001:
        node.label = int(np.argmax(np.bincount(y, minlength=10)))
        return node

    node.feat = feat
    node.thresh = round(float(thresh), 4)
    left_mask = X[:, feat] <= thresh
    node.left = build_tree_weighted(X[left_mask], y[left_mask], feat_probs, depth + 1, max_depth, min_samples, n_feat_sample, rng)
    node.right = build_tree_weighted(X[~left_mask], y[~left_mask], feat_probs, depth + 1, max_depth, min_samples, n_feat_sample, rng)
    return node


def eval_forest(trees, X, y):
    correct = 0
    for i in range(len(y)):
        votes = Counter()
        for t in trees:
            votes[predict_tree(t, X[i])] += 1
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    return correct / len(y)


def main():
    print("Loading data...")
    X_train, y_train = load_data()
    # Load val
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
            feats = extract_features(img)
            X_val.append(feats)
            y_val.append(cls_idx)
    X_val, y_val = np.array(X_val), np.array(y_val)
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Features: {X_train.shape[1]}")

    # Compute F-ratios and convert to sampling probabilities
    f_ratios = compute_f_ratios(X_train, y_train)
    # Use sqrt of F-ratio to soften the weighting (still favors good features but not too extreme)
    weights = np.sqrt(f_ratios)
    feat_probs = weights / weights.sum()
    print(f"F-ratio range: {f_ratios.min():.3f} to {f_ratios.max():.3f}")
    print(f"Sampling prob range: {feat_probs.min():.4f} to {feat_probs.max():.4f}")

    # Also try different weight schemes
    for scheme_name, probs in [
        ("sqrt(F)", feat_probs),
        ("log(1+F)", np.log1p(f_ratios) / np.log1p(f_ratios).sum()),
        ("uniform (baseline)", np.ones(90) / 90),
    ]:
        print(f"\n--- Scheme: {scheme_name}, 51 trees ---")
        trees = []
        for i in range(51):
            rng = np.random.RandomState(i * 7 + 42)
            indices = rng.choice(len(X_train), len(X_train), replace=True)
            Xi, yi = X_train[indices], y_train[indices]
            tree = build_tree_weighted(Xi, yi, probs, max_depth=14, min_samples=16, n_feat_sample=18, rng=rng)
            trees.append(tree)
        train_acc = eval_forest(trees, X_train, y_train)
        val_acc = eval_forest(trees, X_val, y_val)
        print(f"  Train: {train_acc:.1%}, Val: {val_acc:.1%}, Gap: {100*(train_acc-val_acc):.1f}pp")


if __name__ == "__main__":
    main()
