# hlinet/features/spatial

<!-- RCC-MINI-README:START -->

## Purpose

Grid, layout, and spatial predicate features.

## S - Formal specification

This folder defines features based on image regions, layout, and spatial placement.

## H - Hooks and integration edges

Consumes SceneGraph relations and raw layout cues; feeds classifier scoring and tiebreakers.

## A - Artifacts

grid_features.py, layout_predicates.py, and __init__.py.

## T - Theory or method basis

Spatial features give the symbolic system a structured representation of where evidence appears in the image.

## I - Invariants

- Preserve grid coordinate assumptions.
- Avoid changing layout semantics without checking classes that rely on spatial context.
- Keep spatial predicates human-readable.

## E - Example

After editing grid or layout predicates, run evaluation and inspect proof traces for affected classes.

<!-- RCC-MINI-README:END -->
