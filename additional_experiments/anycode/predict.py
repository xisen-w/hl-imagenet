"""The entire classifier. This file gets rewritten by the HL loop.
Interface contract: predict(image: np.ndarray) -> str (class label)

CONSTRAINT: No stored training data. No templates, no saved histograms,
no nearest-neighbor lookup against training images. The code itself must
encode visual knowledge as programs and thresholds, not memorized instances.

The test: if you delete the training data, this file must still work.

Approach: Gaussian Naive Bayes with 46 visual features and class priors.
Each class has characteristic means and stds. Classification uses
weighted log-likelihood scoring with std floor regularization.
Additional hard rules and confusion resolution for difficult pairs."""

import cv2
import numpy as np


CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]

# 46 features total (0-43 original + 44: hue_in_yellow, 45: warm_uniform)
CLASS_MEANS = {
    "golden_retriever": [90.53, 33.90, 0.035, 0.206, 0.050, 0.063, 0.109, 95.75, 0.146, 0.064, 5976.0, 75.26, 54.31, 23.31, 0.619, 0.229, 0.865, 0.266, 0.161, 1.011, 0.237, 5.90, 1.458, 0.345, 0.144, 0.327, 69.22, 138.94, 1.132, 3.70, 0.197, 0.033,
                         0.1615, 0.2139, 0.9833, 0.3292, 0.281, 0.0252, 0.2721, 34.06, 0.506, 1.575, 1.1045, 1.556, 0.2259, 0.3418],
    "mushroom": [124.08, 40.27, 0.016, 0.192, 0.153, 0.208, 0.262, 122.58, 0.079, 0.141, 10878.0, 92.83, 55.87, 24.74, 0.617, 0.127, 0.875, 0.283, 0.141, 0.919, 0.277, 23.09, 1.843, 0.206, 0.096, 0.326, 96.22, 122.55, 1.141, 21.22, 0.453, 0.063,
                 0.1228, 0.143, 0.9124, 0.2689, 0.1588, 0.0363, 0.167, 43.61, 0.5526, 1.642, 1.0226, 2.129, 0.3554, 0.2315],
    "teapot": [88.79, 28.42, 0.036, 0.171, 0.067, 0.053, 0.154, 93.14, 0.165, 0.129, 5928.6, 72.98, 55.51, 30.31, 0.667, 0.257, 0.764, 0.229, 0.145, 0.867, 0.228, 5.20, 1.461, 0.219, 0.164, 0.288, 67.67, 120.96, 1.168, 3.56, 0.303, 0.041,
               0.2709, 0.354, 1.1944, 0.4229, 0.2938, 0.0306, 0.3544, 44.12, 0.5706, 1.688, 1.2745, 1.869, 0.2920, 0.2193],
    "school_bus": [105.85, 28.07, 0.097, 0.186, 0.125, 0.065, 0.212, 124.57, 0.141, 0.141, 12170.4, 116.56, 64.80, 36.51, 0.579, 0.198, 0.733, 0.294, 0.093, 0.721, 0.170, 26.50, 1.423, 0.175, 0.129, 0.320, 112.52, 132.31, 1.091, -8.32, 0.355, 0.086,
                   0.1471, 0.1951, 1.0182, 0.2661, 0.2272, 0.0552, 0.2729, 29.90, 0.6408, 1.990, 1.1258, 2.417, 0.3624, 0.2534],
    "banana": [143.70, 67.42, 0.035, 0.255, 0.300, 0.062, 0.407, 158.67, 0.104, 0.086, 4842.3, 68.43, 53.28, 22.46, 0.622, 0.147, 0.885, 0.467, 0.144, 0.988, 0.412, 11.64, 2.783, 0.165, 0.065, 0.270, 63.07, 149.35, 1.218, 7.56, 0.228, 0.254,
               0.2818, 0.3643, 1.1563, 0.1402, 0.1764, 0.0286, 0.171, 31.32, 0.5386, 2.127, 1.1826, 1.598, 0.5563, 0.4468],
    "orange": [170.78, 99.89, 0.036, 0.490, 0.138, 0.058, 0.580, 195.91, 0.076, 0.095, 3562.1, 59.28, 50.00, 24.42, 0.660, 0.103, 0.902, 0.365, 0.314, 0.896, 0.527, 5.08, 5.155, 0.097, 0.047, 0.269, 54.54, 170.56, 1.518, 8.91, 0.212, 0.120,
              0.289, 0.3938, 1.1888, 0.0773, 0.1227, 0.0378, 0.1306, 42.41, 0.5648, 1.802, 1.2034, 1.657, 0.2985, 0.5028],
    "brown_bear": [85.90, 20.26, 0.051, 0.111, 0.082, 0.133, 0.083, 93.62, 0.119, 0.112, 9529.6, 87.53, 56.49, 24.80, 0.602, 0.192, 0.789, 0.251, 0.081, 0.924, 0.182, 14.40, 1.285, 0.276, 0.157, 0.340, 88.09, 111.40, 1.036, -18.21, 0.322, 0.039,
                   0.1048, 0.126, 0.899, 0.3404, 0.2362, 0.0324, 0.262, 30.70, 0.5483, 1.542, 1.0245, 1.923, 0.3205, 0.1975],
    "king_penguin": [61.53, 4.27, 0.085, 0.037, 0.059, 0.059, 0.061, 63.10, 0.196, 0.099, 6972.7, 71.85, 56.21, 28.33, 0.608, 0.299, 0.616, 0.127, 0.032, 1.104, 0.223, -3.15, 1.076, 0.123, 0.255, 0.274, 68.78, 117.37, 0.992, 0.36, 0.249, 0.030,
                     0.2135, 0.2792, 1.1744, 0.6181, 0.3281, 0.0357, 0.489, 31.70, 0.4436, 1.841, 1.061, 2.052, 0.3344, 0.0904],
    "jellyfish": [165.05, -72.19, 0.559, 0.039, 0.019, 0.053, 0.528, 149.65, 0.048, 0.154, 3167.9, 43.94, 42.69, 23.60, 0.751, 0.077, 0.190, 0.046, 0.048, 0.983, 0.462, 15.86, 0.694, 0.047, 0.051, 0.254, 32.39, 133.98, 0.956, 27.81, 0.327, 0.012,
                  0.4423, 0.5556, 1.3387, 0.2, 0.1046, 0.0235, 0.1115, 42.65, 0.5281, 1.814, 1.6388, 1.659, 0.0662, 0.0503],
    "sports_car": [90.52, 20.08, 0.084, 0.073, 0.065, 0.072, 0.181, 103.13, 0.145, 0.177, 11679.7, 114.57, 63.86, 45.85, 0.611, 0.216, 0.519, 0.118, 0.107, 0.620, 0.186, 19.97, 1.350, 0.100, 0.173, 0.305, 87.03, 116.39, 1.189, 0.63, 0.412, 0.039,
                   0.1706, 0.23, 1.0978, 0.4085, 0.2406, 0.0522, 0.3732, 34.40, 0.6879, 2.391, 1.1454, 2.47, 0.2205, 0.1006],
}

