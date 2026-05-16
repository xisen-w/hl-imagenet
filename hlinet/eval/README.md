# hlinet/eval

<!-- RCC-MINI-README:START -->

## Purpose

Evaluation harness for dataset loading, metrics, and evaluation execution.

## S - Formal specification

This folder defines how images are loaded, predictions are scored, metrics are computed, and evaluation runs are executed.

## H - Hooks and integration edges

Consumes hlinet/classifier predictions and dataset paths; writes or supports logs under logs/phase1 and future phase outputs.

## A - Artifacts

dataset.py, metrics.py, runner.py, and __init__.py.

## T - Theory or method basis

Evaluation methodology is the claim boundary. Development-set, validation-folder, non-overlapping validation, and Phase 2 split-clean metrics must remain distinct.

## I - Invariants

- Do not report development-set accuracy as held-out accuracy.
- Preserve overlap and split caveats.
- Metrics changes require README/doc updates.
- Evaluation code changes affect public claims.

## E - Example

Run python -m hlinet.eval.runner after changing dataset, metrics, or runner behavior.

<!-- RCC-MINI-README:END -->
