"""Build an optimal decision tree from training data and output it as Python code.

This is the bold move: auto-generate predict.py as a pure decision tree.
No GNB, no stored means/stds. Just if/else branches that encode the
optimal splitting logic discovered from the training data.

The tree captures feature interactions that GNB fundamentally cannot."""

import sys
from pathlib import Path
from collections import Counter, defaultdict
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
    # spatial grid features
    "q0_h", "q0_s", "q0_v", "q0_edge",
    "q1_h", "q1_s", "q1_v", "q1_edge",
    "q2_h", "q2_s", "q2_v", "q2_edge",
    "q3_h", "q3_s", "q3_v", "q3_edge",
    # additional spatial
    "v_top_third", "v_mid_third", "v_bot_third",
    "s_top_third", "s_mid_third", "s_bot_third",
    "h_center_mean", "edge_top_ratio", "edge_bot_ratio",
]


def extract_features(image):
    """Extract all features including spatial grid."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    b_ch, g_ch, r_ch = cv2.split(image)

    avg_r = float(np.mean(r_ch))
    avg_g = float(np.mean(g_ch))
    avg_b = float(np.mean(b_ch))

    features = []

    # 0: avg_s
    features.append(float(np.mean(s)))
    # 1: r_minus_b
    features.append(avg_r - avg_b)
    # 2: blue_ratio
    features.append(float(np.mean((h >= 90) & (h <= 130) & (s > 80))))
    # 3: orange_hue
    features.append(float(np.mean((h >= 5) & (h <= 20) & (s > 120))))
    # 4: yellow_ratio
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 100))))
    # 5: green_ratio
    features.append(float(np.mean((h >= 35) & (h <= 80) & (s > 50))))
    # 6: high_sat
    features.append(float(np.mean(s > 180)))
    # 7: sat_center
    features.append(float(np.mean(s[16:48, 16:48])))
    # 8: white_ratio
    features.append(float(np.mean((s < 50) & (v > 180))))
    # 9: black_ratio
    features.append(float(np.mean(v < 40)))
    # 10: texture_var
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    features.append(float(np.var(lap)))
    # 11: horiz_edges
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    horiz_e = float(np.mean(np.abs(sobely)))
    features.append(horiz_e)
    # 12: contrast
    features.append(float(np.std(gray)))
    # 13: hue_std
    sat_mask = s > 50
    features.append(float(np.std(h[sat_mask].astype(float))) if np.sum(sat_mask) > 100 else 0.0)
    # 14: symmetry
    left = gray[:, :32].astype(float)
    right = gray[:, 32:][:, ::-1].astype(float)
    features.append(1.0 - float(np.mean(np.abs(left - right))) / 128.0)
    # 15: low_sat_high_val
    features.append(float(np.mean((s < 60) & (v > 150))))
    # 16: warm_cool
    if np.sum(sat_mask) > 50:
        h_sat = h[sat_mask]
        warm = float(np.sum(h_sat < 30))
        cool = float(np.sum(h_sat > 90))
        features.append(warm / max(warm + cool, 1.0))
    else:
        features.append(0.5)
    # 17: hue_15_30
    features.append(float(np.mean((h >= 15) & (h < 30) & (s > 50))))
    # 18: very_orange
    features.append(float(np.mean((h < 15) & (s > 100))))
    # 19: vert_edge_ratio
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    vert_e = float(np.mean(np.abs(sobelx)))
    features.append(vert_e / max(horiz_e, 1.0))
    # 20: circularity
    sat_thresh = (s > 100).astype(np.uint8) * 255
    contours, _ = cv2.findContours(sat_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        perimeter = cv2.arcLength(largest, True)
        features.append(4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0.0)
    else:
        features.append(0.0)
    # 21: top_minus_bot
    features.append(float(np.mean(v[:32, :])) - float(np.mean(v[32:, :])))
    # 22: rb_ratio
    features.append(avg_r / max(avg_b, 1.0))
    # 23: warm_brown
    features.append(float(np.mean((h >= 10) & (h <= 25) & (s >= 40) & (s <= 150))))
    # 24: medium_gray
    features.append(float(np.mean((gray >= 80) & (gray <= 160) & (s < 60))))
    # 25: edge_density_center
    edges = cv2.Canny(gray, 30, 100)
    features.append(float(np.mean(edges[16:48, 16:48] > 0)))
    # 26: warm_texture
    warm_region = (h < 30) & (s > 30) & (v > 50)
    if np.sum(warm_region) > 100:
        features.append(float(np.std(lap[warm_region])))
    else:
        features.append(0.0)
    # 27: warm_brightness
    if np.sum(warm_region) > 100:
        features.append(float(np.mean(v[warm_region])))
    else:
        features.append(128.0)
    # 28: rg_ratio
    features.append(avg_r / max(avg_g, 1.0))
    # 29: center_vs_periph
    center_gray = float(np.mean(gray[16:48, 16:48]))
    periph_gray = (float(np.mean(gray[:16, :])) + float(np.mean(gray[48:, :])) +
                   float(np.mean(gray[:, :16])) + float(np.mean(gray[:, 48:]))) / 4.0
    features.append(center_gray - periph_gray)
    # 30: dark_bottom
    features.append(float(np.mean(v[48:, :] < 80)))
    # 31: yellow_band
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 80) & (v > 120))))
    # 32: smooth_frac
    features.append(float(np.mean(np.abs(lap) < 5)))
    # 33: lbp_uniformity
    padded = np.pad(gray, 1, mode='reflect')
    center_p = padded[1:-1, 1:-1].astype(np.int16)
    d_top = np.abs(padded[0:-2, 1:-1].astype(np.int16) - center_p)
    d_bot = np.abs(padded[2:, 1:-1].astype(np.int16) - center_p)
    d_left = np.abs(padded[1:-1, 0:-2].astype(np.int16) - center_p)
    d_right = np.abs(padded[1:-1, 2:].astype(np.int16) - center_p)
    uniform = (d_top < 10) & (d_bot < 10) & (d_left < 10) & (d_right < 10)
    features.append(float(np.mean(uniform)))
    # 34: gradient_uniformity
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    grad_mean = float(np.mean(grad_mag))
    grad_std = float(np.std(grad_mag))
    features.append(grad_std / max(grad_mean, 1.0))
    # 35: center_sat_low
    features.append(float(np.mean(s[16:48, 16:48] < 60)))
    # 36: high_val_low_sat
    features.append(float(np.mean((v > 150) & (s < 80))))
    # 37: v_bimodal
    v_hist = np.histogram(v, bins=4, range=(0, 256))[0].astype(float) / (64 * 64)
    features.append(float(v_hist[0] * v_hist[3]))
    # 38: achromatic
    features.append(float(np.mean(s < 40)))
    # 39: center_obj_diff
    center_v = float(np.mean(v[16:48, 16:48]))
    border_pixels = np.concatenate([v[:8, :].flatten(), v[56:, :].flatten(),
                                    v[:, :8].flatten(), v[:, 56:].flatten()])
    border_v = float(np.mean(border_pixels))
    features.append(abs(center_v - border_v))
    # 40: horiz_line_score
    h_energy = float(np.sum(sobely**2))
    v_energy = float(np.sum(sobelx**2))
    features.append(h_energy / max(h_energy + v_energy, 1.0))
    # 41: aspect_main_contour
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
    # 42: edge_in_center_ratio
    center_edge = float(np.mean(edges[16:48, 16:48] > 0))
    total_edge = float(np.mean(edges > 0))
    features.append(center_edge / max(total_edge, 0.001))
    # 43: color_entropy
    sat_pixels = h[s > 50]
    if len(sat_pixels) > 100:
        h_hist_arr = np.histogram(sat_pixels, bins=18, range=(0, 180))[0].astype(float)
        h_hist_arr = h_hist_arr / max(np.sum(h_hist_arr), 1)
        h_hist_arr = h_hist_arr[h_hist_arr > 0]
        features.append(-float(np.sum(h_hist_arr * np.log2(h_hist_arr))))
    else:
        features.append(0.0)
    # 44: hue_in_yellow
    if len(sat_pixels) > 100:
        features.append(float(np.sum((sat_pixels >= 18) & (sat_pixels <= 38))) / len(sat_pixels))
    else:
        features.append(0.0)
    # 45: warm_uniform
    features.append(float(np.mean((h >= 10) & (h <= 30) & (s > 50) & (v > 100))))

    # === SPATIAL GRID FEATURES (46-61) ===
    # 2x2 quadrants: mean H, mean S, mean V, edge density
    H2 = 32
    W2 = 32
    for qi, (r0, c0) in enumerate([(0, 0), (0, W2), (H2, 0), (H2, W2)]):
        r1, c1 = r0 + H2, c0 + W2
        features.append(float(np.mean(h[r0:r1, c0:c1])))       # q_h
        features.append(float(np.mean(s[r0:r1, c0:c1])))       # q_s
        features.append(float(np.mean(v[r0:r1, c0:c1])))       # q_v
        features.append(float(np.mean(edges[r0:r1, c0:c1] > 0)))  # q_edge

    # === THIRD-SPLIT FEATURES (62-70) ===
    third = 64 // 3
    # V in top/mid/bot thirds
    features.append(float(np.mean(v[:third, :])))
    features.append(float(np.mean(v[third:2*third, :])))
    features.append(float(np.mean(v[2*third:, :])))
    # S in top/mid/bot thirds
    features.append(float(np.mean(s[:third, :])))
    features.append(float(np.mean(s[third:2*third, :])))
    features.append(float(np.mean(s[2*third:, :])))
    # H in center region
    features.append(float(np.mean(h[16:48, 16:48])))
    # Edge density in top vs bottom
    features.append(float(np.mean(edges[:third, :] > 0)))
    features.append(float(np.mean(edges[2*third:, :] > 0)))

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


def find_best_split(X, y, feature_subset=None):
    n, d = X.shape
    best_gain = -1
    best_feat = 0
    best_thresh = 0.0
    parent_gini = gini(y)

    if feature_subset is None:
        feature_subset = range(d)

    for f in feature_subset:
        vals = np.unique(X[:, f])
        if len(vals) <= 1:
            continue
        # Try percentile-based thresholds for speed
        thresholds = np.percentile(X[:, f], np.arange(5, 100, 5))
        thresholds = np.unique(thresholds)
        for t in thresholds:
            left_mask = X[:, f] <= t
            right_mask = ~left_mask
            nl, nr = np.sum(left_mask), np.sum(right_mask)
            if nl < 3 or nr < 3:
                continue
            gain = parent_gini - (nl * gini(y[left_mask]) + nr * gini(y[right_mask])) / n
            if gain > best_gain:
                best_gain = gain
                best_feat = f
                best_thresh = t

    return best_feat, best_thresh, best_gain


class Node:
    def __init__(self):
        self.feat = None
        self.thresh = None
        self.left = None
        self.right = None
        self.label = None
        self.counts = None


def build_tree(X, y, depth=0, max_depth=18, min_samples=5):
    node = Node()
    node.counts = np.bincount(y, minlength=10)

    if depth >= max_depth or len(y) < min_samples or gini(y) < 0.05:
        node.label = int(np.argmax(node.counts))
        return node

    # Use random feature subsets at deeper levels for diversity
    n_features = X.shape[1]
    if depth > 8:
        feature_subset = np.random.choice(n_features, min(n_features, 30), replace=False)
    else:
        feature_subset = None

    feat, thresh, gain = find_best_split(X, y, feature_subset)
    if gain <= 0.001:
        node.label = int(np.argmax(node.counts))
        return node

    node.feat = feat
    node.thresh = round(float(thresh), 4)

    left_mask = X[:, feat] <= thresh
    right_mask = ~left_mask

    node.left = build_tree(X[left_mask], y[left_mask], depth + 1, max_depth, min_samples)
    node.right = build_tree(X[right_mask], y[right_mask], depth + 1, max_depth, min_samples)

    return node


def tree_to_code(node, indent=1):
    """Convert decision tree to Python if/else code."""
    pad = "    " * indent
    if node.label is not None:
        return f'{pad}return "{CLASSES[node.label]}"\n'

    fname = FEATURE_NAMES[node.feat] if node.feat < len(FEATURE_NAMES) else f"f[{node.feat}]"
    code = f'{pad}if f[{node.feat}] <= {node.thresh}:  # {fname}\n'
    code += tree_to_code(node.left, indent + 1)
    code += f'{pad}else:\n'
    code += tree_to_code(node.right, indent + 1)
    return code


def count_nodes(node):
    if node.label is not None:
        return 1
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def tree_accuracy(node, X, y):
    correct = 0
    for i in range(len(y)):
        pred = predict_tree(node, X[i])
        if pred == y[i]:
            correct += 1
    return correct / len(y)


def predict_tree(node, x):
    if node.label is not None:
        return node.label
    if x[node.feat] <= node.thresh:
        return predict_tree(node.left, x)
    else:
        return predict_tree(node.right, x)


def generate_predict_py(tree_code):
    """Generate the full predict.py with embedded decision tree."""
    return f'''"""The entire classifier. This file gets rewritten by the HL loop.
