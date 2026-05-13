# Eval Run: 2026-05-13_10-02-50

**Tag:** iter16d_no_bear_kp_rank3
**Samples:** 2000
**Top-1 Accuracy:** 0.483
**Top-3 Accuracy:** 0.749
**Mean Latency:** 99 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.545 | 109/200 |
| brown_bear | 0.405 | 81/200 |
| golden_retriever | 0.380 | 76/200 |
| jellyfish | 0.635 | 127/200 |
| king_penguin | 0.475 | 95/200 |
| mushroom | 0.445 | 89/200 |
| orange | 0.450 | 90/200 |
| school_bus | 0.780 | 156/200 |
| sports_car | 0.505 | 101/200 |
| teapot | 0.215 | 43/200 |

## Top Confusions

- orange → banana: 51
- teapot → king_penguin: 46
- sports_car → school_bus: 42
- mushroom → banana: 35
- teapot → banana: 33
- brown_bear → school_bus: 29
- brown_bear → mushroom: 25
- golden_retriever → banana: 24
- banana → orange: 24
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
