# hlinet/eval

<!-- RCC-MINI-README:START -->

## Purpose

Evaluation, diagnostics, and benchmark-comparison surface for HL-ImageNet. This folder contains dataset loading, metrics, evaluation runner logic, Phase 2 diagnostic analysis, and Phase 2 non-neural baseline benchmarking.

## S - Formal specification

This folder defines how images are loaded, predictions are scored, metrics are computed, evaluation reports are emitted, existing Phase 2 logs are analyzed, and transparent baselines are compared against the current HL symbolic classifier.

The diagnostic lens reads evaluation artifacts. The benchmark harness reads local image splits and compares models. Neither layer changes classifier behavior.

## H - Hooks and integration edges

- `dataset.py` loads Phase 1 and Phase 2 samples.
- `metrics.py` records accuracy, top-k behavior, confusion, latency, and feature reuse.
- `runner.py` orchestrates evaluation and writes logs.
- `diagnostics.py` reads existing Phase 2 eval JSON reports and emits diagnostic JSON/Markdown artifacts.
- `baselines.py` defines random, majority-class, color-centroid, image-statistics centroid, and handcrafted-stat kNN baselines.
- `benchmark.py` fits baselines on the train split and compares them against the current HL classifier on the requested split.
- `scripts/run_phase2_diagnostics.py` is the human-facing runner for diagnostics.
- `scripts/run_phase2_benchmarks.py` is the human-facing runner for benchmark comparisons.
- Outputs route into `logs/phase1`, `logs/phase2`, `logs/phase2/diagnostics`, and `logs/phase2/benchmarks`.

## A - Artifacts

- `dataset.py`
- `metrics.py`
- `runner.py`
- `diagnostics.py`
- `baselines.py`
- `benchmark.py`
- generated evaluation reports under `logs/`
- generated diagnostics under `logs/phase2/diagnostics/`
- generated benchmark reports under `logs/phase2/benchmarks/`

## T - Theory or method basis

Evaluation methodology is the claim boundary. Development-set, validation-folder, non-overlapping validation, train, validation, test, and external-test results must remain distinct.

Phase 2 diagnostics treat classifier failures as a confusion-field geometry: classes can become false-positive attractors, true labels can become victim classes, and repeated true-to-predicted errors form confusion gravity wells.

Phase 2 benchmarks compare the current HL symbolic classifier against transparent non-neural baselines on the same split before any stronger performance claim is made.

## I - Invariants

- Do not report development-set accuracy as held-out accuracy.
- Preserve train/validation/test/external labels whenever available.
- Diagnostics do not change classifier behavior.
- Benchmarks do not change classifier behavior.
- Diagnostics do not prove classifier correctness.
- Benchmarks do not prove final ImageNet performance.
- Benchmark tooling does not imply classifier improvement.
- Baselines must fit only on the train split.
- Validation results are not final test results.
- Metrics changes require README/doc updates.
- Evaluation code changes affect public claims.

## E - Example

Run evaluation:

    python -m hlinet.eval.runner

Run the Phase 2 diagnostic lens:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

Run the Phase 2 benchmark harness:

    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val

<!-- RCC-MINI-README:END -->