CLASS_STDS = {
    "golden_retriever": [40.44, 29.04, 0.092, 0.216, 0.089, 0.117, 0.145, 42.56, 0.155, 0.081, 4390.5, 20.90, 13.20, 16.74, 0.127, 0.183, 0.219, 0.215, 0.167, 0.221, 0.177, 39.02, 0.585, 0.203, 0.154, 0.034, 31.28, 27.70, 0.160, 35.66, 0.219, 0.066,
                         0.09, 0.1356, 0.1781, 0.2772, 0.1933, 0.0251, 0.2413, 24.82, 0.1057, 0.568, 0.1677, 0.779, 0.2225, 0.2383],
    "mushroom": [47.96, 28.65, 0.040, 0.206, 0.168, 0.227, 0.215, 52.59, 0.091, 0.134, 7196.5, 26.74, 11.48, 17.11, 0.111, 0.126, 0.210, 0.218, 0.167, 0.202, 0.226, 34.93, 1.061, 0.158, 0.120, 0.047, 38.81, 30.81, 0.265, 31.00, 0.247, 0.107,
                 0.1166, 0.1546, 0.2082, 0.2809, 0.1353, 0.0275, 0.1978, 31.13, 0.1068, 0.577, 0.1567, 0.675, 0.2380, 0.2028],
    "teapot": [46.16, 30.38, 0.088, 0.200, 0.117, 0.119, 0.173, 51.34, 0.187, 0.162, 4350.0, 23.20, 15.12, 21.52, 0.130, 0.216, 0.281, 0.243, 0.191, 0.235, 0.180, 39.24, 0.666, 0.208, 0.169, 0.065, 33.90, 38.32, 0.294, 45.87, 0.287, 0.089,
               0.1363, 0.1641, 0.2518, 0.3202, 0.2197, 0.035, 0.2843, 35.97, 0.1028, 0.693, 0.3444, 0.843, 0.2576, 0.2344],
    "school_bus": [37.18, 27.97, 0.124, 0.132, 0.109, 0.087, 0.151, 39.36, 0.129, 0.116, 5603.2, 28.00, 11.82, 11.74, 0.120, 0.152, 0.224, 0.159, 0.087, 0.213, 0.128, 43.82, 0.623, 0.110, 0.101, 0.043, 29.09, 29.35, 0.148, 29.48, 0.241, 0.095,
                   0.0979, 0.121, 0.1705, 0.2003, 0.1539, 0.0337, 0.1948, 21.61, 0.1084, 1.188, 0.1955, 0.592, 0.1870, 0.1468],
    "banana": [52.71, 43.37, 0.105, 0.235, 0.222, 0.159, 0.259, 52.96, 0.165, 0.149, 4681.1, 29.35, 13.22, 17.94, 0.144, 0.195, 0.196, 0.243, 0.173, 0.422, 0.236, 36.83, 2.989, 0.149, 0.123, 0.070, 32.34, 34.27, 0.284, 31.74, 0.248, 0.198,
               0.1643, 0.206, 0.3052, 0.2172, 0.208, 0.0284, 0.2293, 25.24, 0.1606, 1.169, 0.2898, 0.793, 0.2856, 0.2404],
    "orange": [53.24, 58.62, 0.101, 0.273, 0.160, 0.126, 0.273, 48.54, 0.137, 0.159, 3675.0, 22.28, 13.87, 18.80, 0.130, 0.157, 0.169, 0.262, 0.245, 0.215, 0.231, 38.92, 5.965, 0.118, 0.103, 0.068, 23.94, 38.84, 0.425, 33.25, 0.287, 0.156,
              0.1516, 0.1883, 0.3081, 0.177, 0.1674, 0.0472, 0.196, 37.32, 0.1162, 0.800, 0.3329, 0.744, 0.2506, 0.2825],
    "brown_bear": [33.62, 23.45, 0.138, 0.132, 0.121, 0.199, 0.094, 37.31, 0.115, 0.110, 5744.6, 20.69, 13.51, 16.32, 0.120, 0.151, 0.297, 0.229, 0.101, 0.195, 0.150, 41.56, 0.338, 0.208, 0.137, 0.044, 35.17, 25.39, 0.135, 29.54, 0.226, 0.081,
                   0.0704, 0.1104, 0.1763, 0.2672, 0.1579, 0.0301, 0.2147, 26.78, 0.1012, 0.565, 0.1176, 0.682, 0.2626, 0.1849],
    "king_penguin": [35.04, 24.48, 0.177, 0.068, 0.117, 0.135, 0.101, 36.74, 0.187, 0.108, 5901.5, 26.91, 14.05, 15.62, 0.151, 0.212, 0.352, 0.158, 0.074, 0.369, 0.167, 37.74, 0.269, 0.143, 0.196, 0.073, 39.33, 27.65, 0.130, 36.75, 0.215, 0.057,
                     0.1577, 0.2029, 0.3533, 0.2721, 0.2122, 0.0354, 0.2736, 25.79, 0.1437, 0.902, 0.2736, 0.798, 0.2842, 0.1204],
    "jellyfish": [62.03, 77.53, 0.372, 0.093, 0.062, 0.154, 0.345, 66.00, 0.106, 0.249, 3711.7, 25.26, 18.70, 18.22, 0.138, 0.135, 0.292, 0.103, 0.110, 0.433, 0.288, 34.97, 0.849, 0.115, 0.114, 0.086, 43.71, 43.30, 1.420, 34.18, 0.375, 0.044,
                  0.2015, 0.2228, 0.3798, 0.2665, 0.1614, 0.0349, 0.1771, 37.60, 0.1416, 0.840, 0.6201, 0.827, 0.1637, 0.1095],
    "sports_car": [40.80, 28.56, 0.119, 0.115, 0.109, 0.098, 0.155, 49.59, 0.129, 0.139, 5136.8, 25.39, 12.52, 19.15, 0.111, 0.162, 0.295, 0.151, 0.132, 0.158, 0.135, 46.52, 0.573, 0.116, 0.126, 0.045, 45.77, 36.29, 0.364, 36.53, 0.284, 0.084,
                   0.1086, 0.1318, 0.193, 0.265, 0.1625, 0.0339, 0.2289, 28.42, 0.0909, 1.281, 0.2283, 0.672, 0.2247, 0.1374],
}

