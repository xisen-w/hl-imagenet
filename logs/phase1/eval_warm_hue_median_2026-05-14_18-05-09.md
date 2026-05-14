# Eval Run: 2026-05-14_18-05-09

**Tag:** warm_hue_median
**Samples:** 2000
**Top-1 Accuracy:** 0.512
**Top-3 Accuracy:** 0.754
**Mean Latency:** 230 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.525 | 105/200 |
| brown_bear | 0.450 | 90/200 |
| golden_retriever | 0.385 | 77/200 |
| jellyfish | 0.660 | 132/200 |
| king_penguin | 0.495 | 99/200 |
| mushroom | 0.465 | 93/200 |
| orange | 0.545 | 109/200 |
| school_bus | 0.760 | 152/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.320 | 64/200 |

## Top Confusions

- sports_car → school_bus: 35
- orange → banana: 33
- banana → orange: 31
- mushroom → banana: 30
- teapot → banana: 30
- brown_bear → mushroom: 25
- teapot → king_penguin: 23
- brown_bear → king_penguin: 23
- golden_retriever → banana: 22
- golden_retriever → king_penguin: 22

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
