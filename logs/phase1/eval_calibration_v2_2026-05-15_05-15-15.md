# Eval Run: 2026-05-15_05-15-15

**Tag:** calibration_v2
**Samples:** 2000
**Top-1 Accuracy:** 0.514
**Top-3 Accuracy:** 0.758
**Mean Latency:** 138 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.430 | 86/200 |
| golden_retriever | 0.385 | 77/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.505 | 101/200 |
| mushroom | 0.475 | 95/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.745 | 149/200 |
| sports_car | 0.525 | 105/200 |
| teapot | 0.310 | 62/200 |

## Top Confusions

- sports_car → school_bus: 34
- banana → orange: 33
- teapot → banana: 32
- brown_bear → king_penguin: 30
- teapot → king_penguin: 29
- mushroom → banana: 27
- orange → banana: 26
- brown_bear → mushroom: 26
- golden_retriever → king_penguin: 25
- golden_retriever → mushroom: 21

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
