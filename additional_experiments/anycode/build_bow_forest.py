"""Bag-of-Visual-Words forest.

Extract 8x8 patches, compute mini-descriptors (4 values each: mean_h, mean_s,
mean_edge, dominant_gradient_dir). K-means cluster into 32 codewords.
Each image = histogram over codewords = 32-dim feature vector.

This is POSITION-INVARIANT (histogram discards position) and captures
LOCAL structure (each patch describes a small region's properties).

The codebook centroids are hardcoded as constants — no stored data at inference."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import CLASSES, gini, Node, find_best_split, build_tree, count_nodes, predict_tree

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def extract_patch_descriptors(image, patch_size=8, stride=4):
    """Extract mini-descriptors from overlapping patches."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)

    descriptors = []
    for row in range(0, 64 - patch_size + 1, stride):
        for col in range(0, 64 - patch_size + 1, stride):
            ph = h[row:row+patch_size, col:col+patch_size]
            ps = s[row:row+patch_size, col:col+patch_size]
            pv = v[row:row+patch_size, col:col+patch_size]
            pgx = gx[row:row+patch_size, col:col+patch_size]
            pgy = gy[row:row+patch_size, col:col+patch_size]

            # 6-dim descriptor per patch
            desc = [
                float(np.mean(ph)) / 180.0,  # normalized hue
                float(np.mean(ps)) / 255.0,  # normalized sat
                float(np.mean(pv)) / 255.0,  # normalized val
                float(np.std(pv)) / 128.0,   # texture (val variance)
                float(np.mean(np.abs(pgx))) / 50.0,  # edge magnitude (normalized)
                float(np.arctan2(np.mean(pgy), np.mean(pgx))) / np.pi,  # dominant direction
            ]
            descriptors.append(desc)
    return np.array(descriptors)


def build_codebook(images_root, n_clusters=32):
    """Build visual vocabulary from training images."""
    all_descs = []
    for cls in CLASSES:
        cls_dir = images_root / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images[:50]:  # subsample for speed
            img = cv2.imread(str(p))
            if img is None:
                continue
            descs = extract_patch_descriptors(img)
            all_descs.append(descs)

    all_descs = np.vstack(all_descs)
    print(f"Total descriptors for clustering: {len(all_descs)}")

    # K-means
    from scipy.cluster.vq import kmeans2
    centroids, labels = kmeans2(all_descs.astype(np.float32), n_clusters, minit='points', iter=20)
    return centroids


def image_to_bow(image, centroids):
    """Convert image to bag-of-words histogram."""
    descs = extract_patch_descriptors(image)
    n_clusters = len(centroids)

    # Assign each descriptor to nearest centroid
    # dists shape: (n_patches, n_clusters)
    dists = np.sum((descs[:, None, :] - centroids[None, :, :])**2, axis=2)
    assignments = np.argmin(dists, axis=1)

    # Histogram
    hist = np.bincount(assignments, minlength=n_clusters).astype(float)
    hist /= max(np.sum(hist), 1.0)  # L1 normalize
    return hist


def load_bow_data(data_root, centroids):
    """Load all images as BoW histograms."""
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
            hist = image_to_bow(img, centroids)
            X.append(hist)
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
    print("Building visual codebook...")
    centroids = build_codebook(DATA_ROOT, n_clusters=32)
    print(f"Codebook shape: {centroids.shape}")

    print("\nEncoding training images...")
    X_train, y_train = load_bow_data(DATA_ROOT, centroids)
    print(f"Train: {X_train.shape}")

    print("Encoding val images...")
    X_val, y_val = load_bow_data(VAL_ROOT, centroids)
    print(f"Val: {X_val.shape}")

    # Build forest on BoW features
    n_feat = X_train.shape[1]
    n_feat_sample = max(int(np.sqrt(n_feat) * 2), 8)
    print(f"\nBuilding forest: 101 trees, {n_feat} features, n_feat_sample={n_feat_sample}")

    trees = []
    for i in range(101):
        rng = np.random.RandomState(i * 7 + 42)
        idx = rng.choice(len(X_train), len(X_train), replace=True)
        tree = build_tree(X_train[idx], y_train[idx], max_depth=14, min_samples=16,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
        if i % 25 == 0:
            print(f"  Tree {i}: {count_nodes(tree)} nodes")

    train_acc = eval_forest_fn(trees, X_train, y_train)
    val_acc = eval_forest_fn(trees, X_val, y_val)
    print(f"\nBoW Forest: Train={train_acc:.1%}, Val={val_acc:.1%}, Gap={100*(train_acc-val_acc):.1f}pp")

    # Also try combining with original features
    from build_forest import extract_features, load_data
    X_train_orig, _ = load_data()
    X_train_comb = np.hstack([X_train_orig, X_train])
    X_val_orig = []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = VAL_ROOT / cls
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None: continue
            X_val_orig.append(extract_features(img))
    X_val_orig = np.array(X_val_orig)
    X_val_comb = np.hstack([X_val_orig, X_val])

    n_comb = X_train_comb.shape[1]
    n_feat_comb = int(np.sqrt(n_comb) * 2)
    print(f"\nCombined: {n_comb} features, n_feat_sample={n_feat_comb}")
    trees_comb = []
    for i in range(101):
        rng = np.random.RandomState(i * 7 + 42)
        idx = rng.choice(len(X_train_comb), len(X_train_comb), replace=True)
        tree = build_tree(X_train_comb[idx], y_train[idx], max_depth=14, min_samples=16,
                         n_feat_sample=n_feat_comb, rng=rng)
        trees_comb.append(tree)

    train_comb = eval_forest_fn(trees_comb, X_train_comb, y_train)
    val_comb = eval_forest_fn(trees_comb, X_val_comb, y_val)
    print(f"Combined: Train={train_comb:.1%}, Val={val_comb:.1%}, Gap={100*(train_comb-val_comb):.1f}pp")


if __name__ == "__main__":
    main()
