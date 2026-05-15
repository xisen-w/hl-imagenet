"""Top-level prediction: image → Prediction with proof."""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np

from hlinet.classifier.hierarchy import ClassNode, build_phase1_hierarchy
from hlinet.classifier.scorer import score_node
from hlinet.classifier.tiebreaker import resolve_tie
from hlinet.scene.builder import SceneGraphBuilder
from hlinet.types import FeatureValue, Prediction, SceneGraph

# Force feature/sensor registration on import
import hlinet.sensors  # noqa: F401
import hlinet.features  # noqa: F401


_hierarchy = build_phase1_hierarchy()
_builder = SceneGraphBuilder()

_HIST_BLEND_W = 0.88

_SCORE_CALIBRATION = {
    "school_bus": -0.02,
    "jellyfish": 0.02,
    "king_penguin": 0.01,
    "mushroom": 0.01,
}

_HIST_MEANS = {
    "banana": 1.233, "brown_bear": 1.331, "golden_retriever": 1.320,
    "jellyfish": 0.664, "king_penguin": 1.215, "mushroom": 1.363,
    "orange": 1.043, "school_bus": 1.527, "sports_car": 1.315, "teapot": 1.316,
}


def _blend_hist_scores(
    candidates: list[tuple[str, float, list[str]]],
    image: np.ndarray,
) -> list[tuple[str, float, list[str]]]:
    """Blend signature scores with mean-centered histogram prototype scores."""
    from hlinet.features.compounds.phase2_signatures import _color_hist_scores

    hist_scores = _color_hist_scores(image)
    if not hist_scores:
        return candidates
    w = _HIST_BLEND_W
    return [
        (label, score * w + (hist_scores.get(f"hist_{label}", 0) - _HIST_MEANS.get(label, 1.2) * 0.3) * (1 - w), route)
        for label, score, route in candidates
    ]


def predict(image: np.ndarray) -> Prediction:
    """Classify an image through the symbolic visual algebra pipeline.

    image: BGR numpy array (as loaded by cv2.imread)
    """
    graph = _builder.build(image)
    cache: dict[str, FeatureValue] = {}

    candidates = _score_all_classes_flat(_hierarchy, graph, cache)

    if not candidates:
        return Prediction(
            label="unknown",
            confidence=0.0,
            proof=["no class matched above threshold"],
            feature_activations=cache,
        )

    candidates = _blend_hist_scores(candidates, image)
    candidates = [
        (label, score + _SCORE_CALIBRATION.get(label, 0.0), route)
        for label, score, route in candidates
    ]

    candidates = _potential_field_repulsion(candidates, graph)

    candidates.sort(key=lambda x: x[1], reverse=True)

    candidates = _pairwise_rerank(candidates, graph)

    candidates = _local_verify(candidates, graph)

    best_label, best_score, best_route = candidates[0]
    alternatives = [(label, score) for label, score, _ in candidates[1:5]]

    proof = _generate_proof(best_label, best_route, cache)

    return Prediction(
        label=best_label,
        confidence=best_score,
        alternatives=alternatives,
        proof=proof,
        feature_activations=cache,
        route=best_route,
    )


_SIGNATURE_MAP = {
    "golden_retriever": "phase2_golden_retriever_signature",
    "mushroom": "phase2_mushroom_signature",
    "teapot": "phase2_teapot_signature",
    "school_bus": "phase2_school_bus_signature",
    "banana": "phase2_banana_signature",
    "orange": "phase2_orange_signature",
    "brown_bear": "phase2_brown_bear_signature",
    "king_penguin": "phase2_king_penguin_signature",
    "jellyfish": "phase2_jellyfish_signature",
    "sports_car": "phase2_sports_car_signature",
}

def _score_signatures_direct(
    graph: SceneGraph, cache: dict[str, FeatureValue]
) -> list[tuple[str, float, list[str]]]:
    """Score all classes by evaluating their phase2 signatures directly."""
    from hlinet.registry import registry

    results = []
    for class_name, feat_name in _SIGNATURE_MAP.items():
        try:
            feat = registry.get_feature(feat_name)
            val = feat.evaluate(graph)
            cache[feat_name] = val
            results.append((class_name, val.confidence, ["root", class_name]))
        except (KeyError, Exception):
            results.append((class_name, 0.0, ["root", class_name]))
    return results


