# hlinet/eval

<!-- RCC-MINI-README:START -->

## Purpose

Evaluation, diagnostics, benchmark comparison, sample-level attribution, candidate selection, and regression-guard surface for HL-ImageNet.

## S - Formal specification

This folder defines how images are loaded, predictions are scored, metrics are computed, evaluation reports are emitted, Phase 2 logs are diagnosed, transparent baselines are compared, individual validation samples are attributed, future classifier-change candidates are ranked, and pre-change regression guardrails are locked.

Diagnostics read evaluation logs. Benchmarks compare models. Attribution reads the local image split and emits per-sample traces. Candidate selection reads diagnostics, benchmarks, and attribution to rank possible future interventions. Regression guards lock pre-change thresholds before classifier deltas. None of these layers change classifier behavior.

## H - Hooks and integration edges

- `dataset.py` loads Phase 1 and Phase 2 samples.
- `metrics.py` records accuracy, top-k behavior, confusion, latency, and feature reuse.
- `runner.py` orchestrates evaluation and writes logs.
- `diagnostics.py` emits diagnostic artifacts.
- `baselines.py` defines transparent non-neural baselines.
- `benchmark.py` compares baselines against the current HL classifier.
- `attribution.py` emits per-sample attribution traces.
- `candidates.py` emits candidate-selection plans.
- `regression_guard.py` emits pre-change regression guard artifacts.
- `scripts/run_phase2_diagnostics.py` runs diagnostics.
- `scripts/run_phase2_benchmarks.py` runs benchmark comparisons.
- `scripts/run_phase2_attribution.py` runs sample-level attribution.
- `scripts/run_phase2_candidates.py` runs candidate selection.
- `scripts/run_phase2_regression_guard.py` runs regression guards.

## A - Artifacts

- `dataset.py`
- `metrics.py`
- `runner.py`
- `diagnostics.py`
- `baselines.py`
- `benchmark.py`
- `attribution.py`
- `candidates.py`
- `regression_guard.py`
- generated evaluation reports under `logs/`
- generated diagnostics under `logs/phase2/diagnostics/`
- generated benchmarks under `logs/phase2/benchmarks/`
- generated attribution traces under `logs/phase2/attribution/`
- generated candidate plans under `logs/phase2/candidates/`
- generated regression guards under `logs/phase2/regression_guard/`

## T - Theory or method basis

Evaluation methodology is the claim boundary. Diagnostics expose aggregate failure geometry. Benchmarks compare the classifier against transparent baselines. Attribution links aggregate failures back to individual images. Candidate selection decides what deserves inspection before classifier changes. Regression guards protect the pre-change evidence baseline before controlled deltas.

## I - Invariants

- Do not report development-set accuracy as held-out accuracy.
- Preserve train/validation/test/external labels.
- Diagnostics do not change classifier behavior.
- Benchmarks do not change classifier behavior.
- Attribution does not change classifier behavior.
- Candidate selection does not change classifier behavior.
- Regression guards do not change classifier behavior.
- None of these layers prove classifier correctness.
- Validation results are not final test results.
- Evaluation code changes affect public claims.

## E - Example

Run evaluation:

    python -m hlinet.eval.runner

Run Phase 2 diagnostics:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

Run Phase 2 benchmarks:

    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val

Run Phase 2 attribution:

    python scripts/run_phase2_attribution.py --data-root ".\data\phase2" --split val

Run Phase 2 candidate selection:

    python scripts/run_phase2_candidates.py

Run Phase 2 regression guard:

    python scripts/run_phase2_regression_guard.py

<!-- RCC-MINI-README:END -->