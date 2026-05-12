# scripts

<!-- RCC-MINI-README:START -->

## Purpose

Human-facing helper scripts for demos, evaluation, prediction, plotting, agent runs, dataset preparation, Phase 2 diagnostics, and Phase 2 benchmark comparisons.

## S - Formal specification

This folder provides command surfaces that call into the `hlinet` package. Scripts should remain runnable from the repository root and should not hide claim-affecting behavior.

## H - Hooks and integration edges

- `run_eval.py` and `python -m hlinet.eval.runner` call evaluation.
- `predict_image.py` calls the classifier on one image.
- `generate_plots.py` regenerates plot artifacts.
- `run_agent.py` connects to the heuristic-learning loop.
- `run_phase2_diagnostics.py` calls `hlinet.eval.diagnostics` and emits reports under `logs/phase2/diagnostics`.
- `run_phase2_benchmarks.py` calls `hlinet.eval.benchmark` and emits reports under `logs/phase2/benchmarks`.

## A - Artifacts

- `demo.py`
- `download_subset.py`
- `generate_plots.py`
- `predict_image.py`
- `run_agent.py`
- `run_eval.py`
- `run_phase2_diagnostics.py`
- `run_phase2_benchmarks.py`

## T - Theory or method basis

Scripts are operational entry points. They should preserve the repository's methodology and claim boundaries. Diagnostic scripts analyze evidence artifacts; benchmark scripts compare transparent baselines against the current classifier; neither should alter classifier runtime behavior.

## I - Invariants

- Keep commands runnable from the repo root.
- Do not change script behavior without updating README command surfaces.
- Plot scripts should regenerate artifacts rather than hand-editing outputs.
- Evaluation scripts affect public claims.
- Diagnostic scripts must preserve non-claim boundaries and split labels.
- Benchmark scripts must preserve train/validation/test boundaries.
- Benchmark scripts must not imply classifier improvement.

## E - Example

Run Phase 2 diagnostics:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

Run Phase 2 benchmarks:

    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val

<!-- RCC-MINI-README:END -->