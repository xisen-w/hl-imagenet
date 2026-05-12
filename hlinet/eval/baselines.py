"""Transparent non-neural baselines for HL-ImageNet Phase 2.

These baselines are intentionally simple. They exist to answer whether the
current symbolic classifier beats trivial or low-complexity non-neural
comparators on the same split.

No function in this module changes classifier behavior.
"""

from __future__ import annotations

import math
import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Protocol

import cv2
import numpy as np

from hlinet.eval.dataset import Sample


@dataclass
class BaselinePrediction:
    label: str
    ranked_labels: list[str]
    latency_ms: float


class BaselineModel(Protocol):
    name: str

    def fit(self, samples: list[Sample]) -> None:
        ...

    def predict(self, image: np.ndarray, path: str | None = None) -> BaselinePrediction:
        ...


def safe_imread(path) -> np.ndarray | None:
    return cv2.imread(str(path))


def color_feature(image: np.ndarray) -> np.ndarray:
    small = cv2.resize(image, (32, 32), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    bgr_mean = small.reshape(-1, 3).mean(axis=0)
    bgr_std = small.reshape(-1, 3).std(axis=0)
    hsv_mean = hsv.reshape(-1, 3).mean(axis=0)
    hist_h = cv2.calcHist([hsv], [0], None, [8], [0, 180]).flatten()
    hist_h = hist_h / max(hist_h.sum(), 1.0)
    return np.concatenate([bgr_mean, bgr_std, hsv_mean, hist_h]).astype(np.float32)


def stats_feature(image: np.ndarray) -> np.ndarray:
    small = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)

    bgr = small.reshape(-1, 3)
    hsv_flat = hsv.reshape(-1, 3)

    bgr_mean = bgr.mean(axis=0)
    bgr_std = bgr.std(axis=0)
    hsv_mean = hsv_flat.mean(axis=0)
    hsv_std = hsv_flat.std(axis=0)

    edges = cv2.Canny(gray, 80, 160)
    edge_density = np.array([edges.mean() / 255.0], dtype=np.float32)

    lap_var = np.array([cv2.Laplacian(gray, cv2.CV_64F).var() / 10000.0], dtype=np.float32)

    h, w = gray.shape
    left = gray[:, : w // 2].astype(np.float32)
    right = cv2.flip(gray[:, w - w // 2 :], 1).astype(np.float32)
    min_w = min(left.shape[1], right.shape[1])
    symmetry = 1.0 - np.mean(np.abs(left[:, :min_w] - right[:, :min_w])) / 255.0
    symmetry = np.array([symmetry], dtype=np.float32)

    hist_h = cv2.calcHist([hsv], [0], None, [8], [0, 180]).flatten()
    hist_h = hist_h / max(hist_h.sum(), 1.0)

    hist_s = cv2.calcHist([hsv], [1], None, [4], [0, 256]).flatten()
    hist_s = hist_s / max(hist_s.sum(), 1.0)

    raw = np.concatenate([
        bgr_mean / 255.0,
        bgr_std / 255.0,
        hsv_mean / np.array([180.0, 255.0, 255.0]),
        hsv_std / np.array([180.0, 255.0, 255.0]),
        edge_density,
        lap_var,
        symmetry,
        hist_h,
        hist_s,
    ]).astype(np.float32)

    return np.nan_to_num(raw, nan=0.0, posinf=0.0, neginf=0.0)


def _normalize_matrix(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    std[std < 1e-6] = 1.0
    return (x - mean) / std, mean, std


class RandomBaseline:
    name = "random"

    def __init__(self, classes: list[str], seed: int = 42):
        self.classes = list(classes)
        self.seed = seed

    def fit(self, samples: list[Sample]) -> None:
        return None

    def predict(self, image: np.ndarray, path: str | None = None) -> BaselinePrediction:
        start = time.perf_counter()
        key = str(path) if path is not None else str(image.shape)
        rng = random.Random(f"{self.seed}:{key}")
        ranked = list(self.classes)
        rng.shuffle(ranked)
        latency_ms = (time.perf_counter() - start) * 1000.0
        return BaselinePrediction(ranked[0], ranked, latency_ms)


class MajorityBaseline:
    name = "majority_class"

    def __init__(self, classes: list[str]):
        self.classes = list(classes)
        self.ranked = list(classes)

    def fit(self, samples: list[Sample]) -> None:
        counts = Counter(sample.label for sample in samples)
        self.ranked = sorted(self.classes, key=lambda c: (-counts.get(c, 0), c))

    def predict(self, image: np.ndarray, path: str | None = None) -> BaselinePrediction:
        start = time.perf_counter()
        latency_ms = (time.perf_counter() - start) * 1000.0
        return BaselinePrediction(self.ranked[0], self.ranked, latency_ms)


class CentroidBaseline:
    def __init__(self, name: str, classes: list[str], feature_fn):
        self.name = name
        self.classes = list(classes)
        self.feature_fn = feature_fn
        self.centroids: dict[str, np.ndarray] = {}
        self.mean: np.ndarray | None = None
        self.std: np.ndarray | None = None

    def fit(self, samples: list[Sample]) -> None:
        vectors = []
        labels = []

        for sample in samples:
            image = safe_imread(sample.path)
            if image is None:
                continue
            vectors.append(self.feature_fn(image))
            labels.append(sample.label)

        if not vectors:
            raise RuntimeError(f"{self.name}: no readable train images")

        x = np.vstack(vectors).astype(np.float32)
        x_norm, self.mean, self.std = _normalize_matrix(x)

        grouped: dict[str, list[np.ndarray]] = defaultdict(list)
        for label, vec in zip(labels, x_norm):
            grouped[label].append(vec)

        for cls in self.classes:
            if grouped.get(cls):
                self.centroids[cls] = np.vstack(grouped[cls]).mean(axis=0)

    def predict(self, image: np.ndarray, path: str | None = None) -> BaselinePrediction:
        start = time.perf_counter()
        vec = self.feature_fn(image).astype(np.float32)

        if self.mean is not None and self.std is not None:
            vec = (vec - self.mean) / self.std

        distances = []
        for cls in self.classes:
            centroid = self.centroids.get(cls)
            if centroid is None:
                dist = float("inf")
            else:
                dist = float(np.linalg.norm(vec - centroid))
            distances.append((cls, dist))

        distances.sort(key=lambda item: item[1])
        ranked = [cls for cls, _ in distances]
        latency_ms = (time.perf_counter() - start) * 1000.0
        return BaselinePrediction(ranked[0], ranked, latency_ms)


class KNNBaseline:
    name = "handcrafted_stats_knn"

    def __init__(self, classes: list[str], k: int = 5):
        self.classes = list(classes)
        self.k = k
        self.x: np.ndarray | None = None
        self.y: list[str] = []
        self.mean: np.ndarray | None = None
        self.std: np.ndarray | None = None

    def fit(self, samples: list[Sample]) -> None:
        vectors = []
        labels = []

        for sample in samples:
            image = safe_imread(sample.path)
            if image is None:
                continue
            vectors.append(stats_feature(image))
            labels.append(sample.label)

        if not vectors:
            raise RuntimeError("handcrafted_stats_knn: no readable train images")

        x = np.vstack(vectors).astype(np.float32)
        self.x, self.mean, self.std = _normalize_matrix(x)
        self.y = labels

    def predict(self, image: np.ndarray, path: str | None = None) -> BaselinePrediction:
        start = time.perf_counter()

        if self.x is None or self.mean is None or self.std is None:
            raise RuntimeError("KNNBaseline must be fit before predict")

        vec = stats_feature(image).astype(np.float32)
        vec = (vec - self.mean) / self.std

        dists = np.linalg.norm(self.x - vec, axis=1)
        idx = np.argsort(dists)[: max(self.k, 1)]

        votes: Counter[str] = Counter()
        for rank, i in enumerate(idx):
            label = self.y[int(i)]
            weight = 1.0 / (float(dists[int(i)]) + 1e-6)
            votes[label] += weight

        ranked = [cls for cls, _ in votes.most_common()]
        for cls in self.classes:
            if cls not in ranked:
                ranked.append(cls)

        latency_ms = (time.perf_counter() - start) * 1000.0
        return BaselinePrediction(ranked[0], ranked, latency_ms)


def make_default_baselines(classes: list[str]) -> list[BaselineModel]:
    return [
        RandomBaseline(classes),
        MajorityBaseline(classes),
        CentroidBaseline("color_centroid", classes, color_feature),
        CentroidBaseline("image_stats_centroid", classes, stats_feature),
        KNNBaseline(classes, k=5),
    ]