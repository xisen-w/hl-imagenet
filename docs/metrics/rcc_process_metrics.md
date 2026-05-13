# HL-ImageNet RCC Process Metrics

Generated: `2026-05-13T11:39:03`

## Summary

| Metric | Value |
|---|---:|
| Phase coverage | 8 / 8 |
| Command coverage | 5 / 5 |
| Boundary coverage | 9 / 9 |
| RCC coverage | 7 / 7 |
| Evidence artifact coverage | 8 / 8 |
| Mini README count | 34 |
| Rejected / failed delta count | 3 |
| Accepted runtime delta count after guard | 0 |

## Dynamic scores

| Dimension | Original reference | Current RCC-governed repo |
|---|---:|---:|
| Navigation Speed | 4.0 | 10.0 |
| Context Fidelity | 5.0 | 10.0 |
| Edit Boundary Clarity | 3.5 | 10.0 |
| Claim Boundary Safety | 6.0 | 10.0 |
| Auditability | 6.5 | 10.0 |
| Agent Efficiency | 4.0 | 10.0 |
| Drift Resistance | 4.0 | 10.0 |
| Onboarding Clarity | 5.0 | 10.0 |
| Evidence Chain Completeness | 3.5 | 10.0 |
| Failure Learning | 2.5 | 10.0 |
| Controlled Evolution | 3.0 | 10.0 |
| Runtime Integrity | 8.0 | 10.0 |

## Probe learning signals

| Probe | Status | Top-1 delta | Top-3 delta | HL-unique wins delta | Baseline-right / HL-wrong delta |
|---|---|---:|---:|---:|---:|
| logs/phase2/rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.md | fail | -0.008500 | -0.005500 | 1.000000 | 18.000000 |
| logs/phase2/rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.md | fail | 0.000500 | 0.001000 | 2.000000 | 1.000000 |
| logs/phase2/rejected_deltas/phase2_6e_golden_orange_banana_backstop/rejected_phase2_6e_probe_compare.md | fail | 0.011000 | -0.000500 | 5.000000 | -17.000000 |

## Interpretation

- RCC is functioning as durable repository memory.
- The repo now exposes navigation, claim boundaries, command surfaces, evidence artifacts, and rejected-delta lessons without needing chat context.
- No accepted runtime classifier delta has been promoted after the guard was installed.
- Rejected probes are becoming useful constraints for the next controlled experiment.

## Non-claim lock

- These metrics measure repository navigation, evidence governance, auditability, and process control.
- These metrics do not prove classifier correctness.
- These metrics do not claim standard ImageNet performance.
- These metrics do not imply RCC changed classifier runtime behavior.