def _pairwise_rerank(
    candidates: list[tuple[str, float, list[str]]],
    graph: SceneGraph,
) -> list[tuple[str, float, list[str]]]:
    """Rerank top candidates using targeted pairwise discriminants.

    Uses gap-aware confidence gating: the discriminant must beat a threshold
    that scales with the score margin — bigger gaps need stronger evidence.
    """
    if len(candidates) < 2:
        return candidates

    from hlinet.features.compounds.phase2_signatures import _stats, _sigmoid

    s = _stats(graph)
    candidates = list(candidates)

    top1_label, top1_score, _ = candidates[0]
    top2_label, top2_score, _ = candidates[1]

    _PAIR_BASE = {
        frozenset(["banana", "teapot"]): 0.30,
        frozenset(["banana", "school_bus"]): 0.20,
        frozenset(["king_penguin", "teapot"]): 0.0,
        frozenset(["brown_bear", "school_bus"]): 0.10,
        frozenset(["banana", "orange"]): 0.10,
        frozenset(["king_penguin", "sports_car"]): 0.15,
        frozenset(["golden_retriever", "orange"]): -0.05,
        frozenset(["brown_bear", "golden_retriever"]): 0.10,
        frozenset(["brown_bear", "mushroom"]): 0.10,
        frozenset(["golden_retriever", "sports_car"]): -0.05,
        frozenset(["banana", "golden_retriever"]): -0.05,
        frozenset(["mushroom", "school_bus"]): -0.05,
        frozenset(["school_bus", "sports_car"]): -0.10,
        frozenset(["banana", "mushroom"]): 0.05,
        frozenset(["golden_retriever", "teapot"]): 0.15,
        frozenset(["brown_bear", "king_penguin"]): 0.25,
        frozenset(["jellyfish", "king_penguin"]): 0.0,
        frozenset(["orange", "teapot"]): 0.0,
        frozenset(["brown_bear", "teapot"]): 0.10,
        frozenset(["golden_retriever", "king_penguin"]): 0.10,
        frozenset(["jellyfish", "teapot"]): -0.05,
        frozenset(["mushroom", "king_penguin"]): 0.0,
        frozenset(["orange", "mushroom"]): 0.0,
    }

    margin12 = top1_score - top2_score
    if margin12 <= 0.25:
        pair12 = frozenset([top1_label, top2_label])
        signals = _compute_pair_signals(pair12, s, _sigmoid)
        if signals is not None:
            cls1, sig1, cls2, sig2 = signals
            disc_margin = abs(sig1 - sig2)
            base = _PAIR_BASE.get(pair12, 0.05)
            threshold = base + margin12 * 1.5
            if disc_margin > threshold:
                winner = cls1 if sig1 > sig2 else cls2
                if winner == top2_label:
                    candidates[0], candidates[1] = candidates[1], candidates[0]

    _RANK3_WHITELIST = {
        frozenset(["teapot", "sports_car"]),
        frozenset(["banana", "brown_bear"]),
        frozenset(["banana", "golden_retriever"]),
        frozenset(["school_bus", "mushroom"]),
        frozenset(["golden_retriever", "mushroom"]),
        frozenset(["school_bus", "brown_bear"]),
        frozenset(["golden_retriever", "brown_bear"]),
        frozenset(["school_bus", "sports_car"]),
        frozenset(["teapot", "king_penguin"]),
        frozenset(["banana", "orange"]),
        frozenset(["banana", "mushroom"]),
        frozenset(["golden_retriever", "teapot"]),
        frozenset(["jellyfish", "king_penguin"]),
        frozenset(["brown_bear", "king_penguin"]),
        frozenset(["orange", "teapot"]),
        frozenset(["brown_bear", "teapot"]),
        frozenset(["golden_retriever", "king_penguin"]),
        frozenset(["jellyfish", "teapot"]),
        frozenset(["mushroom", "king_penguin"]),
        frozenset(["orange", "mushroom"]),
    }
    if len(candidates) >= 3:
        top1_label, top1_score, _ = candidates[0]
        top3_label, top3_score, _ = candidates[2]
        margin13 = top1_score - top3_score
        pair13 = frozenset([top1_label, top3_label])
        if margin13 <= 0.15 and pair13 in _RANK3_WHITELIST:
            signals = _compute_pair_signals(pair13, s, _sigmoid)
            if signals is not None:
                cls1, sig1, cls2, sig2 = signals
                disc_margin = abs(sig1 - sig2)
                base = _PAIR_BASE.get(pair13, 0.0)
                threshold = base + margin13 * 2.0
                if disc_margin > threshold:
                    winner = cls1 if sig1 > sig2 else cls2
                    if winner == top3_label:
                        candidates[0], candidates[2] = candidates[2], candidates[0]

    return candidates


