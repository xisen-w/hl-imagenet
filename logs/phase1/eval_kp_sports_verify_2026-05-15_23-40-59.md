# Eval Run: 2026-05-15_23-40-59

**Tag:** kp_sports_verify
**Samples:** 2000
**Top-1 Accuracy:** 0.557
**Top-3 Accuracy:** 0.770
**Mean Latency:** 108 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.550 | 110/200 |
| golden_retriever | 0.420 | 84/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.575 | 115/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.635 | 127/200 |
| school_bus | 0.700 | 140/200 |
| sports_car | 0.570 | 114/200 |
| teapot | 0.400 | 80/200 |

## Top Confusions

- banana → orange: 34
- golden_retriever → brown_bear: 26
- teapot → banana: 26
- sports_car → school_bus: 25
- school_bus → sports_car: 24
- brown_bear → mushroom: 24
- golden_retriever → mushroom: 23
- mushroom → brown_bear: 21
- teapot → golden_retriever: 21
- teapot → king_penguin: 20

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
