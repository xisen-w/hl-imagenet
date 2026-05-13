# HL-ImageNet Phase 2.6D Rejected Probe

Probe: `golden_retriever_orange_signature_exclusion`

Overall status: `fail`

## Attempted change

The probe added one class-specific exclusion in `hlinet/classifier/hierarchy.py`:

    golden_retriever excluding_features += phase2_orange_signature

## Pre vs post

| Metric | Pre | Post | Delta |
|---|---:|---:|---:|
| Top-1 | 0.334 | 0.3345 | +0.0005 |
| Top-3 | 0.6865 | 0.6875 | +0.0010 |
| HL-unique wins | 68 | 70 | +2 |
| Baseline-right / HL-wrong | 817 | 818 | +1 |

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
| banana | 416 | 420 | +4 |
| golden_retriever | 245 | 240 | -5 |
| king_penguin | 389 | 387 | -2 |

## Victim class deltas

| Class | Pre recall | Post recall | Delta recall | Pre miss | Post miss |
|---|---:|---:|---:|---:|---:|
| brown_bear | 0.060 | 0.060 | 0.000 | 188 | 188 |
| mushroom | 0.220 | 0.205 | -0.015 | 156 | 159 |
| orange | 0.165 | 0.185 | +0.020 | 167 | 163 |
| sports_car | 0.115 | 0.120 | +0.005 | 177 | 176 |
| teapot | 0.050 | 0.040 | -0.010 | 190 | 192 |

## Decision

Rejected / near miss.

The hierarchy change is not committed.

## Lesson

Class-specific deltas are more promising than global scorer pressure, but `golden_retriever + phase2_orange_signature exclusion` alone caused banana spillover.

Next probe should preserve the golden_retriever/orange benefit while adding a banana backstop.

## Non-claim lock

- This rejected probe does not prove classifier improvement.
- The failed hierarchy change is not committed.
- Validation evidence is not final test evidence.
- This ledger preserves near-miss evidence to constrain future design.