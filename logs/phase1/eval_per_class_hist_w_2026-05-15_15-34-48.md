# Eval Run: 2026-05-15_15-34-48

**Tag:** per_class_hist_w
**Samples:** 2000
**Top-1 Accuracy:** 0.514
**Top-3 Accuracy:** 0.747
**Mean Latency:** 222 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.475 | 95/200 |
| brown_bear | 0.420 | 84/200 |
| golden_retriever | 0.395 | 79/200 |
| jellyfish | 0.690 | 138/200 |
| king_penguin | 0.520 | 104/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.760 | 152/200 |
| sports_car | 0.580 | 116/200 |
| teapot | 0.215 | 43/200 |

## Top Confusions

- brown_bear → mushroom: 36
- sports_car → school_bus: 36
- teapot → king_penguin: 34
- banana → orange: 33
- teapot → golden_retriever: 32
- orange → banana: 27
- teapot → banana: 24
- school_bus → sports_car: 23
- golden_retriever → brown_bear: 22
- teapot → school_bus: 22

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