_REPULSION_PAIRS = [
    ("banana", "orange", 0.012),
    ("sports_car", "school_bus", 0.012),
    ("mushroom", "banana", 0.010),
    ("teapot", "banana", 0.010),
    ("brown_bear", "mushroom", 0.010),
    ("teapot", "king_penguin", 0.012),
    ("golden_retriever", "banana", 0.008),
    ("golden_retriever", "king_penguin", 0.008),
    ("brown_bear", "king_penguin", 0.008),
]


def _potential_field_repulsion(
    candidates: list[tuple[str, float, list[str]]],
    graph: SceneGraph,
) -> list[tuple[str, float, list[str]]]:
    """Apply potential field: boost winner, penalize loser between confused pairs.

    When two classes both score high (proximity > 0.6), the discriminant winner
    gets a small boost and the loser a small penalty. This spreads their scores
    apart before ranking, making the downstream reranking's job easier.
    """
    from hlinet.features.compounds.phase2_signatures import _stats, _sigmoid
    s = _stats(graph)

    score_map = {label: score for label, score, _ in candidates}
    adjustments = {label: 0.0 for label, _, _ in candidates}

    for cls1, cls2, strength in _REPULSION_PAIRS:
        s1 = score_map.get(cls1, 0)
        s2 = score_map.get(cls2, 0)
        if s1 < 0.25 or s2 < 0.25:
            continue
        proximity = min(s1, s2) / max(max(s1, s2), 0.01)
        if proximity < 0.6:
            continue

        pair = frozenset([cls1, cls2])
        signals = _compute_pair_signals(pair, s, _sigmoid)
        if signals is None:
            continue

        c1, sig1, c2, sig2 = signals
        disc_gap = abs(sig1 - sig2)
        if disc_gap < 1.0:
            continue

        winner = c1 if sig1 > sig2 else c2
        loser = c1 if sig1 < sig2 else c2
        force = strength * proximity * min(disc_gap / 4.0, 1.0)
        adjustments[winner] += force * 0.5
        adjustments[loser] -= force * 0.5

    return [
        (label, score + adjustments.get(label, 0.0), route)
        for label, score, route in candidates
    ]


def _local_verify(
    candidates: list[tuple[str, float, list[str]]],
    graph: SceneGraph,
) -> list[tuple[str, float, list[str]]]:
    """Placeholder for local region verifiers. Currently a no-op at 64x64."""
    return candidates



