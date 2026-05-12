# hlinet/features

<!-- RCC-MINI-README:START -->

## Purpose

Feature registry surface for symbolic predicates used by classifier scoring and proof traces.

## S - Formal specification

This folder organizes primitive, texture, part, spatial, compound, and high-level concept detectors. Features should convert scene/sensor evidence into named scores usable by the classifier.

## H - Hooks and integration edges

Consumes hlinet/scene and hlinet/sensors outputs; feeds hlinet/classifier/scorer.py and hlinet/proof/trace.py through registered feature names.

## A - Artifacts

__init__.py plus subfolders _generated, primitives, textures, parts, spatial, compounds, and concepts.

## T - Theory or method basis

Feature predicates are the main symbolic representation layer. They encode the heuristic concepts the agent iteratively refined.

## I - Invariants

- Keep feature names stable unless classifier configs and proof traces are updated.
- Do not hide overfitting by adding undocumented thresholds.
- Preserve readable feature evidence.
- Feature changes must be evaluated against validation boundaries.

## E - Example

Before changing a feature, locate where its name is used in classifier scoring and proof output.

<!-- RCC-MINI-README:END -->
