"""Phase 2 class hierarchy: 10 real Tiny ImageNet classes.

Flat structure (no hierarchical gates) — all classes scored simultaneously.
Each class uses a phase2_*_signature feature as its required feature.
Supporting features are kept minimal to avoid broad features dominating.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ClassNode:
    name: str
    gate_features: list[str] = field(default_factory=list)
    required_features: list[str] = field(default_factory=list)
    required_alternatives: list[list[str]] = field(default_factory=list)
    supporting_features: list[str] = field(default_factory=list)
    excluding_features: list[str] = field(default_factory=list)
    children: list[ClassNode] = field(default_factory=list)
    is_leaf: bool = False


def build_phase1_hierarchy() -> ClassNode:
    """Build the Phase 2 hierarchy (name kept for predict.py compatibility)."""
    return ClassNode(
        name="root",
        children=[
            ClassNode(
                name="golden_retriever",
                is_leaf=True,
                required_features=["phase2_golden_retriever_signature"],
                supporting_features=["golden_fur_in_nature", "quadruped_like"],
                excluding_features=["phase2_jellyfish_signature"],
            ),
            ClassNode(
                name="mushroom",
                is_leaf=True,
                required_features=["phase2_mushroom_signature"],
                supporting_features=["green_context", "blob_textured_interior"],
            ),
            ClassNode(
                name="teapot",
                is_leaf=True,
                required_features=["phase2_teapot_signature"],
                supporting_features=["distinct_background"],
            ),
            ClassNode(
                name="school_bus",
                is_leaf=True,
                required_features=["phase2_school_bus_signature"],
                supporting_features=["horizontal_window_pattern", "yellow_body_with_sky"],
                excluding_features=["phase2_jellyfish_signature"],
            ),
            ClassNode(
                name="banana",
                is_leaf=True,
                required_features=["phase2_banana_signature"],
                supporting_features=["yellow_dominant"],
                excluding_features=["phase2_jellyfish_signature"],
            ),
            ClassNode(
                name="orange",
                is_leaf=True,
                required_features=["phase2_orange_signature"],
            ),
            ClassNode(
                name="brown_bear",
                is_leaf=True,
                required_features=["phase2_brown_bear_signature"],
                supporting_features=["quadruped_like", "green_context"],
            ),
            ClassNode(
                name="king_penguin",
                is_leaf=True,
                required_features=["phase2_king_penguin_signature"],
                excluding_features=["yellow_dominant", "green_context", "golden_fur_in_nature"],
            ),
            ClassNode(
                name="jellyfish",
                is_leaf=True,
                required_features=["phase2_jellyfish_signature"],
                excluding_features=["golden_brown_color", "yellow_dominant"],
            ),
            ClassNode(
                name="sports_car",
                is_leaf=True,
                required_features=["phase2_sports_car_signature"],
                supporting_features=["rectangular_shape"],
            ),
        ],
    )
