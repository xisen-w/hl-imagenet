# Eval Run: 2026-05-15_19-14-32

**Tag:** per_class_hist
**Samples:** 2000
**Top-1 Accuracy:** 0.524
**Top-3 Accuracy:** 0.747
**Mean Latency:** 139 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.490 | 98/200 |
| brown_bear | 0.425 | 85/200 |
| golden_retriever | 0.410 | 82/200 |
| jellyfish | 0.690 | 138/200 |
| king_penguin | 0.530 | 106/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.595 | 119/200 |
| school_bus | 0.765 | 153/200 |
| sports_car | 0.575 | 115/200 |
| teapot | 0.250 | 50/200 |

## Top Confusions

- sports_car → school_bus: 36
- brown_bear → mushroom: 35
- banana → orange: 33
- teapot → golden_retriever: 32
- teapot → king_penguin: 32
- orange → banana: 25
- teapot → banana: 24
- golden_retriever → brown_bear: 22
- teapot → school_bus: 22
- school_bus → sports_car: 22

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
