# Eval Run: 2026-05-14_03-53-30

**Tag:** iter7_teapot_only_bias
**Samples:** 2000
**Top-1 Accuracy:** 0.494
**Top-3 Accuracy:** 0.757
**Mean Latency:** 99 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.495 | 99/200 |
| brown_bear | 0.395 | 79/200 |
| golden_retriever | 0.375 | 75/200 |
| jellyfish | 0.640 | 128/200 |
| king_penguin | 0.500 | 100/200 |
| mushroom | 0.435 | 87/200 |
| orange | 0.585 | 117/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.510 | 102/200 |
| teapot | 0.250 | 50/200 |

## Top Confusions

- teapot → king_penguin: 41
- sports_car → school_bus: 36
- banana → orange: 35
- mushroom → banana: 34
- teapot → banana: 28
- orange → banana: 26
- brown_bear → school_bus: 25
- brown_bear → mushroom: 25
- golden_retriever → banana: 23
- school_bus → sports_car: 23

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
