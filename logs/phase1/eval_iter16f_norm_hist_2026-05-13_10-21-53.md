# Eval Run: 2026-05-13_10-21-53

**Tag:** iter16f_norm_hist
**Samples:** 2000
**Top-1 Accuracy:** 0.486
**Top-3 Accuracy:** 0.764
**Mean Latency:** 104 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.420 | 84/200 |
| golden_retriever | 0.375 | 75/200 |
| jellyfish | 0.680 | 136/200 |
| king_penguin | 0.515 | 103/200 |
| mushroom | 0.430 | 86/200 |
| orange | 0.455 | 91/200 |
| school_bus | 0.740 | 148/200 |
| sports_car | 0.475 | 95/200 |
| teapot | 0.205 | 41/200 |

## Top Confusions

- teapot → king_penguin: 51
- orange → banana: 51
- sports_car → school_bus: 37
- teapot → banana: 35
- mushroom → banana: 34
- brown_bear → king_penguin: 27
- sports_car → king_penguin: 26
- golden_retriever → banana: 24
- brown_bear → mushroom: 24
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
