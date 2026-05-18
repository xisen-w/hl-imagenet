# Eval Run: 2026-05-16_13-09-11

**Tag:** session13_bus_sports_darkbright
**Samples:** 2000
**Top-1 Accuracy:** 0.575
**Top-3 Accuracy:** 0.770
**Mean Latency:** 65 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.570 | 114/200 |
| brown_bear | 0.540 | 108/200 |
| golden_retriever | 0.485 | 97/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.585 | 117/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.625 | 125/200 |
| school_bus | 0.735 | 147/200 |
| sports_car | 0.590 | 118/200 |
| teapot | 0.405 | 81/200 |

## Top Confusions

- teapot → banana: 29
- sports_car → school_bus: 28
- banana → orange: 25
- mushroom → brown_bear: 22
- brown_bear → golden_retriever: 22
- brown_bear → mushroom: 22
- teapot → golden_retriever: 21
- orange → banana: 21
- teapot → king_penguin: 20
- school_bus → sports_car: 20

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
