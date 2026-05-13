# Eval Run: 2026-05-12_15-01-38

**Tag:** phase2_iter12_geomv2_train
**Samples:** 2000
**Top-1 Accuracy:** 0.337
**Top-3 Accuracy:** 0.713
**Mean Latency:** 86 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.540 | 108/200 |
| brown_bear | 0.060 | 12/200 |
| golden_retriever | 0.365 | 73/200 |
| jellyfish | 0.555 | 111/200 |
| king_penguin | 0.735 | 147/200 |
| mushroom | 0.200 | 40/200 |
| orange | 0.135 | 27/200 |
| school_bus | 0.515 | 103/200 |
| sports_car | 0.180 | 36/200 |
| teapot | 0.085 | 17/200 |

## Top Confusions

- teapot → king_penguin: 92
- sports_car → king_penguin: 90
- orange → banana: 83
- brown_bear → king_penguin: 78
- golden_retriever → king_penguin: 66
- school_bus → king_penguin: 58
- orange → golden_retriever: 54
- mushroom → golden_retriever: 52
- mushroom → banana: 51
- brown_bear → golden_retriever: 51

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- yellow_dominant: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- phase2_orange_signature: used by 10 classes
- phase2_brown_bear_signature: used by 10 classes