# Feature weights - carefully tuned
FEATURE_WEIGHTS = [
    1.0,   # 0: avg_s
    1.5,   # 1: r_minus_b
    2.5,   # 2: blue_ratio (jellyfish)
    1.5,   # 3: orange_hue
    1.8,   # 4: yellow_ratio (banana)
    1.8,   # 5: green_ratio (mushroom)
    1.0,   # 6: high_sat
    0.8,   # 7: sat_center
    0.6,   # 8: white_ratio
    0.6,   # 9: black_ratio
    0.8,   # 10: texture_var
    1.2,   # 11: horiz_edges
    0.8,   # 12: contrast
    1.0,   # 13: hue_std
    0.5,   # 14: symmetry
    0.6,   # 15: low_sat_high_val
    1.2,   # 16: warm_cool
    1.0,   # 17: hue_15_30
    1.2,   # 18: very_orange
    1.0,   # 19: vert_edge_ratio
    0.5,   # 20: circularity
    0.2,   # 21: top_minus_bot (weak)
    1.2,   # 22: rb_ratio
    1.5,   # 23: warm_brown
    1.5,   # 24: medium_gray
    0.6,   # 25: edge_density_center
    0.8,   # 26: warm_texture
    1.2,   # 27: warm_brightness
    1.5,   # 28: rg_ratio
    0.3,   # 29: center_vs_periph
    0.8,   # 30: dark_bottom
    2.0,   # 31: yellow_band
    # NEW FEATURES 32-43
    1.0,   # 32: smooth_frac (reduced from 2.0 to avoid cross-class pollution)
    1.0,   # 33: lbp_uniformity (reduced from 2.0)
    1.8,   # 34: gradient_uniformity
    1.5,   # 35: center_sat_low
    0.8,   # 36: high_val_low_sat
    1.0,   # 37: v_bimodal
    1.2,   # 38: achromatic
    0.5,   # 39: center_obj_diff
    2.2,   # 40: horiz_line_score (increased - very discriminative)
    1.0,   # 41: aspect_main_contour
    1.5,   # 42: edge_in_center_ratio
    1.0,   # 43: color_entropy
    # DISCRIMINATIVE FEATURES 44-45
    2.0,   # 44: hue_in_yellow (banana 0.556 vs orange 0.299)
    1.5,   # 45: warm_uniform (golden 0.342 vs bear 0.198)
]

