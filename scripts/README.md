# scripts

<!-- RCC-MINI-README:START -->

## Purpose

Human-facing helper scripts for demos, evaluation, prediction, plotting, agent runs, dataset preparation, Phase 2 diagnostics, Phase 2 benchmark comparisons, Phase 2 sample-level attribution, Phase 2 candidate selection, and Phase 2 regression guards.

## S - Formal specification

This folder provides command surfaces that call into the `hlinet` package. Scripts should remain runnable from the repository root and should not hide claim-affecting behavior.

## H - Hooks and integration edges

- `run_eval.py` and `python -m hlinet.eval.runner` call evaluation.
- `predict_image.py` calls the classifier on one image.
- `generate_plots.py` regenerates plot artifacts.
- `run_agent.py` connects to the heuristic-learning loop.
- `run_phase2_diagnostics.py` calls `hlinet.eval.diagnostics`.
- `run_phase2_benchmarks.py` calls `hlinet.eval.benchmark`.
- `run_phase2_attribution.py` calls `hlinet.eval.attribution`.
- `run_phase2_candidates.py` calls `hlinet.eval.candidates`.
- `run_phase2_regression_guard.py` calls `hlinet.eval.regression_guard`.

## A - Artifacts

- `demo.py`
- `download_subset.py`
- `generate_plots.py`
- `predict_image.py`
- `run_agent.py`
- `run_eval.py`
- `run_phase2_diagnostics.py`
- `run_phase2_benchmarks.py`
- `run_phase2_attribution.py`
- `run_phase2_candidates.py`
- `run_phase2_regression_guard.py`

## T - Theory or method basis

Scripts are operational entry points. Diagnostic scripts analyze evidence artifacts; benchmark scripts compare transparent baselines; attribution scripts inspect per-sample behavior; candidate scripts rank future interventions; regression-guard scripts lock the pre-change evidence baseline. None of these should alter classifier runtime behavior.

## I - Invariants

- Keep commands runnable from the repo root.
- Do not change script behavior without updating README command surfaces.
- Evaluation scripts affect public claims.
- Diagnostic scripts must preserve non-claim boundaries and split labels.
- Benchmark scripts must preserve train/validation/test boundaries.
- Attribution scripts must preserve validation/test boundaries and must not imply classifier improvement.
- Candidate-selection scripts must not imply classifier improvement or authorize blind validation tuning.
- Regression-guard scripts must not imply classifier improvement or authorize broad classifier rewrites.

## E - Example

Run Phase 2 diagnostics:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

Run Phase 2 benchmarks:

    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val

Run Phase 2 attribution:

    python scripts/run_phase2_attribution.py --data-root ".\data\phase2" --split val

Run Phase 2 candidates:

    python scripts/run_phase2_candidates.py

Run Phase 2 regression guard:

    python scripts/run_phase2_regression_guard.py

<!-- RCC-MINI-README:END -->