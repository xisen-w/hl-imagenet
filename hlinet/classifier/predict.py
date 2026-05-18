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

_PER_CLASS_HIST_W = {
    "school_bus": 0.16,
    "orange": 0.16,
    "king_penguin": 0.15,
    "sports_car": 0.14,
    "mushroom": 0.14,
    "golden_retriever": 0.13,
    "brown_bear": 0.12,
    "jellyfish": 0.10,
    "banana": 0.08,
    "teapot": 0.05,
}

_SCORE_CALIBRATION = {
    "school_bus": -0.02,
    "jellyfish": 0.02,
    "king_penguin": 0.01,
    "mushroom": 0.01,
}

_PROTO_MEANS = {
    "banana": {"cm_center_a": 0.5204, "cm_center_b": 0.6355, "sat": 0.5635, "bw": 0.4237, "edge": 0.2065, "warm": 0.638, "color_std": 0.2994, "grad_mean": 1.054},
    "brown_bear": {"cm_center_a": 0.5093, "cm_center_b": 0.5419, "sat": 0.3369, "bw": 0.4921, "edge": 0.3054, "warm": 0.4143, "color_std": 0.1196, "grad_mean": 1.3397},
    "golden_retriever": {"cm_center_a": 0.5261, "cm_center_b": 0.5656, "sat": 0.355, "bw": 0.4408, "edge": 0.2684, "warm": 0.5155, "color_std": 0.1571, "grad_mean": 1.2086},
    "jellyfish": {"cm_center_a": 0.5501, "cm_center_b": 0.4241, "sat": 0.6473, "bw": 0.4964, "edge": 0.146, "warm": 0.0915, "color_std": 0.3712, "grad_mean": 0.6753},
    "king_penguin": {"cm_center_a": 0.5014, "cm_center_b": 0.5169, "sat": 0.2413, "bw": 0.6478, "edge": 0.234, "warm": 0.1878, "color_std": 0.0822, "grad_mean": 1.1929},
    "mushroom": {"cm_center_a": 0.5257, "cm_center_b": 0.5805, "sat": 0.4866, "bw": 0.4689, "edge": 0.3016, "warm": 0.5135, "color_std": 0.1851, "grad_mean": 1.4165},
    "orange": {"cm_center_a": 0.5846, "cm_center_b": 0.6759, "sat": 0.6697, "bw": 0.3643, "edge": 0.1922, "warm": 0.6814, "color_std": 0.4232, "grad_mean": 0.8905},
    "school_bus": {"cm_center_a": 0.5172, "cm_center_b": 0.5704, "sat": 0.4151, "bw": 0.5498, "edge": 0.2682, "warm": 0.3798, "color_std": 0.1368, "grad_mean": 1.6529},
    "sports_car": {"cm_center_a": 0.5344, "cm_center_b": 0.5343, "sat": 0.355, "bw": 0.6594, "edge": 0.2482, "warm": 0.2383, "color_std": 0.1176, "grad_mean": 1.5191},
    "teapot": {"cm_center_a": 0.5205, "cm_center_b": 0.5499, "sat": 0.3482, "bw": 0.5819, "edge": 0.2052, "warm": 0.3828, "color_std": 0.138, "grad_mean": 1.087},
}
_PROTO_STDS = {
    "banana": {"cm_center_a": 0.043, "cm_center_b": 0.0613, "sat": 0.2067, "bw": 0.2161, "edge": 0.0763, "warm": 0.2591, "color_std": 0.1624, "grad_mean": 0.4132},
    "brown_bear": {"cm_center_a": 0.0232, "cm_center_b": 0.0382, "sat": 0.1318, "bw": 0.2124, "edge": 0.054, "warm": 0.2618, "color_std": 0.0752, "grad_mean": 0.2976},
    "golden_retriever": {"cm_center_a": 0.0234, "cm_center_b": 0.0401, "sat": 0.1586, "bw": 0.2102, "edge": 0.0544, "warm": 0.2737, "color_std": 0.101, "grad_mean": 0.3288},
    "jellyfish": {"cm_center_a": 0.0814, "cm_center_b": 0.1164, "sat": 0.2433, "bw": 0.3027, "edge": 0.0786, "warm": 0.1523, "color_std": 0.2709, "grad_mean": 0.3614},
    "king_penguin": {"cm_center_a": 0.0167, "cm_center_b": 0.0371, "sat": 0.1374, "bw": 0.2318, "edge": 0.084, "warm": 0.2047, "color_std": 0.0715, "grad_mean": 0.4059},
    "mushroom": {"cm_center_a": 0.0501, "cm_center_b": 0.0499, "sat": 0.1881, "bw": 0.2085, "edge": 0.0663, "warm": 0.2855, "color_std": 0.116, "grad_mean": 0.3857},
    "orange": {"cm_center_a": 0.0536, "cm_center_b": 0.0733, "sat": 0.2088, "bw": 0.239, "edge": 0.0716, "warm": 0.268, "color_std": 0.2259, "grad_mean": 0.3287},
    "school_bus": {"cm_center_a": 0.0226, "cm_center_b": 0.0482, "sat": 0.1458, "bw": 0.1636, "edge": 0.0493, "warm": 0.1809, "color_std": 0.0951, "grad_mean": 0.3867},
    "sports_car": {"cm_center_a": 0.0518, "cm_center_b": 0.0575, "sat": 0.16, "bw": 0.1791, "edge": 0.0535, "warm": 0.201, "color_std": 0.1011, "grad_mean": 0.3287},
    "teapot": {"cm_center_a": 0.0386, "cm_center_b": 0.0474, "sat": 0.181, "bw": 0.2487, "edge": 0.0622, "warm": 0.2958, "color_std": 0.1101, "grad_mean": 0.3307},
}
_PROTO_W = 0.025


