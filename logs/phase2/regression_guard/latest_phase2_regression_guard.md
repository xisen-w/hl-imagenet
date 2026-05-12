# HL-ImageNet Phase 2 Regression Guard

Generated: `2026-05-12T12:42:35`

## Baseline lock

| Metric | Value |
|---|---:|
| HL top-1 accuracy | 0.334 |
| HL top-3 accuracy | 0.686 |
| Benchmark top-1 | 0.334 |
| Benchmark top-3 | 0.686 |
| Correct | 668 |
| Top-3 rescue | 705 |
| Miss | 627 |
| Baseline-right / HL-wrong | 817 |
| HL-right / all-baselines-wrong | 68 |

## Major attractor false positives

| Attractor | False positives |
|---|---:|
| banana | 416 |
| king_penguin | 389 |
| golden_retriever | 245 |

## Victim class baseline

| Class | Recall | Top-3 recall | Misses |
|---|---:|---:|---:|
| teapot | 0.050 | 0.450 | 190 |
| brown_bear | 0.060 | 0.550 | 188 |
| sports_car | 0.115 | 0.615 | 177 |
| orange | 0.165 | 0.720 | 167 |
| mushroom | 0.220 | 0.550 | 156 |

## Guard contract

| Guard | Threshold |
|---|---:|
| Minimum top-1 accuracy | 0.329 |
| Minimum top-3 accuracy | 0.681 |
| Minimum HL-unique wins | 61 |
| Maximum major-attractor increase | 0 |
| Required major-attractor decrease | 1 |
| Required victim-class improvement | 1 |

## Current guard status

Overall status: `pass`

| Check | Value | Threshold | Status |
|---|---:|---:|---|
| top1_accuracy_baseline | 0.334 | 0.329 | pass |
| top3_accuracy_baseline | 0.686 | 0.681 | pass |
| hl_unique_wins_baseline | 68.000 | 61.000 | pass |

## Phase 2.6B gate

- Allowed next step: one controlled classifier delta only
- Preferred target: tighten globally overactive Phase 2 signatures or add regression guards before attractor suppression

Forbidden moves:

- broad scorer rewrite
- multiple simultaneous classifier changes
- validation-only tuning without reruns
- claiming improvement without benchmark/attribution comparison

Required reruns after any classifier change:

    python scripts/run_phase2_diagnostics.py --input <new_phase2_eval_json>
    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val
    python scripts/run_phase2_attribution.py --data-root ".\data\phase2" --split val
    python scripts/run_phase2_candidates.py
    python scripts/run_phase2_regression_guard.py

## Non-claim lock

- This regression guard does not change classifier behavior.
- This regression guard does not claim accuracy improvement.
- This regression guard does not prove classifier correctness.
- Validation regression checks are not final test evidence.
- Any future classifier change must rerun diagnostics, benchmarks, attribution, candidates, and regression guard.
