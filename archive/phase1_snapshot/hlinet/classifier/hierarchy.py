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
    required_alternatives: list[list[str]] = field(default_factory=list)
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
                        required_features=["striped_texture", "pure_vertical_stripes"],
                        supporting_features=["black_white_dominant", "quadruped_like", "green_context", "repeated_vertical_lines", "stripes_with_nature", "outdoor_animal_scene"],
                        excluding_features=["wheel_like", "keyboard_pattern", "yellow_dominant", "yellow_center_mass", "bw_keys_indoor", "yellow_body_with_sky", "horizontal_window_pattern"],
                    ),
                    ClassNode(
                        name="golden_retriever",
                        is_leaf=True,
                        required_features=["golden_brown_color"],
                        required_alternatives=[["organic_texture"]],
                        supporting_features=["quadruped_like", "fur_texture", "green_context", "golden_fur_in_nature", "outdoor_animal_scene", "large_warm_blob", "blob_smooth_interior", "blob_hue_uniform"],
                        excluding_features=["striped_texture", "keyboard_pattern", "uniform_background", "round_object_on_surface", "yellow_body_with_sky", "horizontal_window_pattern", "pure_vertical_stripes", "distinct_background", "bottom_detail_bright_cap", "top_textured_bottom_plain", "teapot_on_table"],
                    ),
                    ClassNode(
                        name="eagle",
                        is_leaf=True,
                        required_features=["bird_like"],
                        supporting_features=["bilateral_symmetry", "golden_brown_color", "sky_above_object"],
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
                        required_features=["horizontal_window_pattern"],
                        supporting_features=["yellow_center_mass", "sky_above_object", "yellow_dominant", "rectangular_shape", "yellow_body_with_sky"],
                        excluding_features=["fur_texture", "green_context", "round_object_on_surface", "pure_vertical_stripes"],
                    ),
                    ClassNode(
                        name="bicycle",
                        is_leaf=True,
                        required_features=["wheel_like"],
                        supporting_features=["circular_components", "bilateral_symmetry", "elongated_shape"],
                        excluding_features=["yellow_dominant", "fur_texture", "keyboard_pattern", "yellow_body_with_sky", "horizontal_window_pattern", "bottom_detail_bright_cap"],
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
                        supporting_features=["uniform_background", "top_heavy_blob", "round_object_on_surface", "bottom_detail_bright_cap", "blob_textured_interior", "indoor_still_object"],
                        excluding_features=["wheel_like", "keyboard_pattern", "yellow_dominant", "striped_texture", "sky_above_object", "yellow_center_mass", "golden_fur_in_nature", "outdoor_animal_scene", "horizontal_window_pattern", "yellow_body_with_sky", "top_textured_bottom_plain", "blob_smooth_interior"],
                    ),
                    ClassNode(
                        name="banana",
                        is_leaf=True,
                        required_features=["yellow_dominant"],
                        supporting_features=["curved_elongated_yellow", "uniform_background", "elongated_shape", "organic_texture"],
                        excluding_features=["wheel_like", "rectangular_shape", "fur_texture", "sky_above_object", "yellow_body_with_sky", "bottom_detail_bright_cap", "golden_fur_in_nature", "outdoor_animal_scene", "round_object_on_surface", "distinct_background", "horizontal_window_pattern", "quadruped_like"],
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
                        required_features=["large_dark_rectangle_center"],
                        supporting_features=["screen_rectangle", "keyboard_pattern", "rectangular_shape"],
                        excluding_features=["fur_texture", "organic_texture", "green_context", "yellow_dominant"],
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
                        required_features=["repeated_vertical_lines", "black_white_dominant"],
                        supporting_features=["keyboard_pattern", "rectangular_shape", "bw_keys_indoor"],
                        excluding_features=["screen_rectangle", "fur_texture", "golden_brown_color", "yellow_dominant", "sky_above_object", "green_context", "stripes_with_nature", "outdoor_animal_scene", "pure_vertical_stripes"],
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
                        required_features=["organic_texture"],
                        supporting_features=["handle_spout", "circular_components", "uniform_background", "spout_handle_shape", "round_object_on_surface", "distinct_background", "top_textured_bottom_plain", "teapot_on_table", "indoor_still_object"],
                        excluding_features=["wheel_like", "fur_texture", "keyboard_pattern", "yellow_dominant", "striped_texture", "sky_above_object", "yellow_center_mass", "golden_fur_in_nature", "outdoor_animal_scene", "warm_color_dominated", "horizontal_window_pattern", "yellow_body_with_sky", "bottom_detail_bright_cap", "blob_smooth_interior"],
                    ),
                ],
            ),
        ],
    )
