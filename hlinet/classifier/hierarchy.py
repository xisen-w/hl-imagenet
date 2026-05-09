"""The class hierarchy tree for coarse-to-fine classification.

Phase 1 hierarchy (10 classes):
  root
  ├── animal
  │   ├── zebra
  │   ├── golden_retriever
  │   └── eagle
  ├── vehicle
  │   ├── school_bus
  │   └── bicycle
  ├── food
  │   ├── mushroom
  │   └── banana
  ├── electronics
  │   └── laptop
  ├── instrument
  │   └── piano
  └── container
      └── teapot
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ClassNode:
    name: str
    gate_features: list[str] = field(default_factory=list)
    required_features: list[str] = field(default_factory=list)
    supporting_features: list[str] = field(default_factory=list)
    excluding_features: list[str] = field(default_factory=list)
    children: list[ClassNode] = field(default_factory=list)
    is_leaf: bool = False


def build_phase1_hierarchy() -> ClassNode:
    return ClassNode(
        name="root",
        children=[
            ClassNode(
                name="animal",
                gate_features=["quadruped_like", "bird_like"],
                children=[
                    ClassNode(
                        name="zebra",
                        is_leaf=True,
                        required_features=["striped_texture", "quadruped_like"],
                        supporting_features=["black_white_dominant", "green_context", "bilateral_symmetry"],
                        excluding_features=["wheel_like", "keyboard_pattern"],
                    ),
                    ClassNode(
                        name="golden_retriever",
                        is_leaf=True,
                        required_features=["fur_texture", "quadruped_like"],
                        supporting_features=["golden_brown_color", "green_context"],
                        excluding_features=["striped_texture", "wheel_like"],
                    ),
                    ClassNode(
                        name="eagle",
                        is_leaf=True,
                        required_features=["bird_like"],
                        supporting_features=["bilateral_symmetry", "golden_brown_color"],
                        excluding_features=["wheel_like", "fur_texture", "keyboard_pattern"],
                    ),
                ],
            ),
            ClassNode(
                name="vehicle",
                gate_features=["vehicle_like"],
                children=[
                    ClassNode(
                        name="school_bus",
                        is_leaf=True,
                        required_features=["yellow_dominant", "rectangular_shape"],
                        supporting_features=["wheel_like", "smooth_texture"],
                        excluding_features=["fur_texture", "organic_texture"],
                    ),
                    ClassNode(
                        name="bicycle",
                        is_leaf=True,
                        required_features=["circular_components", "bilateral_symmetry"],
                        supporting_features=["wheel_like", "elongated_shape"],
                        excluding_features=["yellow_dominant", "fur_texture", "keyboard_pattern"],
                    ),
                ],
            ),
            ClassNode(
                name="food",
                gate_features=["food_like"],
                children=[
                    ClassNode(
                        name="mushroom",
                        is_leaf=True,
                        required_features=["organic_texture"],
                        supporting_features=["smooth_texture", "green_context"],
                        excluding_features=["wheel_like", "keyboard_pattern", "yellow_dominant"],
                    ),
                    ClassNode(
                        name="banana",
                        is_leaf=True,
                        required_features=["yellow_dominant", "elongated_shape"],
                        supporting_features=["smooth_texture", "organic_texture"],
                        excluding_features=["wheel_like", "rectangular_shape", "fur_texture"],
                    ),
                ],
            ),
            ClassNode(
                name="electronics",
                gate_features=["rectangular_shape", "screen_rectangle"],
                children=[
                    ClassNode(
                        name="laptop",
                        is_leaf=True,
                        required_features=["screen_rectangle", "keyboard_pattern"],
                        supporting_features=["rectangular_shape", "smooth_texture"],
                        excluding_features=["fur_texture", "organic_texture", "green_context"],
                    ),
                ],
            ),
            ClassNode(
                name="instrument",
                gate_features=["keyboard_pattern"],
                children=[
                    ClassNode(
                        name="piano",
                        is_leaf=True,
                        required_features=["keyboard_pattern", "black_white_dominant"],
                        supporting_features=["rectangular_shape", "smooth_texture"],
                        excluding_features=["screen_rectangle", "fur_texture"],
                    ),
                ],
            ),
            ClassNode(
                name="container",
                gate_features=["handle_spout", "circular_components"],
                children=[
                    ClassNode(
                        name="teapot",
                        is_leaf=True,
                        required_features=["smooth_texture"],
                        supporting_features=["handle_spout", "circular_components"],
                        excluding_features=["wheel_like", "fur_texture", "keyboard_pattern", "yellow_dominant"],
                    ),
                ],
            ),
        ],
    )
