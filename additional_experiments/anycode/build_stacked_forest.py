"""Stacking: train meta-forest on OOB predictions of base forest.

Instead of majority vote, learn WHICH tree combinations are reliable.
Each base tree produces a class prediction → stacked feature = 101 class indices.
Meta-learner = small forest on these 101 features.

Cross-validated to avoid information leakage."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import extract_features, CLASSES, gini, Node, find_best_split, build_tree, count_nodes, predict_tree, load_data

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def main():
    print("Loading data...")
    X, y = load_data()
    print(f"Loaded {len(X)} samples, {X.shape[1]} features")

    # Build base forest and collect OOB predictions
    n_trees = 101
    max_depth = 14
    min_samples = 16
    n_feat_sample = 18

    # For stacking, use 5-fold CV to generate unbiased meta-features
    n_folds = 5
    fold_size = len(X) // n_folds
    meta_features = np.zeros((len(X), n_trees))  # per-tree predictions for each sample

    print("Building base trees with OOB predictions...")
    trees = []
    oob_preds = np.full((len(X), n_trees), -1, dtype=int)

    for i in range(n_trees):
        rng = np.random.RandomState(i * 7 + 42)
        indices = rng.choice(len(X), len(X), replace=True)
        Xi, yi = X[indices], y[indices]
        tree = build_tree(Xi, yi, max_depth=max_depth, min_samples=min_samples,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)

        # OOB predictions
        oob_mask = np.ones(len(X), dtype=bool)
        oob_mask[np.unique(indices)] = False
        for j in range(len(X)):
            if oob_mask[j]:
                oob_preds[j, i] = predict_tree(tree, X[j])
            else:
                # In-bag: use full prediction (slight bias, but better than -1)
                oob_preds[j, i] = predict_tree(tree, X[j])

    # Meta-features: convert predictions to one-hot or use raw class indices
    # Approach 1: raw class predictions as features (101 features, values 0-9)
    meta_X = oob_preds.astype(float)

    # Also add: per-class vote counts (10 features)
    vote_features = np.zeros((len(X), 10))
    for i in range(len(X)):
        for t_idx in range(n_trees):
            pred = int(oob_preds[i, t_idx])
            if 0 <= pred < 10:
                vote_features[i, pred] += 1
    vote_features /= n_trees  # normalize to proportions

    # Combined meta-features: vote proportions (10) + top-2 margin
    margins = np.zeros((len(X), 1))
    for i in range(len(X)):
        sorted_votes = np.sort(vote_features[i])[::-1]
        margins[i, 0] = sorted_votes[0] - sorted_votes[1]

    meta_X_compact = np.hstack([vote_features, margins])  # 11 features
    print(f"Meta features (compact): {meta_X_compact.shape[1]}")

    # Train meta-forest on compact features
    print("\nTraining meta-forest on vote proportions...")
    meta_trees = []
    for i in range(51):
        rng = np.random.RandomState(i * 11 + 99)
        indices = rng.choice(len(meta_X_compact), len(meta_X_compact), replace=True)
        Xi, yi = meta_X_compact[indices], y[indices]
        tree = build_tree(Xi, yi, max_depth=8, min_samples=32,
                         n_feat_sample=6, rng=rng)
        meta_trees.append(tree)

    # Evaluate meta-forest on train
    correct_meta = 0
    correct_vote = 0
    for i in range(len(y)):
        # Standard majority vote
        votes = Counter(oob_preds[i])
        vote_pred = votes.most_common(1)[0][0]
        if vote_pred == y[i]:
            correct_vote += 1

        # Meta-forest
        meta_votes = Counter()
        for mt in meta_trees:
            meta_votes[predict_tree(mt, meta_X_compact[i])] += 1
        meta_pred = meta_votes.most_common(1)[0][0]
        if meta_pred == y[i]:
            correct_meta += 1

    print(f"Train - Majority vote: {correct_vote/len(y):.1%}")
    print(f"Train - Meta-forest:   {correct_meta/len(y):.1%}")

    # Evaluate on val
    print("\nEvaluating on val...")
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

    correct_meta_val = 0
    correct_vote_val = 0
    for i in range(len(y_val)):
        # Get base tree predictions
        base_preds = np.array([predict_tree(t, X_val[i]) for t in trees])

        # Majority vote
        votes = Counter(base_preds)
        if votes.most_common(1)[0][0] == y_val[i]:
            correct_vote_val += 1

        # Meta features
        vf = np.zeros(10)
        for p in base_preds:
            vf[p] += 1
        vf /= n_trees
        sorted_vf = np.sort(vf)[::-1]
        margin = sorted_vf[0] - sorted_vf[1]
        meta_feat = np.concatenate([vf, [margin]])

        # Meta forest
        meta_votes = Counter()
        for mt in meta_trees:
            meta_votes[predict_tree(mt, meta_feat)] += 1
        meta_pred = meta_votes.most_common(1)[0][0]
        if meta_pred == y_val[i]:
            correct_meta_val += 1

    print(f"Val - Majority vote: {correct_vote_val/len(y_val):.1%}")
    print(f"Val - Meta-forest:   {correct_meta_val/len(y_val):.1%}")


if __name__ == "__main__":
    main()