def _compute_pair_signals(pair, s, _sigmoid):
    if pair == frozenset(["king_penguin", "sports_car"]):
        return ("sports_car",
                _sigmoid(s.get("grad_mean", 0), 1.35, 3) + _sigmoid(s.get("grad_dir_entropy", 1), 0.95, -10)
                + _sigmoid(s.get("lap_var", 0), 8000, 0.0003) + _sigmoid(s.get("warm_aspect", 0), 1.40, 2),
                "king_penguin",
                _sigmoid(s.get("grad_mean", 1), 1.35, -3) + _sigmoid(s.get("grad_dir_entropy", 0), 0.95, 10)
                + _sigmoid(s.get("lap_var", 99999), 8000, -0.0003) + _sigmoid(s.get("warm_aspect", 1), 1.40, -2))

    if pair == frozenset(["banana", "orange"]):
        return ("orange",
                _sigmoid(s.get("hue_red", 0), 0.25, 6) + _sigmoid(s.get("color_std", 0), 0.35, 5)
                + _sigmoid(s.get("bw", 1), 0.25, -5) + _sigmoid(s.get("grad_mean", 1), 0.80, -3)
                + _sigmoid(s.get("hist_orange_minus_banana", 0), 0.0, 3)
                + _sigmoid(s.get("warm_hue_mean", 1), 0.40, -6)
                + _sigmoid(s.get("warm_val_mean", 0), 0.66, 5)
                + _sigmoid(s.get("sat_color_std", 0), 0.25, 5),
                "banana",
                _sigmoid(s.get("hue_red", 1), 0.25, -6) + _sigmoid(s.get("color_std", 1), 0.35, -5)
                + _sigmoid(s.get("bw", 0), 0.25, 5) + _sigmoid(s.get("grad_mean", 0), 0.80, 3)
                + _sigmoid(s.get("hist_orange_minus_banana", 0), 0.0, -3)
                + _sigmoid(s.get("warm_hue_mean", 0), 0.40, 6)
                + _sigmoid(s.get("warm_val_mean", 1), 0.66, -5)
                + _sigmoid(s.get("sat_color_std", 1), 0.25, -5))

    if pair == frozenset(["banana", "golden_retriever"]):
        return ("golden_retriever",
                _sigmoid(s.get("edge", 0), 0.24, 10) + _sigmoid(s.get("sat", 1), 0.45, -5)
                + _sigmoid(s.get("yellow", 1), 0.30, -5) + _sigmoid(s.get("bot_edge", 0), 0.24, 8)
                + _sigmoid(s.get("hist_gr_minus_banana", 0), 0.0, 2)
                + _sigmoid(s.get("warm_hue_median", 1), 18.0, -0.3),
                "banana",
                _sigmoid(s.get("edge", 1), 0.24, -10) + _sigmoid(s.get("sat", 0), 0.45, 5)
                + _sigmoid(s.get("yellow", 0), 0.30, 5) + _sigmoid(s.get("bot_edge", 1), 0.24, -8)
                + _sigmoid(s.get("hist_gr_minus_banana", 0), 0.0, -2)
                + _sigmoid(s.get("warm_hue_median", 0), 18.0, 0.3))

    if pair == frozenset(["mushroom", "golden_retriever"]):
        return ("mushroom",
                _sigmoid(s.get("val", 1), 0.50, -4) + _sigmoid(s.get("sat_br", 0), 0.43, 5)
                + _sigmoid(s.get("lap_var", 0), 8000, 0.0002) + _sigmoid(s.get("hue_yellow", 0), 0.12, 5)
                + _sigmoid(s.get("dct_high", 0), 0.20, 5)
                + _sigmoid(s.get("dct_mid_over_low", 0), 0.40, 4),
                "golden_retriever",
                _sigmoid(s.get("val", 0), 0.50, 4) + _sigmoid(s.get("sat_br", 1), 0.43, -5)
                + _sigmoid(s.get("lap_var", 99999), 8000, -0.0002) + _sigmoid(s.get("hue_yellow", 1), 0.12, -5)
                + _sigmoid(s.get("dct_low", 0), 0.22, 4)
                + _sigmoid(s.get("dct_mid_over_low", 1), 0.40, -4))

    if pair == frozenset(["orange", "golden_retriever"]):
        return ("orange",
                _sigmoid(s.get("sat", 0), 0.55, 5) + _sigmoid(s.get("color_std", 0), 0.30, 5)
                + _sigmoid(s.get("blob_coverage", 0), 0.50, 4) + _sigmoid(s.get("circularity", 0), 0.03, 20),
                "golden_retriever",
                _sigmoid(s.get("radial_warm_diff", 0), 0.15, 4) + _sigmoid(s.get("bot_edge", 0), 0.22, 8)
                + _sigmoid(s.get("warm_br", 0), 0.45, 4) + _sigmoid(s.get("grad_dir_entropy", 0), 0.97, 8))

    if pair == frozenset(["sports_car", "golden_retriever"]):
        return ("sports_car",
                _sigmoid(s.get("grad_dir_entropy", 1), 0.93, -12) + _sigmoid(s.get("lap_var", 0), 9000, 0.0003)
                + _sigmoid(s.get("bw", 0), 0.55, 4) + _sigmoid(s.get("sky_ratio", 0), 0.20, 4),
                "golden_retriever",
                _sigmoid(s.get("warm", 0), 0.40, 5) + _sigmoid(s.get("radial_warm_diff", 0), 0.15, 4)
                + _sigmoid(s.get("hue_red", 0), 0.25, 4) + _sigmoid(s.get("warm_br", 0), 0.45, 4))

    if pair == frozenset(["banana", "school_bus"]):
        return ("banana",
                _sigmoid(s.get("val", 0), 0.65, 4) + _sigmoid(s.get("blue_purple", 1), 0.04, -5)
                + _sigmoid(s.get("warm_band_top", 0), 0.50, 4) + _sigmoid(s.get("lap_var", 99999), 9000, -0.0002),
                "school_bus",
                _sigmoid(s.get("val", 1), 0.65, -4) + _sigmoid(s.get("blue_purple", 0), 0.04, 5)
                + _sigmoid(s.get("warm_band_top", 1), 0.50, -4) + _sigmoid(s.get("lap_var", 0), 9000, 0.0002))

    if pair == frozenset(["brown_bear", "sports_car"]):
        return ("brown_bear",
                _sigmoid(s.get("grad_dir_entropy", 0), 0.96, 10) + _sigmoid(s.get("edge", 0), 0.30, 8)
                + _sigmoid(s.get("green_bl", 0), 0.15, 5) + _sigmoid(s.get("sat_br", 1), 0.32, -5),
                "sports_car",
                _sigmoid(s.get("grad_dir_entropy", 1), 0.96, -10) + _sigmoid(s.get("edge", 1), 0.30, -8)
                + _sigmoid(s.get("green_bl", 1), 0.15, -5) + _sigmoid(s.get("sat_br", 0), 0.32, 5))

    if pair == frozenset(["sports_car", "teapot"]):
        return ("sports_car",
                _sigmoid(s.get("grad_dir_entropy", 1), 0.93, -10) + _sigmoid(s.get("hue_red", 1), 0.40, -4)
                + _sigmoid(s.get("top_uniformity", 0), 0.66, 4) + _sigmoid(s.get("lap_var", 0), 7500, 0.0003),
                "teapot",
                _sigmoid(s.get("grad_dir_entropy", 0), 0.93, 10) + _sigmoid(s.get("hue_red", 0), 0.40, 4)
                + _sigmoid(s.get("top_uniformity", 1), 0.66, -4) + _sigmoid(s.get("lap_var", 99999), 7500, -0.0003))

    if pair == frozenset(["mushroom", "school_bus"]):
        return ("mushroom",
                _sigmoid(s.get("grad_dir_entropy", 0), 0.97, 10) + _sigmoid(s.get("edge_br", 0), 0.33, 8)
                + _sigmoid(s.get("lbp_entropy", 0), 5.32, 8) + _sigmoid(s.get("edge", 0), 0.33, 8),
                "school_bus",
                _sigmoid(s.get("grad_dir_entropy", 1), 0.97, -10) + _sigmoid(s.get("edge_br", 1), 0.33, -8)
                + _sigmoid(s.get("lbp_entropy", 1), 5.32, -8) + _sigmoid(s.get("edge", 1), 0.33, -8))

    if pair == frozenset(["brown_bear", "school_bus"]):
        return ("brown_bear",
                _sigmoid(s.get("green", 0), 0.15, 5) + _sigmoid(s.get("edge", 0), 0.30, 8)
                + _sigmoid(s.get("grad_dir_entropy", 0), 0.96, 10) + _sigmoid(s.get("hue_cyan_blue", 1), 0.02, -8)
                + _sigmoid(s.get("autocorr_h", 1), 0.17, -6)
                + _sigmoid(s.get("horiz_dominance", 1), 1.30, -3),
                "school_bus",
                _sigmoid(s.get("green", 1), 0.15, -5) + _sigmoid(s.get("edge", 1), 0.30, -8)
                + _sigmoid(s.get("grad_dir_entropy", 1), 0.96, -10) + _sigmoid(s.get("hue_cyan_blue", 0), 0.02, 8)
                + _sigmoid(s.get("autocorr_h", 0), 0.17, 6)
                + _sigmoid(s.get("horiz_dominance", 0), 1.30, 3))

    if pair == frozenset(["sports_car", "school_bus"]):
        return ("sports_car",
                _sigmoid(s.get("hue_orange", 1), 0.30, -5) + _sigmoid(s.get("yellow", 1), 0.15, -5)
                + _sigmoid(s.get("warm", 1), 0.30, -4) + _sigmoid(s.get("blob_lap_var", 1), 0.60, -3)
                + _sigmoid(s.get("hist_sports_minus_bus", 0), -0.15, 2)
                + _sigmoid(s.get("warm_bl", 1), 0.33, -4)
                + _sigmoid(s.get("radial_warm_diff", 1), 0.10, -4)
                + _sigmoid(s.get("blob_coverage", 1), 0.25, -4)
                + _sigmoid(s.get("dct_high", 0), 0.195, 5)
                + _sigmoid(s.get("vert_regularity", 0), 3.3, 3),
                "school_bus",
                _sigmoid(s.get("hue_orange", 0), 0.30, 5) + _sigmoid(s.get("yellow", 0), 0.15, 5)
                + _sigmoid(s.get("warm", 0), 0.30, 4) + _sigmoid(s.get("blob_lap_var", 0), 0.60, 3)
                + _sigmoid(s.get("hist_sports_minus_bus", 0), -0.15, -2)
                + _sigmoid(s.get("warm_bl", 0), 0.33, 4)
                + _sigmoid(s.get("radial_warm_diff", 0), 0.10, 4)
                + _sigmoid(s.get("blob_coverage", 0), 0.25, 4)
                + _sigmoid(s.get("dct_high", 1), 0.195, -5)
                + _sigmoid(s.get("vert_regularity", 10), 3.3, -3))

    if pair == frozenset(["brown_bear", "golden_retriever"]):
        return ("brown_bear",
                _sigmoid(s.get("textured_decentered", 0), 0.10, 8) + _sigmoid(s.get("center_surround", 1), 0.90, -4)
                + _sigmoid(s.get("edge_tl", 0), 0.26, 8) + _sigmoid(s.get("warm_val_mean", 1), 0.51, -5)
                + _sigmoid(s.get("hist_bear_minus_gr", 0), 0.0, 3)
                + _sigmoid(s.get("dct_high", 0), 0.20, 4)
                + _sigmoid(s.get("gabor_45_04_var", 0), 0.70, 3),
                "golden_retriever",
                _sigmoid(s.get("textured_decentered", 1), 0.10, -8) + _sigmoid(s.get("center_surround", 0), 0.90, 4)
                + _sigmoid(s.get("edge_tl", 1), 0.26, -8) + _sigmoid(s.get("warm_val_mean", 0), 0.51, 5)
                + _sigmoid(s.get("hist_bear_minus_gr", 0), 0.0, -3)
                + _sigmoid(s.get("dct_low", 0), 0.22, 4)
                + _sigmoid(s.get("gabor_45_04_var", 1), 0.70, -3))

    if pair == frozenset(["brown_bear", "banana"]):
        return ("brown_bear",
                _sigmoid(s.get("textured_decentered", 0), 0.09, 10) + _sigmoid(s.get("smooth_yellow", 1), 0.08, -6)
                + _sigmoid(s.get("edge", 0), 0.25, 8) + _sigmoid(s.get("warm_val_mean", 1), 0.54, -5),
                "banana",
                _sigmoid(s.get("textured_decentered", 1), 0.09, -10) + _sigmoid(s.get("smooth_yellow", 0), 0.08, 6)
                + _sigmoid(s.get("edge", 1), 0.25, -8) + _sigmoid(s.get("warm_val_mean", 0), 0.54, 5))

    if pair == frozenset(["brown_bear", "mushroom"]):
        return ("brown_bear",
                _sigmoid(s.get("textured_decentered", 0), 0.09, 10) + _sigmoid(s.get("center_surround", 1), 0.95, -5)
                + _sigmoid(s.get("sat", 1), 0.42, -4) + _sigmoid(s.get("sat_bl", 1), 0.42, -4)
                + _sigmoid(s.get("hist_mushroom_minus_bear", 0), 0.0, -3),
                "mushroom",
                _sigmoid(s.get("textured_decentered", 1), 0.09, -10) + _sigmoid(s.get("center_surround", 0), 0.95, 5)
                + _sigmoid(s.get("sat", 0), 0.42, 4) + _sigmoid(s.get("sat_bl", 0), 0.42, 4)
                + _sigmoid(s.get("hist_mushroom_minus_bear", 0), 0.0, 3))

    if pair == frozenset(["teapot", "king_penguin"]):
        return ("teapot",
                _sigmoid(s.get("hist_teapot_minus_kp", 0), -0.03, 4)
                + _sigmoid(s.get("warm_bl", 0), 0.20, 5)
                + _sigmoid(s.get("smooth_warm", 0), 0.06, 6)
                + _sigmoid(s.get("horiz_dominance", 0), 1.05, 4)
                + _sigmoid(s.get("autocorr_h", 0), 0.14, 6)
                + _sigmoid(s.get("sat_br", 0), 0.25, 5)
                + _sigmoid(s.get("mid_wider", 0), 0.5, 5)
                + _sigmoid(s.get("mid_width_ratio", 0), 1.35, 3)
                + _sigmoid(s.get("gabor_dominant_orient", 0), 0.20, 5),
                "king_penguin",
                _sigmoid(s.get("hist_teapot_minus_kp", 0), -0.03, -4)
                + _sigmoid(s.get("warm_bl", 1), 0.20, -5)
                + _sigmoid(s.get("smooth_warm", 1), 0.06, -6)
                + _sigmoid(s.get("horiz_dominance", 1), 1.05, -4)
                + _sigmoid(s.get("autocorr_h", 1), 0.14, -6)
                + _sigmoid(s.get("sat_br", 1), 0.25, -5)
                + _sigmoid(s.get("mid_wider", 1), 0.5, -5)
                + _sigmoid(s.get("mid_width_ratio", 1), 1.35, -3)
                + _sigmoid(s.get("gabor_dominant_orient", 1), 0.20, -5))

    if pair == frozenset(["teapot", "banana"]):
        return ("teapot",
                _sigmoid(s.get("yellow", 1), 0.30, -5) + _sigmoid(s.get("edge", 1), 0.20, -8)
                + _sigmoid(s.get("top_uniformity", 0), 0.70, 5) + _sigmoid(s.get("hist_teapot_minus_banana", 0), 0.0, 3)
                + _sigmoid(s.get("sat", 1), 0.45, -5)
                + _sigmoid(s.get("color_std", 1), 0.22, -5)
                + _sigmoid(s.get("mid_wider", 0), 0.5, 4)
                + _sigmoid(s.get("gabor_dominant_orient", 0), 0.30, 4),
                "banana",
                _sigmoid(s.get("yellow", 0), 0.30, 5) + _sigmoid(s.get("edge", 0), 0.20, 8)
                + _sigmoid(s.get("top_uniformity", 1), 0.70, -5) + _sigmoid(s.get("hist_teapot_minus_banana", 0), 0.0, -3)
                + _sigmoid(s.get("sat", 0), 0.45, 5)
                + _sigmoid(s.get("color_std", 0), 0.22, 5)
                + _sigmoid(s.get("mid_wider", 1), 0.5, -4)
                + _sigmoid(s.get("gabor_dominant_orient", 1), 0.30, -4))

    if pair == frozenset(["banana", "mushroom"]):
        return ("banana",
                _sigmoid(s.get("warm_val_mean", 0), 0.55, 5) + _sigmoid(s.get("smooth_warm", 0), 0.15, 5)
                + _sigmoid(s.get("val", 0), 0.55, 4) + _sigmoid(s.get("hist_banana_minus_mushroom", 0), 0.0, 3)
                + _sigmoid(s.get("smooth_yellow", 0), 0.08, 8)
                + _sigmoid(s.get("sat_smooth_warm", 0), 0.08, 6)
                + _sigmoid(s.get("dct_low", 0), 0.23, 5),
                "mushroom",
                _sigmoid(s.get("round_edge", 0), 0.20, 6) + _sigmoid(s.get("edge", 0), 0.25, 6)
                + _sigmoid(s.get("warm_blob_count", 0), 0.4, 4) + _sigmoid(s.get("hist_banana_minus_mushroom", 0), 0.0, -3)
                + _sigmoid(s.get("bot_edge", 0), 0.26, 5)
                + _sigmoid(s.get("edge_br", 0), 0.26, 5)
                + _sigmoid(s.get("dct_high", 0), 0.20, 5))

    if pair == frozenset(["golden_retriever", "teapot"]):
        return ("golden_retriever",
                _sigmoid(s.get("edge", 0), 0.23, 8) + _sigmoid(s.get("bot_edge", 0), 0.25, 8)
                + _sigmoid(s.get("horiz_dominance", 1), 1.10, -4) + _sigmoid(s.get("hist_gr_minus_teapot", 0), 0.0, 3),
                "teapot",
                _sigmoid(s.get("edge", 1), 0.23, -8) + _sigmoid(s.get("autocorr_h", 0), 0.15, 5)
                + _sigmoid(s.get("horiz_dominance", 0), 1.10, 4) + _sigmoid(s.get("hist_gr_minus_teapot", 0), 0.0, -3))

    if pair == frozenset(["brown_bear", "king_penguin"]):
        return ("brown_bear",
                _sigmoid(s.get("textured_decentered", 0), 0.10, 8) + _sigmoid(s.get("edge", 0), 0.27, 6)
                + _sigmoid(s.get("warm_tl", 0), 0.35, 4) + _sigmoid(s.get("hist_bear_minus_kp", 0), 0.0, 3),
                "king_penguin",
                _sigmoid(s.get("center_surround", 0), 0.95, 4) + _sigmoid(s.get("edge", 1), 0.27, -6)
                + _sigmoid(s.get("warm_tl", 1), 0.35, -4) + _sigmoid(s.get("hist_bear_minus_kp", 0), 0.0, -3))

    if pair == frozenset(["jellyfish", "king_penguin"]):
        return ("jellyfish",
                _sigmoid(s.get("sat", 0), 0.45, 5) + _sigmoid(s.get("color_std", 0), 0.25, 5)
                + _sigmoid(s.get("sat_br", 0), 0.45, 4) + _sigmoid(s.get("hist_jelly_minus_kp", 0), 0.0, 3),
                "king_penguin",
                _sigmoid(s.get("grad_mean", 0), 0.95, 3) + _sigmoid(s.get("sat", 1), 0.45, -5)
                + _sigmoid(s.get("color_std", 1), 0.25, -5) + _sigmoid(s.get("hist_jelly_minus_kp", 0), 0.0, -3))

    if pair == frozenset(["orange", "teapot"]):
        return ("orange",
                _sigmoid(s.get("sat", 0), 0.50, 5) + _sigmoid(s.get("color_std", 0), 0.25, 5)
                + _sigmoid(s.get("sat_bl", 0), 0.50, 4) + _sigmoid(s.get("hist_orange_minus_teapot", 0), 0.0, 3),
                "teapot",
                _sigmoid(s.get("sat", 1), 0.50, -5) + _sigmoid(s.get("autocorr_h", 0), 0.15, 5)
                + _sigmoid(s.get("color_std", 1), 0.25, -5) + _sigmoid(s.get("hist_orange_minus_teapot", 0), 0.0, -3))

    if pair == frozenset(["brown_bear", "teapot"]):
        return ("brown_bear",
                _sigmoid(s.get("edge", 0), 0.25, 8) + _sigmoid(s.get("textured_decentered", 0), 0.10, 8)
                + _sigmoid(s.get("top_edge", 0), 0.24, 6) + _sigmoid(s.get("hist_bear_minus_teapot", 0), 0.0, 3),
                "teapot",
                _sigmoid(s.get("autocorr_h", 0), 0.14, 6) + _sigmoid(s.get("edge", 1), 0.25, -8)
                + _sigmoid(s.get("top_edge", 1), 0.24, -6) + _sigmoid(s.get("hist_bear_minus_teapot", 0), 0.0, -3))

    if pair == frozenset(["golden_retriever", "king_penguin"]):
        return ("golden_retriever",
                _sigmoid(s.get("warm", 0), 0.35, 5) + _sigmoid(s.get("blob_coverage", 0), 0.30, 4)
                + _sigmoid(s.get("hue_red", 0), 0.25, 4) + _sigmoid(s.get("hist_gr_minus_kp", 0), 0.0, 3)
                + _sigmoid(s.get("warm_hue_median", 1), 18.0, -0.3),
                "king_penguin",
                _sigmoid(s.get("warm", 1), 0.35, -5) + _sigmoid(s.get("blob_coverage", 1), 0.30, -4)
                + _sigmoid(s.get("hue_red", 1), 0.25, -4) + _sigmoid(s.get("hist_gr_minus_kp", 0), 0.0, -3)
                + _sigmoid(s.get("warm_hue_median", 0), 18.0, 0.3))

    return None



