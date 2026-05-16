# Eval Run: 2026-05-15_06-18-44

**Tag:** adaptive_hist_blend
**Samples:** 2000
**Top-1 Accuracy:** 0.493
**Top-3 Accuracy:** 0.732
**Mean Latency:** 152 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.440 | 88/200 |
| brown_bear | 0.330 | 66/200 |
| golden_retriever | 0.365 | 73/200 |
| jellyfish | 0.650 | 130/200 |
| king_penguin | 0.500 | 100/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.605 | 121/200 |
| school_bus | 0.790 | 158/200 |
| sports_car | 0.575 | 115/200 |
| teapot | 0.165 | 33/200 |

## Top Confusions

- sports_car → school_bus: 44
- banana → orange: 38
- brown_bear → mushroom: 38
- teapot → king_penguin: 36
- banana → school_bus: 36
- teapot → school_bus: 34
- brown_bear → king_penguin: 29
- teapot → banana: 26
- teapot → golden_retriever: 26
- golden_retriever → king_penguin: 24

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
