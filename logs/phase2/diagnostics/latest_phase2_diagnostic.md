# HL-ImageNet Phase 2 Diagnostic Lens

Generated: `2026-05-12T10:36:15`
Source report: `logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json`
Source tag: `phase2_iter9_val`

## Summary

- Samples: `2000`
- Top-1 accuracy: `0.334`
- Top-3 accuracy: `0.686`
- Top-3 rescue gap: `0.352`
- Mean latency ms: `89.85580861568451`

## Per-class diagnostic table

| Class | Recall | Precision | Victim Score | Attractor Score | Correct | True Total | Pred Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| banana | 0.580 | 0.218 | 0.420 | 0.782 | 116 | 200 | 532 |
| brown_bear | 0.060 | 0.429 | 0.940 | 0.571 | 12 | 200 | 28 |
| golden_retriever | 0.275 | 0.183 | 0.725 | 0.817 | 55 | 200 | 300 |
| jellyfish | 0.655 | 0.804 | 0.345 | 0.196 | 131 | 200 | 163 |
| king_penguin | 0.645 | 0.249 | 0.355 | 0.751 | 129 | 200 | 518 |
| mushroom | 0.220 | 0.400 | 0.780 | 0.600 | 44 | 200 | 110 |
| orange | 0.165 | 0.733 | 0.835 | 0.267 | 33 | 200 | 45 |
| school_bus | 0.575 | 0.615 | 0.425 | 0.385 | 115 | 200 | 187 |
| sports_car | 0.115 | 0.460 | 0.885 | 0.540 | 23 | 200 | 50 |
| teapot | 0.050 | 0.149 | 0.950 | 0.851 | 10 | 200 | 67 |

## Top confusion gravity wells

| True | Predicted | Count |
|---|---|---:|
| sports_car | king_penguin | 113 |
| orange | banana | 83 |
| golden_retriever | banana | 82 |
| teapot | king_penguin | 72 |
| brown_bear | banana | 70 |
| mushroom | banana | 67 |
| orange | golden_retriever | 61 |
| brown_bear | king_penguin | 58 |
| teapot | golden_retriever | 50 |
| teapot | banana | 43 |
| mushroom | king_penguin | 35 |
| golden_retriever | king_penguin | 34 |
| brown_bear | golden_retriever | 32 |
| jellyfish | king_penguin | 32 |
| king_penguin | banana | 30 |

## Top false-positive attractors

| Class | Pred Total | False Positive | Attractor Score | Precision |
|---|---:|---:|---:|---:|
| banana | 532 | 416 | 0.782 | 0.218 |
| king_penguin | 518 | 389 | 0.751 | 0.249 |
| golden_retriever | 300 | 245 | 0.817 | 0.183 |
| school_bus | 187 | 72 | 0.385 | 0.615 |
| mushroom | 110 | 66 | 0.600 | 0.400 |
| teapot | 67 | 57 | 0.851 | 0.149 |
| jellyfish | 163 | 32 | 0.196 | 0.804 |
| sports_car | 50 | 27 | 0.540 | 0.460 |
| brown_bear | 28 | 16 | 0.571 | 0.429 |
| orange | 45 | 12 | 0.267 | 0.733 |

## Top victim classes

| Class | True Total | False Negative | Victim Score | Recall |
|---|---:|---:|---:|---:|
| teapot | 200 | 190 | 0.950 | 0.050 |
| brown_bear | 200 | 188 | 0.940 | 0.060 |
| sports_car | 200 | 177 | 0.885 | 0.115 |
| orange | 200 | 167 | 0.835 | 0.165 |
| mushroom | 200 | 156 | 0.780 | 0.220 |
| golden_retriever | 200 | 145 | 0.725 | 0.275 |
| school_bus | 200 | 85 | 0.425 | 0.575 |
| banana | 200 | 84 | 0.420 | 0.580 |
| king_penguin | 200 | 71 | 0.355 | 0.645 |
| jellyfish | 200 | 69 | 0.345 | 0.655 |

## High feature-reuse warnings

| Feature | Class Count |
|---|---:|
| phase2_golden_retriever_signature | 10 |
| golden_fur_in_nature | 10 |
| quadruped_like | 10 |
| phase2_jellyfish_signature | 10 |
| phase2_mushroom_signature | 10 |
| blob_textured_interior | 10 |
| phase2_teapot_signature | 10 |
| distinct_background | 10 |
| phase2_school_bus_signature | 10 |
| horizontal_window_pattern | 10 |
| yellow_body_with_sky | 10 |
| phase2_banana_signature | 10 |
| phase2_brown_bear_signature | 10 |
| phase2_king_penguin_signature | 10 |
| bilateral_symmetry | 10 |

## Warnings

- Low-recall victim classes detected: brown_bear, sports_car, teapot
- False-positive attractor classes detected: banana, king_penguin, golden_retriever, school_bus, mushroom, teapot, sports_car
- Large top-3 rescue gap detected; true class may often be near the decision surface but lose top-1.
- High feature-reuse counts detected; current feature_reuse may reflect global cache activation rather than class-specific dependence.

## Recommendations

- Do not change classifier behavior until attractor and victim classes are inspected.
- Inspect top confusion gravity wells before adding new signatures.
- Treat feature_reuse as a coarse warning until sample-level/class-node attribution exists.
- Preserve train/validation/test labels when summarizing results.
- Consider future attractor-balanced scoring only after reviewing false-positive attractors.
- Prioritize victim-class analysis for: brown_bear, sports_car, teapot

## Non-claim lock

- This diagnostic does not prove classifier correctness.
- This diagnostic does not change classifier behavior.
- This diagnostic does not claim RCC improved classifier accuracy.
- This diagnostic should guide inspection before Phase 2.3 scoring or signature changes.