# Class bias - penalize greedy classes
CLASS_BIAS = {
    "king_penguin": -3.5,
    "orange": -1.5,
    "brown_bear": -1.0,
}

# Minimum std floor per feature
STD_FLOOR = [
    35.0, 24.0, 0.060, 0.090, 0.080, 0.090, 0.094, 37.0, 0.091, 0.081,
    3700.0, 20.7, 11.5, 12.0, 0.111, 0.126, 0.170, 0.103, 0.074, 0.158,
    0.128, 35.0, 0.270, 0.110, 0.101, 0.034, 24.0, 25.4, 0.130, 29.5,
    0.215, 0.044,
    # New features 32-43 std floors
    0.070, 0.110, 0.170, 0.177, 0.135, 0.025, 0.170, 21.6, 0.091, 0.565,
    0.118, 0.592,
    # Features 44-45 std floors
    0.164, 0.110,
]


def predict(image: np.ndarray) -> str:
    """Classify a 64x64 BGR image using GNB + hard rules + confusion resolution."""
    features = _extract_features(image)

    # Shorthand for commonly used features
    blue_ratio = features[2]
    r_minus_b = features[1]
    orange_hue = features[3]
    sat_center = features[7]
    high_sat = features[6]
    yellow_band = features[31]
    smooth_frac = features[32]
    lbp_uni = features[33]
    achromatic = features[38]
    horiz_line = features[40]
    gradient_uni = features[34]
    avg_s = features[0]
    green_ratio = features[5]
    warm_brown = features[23]
    hue_in_yellow = features[44]
    warm_uniform = features[45]

    # ============================================================
    # HARD OVERRIDES for very strong signals
    # ============================================================

    # Jellyfish: extremely blue + smooth
    if blue_ratio > 0.35 and r_minus_b < -40:
        return "jellyfish"

    # Orange: extremely high orange + high saturation
    if orange_hue > 0.45 and sat_center > 160 and high_sat > 0.45:
        return "orange"

    # Banana: very high yellow band
    if yellow_band > 0.30 and r_minus_b > 30:
        return "banana"

    # Sports car: very high horizontal line score + high texture + wide aspect
    if horiz_line > 0.75 and features[10] > 10000 and features[41] > 2.0:
        return "sports_car"

    # School bus: strong yellow + high horizontal lines + yellow hue
    if yellow_band > 0.10 and horiz_line > 0.65 and orange_hue < 0.15:
        return "school_bus"

    # King penguin: extremely achromatic + low saturation center + vertical bias
    if achromatic > 0.70 and features[35] > 0.80 and horiz_line < 0.50:
        return "king_penguin"

    # ============================================================
    # GNB SCORING
    # ============================================================
    scores = {}
    for cls in CLASSES:
        scores[cls] = _score_class(features, cls)

    best_class = max(scores, key=scores.get)
    best_score = scores[best_class]

    # Sort by score
    sorted_classes = sorted(scores.items(), key=lambda x: -x[1])
    second_class = sorted_classes[1][0]
    margin = best_score - sorted_classes[1][1]

    # ============================================================
    # POST-GNB CORRECTIONS
    # ============================================================

    # TEAPOT RESCUE: teapot is systematically under-predicted
    teapot_rank = next(i for i, (c, _) in enumerate(sorted_classes) if c == "teapot")
    if teapot_rank <= 3 and teapot_rank > 0:
        teapot_evidence = 0.0
        # Positive teapot signals
        if smooth_frac > 0.18:
            teapot_evidence += 1.5
        if lbp_uni > 0.25:
            teapot_evidence += 1.5
        if gradient_uni > 1.05:
            teapot_evidence += 1.5
        if features[14] > 0.63:  # symmetry (teapot mean 0.667)
            teapot_evidence += 2.0
        if features[42] > 1.15:  # edge_in_center_ratio
            teapot_evidence += 1.0
        if features[36] > 0.25:  # high_val_low_sat (metallic)
            teapot_evidence += 0.5
        if features[13] > 26:  # hue_std (teapot mean 30.3, varied colors)
            teapot_evidence += 1.0
        # Negative signals (not teapot)
        if warm_brown > 0.35:
            teapot_evidence -= 3.0
        if green_ratio > 0.15:
            teapot_evidence -= 3.0
        if features[4] > 0.18:  # yellow
            teapot_evidence -= 3.0
        if orange_hue > 0.20:
            teapot_evidence -= 3.0
        if high_sat > 0.40:
            teapot_evidence -= 2.0
        if features[18] > 0.12:  # very_orange
            teapot_evidence -= 2.0
        if features[10] > 11000:  # high texture
            teapot_evidence -= 1.5
        if avg_s > 130:  # high overall saturation = likely orange/banana
            teapot_evidence -= 2.0
        if hue_in_yellow > 0.50:  # banana/school_bus signal
            teapot_evidence -= 2.0
        if warm_uniform > 0.35:  # golden retriever signal
            teapot_evidence -= 1.5

        # Special handling for king_penguin confusion
        if best_class == "king_penguin":
            if features[14] > 0.66:
                teapot_evidence += 1.5
            if horiz_line > 0.55:
                teapot_evidence += 1.5
            if features[42] > 1.20:
                teapot_evidence += 1.0
            # True penguins: low horiz_line, very achromatic
            if horiz_line < 0.44:
                teapot_evidence -= 3.0
            if achromatic > 0.60:
                teapot_evidence -= 2.5
            if features[35] > 0.65:
                teapot_evidence -= 2.0
            if features[9] > 0.08:  # black_ratio - penguins have black
                teapot_evidence -= 1.5

        # Special handling for golden_retriever confusion
        if best_class == "golden_retriever":
            if smooth_frac > 0.20:
                teapot_evidence += 1.5
            if features[14] > 0.65:
                teapot_evidence += 1.0
            if warm_brown > 0.28:
                teapot_evidence -= 2.5
            if warm_uniform > 0.30:
                teapot_evidence -= 2.0

        if teapot_evidence > 3.5:
            scores["teapot"] += teapot_evidence * 1.5
            best_class = max(scores, key=scores.get)
            best_score = scores[best_class]
            sorted_classes = sorted(scores.items(), key=lambda x: -x[1])
            second_class = sorted_classes[1][0]
            margin = best_score - sorted_classes[1][1]

    # ============================================================
    # CONFUSION RESOLUTION at margin < 6
    # ============================================================
    if margin < 6.0:
        pair = frozenset([best_class, second_class])

        # golden_retriever vs teapot
        if pair == frozenset(["golden_retriever", "teapot"]):
            if smooth_frac > 0.22 and lbp_uni > 0.28 and warm_brown < 0.30:
                return "teapot"
            if warm_brown > 0.35:
                return "golden_retriever"
            if smooth_frac < 0.13:
                return "golden_retriever"
            if features[14] > 0.70 and gradient_uni > 1.1:
                return "teapot"
            return best_class

        # golden_retriever vs brown_bear
        if pair == frozenset(["golden_retriever", "brown_bear"]):
            warm_brightness = features[27]
            # warm_uniform is key: golden=0.342, bear=0.198
            if warm_uniform > 0.32:
                return "golden_retriever"
            if warm_uniform < 0.13:
                return "brown_bear"
            if warm_brightness > 135:
                return "golden_retriever"
            if warm_brightness < 108:
                return "brown_bear"
            if smooth_frac < 0.09:
                return "brown_bear"
            if smooth_frac > 0.18:
                return "golden_retriever"
            if features[25] > 0.36:
                return "brown_bear"
            return best_class

        # teapot vs king_penguin
        if pair == frozenset(["teapot", "king_penguin"]):
            center_sat_low = features[35]
            if center_sat_low > 0.70 and horiz_line < 0.45:
                return "king_penguin"
            if features[14] > 0.65 and smooth_frac > 0.22:
                return "teapot"
            if features[13] > 28:  # hue_std
                return "teapot"
            if horiz_line > 0.55:
                return "teapot"
            if features[42] > 1.25:  # edge in center
                return "teapot"
            return best_class

        # teapot vs sports_car
        if pair == frozenset(["teapot", "sports_car"]):
            if horiz_line > 0.68:
                return "sports_car"
            if features[41] > 2.2:
                return "sports_car"
            if smooth_frac > 0.25 and features[14] > 0.65:
                return "teapot"
            if features[10] > 9000:
                return "sports_car"
            return best_class

        # banana vs orange
        if pair == frozenset(["banana", "orange"]):
            rg_ratio = features[28]
            yellow_ratio = features[4]
            # Use hue_in_yellow as primary separator (banana=0.556, orange=0.299)
            if hue_in_yellow > 0.45:
                return "banana"
            if hue_in_yellow < 0.20:
                return "orange"
            # Orange: extreme R/G with very orange and low yellow
            if rg_ratio > 1.50 and features[18] > 0.25 and yellow_ratio < 0.08:
                return "orange"
            # Banana: has yellow band or yellow ratio
            if yellow_band > 0.12:
                return "banana"
            if yellow_ratio > 0.15 and rg_ratio < 1.45:
                return "banana"
            if features[41] > 2.3:  # elongated
                return "banana"
            # Orange: high R/G with no yellow at all
            if rg_ratio > 1.40 and yellow_ratio < 0.04 and yellow_band < 0.04:
                return "orange"
            if rg_ratio < 1.15:
                return "banana"
            return best_class

        # school_bus vs sports_car
        if pair == frozenset(["school_bus", "sports_car"]):
            if yellow_band > 0.05 and features[4] > 0.06:
                return "school_bus"
            if achromatic > 0.40 and yellow_band < 0.03:
                return "sports_car"
            if features[13] > 48:  # high hue diversity
                return "sports_car"
            if achromatic < 0.25 and features[13] < 40:
                return "school_bus"
            if features[43] > 2.7 and achromatic > 0.35:
                return "sports_car"
            return best_class

        # mushroom vs brown_bear
        if pair == frozenset(["mushroom", "brown_bear"]):
            # center_vs_periph is the best separator
            if features[29] > 15:
                return "mushroom"
            if features[29] < -5:
                return "brown_bear"
            if green_ratio > 0.12 and features[29] > 0:
                return "mushroom"
            if warm_brown > 0.20 and features[29] < 5:
                return "brown_bear"
            if lbp_uni < 0.10:
                return "brown_bear"
            return best_class

        # king_penguin vs sports_car
        if pair == frozenset(["king_penguin", "sports_car"]):
            if horiz_line < 0.48:
                return "king_penguin"
            if horiz_line > 0.68:
                return "sports_car"
            if features[35] > 0.55:
                return "king_penguin"
            return best_class

        # golden_retriever vs king_penguin
        if pair == frozenset(["golden_retriever", "king_penguin"]):
            if features[16] > 0.75:
                return "golden_retriever"
            if achromatic > 0.50 and features[35] > 0.50:
                return "king_penguin"
            if warm_brown > 0.25:
                return "golden_retriever"
            return best_class

        # mushroom vs golden_retriever
        if pair == frozenset(["mushroom", "golden_retriever"]):
            if green_ratio > 0.10:
                return "mushroom"
            if features[29] > 15:
                return "mushroom"
            if warm_brown > 0.30:
                return "golden_retriever"
            return best_class

        # brown_bear vs king_penguin
        if pair == frozenset(["brown_bear", "king_penguin"]):
            if achromatic > 0.45 and warm_brown < 0.10:
                return "king_penguin"
            if warm_brown > 0.15:
                return "brown_bear"
            if avg_s > 80:
                return "brown_bear"
            return best_class

        # teapot vs mushroom
        if pair == frozenset(["teapot", "mushroom"]):
            if smooth_frac > 0.25 and green_ratio < 0.08:
                return "teapot"
            if green_ratio > 0.12:
                return "mushroom"
            if features[10] > 9000:
                return "mushroom"
            return best_class

        # banana vs mushroom
        if pair == frozenset(["banana", "mushroom"]):
            if yellow_band > 0.10:
                return "banana"
            if features[4] > 0.15:
                return "banana"
            if green_ratio > 0.15:
                return "mushroom"
            if features[29] > 20:
                return "mushroom"
            return best_class

    return best_class


