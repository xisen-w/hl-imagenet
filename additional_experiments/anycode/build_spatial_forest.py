"""Build forest on dense spatial color features.

The key insight: the 64.4% ceiling comes from spatial erasure.
A 2x2 grid can't distinguish "yellow top + dark bottom" (bus) from
"yellow everywhere" (banana). An 8x8 grid of color statistics MIGHT.

Features: 8x8 grid × 3 channels (hue_mode, saturation, value) = 192 features
But that's too many for n_feat_sample. Instead:
- 4x4 grid × 5 stats (hue_mode, sat, val, edge_dens, green_frac) = 80
- Plus 10 inter-cell relationship features = 90 total

This specifically targets the spatial information that globals erase."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import gini, Node, find_best_split, build_tree, count_nodes, predict_tree

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"

CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]


def extract_spatial_features(image):
    """Dense spatial color/texture grid."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 100)

    features = []

    # 4x4 grid, each cell is 16x16
    cell = 16
    for row in range(4):
        for col in range(4):
            r0, r1 = row * cell, (row + 1) * cell
            c0, c1 = col * cell, (col + 1) * cell

            ch = h[r0:r1, c0:c1]
            cs = s[r0:r1, c0:c1]
            cv_arr = v[r0:r1, c0:c1]
            ce = edges[r0:r1, c0:c1]

            # Dominant hue (mode via histogram)
            h_hist = np.histogram(ch[cs > 40], bins=18, range=(0, 180))[0]
            if np.sum(h_hist) > 10:
                features.append(float(np.argmax(h_hist) * 10 + 5))  # center of mode bin
            else:
                features.append(90.0)  # achromatic default

            # Mean saturation
            features.append(float(np.mean(cs)))
            # Mean value
            features.append(float(np.mean(cv_arr)))
            # Edge density
            features.append(float(np.mean(ce > 0)))
            # Warm fraction (hue < 30 and sat > 50)
            features.append(float(np.mean((ch < 30) & (cs > 50))))

    # Inter-cell relationships (10 features)
    # Top-bottom hue difference (avg of top 2 rows vs bottom 2 rows hue)
    top_hue = np.mean([features[i * 5] for i in range(8)])   # rows 0-1
    bot_hue = np.mean([features[i * 5] for i in range(8, 16)])  # rows 2-3
    features.append(top_hue - bot_hue)

    # Left-right saturation symmetry
    left_sat = np.mean([features[i * 5 + 1] for i in [0, 2, 4, 6, 8, 10, 12, 14]])
    right_sat = np.mean([features[i * 5 + 1] for i in [1, 3, 5, 7, 9, 11, 13, 15]])
    features.append(abs(left_sat - right_sat))

    # Center vs periphery value
    center_val = np.mean([features[i * 5 + 2] for i in [5, 6, 9, 10]])  # inner 2x2
    corner_val = np.mean([features[i * 5 + 2] for i in [0, 3, 12, 15]])  # corners
    features.append(center_val - corner_val)

    # Edge concentration: center vs border
    center_edge = np.mean([features[i * 5 + 3] for i in [5, 6, 9, 10]])
    border_edge = np.mean([features[i * 5 + 3] for i in [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15]])
    features.append(center_edge - border_edge)

    # Warm gradient: does warm fraction increase toward center?
    center_warm = np.mean([features[i * 5 + 4] for i in [5, 6, 9, 10]])
    border_warm = np.mean([features[i * 5 + 4] for i in [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15]])
    features.append(center_warm - border_warm)

    # Row-wise value profile (brightness distribution top to bottom)
    for row in range(4):
        row_val = np.mean([features[(row * 4 + col) * 5 + 2] for col in range(4)])
        features.append(row_val / 255.0)

    # Most-saturated quadrant
    quadrant_sats = [
        np.mean([features[i * 5 + 1] for i in [0, 1, 4, 5]]),    # TL
        np.mean([features[i * 5 + 1] for i in [2, 3, 6, 7]]),    # TR
        np.mean([features[i * 5 + 1] for i in [8, 9, 12, 13]]),  # BL
        np.mean([features[i * 5 + 1] for i in [10, 11, 14, 15]]),# BR
    ]
    features.append(float(np.argmax(quadrant_sats)))

    return features  # 80 + 10 = 90 features


def load_data(data_root):
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
            feats = extract_spatial_features(img)
            X.append(feats)
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


def main():
    print("Loading spatial features...")
    X_train, y_train = load_data(DATA_ROOT)
    X_val, y_val = load_data(VAL_ROOT)
    print(f"Train: {len(X_train)} samples, {X_train.shape[1]} features")
    print(f"Val: {len(X_val)} samples")

    n_trees = 101
    max_depth = 14
    min_samples = 16
    n_feat_sample = int(np.sqrt(X_train.shape[1]) * 2)
    print(f"Config: {n_trees} trees, depth {max_depth}, min_samples {min_samples}, n_feat={n_feat_sample}")

    trees = []
    for i in range(n_trees):
        rng = np.random.RandomState(i * 7 + 42)
        indices = rng.choice(len(X_train), len(X_train), replace=True)
        Xi, yi = X_train[indices], y_train[indices]
        tree = build_tree(Xi, yi, max_depth=max_depth, min_samples=min_samples,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
        if i % 20 == 0:
            print(f"  Tree {i}: {count_nodes(tree)} nodes")

    train_acc = eval_forest(trees, X_train, y_train)
    val_acc = eval_forest(trees, X_val, y_val)
    print(f"\nSpatial Forest: Train={train_acc:.1%}, Val={val_acc:.1%}, Gap={100*(train_acc-val_acc):.1f}pp")

    # Per-class breakdown on val
    from collections import defaultdict
    per_class = defaultdict(lambda: [0, 0])
    for i in range(len(y_val)):
        votes = Counter()
        for t in trees:
            votes[predict_tree(t, X_val[i])] += 1
        pred = votes.most_common(1)[0][0]
        cls = CLASSES[y_val[i]]
        per_class[cls][1] += 1
        if pred == y_val[i]:
            per_class[cls][0] += 1
    for cls in CLASSES:
        cc, ct = per_class[cls]
        print(f"  {cls:20s} {cc/ct:.1%} ({cc}/{ct})")


if __name__ == "__main__":
    main()
