# HL-ImageNet Phase 2.6E Probe Comparison

Generated: `2026-05-13T09:44:45`
Probe: `golden_retriever_orange_exclusion_plus_banana_backstop`
Overall status: `fail`

## Pre vs post

| Metric | Pre | Post | Delta |
|---|---:|---:|---:|
| Top-1 | 0.334 | 0.345 | 0.011000 |
| Top-3 | 0.6865 | 0.686 | -0.000500 |
| HL-unique wins | 68 | 73 | 5.000000 |
| Baseline-right / HL-wrong | 817 | 800 | -17.000000 |

## Guard checks

| Check | Value | Threshold | Status |
|---|---:|---:|---|
| minimum_top1_accuracy | 0.345 | 0.329 | pass |
| minimum_top3_accuracy | 0.686 | 0.6815 | pass |
| minimum_hl_unique_wins | 73 | 61 | pass |
| no_major_attractor_increase | 2 | 0 | fail |
| major_attractor_decrease_present | 1 | 1 | pass |
| victim_class_improvement_present | 3 | 1 | pass |

## Major attractor deltas

| Attractor | Pre | Post | Delta |
|---|---:|---:|---:|
| banana | 416 | 368 | -48 |
| golden_retriever | 245 | 250 | 5 |
| king_penguin | 389 | 392 | 3 |

## Victim class deltas

| Class | Pre recall | Post recall | Delta recall | Pre miss | Post miss |
|---|---:|---:|---:|---:|---:|
| brown_bear | 0.060 | 0.060 | 0.000 | 188 | 188 |
| mushroom | 0.220 | 0.245 | 0.025 | 156 | 151 |
| orange | 0.165 | 0.260 | 0.095 | 167 | 148 |
| sports_car | 0.115 | 0.120 | 0.005 | 177 | 176 |
| teapot | 0.050 | 0.045 | -0.005 | 190 | 191 |

## Decision

This local probe failed the current regression guard. Revert or ledger as rejected before commit.

## Non-claim lock

- This probe comparison does not prove final classifier improvement.
- Validation evidence is not final test evidence.
- A failing probe should be reverted or ledgered as rejected.
- A passing probe still requires README/RCC boundary updates before push.
