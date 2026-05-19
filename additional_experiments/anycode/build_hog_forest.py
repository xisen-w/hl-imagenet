"""Build a second forest on HOG-like spatial gradient features.

HOG captures LOCAL edge orientation structure in a 4x4 spatial grid.
This is precisely the information the global-statistics forest CANNOT capture:
- Where edges occur (not just how many)
- Local orientation patterns (object shape)
- Spatial relationships between edge regions

Features: 4x4 grid × (4 orientation bins + magnitude) = 80 features
Plus 10 additional spatial shape features = 90 total.
"""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"

CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]


def extract_hog_features(image):
    """Extract HOG-like spatial gradient features."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)

    # Compute gradients
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(gx**2 + gy**2)
    angle = np.arctan2(gy, gx)  # -pi to pi
    angle = (angle + np.pi) * 180.0 / np.pi  # 0 to 360
    angle = angle % 180.0  # unsigned: 0 to 180

    features = []

    # 4x4 spatial grid, each cell is 16x16
    cell_size = 16
    n_bins = 4
    bin_edges = np.linspace(0, 180, n_bins + 1)

    for row in range(4):
        for col in range(4):
            r0, r1 = row * cell_size, (row + 1) * cell_size
            c0, c1 = col * cell_size, (col + 1) * cell_size
            cell_mag = mag[r0:r1, c0:c1]
            cell_angle = angle[r0:r1, c0:c1]

            # Orientation histogram (magnitude-weighted)
            for b in range(n_bins):
                lo, hi = bin_edges[b], bin_edges[b + 1]
                mask = (cell_angle >= lo) & (cell_angle < hi)
                features.append(float(np.sum(cell_mag[mask])))

            # Mean magnitude
            features.append(float(np.mean(cell_mag)))

    # Normalize HOG features by total magnitude to be scale-invariant
    total_mag = sum(features[:80]) + 1e-6
    features = [f / total_mag for f in features[:80]]

    # Additional spatial shape features (10 more)
    edges = cv2.Canny(gray.astype(np.uint8), 50, 150)

    # Edge centroid (where is the edge mass?)
    ey, ex = np.where(edges > 0)
    if len(ey) > 10:
        features.append(float(np.mean(ex)) / 64.0)  # x centroid
        features.append(float(np.mean(ey)) / 64.0)  # y centroid
        features.append(float(np.std(ex)) / 32.0)   # x spread
        features.append(float(np.std(ey)) / 32.0)   # y spread
    else:
        features.extend([0.5, 0.5, 0.5, 0.5])

    # Radial edge distribution (3 rings)
    cy, cx = 32, 32
    yy, xx = np.mgrid[0:64, 0:64]
    dist = np.sqrt((yy - cy)**2 + (xx - cx)**2)
    ring1 = (dist < 12) & (edges > 0)
    ring2 = (dist >= 12) & (dist < 24) & (edges > 0)
    ring3 = (dist >= 24) & (edges > 0)
    total_edges = max(float(np.sum(edges > 0)), 1.0)
    features.append(float(np.sum(ring1)) / total_edges)
    features.append(float(np.sum(ring2)) / total_edges)
    features.append(float(np.sum(ring3)) / total_edges)

    # Diagonal vs anti-diagonal gradient energy
    diag_energy = float(np.sum(mag * np.abs(np.sin(2 * angle * np.pi / 180))))
    anti_diag = float(np.sum(mag * np.abs(np.cos(2 * angle * np.pi / 180))))
    features.append(diag_energy / max(diag_energy + anti_diag, 1.0))

    # Vertical symmetry of gradient pattern
    left_mag = mag[:, :32]
    right_mag = mag[:, 32:][:, ::-1]
    features.append(float(np.corrcoef(left_mag.flatten(), right_mag.flatten())[0, 1]))

    # Top-bottom gradient asymmetry
    top_mag = float(np.mean(mag[:32, :]))
    bot_mag = float(np.mean(mag[32:, :]))
    features.append((top_mag - bot_mag) / max(top_mag + bot_mag, 1.0))

    return features


def load_data():
    X, y = [], []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = DATA_ROOT / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            feats = extract_hog_features(img)
            X.append(feats)
            y.append(cls_idx)
    return np.array(X), np.array(y)


def gini(y):
    if len(y) == 0:
        return 0.0
    counts = np.bincount(y, minlength=10)
    probs = counts / len(y)
    return 1.0 - np.sum(probs**2)


class Node:
    def __init__(self):
        self.feat = None
        self.thresh = None
        self.left = None
        self.right = None
        self.label = None


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


def build_tree(X, y, depth=0, max_depth=14, min_samples=16, n_feat_sample=None, rng=None):
    node = Node()
    if depth >= max_depth or len(y) < min_samples or gini(y) < 0.05:
        node.label = int(np.argmax(np.bincount(y, minlength=10)))
        return node

    n_features = X.shape[1]
    if n_feat_sample and n_feat_sample < n_features:
        feature_subset = rng.choice(n_features, n_feat_sample, replace=False)
    else:
        feature_subset = np.arange(n_features)

    feat, thresh, gain = find_best_split(X, y, feature_subset)
    if gain <= 0.001:
        node.label = int(np.argmax(np.bincount(y, minlength=10)))
        return node

    node.feat = feat
    node.thresh = round(float(thresh), 6)
    left_mask = X[:, feat] <= thresh
    node.left = build_tree(X[left_mask], y[left_mask], depth + 1, max_depth, min_samples, n_feat_sample, rng)
    node.right = build_tree(X[~left_mask], y[~left_mask], depth + 1, max_depth, min_samples, n_feat_sample, rng)
    return node


def tree_to_code(node, func_name, indent=1):
    header = f"def {func_name}(f):\n"
    body = _node_to_code(node, indent)
    return header + body


def _node_to_code(node, indent):
    pad = "    " * indent
    if node.label is not None:
        return f"{pad}return {node.label}\n"
    code = f"{pad}if f[{node.feat}] <= {node.thresh}:\n"
    code += _node_to_code(node.left, indent + 1)
    code += f"{pad}else:\n"
    code += _node_to_code(node.right, indent + 1)
    return code


def count_nodes(node):
    if node.label is not None:
        return 1
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def predict_tree(node, x):
    if node.label is not None:
        return node.label
    if x[node.feat] <= node.thresh:
        return predict_tree(node.left, x)
    return predict_tree(node.right, x)


def main():
    print("Loading training data with HOG features...")
    X, y = load_data()
    print(f"Loaded {len(X)} samples, {X.shape[1]} features")

    n_trees = 101
    max_depth = 14
    min_samples = 16
    n_feat_sample = int(np.sqrt(X.shape[1]) * 2)
    print(f"Config: {n_trees} trees, depth {max_depth}, min_samples {min_samples}, n_feat_sample {n_feat_sample}")

    trees = []
    tree_codes = []
    for i in range(n_trees):
        rng = np.random.RandomState(i * 13 + 77)  # different seed from forest 1
        indices = rng.choice(len(X), len(X), replace=True)
        Xi, yi = X[indices], y[indices]
        tree = build_tree(Xi, yi, max_depth=max_depth, min_samples=min_samples,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
        nodes = count_nodes(tree)
        oob_mask = np.ones(len(X), dtype=bool)
        oob_mask[np.unique(indices)] = False
        oob_correct = sum(predict_tree(tree, X[j]) == y[j] for j in range(len(X)) if oob_mask[j])
        oob_total = np.sum(oob_mask)
        oob_acc = oob_correct / oob_total if oob_total > 0 else 0
        if i % 10 == 0:
            print(f"  Tree {i}: {nodes} nodes, OOB acc: {oob_acc:.1%}")
        tree_codes.append(tree_to_code(tree, f"_hog_tree_{i}"))

    # Forest accuracy on full train
    correct = 0
    for i in range(len(y)):
        votes = Counter()
        for t in trees:
            votes[predict_tree(t, X[i])] += 1
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    print(f"\nHOG Forest train accuracy: {correct/len(y):.1%}")

    # Save tree code for ensemble
    out_path = Path(__file__).parent / "hog_trees.py"
    tree_funcs = "\n\n".join(tree_codes)
    hog_calls = ", ".join(f"_hog_tree_{i}(f)" for i in range(n_trees))

    code = f'''"""HOG forest: {n_trees} trees on spatial gradient features."""


{tree_funcs}


def _hog_vote(f):
    from collections import Counter
    votes = [{hog_calls}]
    counts = Counter(votes)
    return counts.most_common(1)[0][0]
'''
    with open(out_path, "w") as fout:
        fout.write(code)
    total_nodes = sum(count_nodes(t) for t in trees)
    print(f"Wrote hog_trees.py ({len(code)} bytes, {total_nodes} nodes)")

    # Also evaluate on val
    print("\nEvaluating on val...")
    VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"
    val_correct = 0
    val_total = 0
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = VAL_ROOT / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        cls_correct = 0
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            feats = extract_hog_features(img)
            votes = Counter()
            for t in trees:
                votes[predict_tree(t, np.array(feats))] += 1
            pred = votes.most_common(1)[0][0]
            val_total += 1
            if pred == cls_idx:
                val_correct += 1
                cls_correct += 1
        print(f"  {cls:20s} {cls_correct}/{len(images)}")
    print(f"\nHOG Forest val accuracy: {val_correct/val_total:.1%} ({val_correct}/{val_total})")


if __name__ == "__main__":
    main()
