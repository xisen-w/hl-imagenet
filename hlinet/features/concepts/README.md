# hlinet/features/concepts

<!-- RCC-MINI-README:START -->

## Purpose

High-level concept detectors layered above primitive and compound visual signals.

## S - Formal specification

This folder contains features that approximate broader object or scene concepts.

## H - Hooks and integration edges

Consumes lower-level and compound features; feeds classifier scoring and explanations.

## A - Artifacts

high_level.py and __init__.py.

## T - Theory or method basis

Concept detectors are symbolic summaries, not neural concepts or embeddings.

## I - Invariants

- Keep concept names honest and bounded.
- Do not present concept detection as semantic understanding beyond the implemented heuristic.
- Update classifier and proof expectations if concept names change.

## E - Example

Read high_level.py before changing any class-facing concept predicate.

<!-- RCC-MINI-README:END -->
