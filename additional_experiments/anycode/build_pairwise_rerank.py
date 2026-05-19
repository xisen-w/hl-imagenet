"""Post-prediction pairwise reranking for the compiled forest.

When the forest is uncertain between two confusing classes, consult
a specialized pairwise discriminant tree trained ONLY on that pair.

This adds a second stage that can fix forest errors without changing
the base forest at all — analogous to Phase 2's reranking approach."""

import sys
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import extract_features, CLASSES, gini, Node, count_nodes, predict_tree, build_tree, load_data

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"

# Top confusion pairs to build discriminants for
PAIRS = [
    (5, 4),  # orange -> banana
    (6, 0),  # bear -> GR
    (4, 5),  # banana -> orange
    (2, 0),  # teapot -> GR
    (0, 1),  # GR -> mushroom
    (1, 6),  # mushroom -> bear
    (9, 3),  # sports -> bus
    (6, 1),  # bear -> mushroom
    (0, 2),  # GR -> teapot
    (0, 6),  # GR -> bear
    (4, 3),  # banana -> bus
    (6, 7),  # bear -> KP
    (1, 0),  # mushroom -> GR
    (4, 1),  # banana -> mushroom
    (7, 2),  # KP -> teapot
]


def build_pairwise_tree(X, y, cls_a, cls_b, max_depth=8, min_samples=10, n_feat_sample=45):
    """Build tree that discriminates cls_a from cls_b."""
    mask = (y == cls_a) | (y == cls_b)
    Xp = X[mask]
    yp = (y[mask] == cls_a).astype(int)  # 1 = cls_a, 0 = cls_b

    rng = np.random.RandomState(cls_a * 10 + cls_b + 42)
    # No bagging for pairwise — use all data
    tree = build_tree(Xp, yp, max_depth=max_depth, min_samples=min_samples,
                     n_feat_sample=n_feat_sample, rng=rng)
    return tree


def build_pairwise_forest(X, y, cls_a, cls_b, n_trees=21, max_depth=8, min_samples=10, n_feat_sample=45):
    """Build small forest to discriminate cls_a from cls_b."""
    mask = (y == cls_a) | (y == cls_b)
    Xp = X[mask]
    yp = (y[mask] == cls_a).astype(int)

    trees = []
    for i in range(n_trees):
        rng = np.random.RandomState(cls_a * 100 + cls_b * 10 + i * 7 + 42)
        indices = rng.choice(len(Xp), len(Xp), replace=True)
        tree = build_tree(Xp[indices], yp[indices], max_depth=max_depth,
                         min_samples=min_samples, n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
    return trees


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

    # Build base forest
    print("Building base forest...")
    base_trees = []
    for i in range(101):
        rng = np.random.RandomState(i * 7 + 42)
        indices = rng.choice(len(X_train), len(X_train), replace=True)
        Xi, yi = X_train[indices], y_train[indices]
        tree = build_tree(Xi, yi, max_depth=14, min_samples=16, n_feat_sample=18, rng=rng)
        base_trees.append(tree)

    # Build pairwise discriminants
    print("Building pairwise discriminants...")
    pair_trees = {}
    for cls_a, cls_b in PAIRS:
        trees = build_pairwise_forest(X_train, y_train, cls_a, cls_b,
                                     n_trees=21, max_depth=8, min_samples=10, n_feat_sample=45)
        # Evaluate on training pair
        mask = (y_train == cls_a) | (y_train == cls_b)
        correct = 0
        for i in np.where(mask)[0]:
            votes = Counter([predict_tree(t, X_train[i]) for t in trees])
            pred_binary = votes.most_common(1)[0][0]
            true_binary = 1 if y_train[i] == cls_a else 0
            if pred_binary == true_binary:
                correct += 1
        acc = correct / np.sum(mask)
        pair_trees[(cls_a, cls_b)] = trees
        print(f"  {CLASSES[cls_a]:15s} vs {CLASSES[cls_b]:15s}: train acc = {acc:.1%}")

    # Evaluate with reranking
    print("\nEvaluating on val...")
    for margin_thresh in [0.05, 0.10, 0.15, 0.20]:
        correct_base = 0
        correct_rerank = 0
        rerank_helps = 0
        rerank_hurts = 0

        for i in range(len(y_val)):
            # Base forest prediction
            votes = Counter([predict_tree(t, X_val[i]) for t in base_trees])
            top2 = votes.most_common(2)
            base_pred = top2[0][0]
            if base_pred == y_val[i]:
                correct_base += 1

            # Check margin
            margin = (top2[0][1] - (top2[1][1] if len(top2) > 1 else 0)) / 101.0
            final_pred = base_pred

            if margin < margin_thresh and len(top2) > 1:
                cls_a, cls_b = top2[0][0], top2[1][0]
                # Check both directions
                key1 = (cls_a, cls_b)
                key2 = (cls_b, cls_a)
                if key1 in pair_trees:
                    disc_votes = Counter([predict_tree(t, X_val[i]) for t in pair_trees[key1]])
                    disc_pred = disc_votes.most_common(1)[0][0]
                    # disc_pred=1 means cls_a, disc_pred=0 means cls_b
                    if disc_pred == 0:
                        final_pred = cls_b  # discriminant says it's B
                elif key2 in pair_trees:
                    disc_votes = Counter([predict_tree(t, X_val[i]) for t in pair_trees[key2]])
                    disc_pred = disc_votes.most_common(1)[0][0]
                    # disc_pred=1 means cls_b, disc_pred=0 means cls_a
                    if disc_pred == 1:
                        final_pred = cls_b

            if final_pred == y_val[i]:
                correct_rerank += 1
            if final_pred == y_val[i] and base_pred != y_val[i]:
                rerank_helps += 1
            if final_pred != y_val[i] and base_pred == y_val[i]:
                rerank_hurts += 1

        print(f"\n  Margin threshold: {margin_thresh}")
        print(f"    Base:    {correct_base/len(y_val):.1%}")
        print(f"    Rerank:  {correct_rerank/len(y_val):.1%}")
        print(f"    Helps: {rerank_helps}, Hurts: {rerank_hurts}, Net: {rerank_helps-rerank_hurts:+d}")


if __name__ == "__main__":
    main()
