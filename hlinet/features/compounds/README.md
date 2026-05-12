# hlinet/features/compounds

<!-- RCC-MINI-README:START -->

## Purpose

Compound feature detectors that combine primitive, spatial, relational, and contextual signals.

## S - Formal specification

This folder creates higher-level symbolic predicates from multiple weaker signals.

## H - Hooks and integration edges

Consumes primitives, textures, spatial predicates, and scene relations; feeds classifier required/supporting/excluding rules.

## A - Artifacts

meta_features.py, relational.py, spatial_attention.py, and __init__.py.

## T - Theory or method basis

Compound features represent the agent's learned heuristic conjunctions and are a key source of both gains and overfitting risk.

## I - Invariants

- Preserve interpretability of conjunctions.
- Do not silently add brittle dev-set thresholds.
- Check regressions because compound features can affect many classes at once.

## E - Example

After editing a compound feature, inspect the changed feature in proof traces and rerun evaluation.

<!-- RCC-MINI-README:END -->
