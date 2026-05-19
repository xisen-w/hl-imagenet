"""Build a random forest and compile it into a single predict.py.

Each tree is compiled to a Python function (tree_0, tree_1, ...).
predict() calls all trees and takes majority vote.
No stored data at inference — only if/else branches.

This captures feature interactions that GNB cannot and uses ensemble
diversity to reduce overfitting vs a single tree."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2
import json

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"

CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]

FEATURE_NAMES = [
    "avg_s", "r_minus_b", "blue_ratio", "orange_hue", "yellow_ratio",
    "green_ratio", "high_sat", "sat_center", "white_ratio", "black_ratio",
    "texture_var", "horiz_edges", "contrast", "hue_std", "symmetry",
    "low_sat_high_val", "warm_cool", "hue_15_30", "very_orange",
    "vert_edge_ratio", "circularity", "top_minus_bot", "rb_ratio",
    "warm_brown", "medium_gray", "edge_density_center", "warm_texture",
    "warm_brightness", "rg_ratio", "center_vs_periph", "dark_bottom",
    "yellow_band", "smooth_frac", "lbp_uniformity", "gradient_uniformity",
    "center_sat_low", "high_val_low_sat", "v_bimodal", "achromatic",
    "center_obj_diff", "horiz_line_score", "aspect_main_contour",
    "edge_in_center_ratio", "color_entropy",
    "hue_in_yellow", "warm_uniform",
    "q0_h", "q0_s", "q0_v", "q0_edge",
    "q1_h", "q1_s", "q1_v", "q1_edge",
    "q2_h", "q2_s", "q2_v", "q2_edge",
    "q3_h", "q3_s", "q3_v", "q3_edge",
    "v_top_third", "v_mid_third", "v_bot_third",
    "s_top_third", "s_mid_third", "s_bot_third",
    "h_center_mean", "edge_top_ratio", "edge_bot_ratio",
    # LAB color moments (from Phase 2 — orthogonal to HSV)
    "lab_a_mean", "lab_b_mean", "lab_a_std", "lab_b_std",
    "lab_center_a", "lab_center_b",
    # DCT frequency bands
    "dct_low", "dct_mid", "dct_high",
    # Gabor texture (2 orientations x 2 frequencies)
    "gabor_0_02_mean", "gabor_45_02_mean", "gabor_0_04_mean", "gabor_45_04_mean",
    # FFT features
    "fft_hv_ratio", "fft_high_freq",
    # Additional texture/shape
    "hu1", "hu2",
    "glcm_contrast", "glcm_homogeneity",
]


def extract_features(image):
    """Same feature extraction as build_tree.py"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    b_ch, g_ch, r_ch = cv2.split(image)
    avg_r = float(np.mean(r_ch))
    avg_g = float(np.mean(g_ch))
    avg_b = float(np.mean(b_ch))
    features = []
    features.append(float(np.mean(s)))
    features.append(avg_r - avg_b)
    features.append(float(np.mean((h >= 90) & (h <= 130) & (s > 80))))
    features.append(float(np.mean((h >= 5) & (h <= 20) & (s > 120))))
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 100))))
    features.append(float(np.mean((h >= 35) & (h <= 80) & (s > 50))))
    features.append(float(np.mean(s > 180)))
    features.append(float(np.mean(s[16:48, 16:48])))
    features.append(float(np.mean((s < 50) & (v > 180))))
    features.append(float(np.mean(v < 40)))
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    features.append(float(np.var(lap)))
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    horiz_e = float(np.mean(np.abs(sobely)))
    features.append(horiz_e)
    features.append(float(np.std(gray)))
    sat_mask = s > 50
    features.append(float(np.std(h[sat_mask].astype(float))) if np.sum(sat_mask) > 100 else 0.0)
    left = gray[:, :32].astype(float)
    right = gray[:, 32:][:, ::-1].astype(float)
    features.append(1.0 - float(np.mean(np.abs(left - right))) / 128.0)
    features.append(float(np.mean((s < 60) & (v > 150))))
    if np.sum(sat_mask) > 50:
        h_sat = h[sat_mask]
        warm = float(np.sum(h_sat < 30))
        cool = float(np.sum(h_sat > 90))
        features.append(warm / max(warm + cool, 1.0))
    else:
        features.append(0.5)
    features.append(float(np.mean((h >= 15) & (h < 30) & (s > 50))))
    features.append(float(np.mean((h < 15) & (s > 100))))
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    vert_e = float(np.mean(np.abs(sobelx)))
    features.append(vert_e / max(horiz_e, 1.0))
    sat_thresh = (s > 100).astype(np.uint8) * 255
    contours, _ = cv2.findContours(sat_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        perimeter = cv2.arcLength(largest, True)
        features.append(4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0.0)
    else:
        features.append(0.0)
    features.append(float(np.mean(v[:32, :])) - float(np.mean(v[32:, :])))
    features.append(avg_r / max(avg_b, 1.0))
    features.append(float(np.mean((h >= 10) & (h <= 25) & (s >= 40) & (s <= 150))))
    features.append(float(np.mean((gray >= 80) & (gray <= 160) & (s < 60))))
    edges = cv2.Canny(gray, 30, 100)
    features.append(float(np.mean(edges[16:48, 16:48] > 0)))
    warm_region = (h < 30) & (s > 30) & (v > 50)
    if np.sum(warm_region) > 100:
        features.append(float(np.std(lap[warm_region])))
    else:
        features.append(0.0)
    if np.sum(warm_region) > 100:
        features.append(float(np.mean(v[warm_region])))
    else:
        features.append(128.0)
    features.append(avg_r / max(avg_g, 1.0))
    center_gray = float(np.mean(gray[16:48, 16:48]))
    periph_gray = (float(np.mean(gray[:16, :])) + float(np.mean(gray[48:, :])) +
                   float(np.mean(gray[:, :16])) + float(np.mean(gray[:, 48:]))) / 4.0
    features.append(center_gray - periph_gray)
    features.append(float(np.mean(v[48:, :] < 80)))
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 80) & (v > 120))))
    features.append(float(np.mean(np.abs(lap) < 5)))
    padded = np.pad(gray, 1, mode='reflect')
    center_p = padded[1:-1, 1:-1].astype(np.int16)
    d_top = np.abs(padded[0:-2, 1:-1].astype(np.int16) - center_p)
    d_bot = np.abs(padded[2:, 1:-1].astype(np.int16) - center_p)
    d_left = np.abs(padded[1:-1, 0:-2].astype(np.int16) - center_p)
    d_right = np.abs(padded[1:-1, 2:].astype(np.int16) - center_p)
    uniform = (d_top < 10) & (d_bot < 10) & (d_left < 10) & (d_right < 10)
    features.append(float(np.mean(uniform)))
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    grad_mean = float(np.mean(grad_mag))
    grad_std = float(np.std(grad_mag))
    features.append(grad_std / max(grad_mean, 1.0))
    features.append(float(np.mean(s[16:48, 16:48] < 60)))
    features.append(float(np.mean((v > 150) & (s < 80))))
    v_hist = np.histogram(v, bins=4, range=(0, 256))[0].astype(float) / (64 * 64)
    features.append(float(v_hist[0] * v_hist[3]))
    features.append(float(np.mean(s < 40)))
    center_v = float(np.mean(v[16:48, 16:48]))
    border_pixels = np.concatenate([v[:8, :].flatten(), v[56:, :].flatten(),
                                    v[:, :8].flatten(), v[:, 56:].flatten()])
    border_v = float(np.mean(border_pixels))
    features.append(abs(center_v - border_v))
    h_energy = float(np.sum(sobely**2))
    v_energy = float(np.sum(sobelx**2))
    features.append(h_energy / max(h_energy + v_energy, 1.0))
    edge_img = cv2.Canny(gray, 50, 150)
    contours2, _ = cv2.findContours(edge_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours2:
        largest2 = max(contours2, key=cv2.contourArea)
        if len(largest2) >= 5:
            rect = cv2.minAreaRect(largest2)
            w, h_r = rect[1]
            features.append(max(w, h_r) / max(min(w, h_r), 1.0))
        else:
            features.append(1.0)
    else:
        features.append(1.0)
    center_edge = float(np.mean(edges[16:48, 16:48] > 0))
    total_edge = float(np.mean(edges > 0))
    features.append(center_edge / max(total_edge, 0.001))
    sat_pixels = h[s > 50]
    if len(sat_pixels) > 100:
        h_hist_arr = np.histogram(sat_pixels, bins=18, range=(0, 180))[0].astype(float)
        h_hist_arr = h_hist_arr / max(np.sum(h_hist_arr), 1)
        h_hist_arr = h_hist_arr[h_hist_arr > 0]
        features.append(-float(np.sum(h_hist_arr * np.log2(h_hist_arr))))
    else:
        features.append(0.0)
    if len(sat_pixels) > 100:
        features.append(float(np.sum((sat_pixels >= 18) & (sat_pixels <= 38))) / len(sat_pixels))
    else:
        features.append(0.0)
    features.append(float(np.mean((h >= 10) & (h <= 30) & (s > 50) & (v > 100))))
    # Spatial grid
    H2, W2 = 32, 32
    for qi, (r0, c0) in enumerate([(0, 0), (0, W2), (H2, 0), (H2, W2)]):
        r1, c1 = r0 + H2, c0 + W2
        features.append(float(np.mean(h[r0:r1, c0:c1])))
        features.append(float(np.mean(s[r0:r1, c0:c1])))
        features.append(float(np.mean(v[r0:r1, c0:c1])))
        features.append(float(np.mean(edges[r0:r1, c0:c1] > 0)))
    # Thirds
    third = 64 // 3
    features.append(float(np.mean(v[:third, :])))
    features.append(float(np.mean(v[third:2*third, :])))
    features.append(float(np.mean(v[2*third:, :])))
    features.append(float(np.mean(s[:third, :])))
    features.append(float(np.mean(s[third:2*third, :])))
    features.append(float(np.mean(s[2*third:, :])))
    features.append(float(np.mean(h[16:48, 16:48])))
    features.append(float(np.mean(edges[:third, :] > 0)))
    features.append(float(np.mean(edges[2*third:, :] > 0)))
    # LAB color moments
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_ch, a_ch, b_lab = cv2.split(lab)
    features.append(float(np.mean(a_ch)))
    features.append(float(np.mean(b_lab)))
    features.append(float(np.std(a_ch)))
    features.append(float(np.std(b_lab)))
    features.append(float(np.mean(a_ch[16:48, 16:48])))
    features.append(float(np.mean(b_lab[16:48, 16:48])))
    # DCT frequency bands
    gray_f = gray.astype(np.float32)
    dct = cv2.dct(gray_f)
    features.append(float(np.mean(np.abs(dct[:8, :8]))))
    features.append(float(np.mean(np.abs(dct[8:24, 8:24]))))
    features.append(float(np.mean(np.abs(dct[24:, 24:]))))
    # Gabor texture
    for theta in [0, np.pi/4]:
        for freq in [0.2, 0.4]:
            kern = cv2.getGaborKernel((9, 9), 3.0, theta, 1.0/freq, 0.5, 0, ktype=cv2.CV_32F)
            filtered = cv2.filter2D(gray_f, cv2.CV_32F, kern)
            features.append(float(np.mean(np.abs(filtered))))
    # FFT features
    f_transform = np.fft.fft2(gray_f)
    f_shift = np.fft.fftshift(f_transform)
    magnitude = np.abs(f_shift)
    cy, cx = 32, 32
    h_band = magnitude[cy-2:cy+3, :]
    v_band = magnitude[:, cx-2:cx+3]
    fft_h = float(np.sum(h_band))
    fft_v = float(np.sum(v_band))
    features.append(fft_h / max(fft_v, 1.0))
    features.append(float(np.mean(magnitude[magnitude > np.percentile(magnitude, 90)])))
    # Hu moments
    moments = cv2.moments(gray)
    hu = cv2.HuMoments(moments).flatten()
    features.append(float(hu[0]))
    features.append(float(hu[1]))
    # GLCM approximation (fast co-occurrence)
    shifted_r = np.roll(gray, 1, axis=1)
    diff = np.abs(gray.astype(np.int16) - shifted_r.astype(np.int16))
    features.append(float(np.mean(diff**2)))
    features.append(float(np.mean(diff < 10)))
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
            feats = extract_features(img)
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


def build_tree(X, y, depth=0, max_depth=14, min_samples=8, n_feat_sample=None, rng=None):
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
    node.thresh = round(float(thresh), 4)
    left_mask = X[:, feat] <= thresh
    node.left = build_tree(X[left_mask], y[left_mask], depth + 1, max_depth, min_samples, n_feat_sample, rng)
    node.right = build_tree(X[~left_mask], y[~left_mask], depth + 1, max_depth, min_samples, n_feat_sample, rng)
    return node


def tree_to_code(node, func_name, indent=1):
    """Convert tree to a Python function returning class index."""
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
    print("Loading training data...")
    X, y = load_data()
    print(f"Loaded {len(X)} samples, {X.shape[1]} features")

    # Build forest with bagging + feature subsampling
    n_trees = 101
    max_depth = 14
    min_samples = 16
    n_feat_sample = int(np.sqrt(X.shape[1]) * 2)

    trees = []
    tree_codes = []
    for i in range(n_trees):
        rng = np.random.RandomState(i * 7 + 42)
        # Bootstrap sample
        indices = rng.choice(len(X), len(X), replace=True)
        Xi, yi = X[indices], y[indices]
        tree = build_tree(Xi, yi, max_depth=max_depth, min_samples=min_samples,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
        nodes = count_nodes(tree)
        # OOB accuracy
        oob_mask = np.ones(len(X), dtype=bool)
        oob_mask[np.unique(indices)] = False
        oob_correct = sum(predict_tree(tree, X[j]) == y[j] for j in range(len(X)) if oob_mask[j])
        oob_total = np.sum(oob_mask)
        oob_acc = oob_correct / oob_total if oob_total > 0 else 0
        print(f"  Tree {i}: {nodes} nodes, OOB acc: {oob_acc:.1%} ({oob_total} samples)")
        tree_codes.append(tree_to_code(tree, f"_tree_{i}"))

    # Forest accuracy on full train
    correct = 0
    for i in range(len(y)):
        votes = Counter()
        for t in trees:
            votes[predict_tree(t, X[i])] += 1
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    print(f"\nForest train accuracy: {correct/len(y):.1%}")

    # Generate predict.py
    tree_funcs = "\n\n".join(tree_codes)
    tree_calls = ", ".join(f"_tree_{i}(f)" for i in range(n_trees))

    tree_calls = ", ".join(f"_tree_{i}(f)" for i in range(n_trees))

    predict_py = f'''"""Classifier: random forest of {n_trees} decision trees compiled to Python code.
Interface: predict(image: np.ndarray) -> str

CONSTRAINT: No stored training data. Each tree is pure if/else code.
The forest captures feature interactions via conjunctive splits
and uses ensemble voting to reduce overfitting.

{n_trees} trees, max_depth={max_depth}, {X.shape[1]} features including spatial grid."""

import cv2
import numpy as np
from collections import Counter


CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]


def predict(image: np.ndarray) -> str:
    f = _extract_features(image)
    votes = [{tree_calls}]
    counts = Counter(votes)
    return CLASSES[counts.most_common(1)[0][0]]


{tree_funcs}


{_get_extract_features_code()}
'''

    out_path = Path(__file__).parent / "predict.py"
    with open(out_path, "w") as f_out:
        f_out.write(predict_py)
    total_nodes = sum(count_nodes(t) for t in trees)
    print(f"\nWrote predict.py ({len(predict_py)} bytes, {total_nodes} total nodes across {n_trees} trees)")


def _get_extract_features_code():
    return '''def _extract_features(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    b_ch, g_ch, r_ch = cv2.split(image)
    avg_r = float(np.mean(r_ch))
    avg_g = float(np.mean(g_ch))
    avg_b = float(np.mean(b_ch))
    features = []
    features.append(float(np.mean(s)))
    features.append(avg_r - avg_b)
    features.append(float(np.mean((h >= 90) & (h <= 130) & (s > 80))))
    features.append(float(np.mean((h >= 5) & (h <= 20) & (s > 120))))
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 100))))
    features.append(float(np.mean((h >= 35) & (h <= 80) & (s > 50))))
    features.append(float(np.mean(s > 180)))
    features.append(float(np.mean(s[16:48, 16:48])))
    features.append(float(np.mean((s < 50) & (v > 180))))
    features.append(float(np.mean(v < 40)))
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    features.append(float(np.var(lap)))
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    horiz_e = float(np.mean(np.abs(sobely)))
    features.append(horiz_e)
    features.append(float(np.std(gray)))
    sat_mask = s > 50
    features.append(float(np.std(h[sat_mask].astype(float))) if np.sum(sat_mask) > 100 else 0.0)
    left = gray[:, :32].astype(float)
    right = gray[:, 32:][:, ::-1].astype(float)
    features.append(1.0 - float(np.mean(np.abs(left - right))) / 128.0)
    features.append(float(np.mean((s < 60) & (v > 150))))
    if np.sum(sat_mask) > 50:
        h_sat = h[sat_mask]
        warm = float(np.sum(h_sat < 30))
        cool = float(np.sum(h_sat > 90))
        features.append(warm / max(warm + cool, 1.0))
    else:
        features.append(0.5)
    features.append(float(np.mean((h >= 15) & (h < 30) & (s > 50))))
    features.append(float(np.mean((h < 15) & (s > 100))))
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    vert_e = float(np.mean(np.abs(sobelx)))
    features.append(vert_e / max(horiz_e, 1.0))
    sat_thresh = (s > 100).astype(np.uint8) * 255
    contours, _ = cv2.findContours(sat_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        perimeter = cv2.arcLength(largest, True)
        features.append(4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0.0)
    else:
        features.append(0.0)
    features.append(float(np.mean(v[:32, :])) - float(np.mean(v[32:, :])))
    features.append(avg_r / max(avg_b, 1.0))
    features.append(float(np.mean((h >= 10) & (h <= 25) & (s >= 40) & (s <= 150))))
    features.append(float(np.mean((gray >= 80) & (gray <= 160) & (s < 60))))
    edges = cv2.Canny(gray, 30, 100)
    features.append(float(np.mean(edges[16:48, 16:48] > 0)))
    warm_region = (h < 30) & (s > 30) & (v > 50)
    if np.sum(warm_region) > 100:
        features.append(float(np.std(lap[warm_region])))
    else:
        features.append(0.0)
    if np.sum(warm_region) > 100:
        features.append(float(np.mean(v[warm_region])))
    else:
        features.append(128.0)
    features.append(avg_r / max(avg_g, 1.0))
    center_gray = float(np.mean(gray[16:48, 16:48]))
    periph_gray = (float(np.mean(gray[:16, :])) + float(np.mean(gray[48:, :])) +
                   float(np.mean(gray[:, :16])) + float(np.mean(gray[:, 48:]))) / 4.0
    features.append(center_gray - periph_gray)
    features.append(float(np.mean(v[48:, :] < 80)))
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 80) & (v > 120))))
    features.append(float(np.mean(np.abs(lap) < 5)))
    padded = np.pad(gray, 1, mode='reflect')
    center_p = padded[1:-1, 1:-1].astype(np.int16)
    d_top = np.abs(padded[0:-2, 1:-1].astype(np.int16) - center_p)
    d_bot = np.abs(padded[2:, 1:-1].astype(np.int16) - center_p)
    d_left = np.abs(padded[1:-1, 0:-2].astype(np.int16) - center_p)
    d_right = np.abs(padded[1:-1, 2:].astype(np.int16) - center_p)
    uniform = (d_top < 10) & (d_bot < 10) & (d_left < 10) & (d_right < 10)
    features.append(float(np.mean(uniform)))
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    grad_mean = float(np.mean(grad_mag))
    grad_std = float(np.std(grad_mag))
    features.append(grad_std / max(grad_mean, 1.0))
    features.append(float(np.mean(s[16:48, 16:48] < 60)))
    features.append(float(np.mean((v > 150) & (s < 80))))
    v_hist = np.histogram(v, bins=4, range=(0, 256))[0].astype(float) / (64 * 64)
    features.append(float(v_hist[0] * v_hist[3]))
    features.append(float(np.mean(s < 40)))
    center_v = float(np.mean(v[16:48, 16:48]))
    border_pixels = np.concatenate([v[:8, :].flatten(), v[56:, :].flatten(),
                                    v[:, :8].flatten(), v[:, 56:].flatten()])
    border_v = float(np.mean(border_pixels))
    features.append(abs(center_v - border_v))
    h_energy = float(np.sum(sobely**2))
    v_energy = float(np.sum(sobelx**2))
    features.append(h_energy / max(h_energy + v_energy, 1.0))
    edge_img = cv2.Canny(gray, 50, 150)
    contours2, _ = cv2.findContours(edge_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours2:
        largest2 = max(contours2, key=cv2.contourArea)
        if len(largest2) >= 5:
            rect = cv2.minAreaRect(largest2)
            w, h_r = rect[1]
            features.append(max(w, h_r) / max(min(w, h_r), 1.0))
        else:
            features.append(1.0)
    else:
        features.append(1.0)
    center_edge = float(np.mean(edges[16:48, 16:48] > 0))
    total_edge = float(np.mean(edges > 0))
    features.append(center_edge / max(total_edge, 0.001))
    sat_pixels = h[s > 50]
    if len(sat_pixels) > 100:
        h_hist_arr = np.histogram(sat_pixels, bins=18, range=(0, 180))[0].astype(float)
        h_hist_arr = h_hist_arr / max(np.sum(h_hist_arr), 1)
        h_hist_arr = h_hist_arr[h_hist_arr > 0]
        features.append(-float(np.sum(h_hist_arr * np.log2(h_hist_arr))))
    else:
        features.append(0.0)
    if len(sat_pixels) > 100:
        features.append(float(np.sum((sat_pixels >= 18) & (sat_pixels <= 38))) / len(sat_pixels))
    else:
        features.append(0.0)
    features.append(float(np.mean((h >= 10) & (h <= 30) & (s > 50) & (v > 100))))
    H2, W2 = 32, 32
    for qi, (r0, c0) in enumerate([(0, 0), (0, W2), (H2, 0), (H2, W2)]):
        r1, c1 = r0 + H2, c0 + W2
        features.append(float(np.mean(h[r0:r1, c0:c1])))
        features.append(float(np.mean(s[r0:r1, c0:c1])))
        features.append(float(np.mean(v[r0:r1, c0:c1])))
        features.append(float(np.mean(edges[r0:r1, c0:c1] > 0)))
    third = 64 // 3
    features.append(float(np.mean(v[:third, :])))
    features.append(float(np.mean(v[third:2*third, :])))
    features.append(float(np.mean(v[2*third:, :])))
    features.append(float(np.mean(s[:third, :])))
    features.append(float(np.mean(s[third:2*third, :])))
    features.append(float(np.mean(s[2*third:, :])))
    features.append(float(np.mean(h[16:48, 16:48])))
    features.append(float(np.mean(edges[:third, :] > 0)))
    features.append(float(np.mean(edges[2*third:, :] > 0)))
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_ch, a_ch, b_lab = cv2.split(lab)
    features.append(float(np.mean(a_ch)))
    features.append(float(np.mean(b_lab)))
    features.append(float(np.std(a_ch)))
    features.append(float(np.std(b_lab)))
    features.append(float(np.mean(a_ch[16:48, 16:48])))
    features.append(float(np.mean(b_lab[16:48, 16:48])))
    gray_f = gray.astype(np.float32)
    dct = cv2.dct(gray_f)
    features.append(float(np.mean(np.abs(dct[:8, :8]))))
    features.append(float(np.mean(np.abs(dct[8:24, 8:24]))))
    features.append(float(np.mean(np.abs(dct[24:, 24:]))))
    for theta in [0, np.pi/4]:
        for freq in [0.2, 0.4]:
            kern = cv2.getGaborKernel((9, 9), 3.0, theta, 1.0/freq, 0.5, 0, ktype=cv2.CV_32F)
            filtered = cv2.filter2D(gray_f, cv2.CV_32F, kern)
            features.append(float(np.mean(np.abs(filtered))))
    f_transform = np.fft.fft2(gray_f)
    f_shift = np.fft.fftshift(f_transform)
    magnitude = np.abs(f_shift)
    cy, cx = 32, 32
    h_band = magnitude[cy-2:cy+3, :]
    v_band = magnitude[:, cx-2:cx+3]
    fft_h = float(np.sum(h_band))
    fft_v = float(np.sum(v_band))
    features.append(fft_h / max(fft_v, 1.0))
    features.append(float(np.mean(magnitude[magnitude > np.percentile(magnitude, 90)])))
    moments = cv2.moments(gray)
    hu = cv2.HuMoments(moments).flatten()
    features.append(float(hu[0]))
    features.append(float(hu[1]))
    shifted_r = np.roll(gray, 1, axis=1)
    diff = np.abs(gray.astype(np.int16) - shifted_r.astype(np.int16))
    features.append(float(np.mean(diff**2)))
    features.append(float(np.mean(diff < 10)))
    return features'''


if __name__ == "__main__":
    main()
