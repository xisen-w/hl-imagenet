# Eval Run: 2026-05-15_09-29-40

**Tag:** teapot_guard_relax
**Samples:** 2000
**Top-1 Accuracy:** 0.519
**Top-3 Accuracy:** 0.766
**Mean Latency:** 136 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.445 | 89/200 |
| golden_retriever | 0.405 | 81/200 |
| jellyfish | 0.695 | 139/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.500 | 100/200 |
| orange | 0.570 | 114/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.520 | 104/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- sports_car → school_bus: 35
- banana → orange: 33
- teapot → banana: 30
- brown_bear → mushroom: 30
- orange → banana: 28
- teapot → king_penguin: 25
- brown_bear → king_penguin: 24
- mushroom → banana: 22
- school_bus → sports_car: 22
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
