# HL-ImageNet Phase 2.6D Probe Comparison

Generated: `2026-05-13T09:07:19`
Probe: `golden_retriever_orange_signature_exclusion`
Overall status: `fail`

## Pre vs post

| Metric | Pre | Post | Delta |
|---|---:|---:|---:|
| Top-1 | 0.334 | 0.3345 | 0.000500 |
| Top-3 | 0.6865 | 0.6875 | 0.001000 |
| HL-unique wins | 68 | 70 | 2.000000 |
| Baseline-right / HL-wrong | 817 | 818 | 1.000000 |

## Guard checks

| Check | Value | Threshold | Status |
|---|---:|---:|---|
| minimum_top1_accuracy | 0.3345 | 0.329 | pass |
| minimum_top3_accuracy | 0.6875 | 0.6815 | pass |
| minimum_hl_unique_wins | 70 | 61 | pass |
| no_major_attractor_increase | 1 | 0 | fail |
| major_attractor_decrease_present | 2 | 1 | pass |
| victim_class_improvement_present | 2 | 1 | pass |

## Major attractor deltas

| Attractor | Pre | Post | Delta |
|---|---:|---:|---:|
| banana | 416 | 420 | 4 |
| golden_retriever | 245 | 240 | -5 |
| king_penguin | 389 | 387 | -2 |

## Victim class deltas

| Class | Pre recall | Post recall | Delta recall | Pre miss | Post miss |
|---|---:|---:|---:|---:|---:|
| brown_bear | 0.060 | 0.060 | 0.000 | 188 | 188 |
| mushroom | 0.220 | 0.205 | -0.015 | 156 | 159 |
| orange | 0.165 | 0.185 | 0.020 | 167 | 163 |
| sports_car | 0.115 | 0.120 | 0.005 | 177 | 176 |
| teapot | 0.050 | 0.040 | -0.010 | 190 | 192 |

## Decision

This local probe failed the current regression guard. Revert or ledger as rejected before commit.

## Non-claim lock

- This probe comparison does not prove final classifier improvement.
- Validation evidence is not final test evidence.
- A failing probe should be reverted or ledgered as rejected.
- A passing probe still requires README/RCC boundary updates before push.
