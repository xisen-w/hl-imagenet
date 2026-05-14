# Eval Run: 2026-05-13_19-09-09

**Tag:** phase2_iter18i_calibrate_v2
**Samples:** 2000
**Top-1 Accuracy:** 0.506
**Top-3 Accuracy:** 0.752
**Mean Latency:** 84 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.450 | 90/200 |
| brown_bear | 0.440 | 88/200 |
| golden_retriever | 0.465 | 93/200 |
| jellyfish | 0.690 | 138/200 |
| king_penguin | 0.515 | 103/200 |
| mushroom | 0.460 | 92/200 |
| orange | 0.560 | 112/200 |
| school_bus | 0.730 | 146/200 |
| sports_car | 0.540 | 108/200 |
| teapot | 0.210 | 42/200 |

## Top Confusions

- teapot → king_penguin: 49
- banana → orange: 38
- sports_car → school_bus: 33
- brown_bear → golden_retriever: 28
- teapot → banana: 27
- orange → banana: 27
- brown_bear → king_penguin: 26
- school_bus → sports_car: 24
- mushroom → banana: 23
- teapot → golden_retriever: 23

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
