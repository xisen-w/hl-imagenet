# HL-ImageNet RCC Metrics v1.2

Claim-Lock Density Repair

Generated: 2026-05-13T10:51:39

## Summary

| Metric | Value |
|---|---:|
| artifact_count | 20 |
| existing_artifact_count | 20 |
| mean_claim_lock_score_all_existing | 1.312 |
| mean_claim_lock_score_text | 1.875 |
| mean_claim_lock_score_plots | 0.0 |
| required_lock_count | 8 |
| plot_lock_count | 5 |

## Required claim-lock terms

- does not prove classifier correctness
- does not claim ImageNet performance
- does not imply RCC changed classifier runtime behavior
- does not promote classifier behavior
- not a classifier improvement
- validation evidence is not final test evidence
- repository-process
- non-claim

## Plot-governance claim-lock terms

- plots are process-observability artifacts
- plots are not benchmark results
- plots do not prove classifier correctness
- plots do not claim ImageNet performance
- plots do not imply runtime classifier changes

## Artifact audit

| Path | Type | Exists | Claim-lock score |
|---|---|---:|---:|
| README.md | text | True | 3.75 |
| docs/metrics/README.md | text | True | 1.25 |
| scripts/metrics/README.md | text | True | 1.25 |
| docs/plots/README.md | text | True | 0.0 |
| docs/metrics/rcc_process_metrics.md | text | True | 1.25 |
| docs/metrics/rcc_quality_metrics.md | text | True | 1.25 |
| logs/phase2/diagnostics/latest_phase2_diagnostic.md | text | True | 2.5 |
| logs/phase2/benchmarks/latest_phase2_benchmark.md | text | True | 1.25 |
| logs/phase2/attribution/latest_phase2_attribution.md | text | True | 1.25 |
| logs/phase2/candidates/latest_phase2_candidate_plan.md | text | True | 2.5 |
| logs/phase2/regression_guard/latest_phase2_regression_guard.md | text | True | 2.5 |
| logs/phase2/rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.md | text | True | 2.5 |
| logs/phase2/rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.md | text | True | 2.5 |
| logs/phase2/rejected_deltas/phase2_6e_golden_orange_banana_backstop/rejected_phase2_6e_probe_compare.md | text | True | 2.5 |
| docs/plots/rcc_process_dashboard.png | plot | True | 0.0 |
| docs/plots/rcc_process_timeline.png | plot | True | 0.0 |
| docs/plots/rcc_guard_delta_bars.png | plot | True | 0.0 |
| docs/plots/rcc_quality_dashboard.png | plot | True | 0.0 |
| docs/plots/rcc_artifact_freshness.png | plot | True | 0.0 |
| docs/plots/rcc_probe_directionality.png | plot | True | 0.0 |

## Interpretation

- RCC v1.2 repairs the weakest v1.1 metric by auditing explicit boundary language.
- Text artifacts are scored by direct claim-lock term coverage.
- Plot artifacts are governed through docs/plots/README.md because PNG files cannot carry reliable text-boundary metadata.
- The audit improves process trust without changing classifier runtime behavior.

## Non-claim lock

- Claim-lock audit measures explicit boundary language, not classifier correctness.
- High claim-lock density does not prove the source is correct.
- High claim-lock density does not claim ImageNet performance.
- High claim-lock density does not imply RCC changed classifier runtime behavior.
- Plot claim-locks are governed through docs/plots/README.md because PNG files are binary artifacts.
