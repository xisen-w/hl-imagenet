# Eval Run: 2026-05-13_13-13-45

**Tag:** phase2_iter17f_gabor2
**Samples:** 2000
**Top-1 Accuracy:** 0.487
**Top-3 Accuracy:** 0.753
**Mean Latency:** 148 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.560 | 112/200 |
| brown_bear | 0.405 | 81/200 |
| golden_retriever | 0.375 | 75/200 |
| jellyfish | 0.660 | 132/200 |
| king_penguin | 0.495 | 99/200 |
| mushroom | 0.445 | 89/200 |
| orange | 0.450 | 90/200 |
| school_bus | 0.765 | 153/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.205 | 41/200 |

## Top Confusions

- orange → banana: 52
- teapot → king_penguin: 48
- mushroom → banana: 35
- teapot → banana: 34
- sports_car → school_bus: 34
- brown_bear → mushroom: 25
- brown_bear → king_penguin: 25
- golden_retriever → banana: 24
- banana → orange: 24
- brown_bear → school_bus: 24

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