Interface contract: predict(image: np.ndarray) -> str (class label)

CONSTRAINT: No stored training data. No templates, no saved histograms,
no nearest-neighbor lookup against training images. The code itself must
encode visual knowledge as programs and thresholds, not memorized instances.

Approach: Decision tree with {len(FEATURE_NAMES)} visual features including spatial grid.
The tree structure encodes conjunctive feature interactions that
Gaussian Naive Bayes fundamentally cannot capture."""

import cv2
import numpy as np


CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]


def predict(image: np.ndarray) -> str:
    """Classify a 64x64 BGR image using a decision tree."""
    f = _extract_features(image)
{tree_code}

{_generate_extract_features_code()}
'''


def _generate_extract_features_code():
    """Return the _extract_features function code."""
    return '''
def _extract_features(image):
    """Extract features from a 64x64 BGR image."""
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
    padded = np.pad(gray, 1, mode=\'reflect\')
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

    # Spatial grid features (2x2 quadrants)
    H2 = 32
    W2 = 32
    for qi, (r0, c0) in enumerate([(0, 0), (0, W2), (H2, 0), (H2, W2)]):
        r1, c1 = r0 + H2, c0 + W2
        features.append(float(np.mean(h[r0:r1, c0:c1])))
        features.append(float(np.mean(s[r0:r1, c0:c1])))
        features.append(float(np.mean(v[r0:r1, c0:c1])))
        features.append(float(np.mean(edges[r0:r1, c0:c1] > 0)))

    # Thirds features
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

    return features
'''


def main():
    print("Loading training data...")
    X, y = load_data()
    print(f"Loaded {len(X)} samples with {X.shape[1]} features")

    print(f"\nBuilding decision tree (max_depth=18, min_samples=5)...")
    np.random.seed(42)
    tree = build_tree(X, y, max_depth=18, min_samples=5)

    nodes = count_nodes(tree)
    acc = tree_accuracy(tree, X, y)
    print(f"Tree has {nodes} nodes, train accuracy: {acc:.1%}")

    # Also try a forest of 3 trees with different seeds and combine
    print("\nBuilding forest of 5 trees...")
    trees = [tree]
    for seed in [7, 13, 23, 37]:
        np.random.seed(seed)
        t = build_tree(X, y, max_depth=16, min_samples=5)
        trees.append(t)
        ta = tree_accuracy(t, X, y)
        print(f"  Tree {len(trees)}: {count_nodes(t)} nodes, {ta:.1%}")

    # Forest accuracy
    correct = 0
    for i in range(len(y)):
        votes = Counter()
        for t in trees:
            pred = predict_tree(t, X[i])
            votes[pred] += 1
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    print(f"Forest accuracy: {correct/len(y):.1%}")

    # Generate single-tree predict.py
    tree_code = tree_to_code(tree)
    predict_py = generate_predict_py(tree_code)

    out_path = Path(__file__).parent / "predict.py"
    with open(out_path, "w") as f:
        f.write(predict_py)
    print(f"\nWrote predict.py ({len(predict_py)} bytes, {nodes} decision nodes)")

    # Save tree stats
    stats = {
        "nodes": nodes,
        "train_accuracy": acc,
        "n_features": X.shape[1],
        "n_samples": len(X),
        "feature_names": FEATURE_NAMES[:X.shape[1]],
    }
    with open(Path(__file__).parent / "tree_stats.json", "w") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    main()
