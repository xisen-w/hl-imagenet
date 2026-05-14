"""KNN-based prediction using precomputed feature database."""
from __future__ import annotations

import numpy as np
from pathlib import Path

from hlinet.features.compounds.phase2_signatures import _stats
from hlinet.types import SceneGraph


_DB = None

def _load_db():
    global _DB
    if _DB is not None:
        return _DB
    db_path = Path(__file__).parent / "feature_db.npz"
    data = np.load(str(db_path), allow_pickle=True)
    vectors = data["vectors"]  # (2000, 139)
    labels = data["labels"]    # (2000,)
    classes = list(data["classes"])
    feature_keys = list(data["feature_keys"])

    mean = vectors.mean(axis=0)
    std = vectors.std(axis=0) + 1e-8
    vectors_norm = (vectors - mean) / std

    n_classes = len(classes)
    n_features = len(feature_keys)
    weights = np.ones(n_features, dtype=np.float32)

    for f_idx in range(n_features):
        col = vectors[:, f_idx]
        grand_mean = col.mean()
        between_var = 0.0
        within_var = 0.0
        for c in range(n_classes):
            mask = labels == c
            class_col = col[mask]
            class_mean = class_col.mean()
            between_var += mask.sum() * (class_mean - grand_mean) ** 2
            within_var += class_col.var() * mask.sum()
        fisher = between_var / max(within_var, 1e-8)
        weights[f_idx] = fisher

    top_k = 60
    top_indices = np.argsort(weights)[::-1][:top_k]
    weights_sparse = np.zeros_like(weights)
    weights_sparse[top_indices] = weights[top_indices]
    weights_sparse = weights_sparse / (weights_sparse.sum() + 1e-8)

    _DB = {
        "vectors": vectors,
        "vectors_norm": vectors_norm,
        "labels": labels,
        "classes": classes,
        "feature_keys": feature_keys,
        "mean": mean,
        "std": std,
        "weights": weights_sparse,
        "top_indices": top_indices,
    }
    return _DB


def knn_scores(graph: SceneGraph, k: int = 7) -> dict[str, float]:
    """Return per-class KNN scores for the image."""
    db = _load_db()
    s = _stats(graph)
    vec = np.array([s.get(fk, 0.0) for fk in db["feature_keys"]], dtype=np.float32)

    vec_norm = (vec - db["mean"]) / (db["std"] + 1e-8)

    diff = db["vectors_norm"] - vec_norm[None, :]
    weighted_diff = diff * np.sqrt(db["weights"])[None, :]
    dists = np.sum(weighted_diff ** 2, axis=1)

    nn_idx = np.argsort(dists)[:k]
    nn_labels = db["labels"][nn_idx]
    nn_dists = dists[nn_idx]

    inv_dists = 1.0 / (nn_dists + 1e-6)
    total = inv_dists.sum()

    scores = {}
    for c_idx, c_name in enumerate(db["classes"]):
        mask = nn_labels == c_idx
        if mask.any():
            scores[c_name] = float(inv_dists[mask].sum() / total)
        else:
            scores[c_name] = 0.0

    return scores