def _proto_scores(graph: SceneGraph) -> dict[str, float]:
    """Score each class by Mahalanobis-like distance from prototype."""
    from hlinet.features.compounds.phase2_signatures import _stats
    s = _stats(graph)
    scores = {}
    for cls, means in _PROTO_MEANS.items():
        stds = _PROTO_STDS[cls]
        dist_sq = 0.0
        n = 0
        for feat, mu in means.items():
            v = s.get(feat)
            if v is not None:
                sigma = stds.get(feat, 0.1)
                dist_sq += ((v - mu) / sigma) ** 2
                n += 1
        if n > 0:
            scores[cls] = -dist_sq / n
    return scores


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
        frozenset(["banana", "orange"]): -0.05,
        frozenset(["king_penguin", "sports_car"]): 0.0,
        frozenset(["golden_retriever", "orange"]): -0.05,
        frozenset(["brown_bear", "golden_retriever"]): 0.0,
        frozenset(["golden_retriever", "sports_car"]): -0.05,
        frozenset(["banana", "golden_retriever"]): -0.05,
        frozenset(["mushroom", "school_bus"]): -0.05,
        frozenset(["school_bus", "sports_car"]): -0.10,
        frozenset(["banana", "mushroom"]): 0.05,
        frozenset(["golden_retriever", "teapot"]): 0.15,
        frozenset(["brown_bear", "king_penguin"]): 0.25,
        frozenset(["jellyfish", "king_penguin"]): 0.0,
        frozenset(["orange", "teapot"]): -0.05,
        frozenset(["brown_bear", "mushroom"]): 0.0,
        frozenset(["brown_bear", "teapot"]): 0.10,
        frozenset(["golden_retriever", "king_penguin"]): 0.10,
        frozenset(["jellyfish", "teapot"]): -0.05,
        frozenset(["mushroom", "king_penguin"]): 0.0,
        frozenset(["orange", "mushroom"]): 0.0,
        frozenset(["teapot", "school_bus"]): 0.0,
        frozenset(["mushroom", "sports_car"]): 0.0,
    }

    margin12 = top1_score - top2_score
    if margin12 <= 0.30:
        pair12 = frozenset([top1_label, top2_label])
        signals = _compute_pair_signals(pair12, s, _sigmoid)
        if signals is not None:
            cls1, sig1, cls2, sig2 = signals
            disc_margin = abs(sig1 - sig2)
            base = _PAIR_BASE.get(pair12, 0.05)
            threshold = base + margin12 * 1.3
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
        frozenset(["teapot", "school_bus"]),
        frozenset(["brown_bear", "mushroom"]),

    }
    if len(candidates) >= 3:
        top1_label, top1_score, _ = candidates[0]
        top3_label, top3_score, _ = candidates[2]
        margin13 = top1_score - top3_score
        pair13 = frozenset([top1_label, top3_label])
        if margin13 <= 0.28 and pair13 in _RANK3_WHITELIST:
            signals = _compute_pair_signals(pair13, s, _sigmoid)
            if signals is not None:
                cls1, sig1, cls2, sig2 = signals
                disc_margin = abs(sig1 - sig2)
                base = _PAIR_BASE.get(pair13, 0.0)
                threshold = base + margin13 * 1.9
                if disc_margin > threshold:
                    winner = cls1 if sig1 > sig2 else cls2
                    if winner == top3_label:
                        candidates[0], candidates[2] = candidates[2], candidates[0]

    _RANK4_WHITELIST = {
        frozenset(["banana", "mushroom"]),
        frozenset(["banana", "orange"]),
        frozenset(["jellyfish", "king_penguin"]),
        frozenset(["orange", "teapot"]),
        frozenset(["brown_bear", "teapot"]),
        frozenset(["school_bus", "sports_car"]),
        frozenset(["banana", "golden_retriever"]),
        frozenset(["banana", "brown_bear"]),
        frozenset(["teapot", "king_penguin"]),
        frozenset(["golden_retriever", "brown_bear"]),
        frozenset(["golden_retriever", "king_penguin"]),


    }
    if len(candidates) >= 4:
        top1_label, top1_score, _ = candidates[0]
        top4_label, top4_score, _ = candidates[3]
        margin14 = top1_score - top4_score
        pair14 = frozenset([top1_label, top4_label])
        if margin14 <= 0.30 and pair14 in _RANK4_WHITELIST:
            signals = _compute_pair_signals(pair14, s, _sigmoid)
            if signals is not None:
                cls1, sig1, cls2, sig2 = signals
                disc_margin = abs(sig1 - sig2)
                base = _PAIR_BASE.get(pair14, 0.0)
                threshold = base + margin14 * 2.8
                if disc_margin > threshold:
                    winner = cls1 if sig1 > sig2 else cls2
                    if winner == top4_label:
                        candidates[0], candidates[3] = candidates[3], candidates[0]

    _RANK5_WHITELIST = {
        frozenset(["banana", "teapot"]),
        frozenset(["school_bus", "sports_car"]),
        frozenset(["brown_bear", "mushroom"]),
        frozenset(["brown_bear", "golden_retriever"]),
        frozenset(["golden_retriever", "teapot"]),
        frozenset(["teapot", "king_penguin"]),
        frozenset(["banana", "mushroom"]),
        frozenset(["brown_bear", "king_penguin"]),
        frozenset(["golden_retriever", "king_penguin"]),
        frozenset(["banana", "orange"]),
        frozenset(["orange", "teapot"]),
        frozenset(["banana", "golden_retriever"]),
        frozenset(["orange", "mushroom"]),


    }
    if len(candidates) >= 5:
        top1_label, top1_score, _ = candidates[0]
        top5_label, top5_score, _ = candidates[4]
        margin15 = top1_score - top5_score
        pair15 = frozenset([top1_label, top5_label])
        if margin15 <= 0.15 and pair15 in _RANK5_WHITELIST:
            signals = _compute_pair_signals(pair15, s, _sigmoid)
            if signals is not None:
                cls1, sig1, cls2, sig2 = signals
                disc_margin = abs(sig1 - sig2)
                base = _PAIR_BASE.get(pair15, 0.0)
                threshold = base + margin15 * 4.0
                if disc_margin > threshold:
                    winner = cls1 if sig1 > sig2 else cls2
                    if winner == top5_label:
                        candidates[0], candidates[4] = candidates[4], candidates[0]

    return candidates


