"""Replace the 10 weakest features with better spatial/shape ones.

Weakest (F < 1.0): hu2, center_obj_diff, top_minus_bot, black_ratio,
v_top_third, q0_v, q1_v, aspect_main_contour, rg_ratio, v_bimodal

Replace with:
- 4 radial color features (concentric rings)
- 3 edge-shape features (contour moments)
- 3 color transition features (borders between regions)
"""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import CLASSES, gini, Node, find_best_split, build_tree, count_nodes, predict_tree

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"

# Indices to REMOVE (worst F-ratios)
REMOVE_INDICES = {87, 39, 21, 9, 62, 48, 52, 41, 28, 37}


def extract_features_v3(image):
    """Modified feature extraction: replace 10 worst with better ones."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    b_ch, g_ch, r_ch = cv2.split(image)
    avg_r = float(np.mean(r_ch))
    avg_g = float(np.mean(g_ch))
    avg_b = float(np.mean(b_ch))
    edges = cv2.Canny(gray.astype(np.uint8), 30, 100)
    sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    lap = cv2.Laplacian(gray, cv2.CV_32F)
    grad_mag = np.sqrt(sobelx**2 + sobely**2)

    features = []
    # ORIGINAL features (indices 0-89), skip REMOVE_INDICES
    # This is a simplified approach: compute all original, then replace
    # Compute all 90 original features the same way as build_forest.py
    sat_mask = s > 50
    warm_region = (h < 30) & (s > 30) & (v > 50)

    # Instead of the full complex extraction, let's just import and modify
    from build_forest import extract_features as orig_extract
    orig = orig_extract(image)

    # Keep all except the 10 worst
    kept = [orig[i] for i in range(90) if i not in REMOVE_INDICES]  # 80 features

    # Now add 10 NEW features

    # 1-3: Radial color rings (3 concentric rings)
    yy, xx = np.mgrid[0:64, 0:64]
    dist = np.sqrt((yy - 32)**2 + (xx - 32)**2)
    ring1 = dist < 12
    ring2 = (dist >= 12) & (dist < 24)
    ring3 = dist >= 24
    kept.append(float(np.mean(s[ring1])))  # inner ring saturation
    kept.append(float(np.mean(s[ring2])))  # middle ring saturation
    kept.append(float(np.mean(s[ring3])))  # outer ring saturation

    # 4: Radial hue gradient (inner warm vs outer warm)
    inner_warm = float(np.mean((h[ring1] < 30) & (s[ring1] > 50)))
    outer_warm = float(np.mean((h[ring3] < 30) & (s[ring3] > 50)))
    kept.append(inner_warm - outer_warm)

    # 5-6: Horizontal and vertical color gradients
    left_half_sat = float(np.mean(s[:, :32]))
    right_half_sat = float(np.mean(s[:, 32:]))
    kept.append(abs(left_half_sat - right_half_sat))
    top_half_hue = float(np.mean(h[:32, :]))
    bot_half_hue = float(np.mean(h[32:, :]))
    kept.append(top_half_hue - bot_half_hue)

    # 7-8: Object size proxies from edge contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        areas = [cv2.contourArea(c) for c in contours]
        largest_area = max(areas) / (64 * 64)
        n_large = sum(1 for a in areas if a > 50) / max(len(areas), 1)
    else:
        largest_area = 0.0
        n_large = 0.0
    kept.append(largest_area)
    kept.append(n_large)

    # 9: Gradient direction coherence (how aligned are gradients?)
    angle = np.arctan2(sobely, sobelx)
    strong = grad_mag > np.percentile(grad_mag, 75)
    if np.sum(strong) > 50:
        angles_strong = angle[strong]
        # Circular variance (0 = all aligned, 1 = random)
        circ_var = 1.0 - np.sqrt(np.mean(np.cos(angles_strong))**2 + np.mean(np.sin(angles_strong))**2)
        kept.append(float(circ_var))
    else:
        kept.append(0.5)

    # 10: Color complexity (number of distinct hue modes)
    sat_pixels = h[s > 60]
    if len(sat_pixels) > 50:
        h_hist = np.histogram(sat_pixels, bins=12, range=(0, 180))[0]
        h_hist = h_hist / max(np.sum(h_hist), 1)
        n_modes = np.sum(h_hist > 0.1)
        kept.append(float(n_modes))
    else:
        kept.append(1.0)

    return kept  # Should be exactly 90


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
            feats = extract_features_v3(img)
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
    print("Loading data with v3 features (replaced worst 10)...")
    X_train, y_train = load_data(DATA_ROOT)
    X_val, y_val = load_data(VAL_ROOT)
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Features: {X_train.shape[1]}")

    n_trees = 101
    max_depth = 14
    min_samples = 16
    n_feat_sample = 18

    trees = []
    for i in range(n_trees):
        rng = np.random.RandomState(i * 7 + 42)
        indices = rng.choice(len(X_train), len(X_train), replace=True)
        Xi, yi = X_train[indices], y_train[indices]
        tree = build_tree(Xi, yi, max_depth=max_depth, min_samples=min_samples,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
        if i % 25 == 0:
            print(f"  Tree {i}: {count_nodes(tree)} nodes")

    train_acc = eval_forest(trees, X_train, y_train)
    val_acc = eval_forest(trees, X_val, y_val)
    print(f"\nv3 Forest: Train={train_acc:.1%}, Val={val_acc:.1%}, Gap={100*(train_acc-val_acc):.1f}pp")
    print(f"  (Baseline: Train=90.2%, Val=64.4%)")


if __name__ == "__main__":
    main()
