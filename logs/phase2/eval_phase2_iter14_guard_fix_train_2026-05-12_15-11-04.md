# Eval Run: 2026-05-12_15-11-04

**Tag:** phase2_iter14_guard_fix_train
**Samples:** 2000
**Top-1 Accuracy:** 0.352
**Top-3 Accuracy:** 0.698
**Mean Latency:** 70 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.540 | 108/200 |
| brown_bear | 0.090 | 18/200 |
| golden_retriever | 0.510 | 102/200 |
| jellyfish | 0.630 | 126/200 |
| king_penguin | 0.615 | 123/200 |
| mushroom | 0.225 | 45/200 |
| orange | 0.130 | 26/200 |
| school_bus | 0.465 | 93/200 |
| sports_car | 0.195 | 39/200 |
| teapot | 0.125 | 25/200 |

## Top Confusions

- sports_car → king_penguin: 76
- orange → banana: 73
- orange → golden_retriever: 72
- teapot → king_penguin: 66
- brown_bear → golden_retriever: 64
- mushroom → golden_retriever: 61
- brown_bear → king_penguin: 61
- teapot → golden_retriever: 59
- school_bus → king_penguin: 51
- golden_retriever → king_penguin: 45

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- phase2_jellyfish_signature: used by 10 classes
- yellow_dominant: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- phase2_orange_signature: used by 10 classes
