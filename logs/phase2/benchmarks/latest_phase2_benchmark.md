# HL-ImageNet Phase 2 Benchmark Harness

Generated: `2026-05-12T11:53:45`
Split: `val`
Train samples: `2000`
Eval samples: `2000`
Data root: `data\phase2`

## Leaderboard

| Model | Top-1 | Top-3 | Mean latency ms |
|---|---:|---:|---:|
| handcrafted_stats_knn | 0.461 | 0.721 | 0.88 |
| image_stats_centroid | 0.434 | 0.731 | 0.68 |
| color_centroid | 0.367 | 0.659 | 0.17 |
| hl_symbolic_classifier | 0.334 | 0.686 | 73.39 |
| majority_class | 0.100 | 0.300 | 0.00 |
| random | 0.099 | 0.324 | 0.05 |

## Per-class recall

| Class | random | majority_class | color_centroid | image_stats_centroid | handcrafted_stats_knn | hl_symbolic_classifier |
|---|---:|---:|---:|---:|---:|---:|
| golden_retriever | 0.095 | 0.000 | 0.365 | 0.365 | 0.370 | 0.275 |
| mushroom | 0.135 | 0.000 | 0.495 | 0.480 | 0.335 | 0.220 |
| teapot | 0.100 | 0.000 | 0.035 | 0.155 | 0.265 | 0.050 |
| school_bus | 0.115 | 0.000 | 0.395 | 0.555 | 0.635 | 0.575 |
| banana | 0.075 | 1.000 | 0.235 | 0.285 | 0.410 | 0.580 |
| orange | 0.095 | 0.000 | 0.585 | 0.600 | 0.530 | 0.165 |
| brown_bear | 0.065 | 0.000 | 0.105 | 0.195 | 0.410 | 0.060 |
| king_penguin | 0.100 | 0.000 | 0.375 | 0.520 | 0.450 | 0.645 |
| jellyfish | 0.090 | 0.000 | 0.680 | 0.690 | 0.665 | 0.655 |
| sports_car | 0.120 | 0.000 | 0.405 | 0.495 | 0.535 | 0.115 |

## Baseline definitions

- `random`: Seeded random class ranking.
- `majority_class`: Ranks classes by train-split frequency.
- `color_centroid`: Nearest class centroid over simple color features fit on train.
- `image_stats_centroid`: Nearest class centroid over handcrafted image statistics fit on train.
- `handcrafted_stats_knn`: kNN over handcrafted image statistics fit on train.
- `hl_symbolic_classifier`: Current upstream HL symbolic classifier, evaluated without behavior changes.

## Non-claim lock

- This benchmark harness does not change classifier behavior.
- This benchmark harness does not claim accuracy improvement.
- Validation results are not final test results.
- Baselines are transparent comparators, not neural-network comparisons.
- Do not claim symbolic methods beat neural systems from this artifact.
