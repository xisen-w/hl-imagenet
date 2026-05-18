# Eval Run: 2026-05-16_19-49-16

**Tag:** session15_r0warm_sports_bus
**Samples:** 2000
**Top-1 Accuracy:** 0.577
**Top-3 Accuracy:** 0.770
**Mean Latency:** 115 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.545 | 109/200 |
| golden_retriever | 0.490 | 98/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.585 | 117/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.630 | 126/200 |
| school_bus | 0.730 | 146/200 |
| sports_car | 0.595 | 119/200 |
| teapot | 0.415 | 83/200 |

## Top Confusions

- sports_car → school_bus: 29
- teapot → banana: 28
- banana → orange: 25
- mushroom → brown_bear: 22
- school_bus → sports_car: 22
- brown_bear → golden_retriever: 22
- brown_bear → mushroom: 22
- orange → banana: 21
- teapot → golden_retriever: 20
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
