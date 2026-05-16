# Eval Run: 2026-05-15_05-51-17

**Tag:** bear_kp_conservative
**Samples:** 2000
**Top-1 Accuracy:** 0.518
**Top-3 Accuracy:** 0.764
**Mean Latency:** 144 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.455 | 91/200 |
| golden_retriever | 0.395 | 79/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.495 | 99/200 |
| mushroom | 0.490 | 98/200 |
| orange | 0.575 | 115/200 |
| school_bus | 0.720 | 144/200 |
| sports_car | 0.530 | 106/200 |
| teapot | 0.335 | 67/200 |

## Top Confusions

- banana → orange: 33
- sports_car → school_bus: 33
- teapot → banana: 32
- brown_bear → mushroom: 30
- orange → banana: 28
- mushroom → banana: 24
- teapot → king_penguin: 24
- brown_bear → king_penguin: 24
- golden_retriever → mushroom: 23
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
