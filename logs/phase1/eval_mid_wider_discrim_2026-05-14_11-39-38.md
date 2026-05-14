# Eval Run: 2026-05-14_11-39-38

**Tag:** mid_wider_discrim
**Samples:** 2000
**Top-1 Accuracy:** 0.509
**Top-3 Accuracy:** 0.754
**Mean Latency:** 145 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.500 | 100/200 |
| brown_bear | 0.465 | 93/200 |
| golden_retriever | 0.375 | 75/200 |
| jellyfish | 0.660 | 132/200 |
| king_penguin | 0.480 | 96/200 |
| mushroom | 0.465 | 93/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.760 | 152/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.290 | 58/200 |

## Top Confusions

- banana → orange: 36
- sports_car → school_bus: 35
- mushroom → banana: 30
- teapot → king_penguin: 29
- teapot → banana: 29
- orange → banana: 26
- brown_bear → mushroom: 25
- brown_bear → king_penguin: 23
- golden_retriever → banana: 22
- golden_retriever → brown_bear: 22

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
