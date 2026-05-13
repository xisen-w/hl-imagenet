# Eval Run: 2026-05-13_09-35-35

**Tag:** iter16_train_baseline
**Samples:** 2000
**Top-1 Accuracy:** 0.475
**Top-3 Accuracy:** 0.749
**Mean Latency:** 112 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.560 | 112/200 |
| brown_bear | 0.425 | 85/200 |
| golden_retriever | 0.355 | 71/200 |
| jellyfish | 0.650 | 130/200 |
| king_penguin | 0.435 | 87/200 |
| mushroom | 0.420 | 84/200 |
| orange | 0.420 | 84/200 |
| school_bus | 0.780 | 156/200 |
| sports_car | 0.505 | 101/200 |
| teapot | 0.200 | 40/200 |

## Top Confusions

- orange → banana: 53
- teapot → king_penguin: 42
- sports_car → school_bus: 42
- mushroom → banana: 38
- teapot → banana: 34
- golden_retriever → banana: 28
- brown_bear → school_bus: 28
- teapot → golden_retriever: 24
- banana → orange: 23
- banana → school_bus: 23

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
