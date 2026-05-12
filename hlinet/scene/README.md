# hlinet/scene

<!-- RCC-MINI-README:START -->

## Purpose

Scene graph construction and spatial relation extraction.

## S - Formal specification

This folder turns sensor atoms into a SceneGraph and computes spatial relations such as above, below, left_of, right_of, contains, inside, adjacent, and similar_size.

## H - Hooks and integration edges

Consumes hlinet/sensors outputs and feeds hlinet/features, hlinet/classifier, hlinet/proof, and tiebreakers that need spatial evidence.

## A - Artifacts

builder.py, relations.py, and __init__.py.

## T - Theory or method basis

Scene graphs provide the symbolic state representation used by heuristic learning: not raw pixels alone, but atoms plus spatial organization.

## I - Invariants

- Preserve relation semantics.
- Do not make final class decisions in scene construction.
- Keep raw_image access stable for downstream tiebreakers and proof logic.
- Spatial changes must be checked for regressions.

## E - Example

Inspect hlinet/scene/relations.py before editing spatial relation thresholds, then run evaluation.

<!-- RCC-MINI-README:END -->