def _score_class(features, cls):
    """Compute weighted log-likelihood with regularized std and class prior."""
    means = CLASS_MEANS[cls]
    stds = CLASS_STDS[cls]

    score = CLASS_BIAS.get(cls, 0.0)
    for i in range(len(features)):
        diff = features[i] - means[i]
        std = max(stds[i], STD_FLOOR[i])
        z = diff / std
        score += FEATURE_WEIGHTS[i] * (-0.5 * z * z - np.log(std))

    return score


def _extract_features(image):
    """Extract 46 features from a 64x64 BGR image."""
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
    # 23: warm_brown (H 10-25, S 40-150)
    features.append(float(np.mean((h >= 10) & (h <= 25) & (s >= 40) & (s <= 150))))
    # 24: medium_gray (gray 80-160, S < 60)
    features.append(float(np.mean((gray >= 80) & (gray <= 160) & (s < 60))))
    # 25: edge_density_center
    edges = cv2.Canny(gray, 30, 100)
    features.append(float(np.mean(edges[16:48, 16:48] > 0)))
    # 26: warm_texture (Laplacian std in warm regions)
    warm_region = (h < 30) & (s > 30) & (v > 50)
    if np.sum(warm_region) > 100:
        features.append(float(np.std(lap[warm_region])))
    else:
        features.append(0.0)
    # 27: warm_brightness (mean V in warm regions)
    if np.sum(warm_region) > 100:
        features.append(float(np.mean(v[warm_region])))
    else:
        features.append(128.0)
    # 28: rg_ratio (R/G mean ratio)
    features.append(avg_r / max(avg_g, 1.0))
    # 29: center_vs_periph
    center_gray = float(np.mean(gray[16:48, 16:48]))
    periph_gray = (float(np.mean(gray[:16, :])) + float(np.mean(gray[48:, :])) +
                   float(np.mean(gray[:, :16])) + float(np.mean(gray[:, 48:]))) / 4.0
    features.append(center_gray - periph_gray)
    # 30: dark_bottom
    features.append(float(np.mean(v[48:, :] < 80)))
    # 31: yellow_band (H 20-35, S>80, V>120)
    features.append(float(np.mean((h >= 20) & (h <= 35) & (s > 80) & (v > 120))))

    # NEW FEATURES 32-43

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

    # 44: hue_in_yellow (fraction of saturated pixels with hue 18-38)
    # banana=0.556, orange=0.299 - strong separator
    if len(sat_pixels) > 100:
        features.append(float(np.sum((sat_pixels >= 18) & (sat_pixels <= 38))) / len(sat_pixels))
    else:
        features.append(0.0)

    # 45: warm_uniform (fraction of pixels that are bright + warm + saturated)
    # golden=0.342, bear=0.198 - good separator
    features.append(float(np.mean((h >= 10) & (h <= 30) & (s > 50) & (v > 100))))

    return features
