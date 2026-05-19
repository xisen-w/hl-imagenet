"""Build forest with augmented training data.

Hypothesis: The 25.8pp overfit gap (90.2% train, 64.4% val) comes partly from
position/brightness-specific correlations in 200 images/class. Augmenting with
horizontal flips + brightness jitter gives trees more diverse training examples,
breaking position-specific memorization.

Key: augment the IMAGES before feature extraction, not the features directly,
so spatial features (quadrants, thirds) see genuinely different inputs."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import extract_features, CLASSES, build_tree, predict_tree, count_nodes

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def augment_image(img, rng):
    """Apply random augmentations: flip, brightness, slight crop."""
    augmented = []

    # Original
    augmented.append(img.copy())

    # Horizontal flip
    augmented.append(cv2.flip(img, 1))

    # Brightness variants (+/- 20%)
    for factor in [0.8, 1.2]:
        bright = np.clip(img.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        augmented.append(bright)

    # Flip + brightness
    flipped = cv2.flip(img, 1)
    for factor in [0.85, 1.15]:
        bright = np.clip(flipped.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        augmented.append(bright)

    return augmented  # 6 images total (1 orig + 1 flip + 2 bright + 2 flip-bright)


def load_augmented_data(aug_factor=6):
    """Load data with augmentation. aug_factor controls how many augmented versions."""
    X, y = [], []
    X_orig, y_orig = [], []

    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = DATA_ROOT / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        rng = np.random.RandomState(cls_idx * 42)
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            # Original features for evaluation
            orig_feats = extract_features(img)
            X_orig.append(orig_feats)
            y_orig.append(cls_idx)

            # Augmented features for training
            augmented_imgs = augment_image(img, rng)
            for aug_img in augmented_imgs[:aug_factor]:
                feats = extract_features(aug_img)
                X.append(feats)
                y.append(cls_idx)

    return np.array(X), np.array(y), np.array(X_orig), np.array(y_orig)


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


def evaluate(trees, X, y, label=""):
    correct = 0
    for i in range(len(y)):
        votes = Counter([predict_tree(t, X[i]) for t in trees])
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    acc = correct / len(y)
    print(f"  {label}: {acc:.1%} ({correct}/{len(y)})")
    return acc


def main():
    print("Loading augmented training data...")
    X_aug, y_aug, X_orig, y_orig = load_augmented_data(aug_factor=6)
    print(f"  Augmented: {len(X_aug)} samples ({len(X_aug)//2000}x original)")
    print(f"  Original:  {len(X_orig)} samples")

    print("\nLoading val data...")
    X_val, y_val = load_val_data()
    print(f"  Val: {len(X_val)} samples")

    # Test different configs
    configs = [
        # (n_trees, max_depth, min_samples, n_feat_sample, description)
        (101, 14, 16, 18, "baseline params on augmented data"),
        (101, 14, 32, 18, "higher min_samples (more regularized)"),
        (101, 12, 24, 18, "shallower + more regularized"),
        (101, 14, 16, 22, "more features per split"),
        (101, 10, 32, 18, "very shallow + very regularized"),
    ]

    for n_trees, max_depth, min_samples, n_feat_sample, desc in configs:
        print(f"\n--- {desc} ---")
        print(f"    n_trees={n_trees}, depth={max_depth}, min_samples={min_samples}, n_feat={n_feat_sample}")

        trees = []
        for i in range(n_trees):
            rng = np.random.RandomState(i * 7 + 42)
            indices = rng.choice(len(X_aug), len(X_aug), replace=True)
            Xi, yi = X_aug[indices], y_aug[indices]
            tree = build_tree(Xi, yi, max_depth=max_depth, min_samples=min_samples,
                            n_feat_sample=n_feat_sample, rng=rng)
            trees.append(tree)

        train_acc = evaluate(trees, X_orig, y_orig, "Train (orig)")
        val_acc = evaluate(trees, X_val, y_val, "Val")
        gap = train_acc - val_acc
        print(f"  Gap: {gap*100:.1f}pp")


if __name__ == "__main__":
    main()
