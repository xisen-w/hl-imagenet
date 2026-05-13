# HL-ImageNet RCC Metrics v1.1

Evidence Quality and Freshness Layer

Generated: 2026-05-13T10:36:41

## Summary

| Metric | Value |
|---|---:|
| artifact_count | 16 |
| existing_artifact_count | 16 |
| probe_count | 3 |
| mean_freshness_score | 10.0 |
| mean_probe_directionality | 5.742 |
| readme_link_integrity_score | 10.0 |
| guard_integrity_score | 10.0 |
| runtime_promotion_safety_score | 10.0 |

## Quality Dimensions

| Dimension | Score |
|---|---:|
| Artifact Existence | 10.0 |
| Artifact Freshness | 10.0 |
| Section Completeness | 10.0 |
| Claim-Lock Density | 5.0 |
| README Link Integrity | 10.0 |
| Regeneration Surface | 10.0 |
| Probe Directionality | 5.742 |
| Probe Claim Locks | 6.0 |
| Guard Integrity | 10.0 |
| Runtime Promotion Safety | 10.0 |
| Artifact Size Health | 10.0 |

## README Link Integrity

| Path | Referenced | Exists | Status |
|---|---:|---:|---|
| docs/metrics/rcc_process_metrics.md | True | True | pass |
| docs/metrics/rcc_process_metrics.json | True | True | pass |
| docs/plots/rcc_process_dashboard.png | True | True | pass |
| docs/plots/rcc_process_timeline.png | True | True | pass |
| docs/plots/rcc_guard_delta_bars.png | True | True | pass |
| scripts/metrics/generate_rcc_process_dashboard.py | True | True | pass |

## Probe Quality

| Probe | Status | Directionality | Top-1 delta | Top-3 delta | HL-unique delta | Baseline-right / HL-wrong delta |
|---|---|---:|---:|---:|---:|---:|
| logs/phase2/rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.md | fail | 0.0 | -0.0085 | -0.0055 | 1.0 | 18.0 |
| logs/phase2/rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.md | fail | 7.225 | 0.0005 | 0.001 | 2.0 | 1.0 |
| logs/phase2/rejected_deltas/phase2_6e_golden_orange_banana_backstop/rejected_phase2_6e_probe_compare.md | fail | 10.0 | 0.011 | -0.0005 | 5.0 | -17.0 |

## Artifact Quality

| Path | Exists | Freshness | Sections | Claim Locks | Size Score |
|---|---:|---:|---:|---:|---:|
| README.md | True | 10.0 | 10.0 | 8.0 | 10.0 |
| docs/metrics/rcc_process_metrics.md | True | 10.0 | 10.0 | 4.4 | 10.0 |
| docs/metrics/rcc_process_metrics.json | True | 10.0 | 10.0 | 6.8 | 10.0 |
| docs/metrics/README.md | True | 10.0 | 10.0 | 3.2 | 10.0 |
| scripts/metrics/generate_rcc_process_dashboard.py | True | 10.0 | 10.0 | 8.0 | 10.0 |
| logs/phase2/diagnostics/latest_phase2_diagnostic.md | True | 10.0 | 10.0 | 5.6 | 10.0 |
| logs/phase2/benchmarks/latest_phase2_benchmark.md | True | 10.0 | 10.0 | 4.4 | 10.0 |
| logs/phase2/attribution/latest_phase2_attribution.md | True | 10.0 | 10.0 | 4.4 | 10.0 |
| logs/phase2/candidates/latest_phase2_candidate_plan.md | True | 10.0 | 10.0 | 5.6 | 10.0 |
| logs/phase2/regression_guard/latest_phase2_regression_guard.md | True | 10.0 | 10.0 | 5.6 | 10.0 |
| logs/phase2/rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.md | True | 10.0 | 10.0 | 5.6 | 10.0 |
| logs/phase2/rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.md | True | 10.0 | 10.0 | 5.6 | 10.0 |
| logs/phase2/rejected_deltas/phase2_6e_golden_orange_banana_backstop/rejected_phase2_6e_probe_compare.md | True | 10.0 | 10.0 | 6.8 | 10.0 |
| docs/plots/rcc_process_dashboard.png | True | 10.0 | 10.0 | 2.0 | 10.0 |
| docs/plots/rcc_process_timeline.png | True | 10.0 | 10.0 | 2.0 | 10.0 |
| docs/plots/rcc_guard_delta_bars.png | True | 10.0 | 10.0 | 2.0 | 10.0 |

## Interpretation

- RCC v1.0 measured coverage.
- RCC v1.1 measures evidence quality, freshness, link integrity, and probe directionality.
- The repository is becoming an evidence-governed process workbench, not just a classifier repository.
- High RCC scores do not prove classifier correctness; they show the process is easier to audit and safer to evolve.

## Non-claim lock

- RCC quality metrics measure repository process quality, not classifier correctness.
- Freshness and coverage are not proof.
- Probe directionality does not imply accepted classifier improvement.
- No runtime classifier delta is promoted by this script.
