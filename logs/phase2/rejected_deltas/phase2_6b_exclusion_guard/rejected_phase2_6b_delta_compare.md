# HL-ImageNet Phase 2.6B Rejected Delta

Delta: `phase2_6b_exclusion_guard_scoring_delta`

Overall status: `fail`

## Attempted change

The rejected delta attempted to globally increase exclusion pressure in `hlinet/classifier/scorer.py`.

Old formula:

    score = required_score * 0.75 + supporting_score * 0.15 - excluding_score * 0.15 - alt_penalty

New formula:

    score = required_score * 0.72 + supporting_score * 0.16 - excluding_score * 0.22 - alt_penalty

## Pre vs post

| Metric | Pre | Post | Delta |
|---|---:|---:|---:|
| Top-1 | 0.334 | 0.3255 | -0.0085 |
| Top-3 | 0.6865 | 0.681 | -0.0055 |
| HL-unique wins | 68 | 69 | +1 |
| Baseline-right / HL-wrong | 817 | 835 | +18 |

## Guard checks

| Check | Value | Threshold | Status |
|---|---:|---:|---|
| minimum_top1_accuracy | 0.3255 | 0.329 | fail |
| minimum_top3_accuracy | 0.681 | 0.6815 | fail |
| minimum_hl_unique_wins | 69 | 61 | pass |
| no_major_attractor_increase | 2 | 0 | fail |
| major_attractor_decrease_present | 1 | 1 | pass |
| victim_class_improvement_present | 1 | 1 | pass |

## Major attractor deltas

| Attractor | Pre | Post | Delta |
|---|---:|---:|---:|
| banana | 416 | 442 | +26 |
| golden_retriever | 245 | 211 | -34 |
| king_penguin | 389 | 410 | +21 |

## Victim class deltas

| Class | Pre recall | Post recall | Delta recall | Pre miss | Post miss |
|---|---:|---:|---:|---:|---:|
| brown_bear | 0.060 | 0.050 | -0.010 | 188 | 190 |
| mushroom | 0.220 | 0.170 | -0.050 | 156 | 166 |
| orange | 0.165 | 0.165 | 0.000 | 167 | 167 |
| sports_car | 0.115 | 0.105 | -0.010 | 177 | 179 |
| teapot | 0.050 | 0.065 | +0.015 | 190 | 187 |

## Decision

Rejected.

The failed scorer change is not committed.

## Lesson

Global exclusion pressure is too blunt. It reduced golden_retriever false positives but increased banana and king_penguin false positives and dropped top-1/top-3 below guard thresholds.

Next classifier delta should be class-specific, not global.

## Non-claim lock

- This rejected delta does not prove classifier improvement.
- The failed scorer change is not committed.
- Validation evidence is not final test evidence.
- This ledger preserves negative evidence to constrain future design.