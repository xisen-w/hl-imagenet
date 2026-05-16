# Eval Run: 2026-05-16_10-18-01

**Tag:** session13_hist_blend_090
**Samples:** 2000
**Top-1 Accuracy:** 0.569
**Top-3 Accuracy:** 0.770
**Mean Latency:** 126 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.550 | 110/200 |
| brown_bear | 0.530 | 106/200 |
| golden_retriever | 0.480 | 96/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.565 | 113/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.600 | 120/200 |
| school_bus | 0.765 | 153/200 |
| sports_car | 0.590 | 118/200 |
| teapot | 0.400 | 80/200 |

## Top Confusions

- teapot → banana: 29
- sports_car → school_bus: 26
- banana → orange: 25
- brown_bear → mushroom: 24
- mushroom → brown_bear: 23
- orange → banana: 22
- teapot → golden_retriever: 21
- orange → teapot: 21
- golden_retriever → mushroom: 19
- brown_bear → golden_retriever: 19

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
