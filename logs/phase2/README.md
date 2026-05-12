# logs/phase2

<!-- RCC-MINI-README:START -->

## Purpose

Phase 2 evaluation logs, derived diagnostic artifacts, benchmark-comparison artifacts, and sample-level attribution artifacts for the split-aware 10-real-class Tiny ImageNet experiment.

## S - Formal specification

This folder stores Phase 2 evaluation JSON/Markdown outputs, Phase 2.2 diagnostic reports, Phase 2.3 benchmark reports, and Phase 2.4 sample-level attribution reports.

## H - Hooks and integration edges

- `hlinet/eval/runner.py` writes Phase 2 evaluation reports here.
- `hlinet/eval/diagnostics.py` reads `eval_phase2*.json` files and writes diagnostics.
- `hlinet/eval/benchmark.py` writes benchmark reports into `logs/phase2/benchmarks`.
- `hlinet/eval/attribution.py` writes attribution reports into `logs/phase2/attribution`.
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

## T - Theory or method basis

Phase 2 is the split-aware evidence path for the symbolic classifier. Diagnostics expose failure geometry, benchmarks compare against baselines, and attribution shows individual validation rows behind the aggregate results.

## I - Invariants

- Do not rewrite historical logs to make results look cleaner.
- Preserve tag, split, source report, sample count, and timestamp context.
- Do not treat diagnostics as classifier improvements.
- Do not treat benchmarks as classifier improvements.
- Do not treat attribution as classifier improvement or correctness proof.
- Do not treat top-3 rescue as top-1 success.
- Do not promote validation results into final benchmark claims.
- Do not commit local Tiny ImageNet image data.

## E - Example

Generate diagnostic reports:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

Generate benchmark reports:

    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val

Generate attribution reports:

    python scripts/run_phase2_attribution.py --data-root ".\data\phase2" --split val

<!-- RCC-MINI-README:END -->