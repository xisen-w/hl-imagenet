# hlinet/features/primitives

<!-- RCC-MINI-README:START -->

## Purpose

Primitive color and shape features used as base symbolic predicates.

## S - Formal specification

This folder contains low-level features derived directly from sensor/scene evidence, especially color and shape primitives.

## H - Hooks and integration edges

Consumes atoms and scene data; feeds compound features and classifier required/supporting/excluding feature lists.

## A - Artifacts

color_features.py, shape_features.py, and __init__.py.

## T - Theory or method basis

Primitive features are the lowest symbolic layer above raw sensor atoms.

## I - Invariants

- Keep primitives simple and inspectable.
- Do not add class-specific hacks without naming them clearly.
- Preserve downstream compatibility for compound features and scoring rules.

## E - Example

After editing color_features.py or shape_features.py, inspect classifier/scorer.py and run evaluation.

<!-- RCC-MINI-README:END -->
