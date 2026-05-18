# Eval Run: 2026-05-16_18-35-19

**Tag:** monitor_train
**Samples:** 2000
**Top-1 Accuracy:** 0.553
**Top-3 Accuracy:** 0.747
**Mean Latency:** 113 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.495 | 99/200 |
| brown_bear | 0.445 | 89/200 |
| golden_retriever | 0.455 | 91/200 |
| jellyfish | 0.690 | 138/200 |
| king_penguin | 0.585 | 117/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.640 | 128/200 |
| school_bus | 0.800 | 160/200 |
| sports_car | 0.640 | 128/200 |
| teapot | 0.275 | 55/200 |

## Top Confusions

- sports_car → school_bus: 31
- teapot → golden_retriever: 30
- banana → orange: 29
- brown_bear → mushroom: 29
- teapot → king_penguin: 28
- teapot → banana: 27
- brown_bear → golden_retriever: 24
- teapot → school_bus: 22
- banana → school_bus: 22
- golden_retriever → mushroom: 21

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
