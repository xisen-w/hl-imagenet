# logs/phase2

<!-- RCC-MINI-README:START -->

## Purpose

Phase 2 evaluation logs, derived diagnostic artifacts, and benchmark-comparison artifacts for the split-aware 10-real-class Tiny ImageNet experiment.

## S - Formal specification

This folder stores Phase 2 evaluation JSON/Markdown outputs, Phase 2.2 diagnostic reports, and Phase 2.3 benchmark reports. Evaluation logs are source evidence artifacts. Diagnostics and benchmarks are derived analysis artifacts generated from those logs or from the local Phase 2 image split.

## H - Hooks and integration edges

- `hlinet/eval/runner.py` writes Phase 2 evaluation reports here when the tag starts with `phase2`.
- `hlinet/eval/diagnostics.py` reads `eval_phase2*.json` files from this folder.
- `hlinet/eval/benchmark.py` writes benchmark reports into `logs/phase2/benchmarks`.
- `scripts/run_phase2_diagnostics.py` writes outputs into `logs/phase2/diagnostics`.
- `scripts/run_phase2_benchmarks.py` writes outputs into `logs/phase2/benchmarks`.
- README and architecture docs may summarize these outputs, but should not strengthen claims beyond the evidence.

## A - Artifacts

- `eval_phase2_*.json`
- `eval_phase2_*.md`
- `diagnostics/latest_phase2_diagnostic.json`
- `diagnostics/latest_phase2_diagnostic.md`
- `diagnostics/README.md`
- `benchmarks/latest_phase2_benchmark.json`
- `benchmarks/latest_phase2_benchmark.md`
- `benchmarks/README.md`

## T - Theory or method basis

Phase 2 is the split-aware evidence path for the symbolic classifier. The diagnostic lens treats the confusion matrix as a failure-geometry surface where false-positive attractors, victim classes, top-3 rescue gaps, and confusion gravity wells can be measured.

The benchmark harness asks whether the current HL symbolic classifier beats transparent non-neural baselines on the same split before stronger claims or classifier tuning are attempted.

## I - Invariants

- Do not rewrite historical logs to make results look cleaner.
- Preserve tag, split, source report, sample count, and timestamp context.
- Do not treat diagnostic outputs as classifier improvements.
- Do not treat benchmark outputs as classifier improvements.
- Do not treat top-3 rescue as top-1 success.
- Do not promote validation results into final benchmark claims.
- Do not commit local Tiny ImageNet image data.

## E - Example

Generate diagnostic reports from the current Phase 2 validation run:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

Generate benchmark reports from the local Phase 2 image split:

    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val

<!-- RCC-MINI-README:END -->