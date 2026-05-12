# docs/architecture

<!-- RCC-MINI-README:START -->

## Purpose

Canonical architecture locks and architecture-delta documents for HL-ImageNet repository evolution.

## S - Formal specification

This folder stores architecture documents that define contribution boundaries, software deltas, diagnostic contracts, benchmark contracts, attribution contracts, candidate-selection contracts, regression-guard contracts, validation surfaces, falsification surfaces, and non-claim locks before implementation changes are made.

## H - Hooks and integration edges

- `hl_imagenet_rcc_phase2_diagnostic_lens_v1_0.tex` locks the Phase 2.2 diagnostic-lens architecture.
- `hl_imagenet_phase2_benchmark_harness_v1_0.tex` locks the Phase 2.3 benchmark-harness architecture.
- `hl_imagenet_phase2_sample_attribution_v1_0.tex` locks the Phase 2.4 sample-level attribution architecture.
- `hl_imagenet_phase2_candidate_selection_v1_0.tex` locks the Phase 2.5 candidate-selection architecture.
- `hl_imagenet_phase2_regression_guard_v1_0.tex` locks the Phase 2.6A regression-guard architecture.
- `hlinet/eval/diagnostics.py` implements the diagnostic lens.
- `hlinet/eval/benchmark.py` and `hlinet/eval/baselines.py` implement the benchmark harness.
- `hlinet/eval/attribution.py` implements the sample-level attribution layer.
- `hlinet/eval/candidates.py` implements candidate selection.
- `hlinet/eval/regression_guard.py` implements regression guards.
- `logs/phase2/diagnostics/` stores generated diagnostic artifacts.
- `logs/phase2/benchmarks/` stores generated benchmark artifacts.
- `logs/phase2/attribution/` stores generated attribution artifacts.
- `logs/phase2/candidates/` stores generated candidate-selection artifacts.
- `logs/phase2/regression_guard/` stores generated regression-guard artifacts.

## A - Artifacts

- `hl_imagenet_rcc_phase2_diagnostic_lens_v1_0.tex`
- `hl_imagenet_phase2_benchmark_harness_v1_0.tex`
- `hl_imagenet_phase2_sample_attribution_v1_0.tex`
- `hl_imagenet_phase2_candidate_selection_v1_0.tex`
- `hl_imagenet_phase2_regression_guard_v1_0.tex`

## T - Theory or method basis

Architecture locks preserve attribution and prevent implementation drift. In this repo, the architecture layer distinguishes upstream classifier work from RCC/context contributions, diagnostic/evidence tooling, benchmark-comparison tooling, attribution tooling, candidate-selection tooling, regression-guard tooling, and future classifier behavior changes.

## I - Invariants

- Architecture documents must preserve original/upstream attribution.
- Architecture documents must say what is and is not being claimed.
- Architecture documents must not imply runtime changes unless such changes are explicitly implemented.
- Diagnostic architecture does not prove classifier correctness or accuracy improvement.
- Benchmark architecture does not prove final ImageNet performance or imply classifier improvement.
- Attribution architecture does not prove classifier correctness or imply classifier improvement.
- Candidate-selection architecture does not prove classifier correctness or imply classifier improvement.
- Regression-guard architecture does not prove classifier correctness or imply classifier improvement.
- Future classifier changes should receive their own architecture delta before implementation.

## E - Example

Read the Phase 2 diagnostic architecture before changing diagnostics:

    docs/architecture/hl_imagenet_rcc_phase2_diagnostic_lens_v1_0.tex

Read the Phase 2 benchmark architecture before changing benchmarks:

    docs/architecture/hl_imagenet_phase2_benchmark_harness_v1_0.tex

Read the Phase 2 attribution architecture before changing attribution:

    docs/architecture/hl_imagenet_phase2_sample_attribution_v1_0.tex

Read the Phase 2 candidate-selection architecture before changing candidates:

    docs/architecture/hl_imagenet_phase2_candidate_selection_v1_0.tex

Read the Phase 2 regression-guard architecture before changing guards:

    docs/architecture/hl_imagenet_phase2_regression_guard_v1_0.tex

<!-- RCC-MINI-README:END -->