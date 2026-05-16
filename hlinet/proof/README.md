# hlinet/proof

<!-- RCC-MINI-README:START -->

## Purpose

Proof trace generation for human-readable prediction explanations.

## S - Formal specification

This folder renders evidence, alternatives, absent features, and explanatory traces for predictions.

## H - Hooks and integration edges

Consumes classifier outputs, feature activations, and scene evidence; supports debugging, documentation, and interpretability.

## A - Artifacts

trace.py and __init__.py.

## T - Theory or method basis

Proof traces are explanation artifacts for the implemented heuristic policy. They expose why a decision happened but do not prove the decision is correct.

## I - Invariants

- Keep proof traces faithful to actual scoring evidence.
- Do not add explanation text that is not backed by classifier/feature output.
- Update traces when scoring semantics change.

## E - Example

After classifier changes, inspect proof output to ensure explanations still match decisions.

<!-- RCC-MINI-README:END -->
