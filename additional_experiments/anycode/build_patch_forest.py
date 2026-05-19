"""Forest on patch-relationship features.

Key insight: global statistics erase spatial layout. Patch DIFFERENCES
capture layout. "Top is bright, bottom is dark" = bus.
"Uniform bright all over" = banana.

Features:
- 4x4 grid: per-patch hue_mode, sat_mean, val_mean (48 base)
- Adjacent differences: horizontal pairs (12), vertical pairs (12)
  for sat and val = 48 relationship features
Total: 48 + 48 = 96 features (close to 90, negligible dilution)

Actually to keep at exactly 90: 4x4 grid × 3 stats = 48 base,
plus 42 relationship features (all adjacent diffs for 3 channels)."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import CLASSES, gini, Node, find_best_split, build_tree, count_nodes, predict_tree

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def extract_patch_features(image):
    """Patch-based spatial relationship features."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cell = 16  # 4x4 grid of 16x16 cells

    # Per-patch statistics
    patch_hue = np.zeros((4, 4))
    patch_sat = np.zeros((4, 4))
    patch_val = np.zeros((4, 4))

    for row in range(4):
        for col in range(4):
            r0, r1 = row * cell, (row + 1) * cell
            c0, c1 = col * cell, (col + 1) * cell
            ch = h[r0:r1, c0:c1]
            cs = s[r0:r1, c0:c1]
            cv_arr = v[r0:r1, c0:c1]

            # Mode-like hue (mean of saturated pixels)
            sat_pixels = ch[cs > 40]
            if len(sat_pixels) > 20:
                patch_hue[row, col] = float(np.mean(sat_pixels))
            else:
                patch_hue[row, col] = 90.0

            patch_sat[row, col] = float(np.mean(cs))
            patch_val[row, col] = float(np.mean(cv_arr))

    features = []

    # Base patch features (48)
    for row in range(4):
        for col in range(4):
            features.append(patch_hue[row, col])
            features.append(patch_sat[row, col])
            features.append(patch_val[row, col])

    # Horizontal differences for sat (12)
    for row in range(4):
        for col in range(3):
            features.append(patch_sat[row, col + 1] - patch_sat[row, col])

    # Vertical differences for sat (12)
    for row in range(3):
        for col in range(4):
            features.append(patch_sat[row + 1, col] - patch_sat[row, col])

    # Horizontal differences for val (12)
    for row in range(4):
        for col in range(3):
            features.append(patch_val[row, col + 1] - patch_val[row, col])

    # Vertical differences for val (12)
    for row in range(3):
        for col in range(4):
            features.append(patch_val[row + 1, col] - patch_val[row, col])

    # Summary statistics (6) to reach 90+
    features.append(float(np.std(patch_sat)))  # spatial variation of saturation
    features.append(float(np.std(patch_val)))  # spatial variation of value
    features.append(float(np.mean(patch_sat[:2, :]) - np.mean(patch_sat[2:, :])))  # top-bottom sat
    features.append(float(np.mean(patch_val[:2, :]) - np.mean(patch_val[2:, :])))  # top-bottom val
    features.append(float(np.max(patch_sat) - np.min(patch_sat)))  # sat range
    features.append(float(np.max(patch_val) - np.min(patch_val)))  # val range

    return features  # 48 + 12 + 12 + 12 + 12 + 6 = 102


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
            feats = extract_patch_features(img)
            X.append(feats)
            y.append(cls_idx)
    return np.array(X), np.array(y)


def eval_forest_fn(trees, X, y):
    correct = 0
    for i in range(len(y)):
        votes = Counter()
        for t in trees:
            votes[predict_tree(t, X[i])] += 1
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    return correct / len(y)


def main():
    print("Loading patch features...")
    X_train, y_train = load_data(DATA_ROOT)
    X_val, y_val = load_data(VAL_ROOT)
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Features: {X_train.shape[1]}")

    n_feat_sample = int(np.sqrt(X_train.shape[1]) * 2)
    print(f"n_feat_sample: {n_feat_sample}")

    # Build forest
    trees = []
    for i in range(101):
        rng = np.random.RandomState(i * 7 + 42)
        indices = rng.choice(len(X_train), len(X_train), replace=True)
        Xi, yi = X_train[indices], y_train[indices]
        tree = build_tree(Xi, yi, max_depth=14, min_samples=16,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
        if i % 25 == 0:
            print(f"  Tree {i}: {count_nodes(tree)} nodes")

    train_acc = eval_forest_fn(trees, X_train, y_train)
    val_acc = eval_forest_fn(trees, X_val, y_val)
    print(f"\nPatch Forest: Train={train_acc:.1%}, Val={val_acc:.1%}, Gap={100*(train_acc-val_acc):.1f}pp")

    # Per-class breakdown
    from collections import defaultdict
    per_class = defaultdict(lambda: [0, 0])
    for i in range(len(y_val)):
        votes = Counter([predict_tree(t, X_val[i]) for t in trees])
        pred = votes.most_common(1)[0][0]
        cls = CLASSES[y_val[i]]
        per_class[cls][1] += 1
        if pred == y_val[i]:
            per_class[cls][0] += 1
    for cls in CLASSES:
        cc, ct = per_class[cls]
        print(f"  {cls:20s} {cc/ct:.1%} ({cc}/{ct})")

    # Try combining patch + original
    print("\n\nTesting: patch features COMBINED with original features...")
    from build_forest import extract_features, load_data as load_orig_data
    X_train_orig, _ = load_orig_data()
    X_train_combined = np.hstack([X_train_orig, X_train])

    X_val_combined_list = []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = VAL_ROOT / cls
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None: continue
            orig = extract_features(img)
            patch = extract_patch_features(img)
            X_val_combined_list.append(orig + patch)
    X_val_combined = np.array(X_val_combined_list)

    n_combined = X_train_combined.shape[1]
    n_feat_comb = int(np.sqrt(n_combined) * 2.5)  # higher to counter dilution
    print(f"Combined features: {n_combined}, n_feat_sample: {n_feat_comb}")

    trees_comb = []
    for i in range(101):
        rng = np.random.RandomState(i * 7 + 42)
        indices = rng.choice(len(X_train_combined), len(X_train_combined), replace=True)
        Xi, yi = X_train_combined[indices], y_train[indices]
        tree = build_tree(Xi, yi, max_depth=14, min_samples=16,
                         n_feat_sample=n_feat_comb, rng=rng)
        trees_comb.append(tree)

    train_comb = eval_forest_fn(trees_comb, X_train_combined, y_train)
    val_comb = eval_forest_fn(trees_comb, X_val_combined, y_val)
    print(f"Combined: Train={train_comb:.1%}, Val={val_comb:.1%}, Gap={100*(train_comb-val_comb):.1f}pp")


if __name__ == "__main__":
    main()
