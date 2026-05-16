# Eval Run: 2026-05-16_09-10-22

**Tag:** session13_sports_bus_rbratio
**Samples:** 2000
**Top-1 Accuracy:** 0.575
**Top-3 Accuracy:** 0.769
**Mean Latency:** 127 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.535 | 107/200 |
| golden_retriever | 0.480 | 96/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.590 | 118/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.620 | 124/200 |
| school_bus | 0.750 | 150/200 |
| sports_car | 0.585 | 117/200 |
| teapot | 0.405 | 81/200 |

## Top Confusions

- teapot → banana: 29
- sports_car → school_bus: 28
- banana → orange: 25
- brown_bear → mushroom: 23
- mushroom → brown_bear: 22
- orange → banana: 22
- brown_bear → golden_retriever: 22
- teapot → golden_retriever: 21
- golden_retriever → mushroom: 20
- teapot → king_penguin: 20

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
