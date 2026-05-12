# hlinet/features/parts

<!-- RCC-MINI-README:START -->

## Purpose

Structural part detectors and object-part heuristics.

## S - Formal specification

This folder defines features for visually meaningful parts and structural cues.

## H - Hooks and integration edges

Consumes scene and sensor evidence; feeds compound features, classifier scoring, and proof trace explanation.

## A - Artifacts

structural.py and __init__.py.

## T - Theory or method basis

Part features express object structure in symbolic form rather than learned embeddings.

## I - Invariants

- Keep part detectors explainable.
- Avoid turning part features into hidden class labels.
- Validate that structural features help without broad regressions.

## E - Example

Review structural.py together with classifier score rules before changing part semantics.

<!-- RCC-MINI-README:END -->
