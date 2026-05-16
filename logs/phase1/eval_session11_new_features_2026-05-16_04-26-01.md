# Eval Run: 2026-05-16_04-26-01

**Tag:** session11_new_features
**Samples:** 2000
**Top-1 Accuracy:** 0.560
**Top-3 Accuracy:** 0.769
**Mean Latency:** 250 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.520 | 104/200 |
| golden_retriever | 0.415 | 83/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.575 | 115/200 |
| mushroom | 0.505 | 101/200 |
| orange | 0.635 | 127/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.600 | 120/200 |
| teapot | 0.385 | 77/200 |

## Top Confusions

- banana → orange: 36
- teapot → banana: 27
- golden_retriever → brown_bear: 26
- sports_car → school_bus: 26
- brown_bear → mushroom: 25
- teapot → king_penguin: 23
- mushroom → brown_bear: 21
- king_penguin → teapot: 21
- golden_retriever → mushroom: 20
- teapot → golden_retriever: 20

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
