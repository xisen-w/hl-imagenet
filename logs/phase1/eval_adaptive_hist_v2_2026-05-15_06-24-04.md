# Eval Run: 2026-05-15_06-24-04

**Tag:** adaptive_hist_v2
**Samples:** 2000
**Top-1 Accuracy:** 0.504
**Top-3 Accuracy:** 0.748
**Mean Latency:** 150 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.480 | 96/200 |
| brown_bear | 0.380 | 76/200 |
| golden_retriever | 0.385 | 77/200 |
| jellyfish | 0.670 | 134/200 |
| king_penguin | 0.505 | 101/200 |
| mushroom | 0.490 | 98/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.770 | 154/200 |
| sports_car | 0.570 | 114/200 |
| teapot | 0.215 | 43/200 |

## Top Confusions

- sports_car → school_bus: 39
- banana → orange: 34
- brown_bear → mushroom: 34
- teapot → king_penguin: 32
- teapot → banana: 30
- brown_bear → king_penguin: 30
- teapot → golden_retriever: 29
- teapot → school_bus: 24
- school_bus → sports_car: 24
- golden_retriever → king_penguin: 23

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- phase2_jellyfish_signature: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- yellow_dominant: used by 10 classes
- phase2_orange_signature: used by 10 classes
