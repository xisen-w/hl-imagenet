# Eval Run: 2026-05-14_18-43-13

**Tag:** calibration_v1
**Samples:** 2000
**Top-1 Accuracy:** 0.513
**Top-3 Accuracy:** 0.766
**Mean Latency:** 225 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.520 | 104/200 |
| brown_bear | 0.455 | 91/200 |
| golden_retriever | 0.385 | 77/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.500 | 100/200 |
| mushroom | 0.480 | 96/200 |
| orange | 0.585 | 117/200 |
| school_bus | 0.705 | 141/200 |
| sports_car | 0.520 | 104/200 |
| teapot | 0.305 | 61/200 |

## Top Confusions

- sports_car → school_bus: 33
- teapot → banana: 32
- teapot → king_penguin: 32
- banana → orange: 32
- brown_bear → king_penguin: 32
- mushroom → banana: 28
- brown_bear → mushroom: 27
- orange → banana: 26
- golden_retriever → king_penguin: 25
- golden_retriever → mushroom: 22

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
