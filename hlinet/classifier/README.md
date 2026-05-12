# hlinet/classifier

<!-- RCC-MINI-README:START -->

## Purpose

Prediction stack for class scoring, pairwise tiebreakers, prototypes, and final classifier output.

## S - Formal specification

This folder contains the final decision path: scoring rules, class prediction, tiebreaker logic, and prototype artifacts.

## H - Hooks and integration edges

Consumes registered features and scene evidence; emits predictions, scores, alternatives, and tiebreaker-adjusted decisions used by evaluation and proof traces.

## A - Artifacts

predict.py, scorer.py, tiebreaker.py, prototypes.npz, __init__.py, and classes subfolder.

## T - Theory or method basis

The classifier is the executable policy in HL terms. It is code, thresholds, required/supporting/excluding rules, and tiebreakers rather than neural weights.

## I - Invariants

- Preserve dev-set versus held-out validation boundaries.
- Do not claim zero learned quantities while prototypes.npz or tuned thresholds exist.
- Tiebreaker changes require regression checks.
- Classifier edits are behavior edits, not documentation-only edits.

## E - Example

After changing scorer.py, predict.py, or tiebreaker.py, run python -m hlinet.eval.runner.

<!-- RCC-MINI-README:END -->