_REPULSION_PAIRS = [
    ("banana", "orange", 0.012),
    ("sports_car", "school_bus", 0.012),
    ("mushroom", "banana", 0.010),
    ("teapot", "banana", 0.014),
    ("brown_bear", "mushroom", 0.014),
    ("teapot", "king_penguin", 0.012),
    ("golden_retriever", "banana", 0.008),
    ("golden_retriever", "king_penguin", 0.008),
    ("brown_bear", "king_penguin", 0.008),
    ("orange", "mushroom", 0.008),
    ("teapot", "school_bus", 0.008),
    ("teapot", "golden_retriever", 0.010),
    ("golden_retriever", "mushroom", 0.010),
    ("brown_bear", "golden_retriever", 0.012),
    ("orange", "teapot", 0.008),
    ("sports_car", "teapot", 0.012),
    ("brown_bear", "sports_car", 0.012),
    ("banana", "king_penguin", 0.012),
    ("mushroom", "sports_car", 0.010),
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


_CONFIDENCE_GATES = {
    "sports_car": 0.40,
    "banana": 0.42,
    "mushroom": 0.42,
    "golden_retriever": 0.37,
    "orange": 0.42,
    "teapot": 0.35,
}


def _proto_dist(s: dict[str, float], cls: str) -> float:
    """Compute prototype distance for a class."""
    means = _PROTO_MEANS.get(cls)
    stds = _PROTO_STDS.get(cls)
    if not means or not stds:
        return 999.0
    dist_sq = 0.0
    n = 0
    for feat, mu in means.items():
        v = s.get(feat)
        if v is not None:
            sigma = stds.get(feat, 0.1)
            dist_sq += ((v - mu) / sigma) ** 2
            n += 1
    return dist_sq / max(n, 1)



def _local_verify(
    candidates: list[tuple[str, float, list[str]]],
    graph: SceneGraph,
) -> list[tuple[str, float, list[str]]]:
    if len(candidates) < 2:
        return candidates
    top_label, top_score, _ = candidates[0]
    sec_label, sec_score, _ = candidates[1]
    gate = _CONFIDENCE_GATES.get(top_label)
    if gate is not None and top_score < gate:
        candidates[0], candidates[1] = candidates[1], candidates[0]
        return candidates

    from hlinet.features.compounds.phase2_signatures import _stats
    s = _stats(graph)

    margin = top_score - sec_score
    pair = frozenset([top_label, sec_label])
    _WIDE_MARGIN = {
        frozenset(["teapot", "banana"]): 0.30,
        frozenset(["mushroom", "banana"]): 0.25,
        frozenset(["orange", "banana"]): 0.25,
        frozenset(["golden_retriever", "banana"]): 0.25,
    }
    margin_gate = _WIDE_MARGIN.get(pair, 0.15)
    if margin < margin_gate:
        if pair == frozenset(["teapot", "banana"]):
            cm_b = s.get("cm_center_b", 0.5)
            orient_e = s.get("orient_entropy", 3.0)
            cmbs = s.get("cm_b_std", 0.0)
            acorr_tb = s.get("autocorr_h", 0.1)
            if cm_b < 0.57 and orient_e > 2.85:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif cmbs > 0.075:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif acorr_tb < 0.069:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("cm_b_skew", 0.0) > 1.0362:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("hist_orange", 0.0) > 1.3175:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("hist_bear_minus_teapot", 0.0) < -0.2037:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["teapot", "king_penguin"]):
            autocorr = s.get("autocorr_h", 0.15)
            horiz = s.get("horiz_dominance", 1.0)
            wss = s.get("warm_sat_std", 0.0)
            if autocorr > 0.16 and horiz > 1.1:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif wss > 0.15:
                idx = 0 if top_label == "king_penguin" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("cm_b_skew", 0.0) > 3.1083:
                idx = 0 if top_label == "king_penguin" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("grad_dir_entropy", 0.0) > 0.9916:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["jellyfish", "teapot"]):
            sat_v = s.get("sat", 0.4)
            color_std_v = s.get("color_std", 0.1)
            ec = s.get("edge_concentration", 1.0)
            if sat_v > 0.50 and color_std_v > 0.20:
                idx = 0 if top_label == "jellyfish" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif ec > 1.3:
                idx = 0 if top_label == "jellyfish" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["teapot", "golden_retriever"]):
            edge_v = s.get("edge", 0.25)
            horiz = s.get("horiz_dominance", 1.0)
            if edge_v < 0.22 and horiz > 1.05:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("hist_mushroom", 0.0) > 1.8272:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["orange", "teapot"]):
            sat_v = s.get("sat", 0.4)
            cm_a = s.get("cm_center_a", 0.52)
            if sat_v > 0.55 and cm_a > 0.56:
                idx = 0 if top_label == "orange" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif cm_a > 0.62:
                idx = 0 if top_label == "orange" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["mushroom", "banana"]):
            edge_v = s.get("edge", 0.25)
            hu1 = s.get("hu1", 2.6)
            cmbs = s.get("cm_b_std", 0.0)
            gra = s.get("green_region_area", 1.0)
            if edge_v > 0.27 and hu1 > 2.65:
                idx = 0 if top_label == "mushroom" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif cmbs > 0.045 and gra < 0.05:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif cmbs > 0.0673:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("hist_jellyfish", 0.0) > 0.6012:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("hue_cyan_blue", 0.0) > 0.0012:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["orange", "banana"]):
            dwr = s.get("dark_warm_ratio", 0.0)
            if dwr > 0.6686:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("hist_sports_car", 0.0) > 1.561:
                idx = 0 if top_label == "orange" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("radial_warm_diff", 0.0) < -0.1301:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["golden_retriever", "school_bus"]):
            acorr_gs = s.get("autocorr_h", 0.1)
            if acorr_gs < 0.064:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["golden_retriever", "banana"]):
            warm_gb = s.get("warm", 0.0)
            if warm_gb > 0.863:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("warm_bl", 0.0) > 0.9097:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("blob_coverage", 0.0) > 0.8606:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["teapot", "brown_bear"]):
            hu1_v = s.get("hu1", 3.0)
            hr = s.get("hue_red", 0.0)
            acorr = s.get("autocorr_h", 0.2)
            if hu1_v < 2.62:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif hr > 0.50:
                idx = 0 if top_label == "brown_bear" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif acorr < 0.10:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("r0_warm", 0) > 0.986:
                idx = 0 if top_label == "brown_bear" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("vert_regularity", 0.0) > 5.2081:
                idx = 0 if top_label == "brown_bear" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("cm_b_skew", 0.0) > 1.1705:
                idx = 0 if top_label == "brown_bear" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["golden_retriever", "brown_bear"]):
            sat_v = s.get("sat", 0.4)
            dh = s.get("dct_high", 0.25)
            horiz = s.get("horiz_dominance", 1.0)
            acorr = s.get("autocorr_h", 0.1)
            if sat_v < 0.28 and dh < 0.20:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif horiz > 1.10 and acorr > 0.13:
                idx = 0 if top_label == "brown_bear" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("hist_jellyfish", 0.0) > 0.7915:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif acorr > 0.1784:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("grad_mean", 0.0) > 1.7735:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("mean_ch_corr", 0.0) > 0.9845:
                idx = 0 if top_label == "brown_bear" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["sports_car", "school_bus"]):
            dct_h = s.get("dct_high", 0.18)
            gm = s.get("grad_mean", 1.4)
            ho = s.get("hue_orange", 0.0)
            hsb = s.get("hist_sports_minus_bus", 0.0)
            hbn = s.get("hist_banana", 0.0)
            if dct_h > 0.20 and gm > 1.60:
                idx = 0 if top_label == "sports_car" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif dct_h < 0.195 and ho > 0.20:
                idx = 0 if top_label == "school_bus" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif hsb < -0.335 and hbn > 2.157:
                idx = 0 if top_label == "school_bus" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("edge_tl", 0.0) > 0.3569:
                idx = 0 if top_label == "sports_car" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["banana", "school_bus"]):
            acorr = s.get("autocorr_h", 0.2)
            if acorr < 0.08:
                idx = 0 if top_label == "banana" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["brown_bear", "mushroom"]):
            green_v = s.get("green", 0.0)
            cstd = s.get("color_std", 0.1)
            if green_v > 0.50 and cstd > 0.18:
                idx = 0 if top_label == "brown_bear" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("cm_center_a", 0.0) > 0.5243:
                idx = 0 if top_label == "mushroom" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["king_penguin", "sports_car"]):
            fft_hv = s.get("fft_hv_ratio", 0.8)
            evmr = s.get("edge_vert_mid_ratio", 0.4)
            if fft_hv > 1.0 and evmr < 0.36:
                idx = 0 if top_label == "king_penguin" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["school_bus", "mushroom"]):
            acorr = s.get("autocorr_h", 0.0)
            dh = s.get("dct_high", 0.25)
            if acorr > 0.10 and dh < 0.23:
                idx = 0 if top_label == "school_bus" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif acorr > 0.0862:
                idx = 0 if top_label == "school_bus" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["school_bus", "brown_bear"]):
            acorr_sb = s.get("autocorr_h", 0.0)
            if acorr_sb > 0.119:
                idx = 0 if top_label == "school_bus" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["mushroom", "king_penguin"]):
            bw_v = s.get("bw", 0.5)
            if bw_v < 0.482:
                idx = 0 if top_label == "king_penguin" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["mushroom", "sports_car"]):
            horiz = s.get("horiz_dominance", 1.0)
            if horiz > 1.344:
                idx = 0 if top_label == "sports_car" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["sports_car", "teapot"]):
            bw_v = s.get("bw", 0.5)
            hd = s.get("horiz_dominance", 1.0)
            if bw_v > 0.80 and hd > 1.50:
                idx = 0 if top_label == "sports_car" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif s.get("gabor_45_04_var", 1.0) < 0.2979:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["teapot", "school_bus"]):
            acorr = s.get("autocorr_h", 0.2)
            dh = s.get("dct_high", 0.18)
            ec = s.get("edge_concentration", 1.0)
            if acorr < 0.25 and dh > 0.18:
                idx = 0 if top_label == "teapot" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
            elif ec > 1.328:
                idx = 0 if top_label == "school_bus" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["brown_bear", "king_penguin"]):
            hbg = s.get("hist_bear_minus_gr", 0.0)
            if hbg > 0.2929:
                idx = 0 if top_label == "brown_bear" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["golden_retriever", "mushroom"]):
            hj = s.get("hist_jellyfish", 0.0)
            if hj > 1.011:
                idx = 0 if top_label == "golden_retriever" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["jellyfish", "king_penguin"]):
            tu = s.get("top_uniformity", 0.5)
            if tu < 0.5796:
                idx = 0 if top_label == "jellyfish" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["mushroom", "orange"]):
            cma_mo = s.get("cm_center_a", 0.52)
            if cma_mo > 0.5243:
                idx = 0 if top_label == "mushroom" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]
        elif pair == frozenset(["jellyfish", "sports_car"]):
            if s.get("hist_banana", 0.0) > 0.9366:
                idx = 0 if top_label == "sports_car" else 1
                if idx == 1:
                    candidates[0], candidates[1] = candidates[1], candidates[0]

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
                + _sigmoid(s.get("sat_color_std", 0), 0.25, 5)
                + _sigmoid(s.get("cm_center_a", 0), 0.545, 40)
                + _sigmoid(s.get("warm_sat_std", 1), 0.18, -6)
                + _sigmoid(s.get("rb_corr", 1), 0.55, -4),
                "banana",
                _sigmoid(s.get("hue_red", 1), 0.25, -6) + _sigmoid(s.get("color_std", 1), 0.35, -5)
                + _sigmoid(s.get("bw", 0), 0.25, 5) + _sigmoid(s.get("grad_mean", 0), 0.80, 3)
                + _sigmoid(s.get("hist_orange_minus_banana", 0), 0.0, -3)
                + _sigmoid(s.get("warm_hue_mean", 0), 0.40, 6)
                + _sigmoid(s.get("warm_val_mean", 1), 0.66, -5)
                + _sigmoid(s.get("sat_color_std", 1), 0.25, -5)
                + _sigmoid(s.get("cm_center_a", 1), 0.545, -40)
                + _sigmoid(s.get("warm_sat_std", 0), 0.18, 6)
                + _sigmoid(s.get("rb_corr", 0), 0.55, 4))

    if pair == frozenset(["banana", "golden_retriever"]):
        return ("golden_retriever",
                _sigmoid(s.get("edge", 0), 0.24, 10) + _sigmoid(s.get("sat", 1), 0.45, -5)
                + _sigmoid(s.get("yellow", 1), 0.30, -5) + _sigmoid(s.get("bot_edge", 0), 0.24, 8)
                + _sigmoid(s.get("hist_gr_minus_banana", 0), 0.0, 2)
                + _sigmoid(s.get("warm_hue_median", 1), 18.0, -0.3)
                + _sigmoid(s.get("cm_b_std", 1), 0.055, -20)
                + _sigmoid(s.get("hu1", 0), 2.60, 15)
                + _sigmoid(s.get("gb_corr", 0), 0.88, 5)
                + _sigmoid(s.get("rb_corr", 0), 0.80, 4),
                "banana",
                _sigmoid(s.get("edge", 1), 0.24, -10) + _sigmoid(s.get("sat", 0), 0.45, 5)
                + _sigmoid(s.get("yellow", 0), 0.30, 5) + _sigmoid(s.get("bot_edge", 1), 0.24, -8)
                + _sigmoid(s.get("hist_gr_minus_banana", 0), 0.0, -2)
                + _sigmoid(s.get("warm_hue_median", 0), 18.0, 0.3)
                + _sigmoid(s.get("cm_b_std", 0), 0.055, 20)
                + _sigmoid(s.get("hu1", 1), 2.60, -15)
                + _sigmoid(s.get("gb_corr", 1), 0.88, -5)
                + _sigmoid(s.get("rb_corr", 1), 0.80, -4))

    if pair == frozenset(["mushroom", "golden_retriever"]):
        return ("mushroom",
                _sigmoid(s.get("val", 1), 0.50, -4) + _sigmoid(s.get("sat_br", 0), 0.43, 5)
                + _sigmoid(s.get("lap_var", 0), 8000, 0.0002) + _sigmoid(s.get("hue_yellow", 0), 0.12, 5)
                + _sigmoid(s.get("dct_high", 0), 0.20, 5)
                + _sigmoid(s.get("dct_mid_over_low", 0), 0.40, 4)
                + _sigmoid(s.get("edge_concentration", 1), 1.10, -3),
                "golden_retriever",
                _sigmoid(s.get("val", 0), 0.50, 4) + _sigmoid(s.get("sat_br", 1), 0.43, -5)
                + _sigmoid(s.get("lap_var", 99999), 8000, -0.0002) + _sigmoid(s.get("hue_yellow", 1), 0.12, -5)
                + _sigmoid(s.get("dct_low", 0), 0.22, 4)
                + _sigmoid(s.get("dct_mid_over_low", 1), 0.40, -4)
                + _sigmoid(s.get("edge_concentration", 0), 1.10, 3))

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
                + _sigmoid(s.get("top_uniformity", 0), 0.66, 4) + _sigmoid(s.get("lap_var", 0), 7500, 0.0003)
                + _sigmoid(s.get("orient_entropy", 1), 2.87, -8),
                "teapot",
                _sigmoid(s.get("grad_dir_entropy", 0), 0.93, 10) + _sigmoid(s.get("hue_red", 0), 0.40, 4)
                + _sigmoid(s.get("top_uniformity", 1), 0.66, -4) + _sigmoid(s.get("lap_var", 99999), 7500, -0.0003)
                + _sigmoid(s.get("orient_entropy", 0), 2.87, 8))

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
                + _sigmoid(s.get("vert_regularity", 0), 3.3, 3)
                + _sigmoid(s.get("hu1", 1), 2.64, -15)
                ,
                "school_bus",
                _sigmoid(s.get("hue_orange", 0), 0.30, 5) + _sigmoid(s.get("yellow", 0), 0.15, 5)
                + _sigmoid(s.get("warm", 0), 0.30, 4) + _sigmoid(s.get("blob_lap_var", 0), 0.60, 3)
                + _sigmoid(s.get("hist_sports_minus_bus", 0), -0.15, -2)
                + _sigmoid(s.get("warm_bl", 0), 0.33, 4)
                + _sigmoid(s.get("radial_warm_diff", 0), 0.10, 4)
                + _sigmoid(s.get("blob_coverage", 0), 0.25, 4)
                + _sigmoid(s.get("dct_high", 1), 0.195, -5)
                + _sigmoid(s.get("vert_regularity", 10), 3.3, -3)
                + _sigmoid(s.get("hu1", 0), 2.64, 15)
                )

    if pair == frozenset(["brown_bear", "golden_retriever"]):
        return ("brown_bear",
                _sigmoid(s.get("textured_decentered", 0), 0.10, 8) + _sigmoid(s.get("center_surround", 1), 0.90, -4)
                + _sigmoid(s.get("edge_tl", 0), 0.26, 8) + _sigmoid(s.get("warm_val_mean", 1), 0.51, -5)
                + _sigmoid(s.get("hist_bear_minus_gr", 0), 0.0, 3)
                + _sigmoid(s.get("dct_high", 0), 0.20, 4)
                + _sigmoid(s.get("gabor_45_04_var", 0), 0.70, 3)
                + _sigmoid(s.get("cm_center_b", 1), 0.555, -25),
                "golden_retriever",
                _sigmoid(s.get("textured_decentered", 1), 0.10, -8) + _sigmoid(s.get("center_surround", 0), 0.90, 4)
                + _sigmoid(s.get("edge_tl", 1), 0.26, -8) + _sigmoid(s.get("warm_val_mean", 0), 0.51, 5)
                + _sigmoid(s.get("hist_bear_minus_gr", 0), 0.0, -3)
                + _sigmoid(s.get("dct_low", 0), 0.22, 4)
                + _sigmoid(s.get("gabor_45_04_var", 1), 0.70, -3)
                + _sigmoid(s.get("cm_center_b", 0), 0.555, 25))

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
                + _sigmoid(s.get("hist_mushroom_minus_bear", 0), 0.0, -3)
                + _sigmoid(s.get("cm_a_std", 1), 0.031, -30)
                ,
                "mushroom",
                _sigmoid(s.get("textured_decentered", 1), 0.09, -10) + _sigmoid(s.get("center_surround", 0), 0.95, 5)
                + _sigmoid(s.get("sat", 0), 0.42, 4) + _sigmoid(s.get("sat_bl", 0), 0.42, 4)
                + _sigmoid(s.get("hist_mushroom_minus_bear", 0), 0.0, 3)
                + _sigmoid(s.get("cm_a_std", 0), 0.031, 30)
                )

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
                + _sigmoid(s.get("gabor_dominant_orient", 0), 0.30, 4)
                + _sigmoid(s.get("cm_center_b", 1), 0.59, -40)
                + _sigmoid(s.get("orient_entropy", 0), 2.88, 8)
                + _sigmoid(s.get("gb_corr", 0), 0.85, 4)
                + _sigmoid(s.get("r0_warm", 0), 0.45, 4),
                "banana",
                _sigmoid(s.get("yellow", 0), 0.30, 5) + _sigmoid(s.get("edge", 0), 0.20, 8)
                + _sigmoid(s.get("top_uniformity", 1), 0.70, -5) + _sigmoid(s.get("hist_teapot_minus_banana", 0), 0.0, -3)
                + _sigmoid(s.get("sat", 0), 0.45, 5)
                + _sigmoid(s.get("color_std", 0), 0.22, 5)
                + _sigmoid(s.get("mid_wider", 1), 0.5, -4)
                + _sigmoid(s.get("gabor_dominant_orient", 1), 0.30, -4)
                + _sigmoid(s.get("cm_center_b", 0), 0.59, 40)
                + _sigmoid(s.get("orient_entropy", 1), 2.88, -8)
                + _sigmoid(s.get("gb_corr", 1), 0.85, -4))

    if pair == frozenset(["banana", "mushroom"]):
        return ("banana",
                _sigmoid(s.get("warm_val_mean", 0), 0.55, 5) + _sigmoid(s.get("smooth_warm", 0), 0.15, 5)
                + _sigmoid(s.get("val", 0), 0.55, 4) + _sigmoid(s.get("hist_banana_minus_mushroom", 0), 0.0, 3)
                + _sigmoid(s.get("smooth_yellow", 0), 0.08, 8)
                + _sigmoid(s.get("sat_smooth_warm", 0), 0.08, 6)
                + _sigmoid(s.get("dct_low", 0), 0.23, 5)
                + _sigmoid(s.get("edge_concentration", 0), 1.10, 3)
                + _sigmoid(s.get("hu1", 1), 2.61, -15)
                + _sigmoid(s.get("hu2", 1), 7.3, -3),
                "mushroom",
                _sigmoid(s.get("round_edge", 0), 0.20, 6) + _sigmoid(s.get("edge", 0), 0.25, 6)
                + _sigmoid(s.get("warm_blob_count", 0), 0.4, 4) + _sigmoid(s.get("hist_banana_minus_mushroom", 0), 0.0, -3)
                + _sigmoid(s.get("bot_edge", 0), 0.26, 5)
                + _sigmoid(s.get("edge_br", 0), 0.26, 5)
                + _sigmoid(s.get("dct_high", 0), 0.20, 5)
                + _sigmoid(s.get("edge_entropy", 0), 3.8, 3)
                + _sigmoid(s.get("hu1", 0), 2.61, 15)
                + _sigmoid(s.get("hu2", 0), 7.3, 3))

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
                + _sigmoid(s.get("warm_tl", 0), 0.35, 4) + _sigmoid(s.get("hist_bear_minus_kp", 0), 0.0, 3)
                + _sigmoid(s.get("fft_hv_ratio", 1), 0.95, -3)
                + _sigmoid(s.get("hu1", 0), 2.63, 15),
                "king_penguin",
                _sigmoid(s.get("center_surround", 0), 0.95, 4) + _sigmoid(s.get("edge", 1), 0.27, -6)
                + _sigmoid(s.get("warm_tl", 1), 0.35, -4) + _sigmoid(s.get("hist_bear_minus_kp", 0), 0.0, -3)
                + _sigmoid(s.get("fft_hv_ratio", 0), 0.95, 3)
                + _sigmoid(s.get("hu1", 1), 2.63, -15))

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
                + _sigmoid(s.get("top_edge", 0), 0.24, 6) + _sigmoid(s.get("hist_bear_minus_teapot", 0), 0.0, 3)
                + _sigmoid(s.get("hu1", 0), 2.64, 15),
                "teapot",
                _sigmoid(s.get("autocorr_h", 0), 0.14, 6) + _sigmoid(s.get("edge", 1), 0.25, -8)
                + _sigmoid(s.get("top_edge", 1), 0.24, -6) + _sigmoid(s.get("hist_bear_minus_teapot", 0), 0.0, -3)
                + _sigmoid(s.get("hu1", 1), 2.64, -15))

    if pair == frozenset(["golden_retriever", "king_penguin"]):
        return ("golden_retriever",
                _sigmoid(s.get("warm", 0), 0.35, 5) + _sigmoid(s.get("blob_coverage", 0), 0.30, 4)
                + _sigmoid(s.get("hue_red", 0), 0.25, 4) + _sigmoid(s.get("hist_gr_minus_kp", 0), 0.0, 3)
                + _sigmoid(s.get("warm_hue_median", 1), 18.0, -0.3)
                + _sigmoid(s.get("fft_hv_ratio", 1), 1.0, -3)
                + _sigmoid(s.get("cm_center_a", 0), 0.515, 40)
                + _sigmoid(s.get("cm_center_b", 0), 0.545, 40),
                "king_penguin",
                _sigmoid(s.get("warm", 1), 0.35, -5) + _sigmoid(s.get("blob_coverage", 1), 0.30, -4)
                + _sigmoid(s.get("hue_red", 1), 0.25, -4) + _sigmoid(s.get("hist_gr_minus_kp", 0), 0.0, -3)
                + _sigmoid(s.get("warm_hue_median", 0), 18.0, 0.3)
                + _sigmoid(s.get("fft_hv_ratio", 0), 1.0, 3)
                + _sigmoid(s.get("cm_center_a", 1), 0.515, -40)
                + _sigmoid(s.get("cm_center_b", 1), 0.545, -40))

    if pair == frozenset(["jellyfish", "teapot"]):
        return ("jellyfish",
                _sigmoid(s.get("sat", 0), 0.50, 5) + _sigmoid(s.get("blue_purple", 0), 0.20, 5)
                + _sigmoid(s.get("color_std", 0), 0.25, 5) + _sigmoid(s.get("edge_entropy", 1), 3.5, -4)
                + _sigmoid(s.get("edge_concentration", 0), 1.4, 3),
                "teapot",
                _sigmoid(s.get("sat", 1), 0.50, -5) + _sigmoid(s.get("blue_purple", 1), 0.20, -5)
                + _sigmoid(s.get("color_std", 1), 0.25, -5) + _sigmoid(s.get("edge_entropy", 0), 3.5, 4)
                + _sigmoid(s.get("edge_concentration", 1), 1.4, -3))

    if pair == frozenset(["orange", "mushroom"]):
        return ("orange",
                _sigmoid(s.get("warm_val_mean", 0), 0.58, 5) + _sigmoid(s.get("smooth_warm", 0), 0.16, 5)
                + _sigmoid(s.get("color_std", 0), 0.27, 5) + _sigmoid(s.get("dct_low", 0), 0.24, 5)
                + _sigmoid(s.get("sat", 0), 0.55, 5),
                "mushroom",
                _sigmoid(s.get("edge", 0), 0.24, 8) + _sigmoid(s.get("grad_mean", 0), 1.1, 3)
                + _sigmoid(s.get("round_edge", 0), 0.20, 5) + _sigmoid(s.get("dct_high", 0), 0.19, 5)
                + _sigmoid(s.get("lap_var", 0), 6500, 0.0002))

    if pair == frozenset(["teapot", "school_bus"]):
        return ("teapot",
                _sigmoid(s.get("grad_dir_entropy", 0), 0.95, 8) + _sigmoid(s.get("dct_low", 0), 0.21, 5)
                + _sigmoid(s.get("edge_concentration", 0), 1.28, 3) + _sigmoid(s.get("top_uniformity", 0), 0.65, 4)
                + _sigmoid(s.get("smooth_warm", 0), 0.11, 5),
                "school_bus",
                _sigmoid(s.get("grad_mean", 0), 1.4, 3) + _sigmoid(s.get("blob_lap_var", 0), 0.80, 3)
                + _sigmoid(s.get("edge", 0), 0.23, 8) + _sigmoid(s.get("autocorr_h", 0), 0.22, 5)
                + _sigmoid(s.get("horiz_dominance", 0), 1.4, 3))

    if pair == frozenset(["mushroom", "king_penguin"]):
        return ("mushroom",
                _sigmoid(s.get("center_surround", 0), 1.10, 3) + _sigmoid(s.get("edge", 0), 0.25, 8)
                + _sigmoid(s.get("sat", 0), 0.40, 5) + _sigmoid(s.get("round_edge", 0), 0.20, 5),
                "king_penguin",
                _sigmoid(s.get("bw", 0), 0.55, 5) + _sigmoid(s.get("fft_hv_ratio", 0), 1.0, 3)
                + _sigmoid(s.get("sat", 1), 0.40, -5) + _sigmoid(s.get("center_surround", 1), 1.10, -3))

    if pair == frozenset(["mushroom", "sports_car"]):
        return ("mushroom",
                _sigmoid(s.get("grad_dir_entropy", 0), 0.95, 10) + _sigmoid(s.get("edge", 0), 0.28, 8)
                + _sigmoid(s.get("warm", 0), 0.35, 5) + _sigmoid(s.get("fft_hv_ratio", 0), 0.85, 3),
                "sports_car",
                _sigmoid(s.get("autocorr_h", 0), 0.15, 6) + _sigmoid(s.get("horiz_dominance", 0), 1.4, 3)
                + _sigmoid(s.get("warm", 1), 0.35, -5) + _sigmoid(s.get("fft_hv_ratio", 1), 0.85, -3))

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
