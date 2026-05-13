# logs/phase2

<!-- RCC-MINI-README:START -->

## Purpose

Phase 2 evaluation logs, derived diagnostic artifacts, benchmark-comparison artifacts, sample-level attribution artifacts, candidate-selection artifacts, and regression-guard artifacts, and rejected-delta and rejected-probe artifacts for the split-aware 10-real-class Tiny ImageNet experiment.

## S - Formal specification

This folder stores Phase 2 evaluation JSON/Markdown outputs, Phase 2.2 diagnostic reports, Phase 2.3 benchmark reports, Phase 2.4 sample-level attribution reports, Phase 2.5 candidate-selection plans, and Phase 2.6A regression-guard baselines, and Phase 2.6C rejected-delta ledgers.

## H - Hooks and integration edges

- `hlinet/eval/runner.py` writes Phase 2 evaluation reports here.
- `hlinet/eval/diagnostics.py` writes diagnostics.
- `hlinet/eval/benchmark.py` writes benchmark reports.
- `hlinet/eval/attribution.py` writes attribution reports.
- `hlinet/eval/candidates.py` writes candidate plans.
- `hlinet/eval/regression_guard.py` writes regression guards.
- README and architecture docs may summarize these outputs, but should not strengthen claims beyond the evidence.

## A - Artifacts

- `eval_phase2_*.json`
- `eval_phase2_*.md`
- `diagnostics/latest_phase2_diagnostic.json`
- `diagnostics/latest_phase2_diagnostic.md`
- `benchmarks/latest_phase2_benchmark.json`
- `benchmarks/latest_phase2_benchmark.md`
- `attribution/latest_phase2_attribution.json`
- `attribution/latest_phase2_attribution.csv`
- `attribution/latest_phase2_attribution.md`
- `candidates/latest_phase2_candidate_plan.json`
- `candidates/latest_phase2_candidate_plan.md`
- `regression_guard/latest_phase2_regression_guard.json`
- `regression_guard/latest_phase2_regression_guard.md`
- `rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.json`
- `rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.md`
- `rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.json`
- `rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.md`

## T - Theory or method basis

Phase 2 is the split-aware evidence path for the symbolic classifier. Diagnostics expose failure geometry, benchmarks compare against baselines, attribution shows individual validation rows, candidate selection ranks future intervention candidates, regression guards lock the baseline before controlled classifier deltas, rejected-delta ledgers preserve failed experiments without promoting them, and rejected-probe ledgers preserve near-miss class-specific experiments without promoting them.

## I - Invariants

- Do not rewrite historical logs to make results look cleaner.
- Preserve tag, split, source report, sample count, and timestamp context.
- Do not treat diagnostics as classifier improvements.
- Do not treat benchmarks as classifier improvements.
- Do not treat attribution as classifier improvement or correctness proof.
- Do not treat candidate selection as classifier improvement or correctness proof.
- Do not treat regression guards as classifier improvement or correctness proof.
- Do not treat rejected-delta ledgers as classifier improvement or correctness proof.
- Do not promote validation results into final benchmark claims.
- Do not commit local Tiny ImageNet image data.

## E - Example

Generate diagnostic reports:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

Generate benchmark reports:

    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val

Generate attribution reports:

    python scripts/run_phase2_attribution.py --data-root ".\data\phase2" --split val

Generate candidate plans:

    python scripts/run_phase2_candidates.py

Generate regression guards:

    python scripts/run_phase2_regression_guard.py

<!-- RCC-MINI-README:END -->