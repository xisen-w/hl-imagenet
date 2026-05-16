# Eval Run: 2026-05-16_11-35-08

**Tag:** session13_speed_test
**Samples:** 2000
**Top-1 Accuracy:** 0.581
**Top-3 Accuracy:** 0.776
**Mean Latency:** 54 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.605 | 121/200 |
| brown_bear | 0.560 | 112/200 |
| golden_retriever | 0.475 | 95/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.585 | 117/200 |
| mushroom | 0.515 | 103/200 |
| orange | 0.605 | 121/200 |
| school_bus | 0.775 | 155/200 |
| sports_car | 0.595 | 119/200 |
| teapot | 0.395 | 79/200 |

## Top Confusions

- teapot → banana: 30
- sports_car → school_bus: 26
- banana → orange: 23
- orange → banana: 23
- mushroom → brown_bear: 22
- teapot → king_penguin: 22
- teapot → golden_retriever: 20
- brown_bear → golden_retriever: 20
- brown_bear → mushroom: 20
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
