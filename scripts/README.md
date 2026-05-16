# scripts

<!-- RCC-MINI-README:START -->

## Purpose

Human-facing helper scripts for demos, evaluation, prediction, plotting, agent runs, and dataset preparation.

## S - Formal specification

This folder provides command surfaces that call into the hlinet package.

## H - Hooks and integration edges

Scripts connect users to hlinet/eval, hlinet/classifier, plotting from logs, dataset download/preparation, demos, and agent orchestration.

## A - Artifacts

demo.py, download_subset.py, generate_plots.py, predict_image.py, run_agent.py, run_eval.py.

## T - Theory or method basis

Scripts are operational entry points; they should preserve the repository's methodology and claim boundaries.

## I - Invariants

- Keep commands runnable from the repo root.
- Do not change script behavior without updating README command surfaces.
- Plot scripts should regenerate artifacts rather than hand-editing outputs.
- Evaluation scripts affect public claims.

## E - Example

Use python scripts/predict_image.py path/to/image.jpg for single-image prediction and python scripts/generate_plots.py for plot regeneration.

<!-- RCC-MINI-README:END -->
