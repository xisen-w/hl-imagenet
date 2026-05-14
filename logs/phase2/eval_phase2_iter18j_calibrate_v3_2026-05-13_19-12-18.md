# Eval Run: 2026-05-13_19-12-18

**Tag:** phase2_iter18j_calibrate_v3
**Samples:** 2000
**Top-1 Accuracy:** 0.506
**Top-3 Accuracy:** 0.752
**Mean Latency:** 87 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.460 | 92/200 |
| brown_bear | 0.435 | 87/200 |
| golden_retriever | 0.455 | 91/200 |
| jellyfish | 0.690 | 138/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.465 | 93/200 |
| orange | 0.555 | 111/200 |
| school_bus | 0.745 | 149/200 |
| sports_car | 0.540 | 108/200 |
| teapot | 0.210 | 42/200 |

## Top Confusions

- teapot → king_penguin: 48
- banana → orange: 37
- sports_car → school_bus: 33
- teapot → banana: 29
- orange → banana: 28
- brown_bear → mushroom: 25
- brown_bear → golden_retriever: 24
- brown_bear → king_penguin: 24
- mushroom → banana: 23
- teapot → golden_retriever: 22

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
