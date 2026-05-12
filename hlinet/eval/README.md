# hlinet/eval

<!-- RCC-MINI-README:START -->

## Purpose

Evaluation and evidence-analysis surface for HL-ImageNet. This folder contains dataset loading, metrics, evaluation runner logic, and Phase 2 diagnostic analysis.

## S - Formal specification

This folder defines how images are loaded, predictions are scored, metrics are computed, evaluation reports are emitted, and existing Phase 2 logs are analyzed. The diagnostic lens reads evaluation artifacts; it does not run or modify classifier behavior.

## H - Hooks and integration edges

- `dataset.py` loads Phase 1 and Phase 2 samples.
- `metrics.py` records accuracy, top-k behavior, confusion, latency, and feature reuse.
- `runner.py` orchestrates evaluation and writes logs.
- `diagnostics.py` reads existing Phase 2 eval JSON reports and emits diagnostic JSON/Markdown artifacts.
- `scripts/run_phase2_diagnostics.py` is the human-facing runner for the diagnostic lens.
- Outputs route into `logs/phase1`, `logs/phase2`, and `logs/phase2/diagnostics`.

## A - Artifacts

- `dataset.py`
- `metrics.py`
- `runner.py`
- `diagnostics.py`
- generated evaluation reports under `logs/`
- generated diagnostics under `logs/phase2/diagnostics/`

## T - Theory or method basis

Evaluation methodology is the claim boundary. Development-set, validation-folder, non-overlapping validation, train, validation, test, and external-test results must remain distinct. Phase 2 diagnostics treat classifier failures as a confusion-field geometry: classes can become false-positive attractors, true labels can become victim classes, and repeated true-to-predicted errors form confusion gravity wells.

## I - Invariants

- Do not report development-set accuracy as held-out accuracy.
- Preserve train/validation/test/external labels whenever available.
- Diagnostics do not change classifier behavior.
- Diagnostics do not prove classifier correctness.
- Diagnostics do not imply RCC improved classifier accuracy.
- Metrics changes require README/doc updates.
- Evaluation code changes affect public claims.

## E - Example

Run evaluation:

    python -m hlinet.eval.runner

Run the Phase 2 diagnostic lens:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

<!-- RCC-MINI-README:END -->