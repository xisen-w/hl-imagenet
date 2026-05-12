# hlinet/eval

<!-- RCC-MINI-README:START -->

## Purpose

Evaluation, diagnostics, benchmark comparison, and sample-level attribution surface for HL-ImageNet.

## S - Formal specification

This folder defines how images are loaded, predictions are scored, metrics are computed, evaluation reports are emitted, Phase 2 logs are diagnosed, transparent baselines are compared, and individual validation samples are attributed.

Diagnostics read evaluation logs. Benchmarks compare models. Attribution reads the local image split and emits per-sample traces. None of these layers change classifier behavior.

## H - Hooks and integration edges

- `dataset.py` loads Phase 1 and Phase 2 samples.
- `metrics.py` records accuracy, top-k behavior, confusion, latency, and feature reuse.
- `runner.py` orchestrates evaluation and writes logs.
- `diagnostics.py` reads Phase 2 eval JSON reports and emits diagnostic JSON/Markdown artifacts.
- `baselines.py` defines random, majority-class, color-centroid, image-statistics centroid, and handcrafted-stat kNN baselines.
- `benchmark.py` fits baselines on train and compares them against the current HL classifier on the requested split.
- `attribution.py` emits per-sample JSON/CSV/Markdown attribution traces.
- `scripts/run_phase2_diagnostics.py` runs diagnostics.
- `scripts/run_phase2_benchmarks.py` runs benchmark comparisons.
- `scripts/run_phase2_attribution.py` runs sample-level attribution.

## A - Artifacts

- `dataset.py`
- `metrics.py`
- `runner.py`
- `diagnostics.py`
- `baselines.py`
- `benchmark.py`
- `attribution.py`
- generated evaluation reports under `logs/`
- generated diagnostics under `logs/phase2/diagnostics/`
- generated benchmarks under `logs/phase2/benchmarks/`
- generated attribution traces under `logs/phase2/attribution/`

## T - Theory or method basis

Evaluation methodology is the claim boundary. Diagnostics expose aggregate failure geometry. Benchmarks compare the classifier against transparent baselines. Attribution links aggregate failures back to individual images, activated features, proof traces, collapse paths, and baseline-agreement flags.

## I - Invariants

- Do not report development-set accuracy as held-out accuracy.
- Preserve train/validation/test/external labels.
- Diagnostics do not change classifier behavior.
- Benchmarks do not change classifier behavior.
- Attribution does not change classifier behavior.
- Diagnostics do not prove classifier correctness.
- Benchmarks do not prove final ImageNet performance.
- Attribution does not prove classifier correctness.
- Baselines must fit only on train.
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

<!-- RCC-MINI-README:END -->