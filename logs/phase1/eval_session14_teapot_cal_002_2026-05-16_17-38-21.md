# Eval Run: 2026-05-16_17-38-21

**Tag:** session14_teapot_cal_002
**Samples:** 2000
**Top-1 Accuracy:** 0.570
**Top-3 Accuracy:** 0.770
**Mean Latency:** 33 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.555 | 111/200 |
| brown_bear | 0.530 | 106/200 |
| golden_retriever | 0.465 | 93/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.570 | 114/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.625 | 125/200 |
| school_bus | 0.745 | 149/200 |
| sports_car | 0.585 | 117/200 |
| teapot | 0.415 | 83/200 |

## Top Confusions

- teapot → banana: 28
- sports_car → school_bus: 26
- banana → orange: 25
- mushroom → brown_bear: 23
- teapot → golden_retriever: 23
- brown_bear → mushroom: 22
- golden_retriever → brown_bear: 20
- orange → banana: 20
- orange → teapot: 20
- golden_retriever → mushroom: 19

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
