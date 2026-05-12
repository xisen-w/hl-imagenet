# HL-ImageNet Phase 2 Sample-Level Attribution

Generated: `2026-05-12T12:27:59`
Split: `val`
Data root: `data\phase2`
Samples: `2000`

## Summary

- Accuracy: `0.334`
- Top-3 accuracy: `0.686`
- Mean margin: `0.083`
- Median margin: `0.072`
- Outcome counts: `{'miss': 627, 'top3_rescue': 705, 'correct': 668}`
- Baseline-right / HL-wrong samples: `817`
- HL-right / all-baselines-wrong samples: `68`

## Top collapse paths

| Collapse path | Count |
|---|---:|
| sports_car->king_penguin | 113 |
| orange->banana | 83 |
| golden_retriever->banana | 82 |
| teapot->king_penguin | 72 |
| brown_bear->banana | 70 |
| mushroom->banana | 67 |
| orange->golden_retriever | 61 |
| brown_bear->king_penguin | 58 |
| teapot->golden_retriever | 50 |
| teapot->banana | 43 |
| mushroom->king_penguin | 35 |
| golden_retriever->king_penguin | 34 |
| brown_bear->golden_retriever | 32 |
| jellyfish->king_penguin | 32 |
| king_penguin->banana | 30 |

## Per-class attribution summary

| Class | N | Recall | Top-3 recall | Misses | Top wrong predictions |
|---|---:|---:|---:|---:|---|
| golden_retriever | 200 | 0.275 | 0.765 | 145 | banana:82, king_penguin:34, mushroom:9, school_bus:8, teapot:4 |
| mushroom | 200 | 0.220 | 0.550 | 156 | banana:67, king_penguin:35, golden_retriever:25, school_bus:11, teapot:8 |
| teapot | 200 | 0.050 | 0.450 | 190 | king_penguin:72, golden_retriever:50, banana:43, mushroom:6, jellyfish:6 |
| school_bus | 200 | 0.575 | 0.850 | 85 | king_penguin:27, banana:22, mushroom:15, golden_retriever:13, sports_car:6 |
| banana | 200 | 0.580 | 0.795 | 84 | golden_retriever:27, teapot:18, king_penguin:12, school_bus:11, mushroom:7 |
| orange | 200 | 0.165 | 0.720 | 167 | banana:83, golden_retriever:61, teapot:9, king_penguin:6, school_bus:5 |
| brown_bear | 200 | 0.060 | 0.550 | 188 | banana:70, king_penguin:58, golden_retriever:32, mushroom:14, school_bus:5 |
| king_penguin | 200 | 0.645 | 0.800 | 71 | banana:30, jellyfish:16, teapot:8, golden_retriever:6, mushroom:5 |
| jellyfish | 200 | 0.655 | 0.770 | 69 | king_penguin:32, golden_retriever:10, banana:10, teapot:7, orange:5 |
| sports_car | 200 | 0.115 | 0.615 | 177 | king_penguin:113, school_bus:22, golden_retriever:21, banana:9, mushroom:7 |

## Top activated features

| Feature | Sample count |
|---|---:|
| bilateral_symmetry | 2000 |
| quadruped_like | 1966 |
| phase2_golden_retriever_signature | 1780 |
| phase2_teapot_signature | 1495 |
| phase2_mushroom_signature | 1490 |
| phase2_banana_signature | 1489 |
| phase2_school_bus_signature | 1463 |
| phase2_brown_bear_signature | 1438 |
| golden_fur_in_nature | 1385 |
| phase2_king_penguin_signature | 1075 |
| phase2_sports_car_signature | 1051 |
| phase2_orange_signature | 1024 |
| golden_brown_color | 1003 |
| yellow_dominant | 973 |
| phase2_jellyfish_signature | 730 |
| distinct_background | 649 |
| yellow_body_with_sky | 577 |
| horizontal_window_pattern | 453 |
| black_white_dominant | 428 |
| blob_textured_interior | 427 |

## Artifact files

- `latest_phase2_attribution.json`
- `latest_phase2_attribution.csv`
- `latest_phase2_attribution.md`

## Non-claim lock

- This attribution layer does not change classifier behavior.
- This attribution layer does not claim accuracy improvement.
- Validation attribution is not a final test result.
- Proof traces explain model behavior; they do not prove correctness.
- Use this artifact to inspect failures before any Phase 2.5 scoring changes.