def _score_all_classes_flat(
    root: ClassNode, graph: SceneGraph, cache: dict[str, FeatureValue]
) -> list[tuple[str, float, list[str]]]:
    """Score ALL leaf classes directly, ignoring gate thresholds."""
    results = []
    _collect_leaves(root, graph, cache, [], results)
    return results


def _collect_leaves(
    node: ClassNode, graph: SceneGraph, cache: dict[str, FeatureValue],
    route: list[str], results: list[tuple[str, float, list[str]]]
) -> None:
    current_route = route + [node.name]
    if node.is_leaf:
        score = score_node(node, graph, cache)
        results.append((node.name, score, current_route))
    else:
        for child in node.children:
            _collect_leaves(child, graph, cache, current_route, results)


def _generate_proof(label: str, route: list[str], cache: dict[str, FeatureValue]) -> list[str]:
    """Generate a human-readable proof trace for the prediction."""
    proof = [f"Claim: image contains '{label}'"]
    proof.append(f"Route: {' → '.join(route)}")
    proof.append("Evidence:")

    active_features = [
        (name, val) for name, val in cache.items()
        if val.present and val.confidence > 0.2
    ]
    active_features.sort(key=lambda x: x[1].confidence, reverse=True)

    for name, val in active_features[:8]:
        evidence_str = "; ".join(val.evidence[:2]) if val.evidence else "detected"
        proof.append(f"  {name}: {val.confidence:.2f} ({evidence_str})")

    absent_features = [
        (name, val) for name, val in cache.items()
        if not val.present and val.evidence
    ]
    if absent_features[:3]:
        proof.append("Absent (supporting exclusion):")
        for name, val in absent_features[:3]:
            proof.append(f"  {name}: not detected")

    return proof


def predict_file(image_path: str | Path) -> Prediction:
    """Convenience: predict from a file path."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return predict(image)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: hlinet-predict <image_path>")
        sys.exit(1)

    path = sys.argv[1]
    result = predict_file(path)

    print(f"\nPrediction: {result.label} ({result.confidence:.2f})")
    if result.alternatives:
        print(f"Alternatives: {', '.join(f'{l} ({s:.2f})' for l, s in result.alternatives)}")
    print()
    for line in result.proof:
        print(line)


if __name__ == "__main__":
    main()
