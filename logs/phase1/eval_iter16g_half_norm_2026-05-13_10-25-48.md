# Eval Run: 2026-05-13_10-25-48

**Tag:** iter16g_half_norm
**Samples:** 2000
**Top-1 Accuracy:** 0.486
**Top-3 Accuracy:** 0.756
**Mean Latency:** 104 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.555 | 111/200 |
| brown_bear | 0.400 | 80/200 |
| golden_retriever | 0.375 | 75/200 |
| jellyfish | 0.670 | 134/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.445 | 89/200 |
| orange | 0.450 | 90/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.490 | 98/200 |
| teapot | 0.210 | 42/200 |

## Top Confusions

- orange → banana: 52
- teapot → king_penguin: 48
- sports_car → school_bus: 38
- mushroom → banana: 35
- teapot → banana: 35
- brown_bear → king_penguin: 26
- brown_bear → mushroom: 25
- golden_retriever → banana: 24
- brown_bear → school_bus: 24
- sports_car → king_penguin: 24

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
