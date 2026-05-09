"""Feature proposer: uses LLM to generate new visual predicate code."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from hlinet.agent.analyzer import ConfusionPair
from hlinet.registry import registry

FEATURE_TEMPLATE = '''\
"""Auto-generated feature: {name}

Generated to help distinguish: {true_class} from {pred_class}
Description: {description}
"""

from __future__ import annotations

import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(
    name="{name}",
    tags={tags},
    description="{description}",
    version="1.0",
)
class {class_name}:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
{body}
'''

SYSTEM_PROMPT = dedent("""\
You are a visual feature engineer for a symbolic image classification system.
You write Python feature classes that evaluate visual predicates on scene graphs.

The scene graph contains atoms of these kinds:
- "edge": contours with descriptors [arc_length, area, aspect_ratio, point_count]
- "contour": shapes with metadata {circularity, solidity, contour}
- "color_region": with metadata {color: str, coverage: float}
- "color_hist": with metadata {dominant_hue_bin, saturation_mean, brightness_mean}
- "texture_patch": with metadata {uniformity, entropy, energy, dominant_orientation}
- "segment": with descriptors [area_frac, eccentricity, solidity, aspect, euler, r, g, b]
- "circle": detected circles with metadata {center, radius}
- "line": detected lines with metadata {angle_deg, length}

Each atom has:
- atom.kind: str
- atom.region: Region (bbox, area_fraction, center, aspect_ratio)
- atom.descriptor: np.ndarray
- atom.confidence: float
- atom.metadata: dict

The Feature must return a FeatureValue:
- FeatureValue.detected(confidence, region=None, evidence=[...])
- FeatureValue.absent("reason")

Write features that are robust, use multiple evidence sources, and have clear
confidence scoring between 0 and 1.
""")


def build_proposal_prompt(confusion: ConfusionPair) -> str:
    """Build a prompt asking the LLM to propose a feature for a confusion pair."""
    existing = [f.name for f in registry.features]

    return dedent(f"""\
    The classifier confuses '{confusion.true_class}' with '{confusion.predicted_class}'.
    This happened {confusion.count} times.

    Existing features: {', '.join(existing)}

    Write a NEW Python feature class that would help distinguish {confusion.true_class}
    from {confusion.predicted_class}. The feature should:
    1. Have a clear visual basis (something you could point to in an image)
    2. Fire strongly for {confusion.true_class} images
    3. NOT fire for {confusion.predicted_class} images
    4. Be robust to viewpoint/lighting changes
    5. Follow the exact Feature class template

    Return ONLY the Python code for the feature class, using the @register_feature decorator.
    """)


def save_generated_feature(code: str, name: str) -> Path:
    """Save a generated feature to the _generated directory."""
    gen_dir = Path(__file__).parent.parent / "features" / "_generated"
    gen_dir.mkdir(parents=True, exist_ok=True)

    filepath = gen_dir / f"{name}.py"
    filepath.write_text(code)
    return filepath
