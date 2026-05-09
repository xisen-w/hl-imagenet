"""Feature quality gate: test proposed features before accepting them."""

from __future__ import annotations

import importlib.util
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from hlinet.eval.dataset import Sample
from hlinet.scene.builder import SceneGraphBuilder
from hlinet.types import Feature, FeatureValue


@dataclass
class QualityReport:
    name: str
    passes: bool
    information_gain: float
    robustness: float
    mean_latency_ms: float
    fires_positive: float  # % of positive class images where it fires
    fires_negative: float  # % of negative class images where it fires
    errors: list[str]


def test_feature(
    feature_path: Path,
    positive_samples: list[Sample],
    negative_samples: list[Sample],
    min_info_gain: float = 0.1,
    min_robustness: float = 0.5,
    max_latency_ms: float = 200.0,
) -> QualityReport:
    """Test a generated feature against quality gates."""
    builder = SceneGraphBuilder()
    errors = []

    # Try to load the feature
    try:
        spec = importlib.util.spec_from_file_location("_test_feature", feature_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        return QualityReport(
            name=feature_path.stem, passes=False,
            information_gain=0, robustness=0, mean_latency_ms=0,
            fires_positive=0, fires_negative=0,
            errors=[f"Import failed: {e}"],
        )

    # Find the registered feature
    from hlinet.registry import registry
    feature = None
    for f in registry.features:
        if f.name == feature_path.stem:
            feature = f
            break

    if feature is None:
        return QualityReport(
            name=feature_path.stem, passes=False,
            information_gain=0, robustness=0, mean_latency_ms=0,
            fires_positive=0, fires_negative=0,
            errors=["Feature not registered after import"],
        )

    # Evaluate on positive and negative samples
    pos_fires = 0
    neg_fires = 0
    latencies = []

    for sample in positive_samples[:20]:
        image = cv2.imread(str(sample.path))
        if image is None:
            continue
        graph = builder.build(image)
        start = time.time()
        try:
            val = feature.evaluate(graph)
            latencies.append((time.time() - start) * 1000)
            if val.present and val.confidence > 0.3:
                pos_fires += 1
        except Exception as e:
            errors.append(f"Error on positive: {e}")

    for sample in negative_samples[:20]:
        image = cv2.imread(str(sample.path))
        if image is None:
            continue
        graph = builder.build(image)
        start = time.time()
        try:
            val = feature.evaluate(graph)
            latencies.append((time.time() - start) * 1000)
            if val.present and val.confidence > 0.3:
                neg_fires += 1
        except Exception as e:
            errors.append(f"Error on negative: {e}")

    n_pos = min(len(positive_samples), 20)
    n_neg = min(len(negative_samples), 20)
    fires_pos = pos_fires / max(n_pos, 1)
    fires_neg = neg_fires / max(n_neg, 1)

    # Information gain: how well does it separate classes
    info_gain = fires_pos - fires_neg

    # Robustness: would need perturbation tests (simplified here)
    robustness = fires_pos if fires_pos > 0 else 0.0

    mean_latency = np.mean(latencies) if latencies else 999.0

    passes = (
        info_gain >= min_info_gain
        and robustness >= min_robustness
        and mean_latency <= max_latency_ms
        and len(errors) == 0
    )

    return QualityReport(
        name=feature_path.stem,
        passes=passes,
        information_gain=info_gain,
        robustness=robustness,
        mean_latency_ms=mean_latency,
        fires_positive=fires_pos,
        fires_negative=fires_neg,
        errors=errors,
    )
