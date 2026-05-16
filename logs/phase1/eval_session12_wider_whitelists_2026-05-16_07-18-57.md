# Eval Run: 2026-05-16_07-18-57

**Tag:** session12_wider_whitelists
**Samples:** 2000
**Top-1 Accuracy:** 0.566
**Top-3 Accuracy:** 0.769
**Mean Latency:** 119 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.525 | 105/200 |
| brown_bear | 0.525 | 105/200 |
| golden_retriever | 0.455 | 91/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.535 | 107/200 |
| mushroom | 0.515 | 103/200 |
| orange | 0.605 | 121/200 |
| school_bus | 0.745 | 149/200 |
| sports_car | 0.630 | 126/200 |
| teapot | 0.415 | 83/200 |

## Top Confusions

- banana → orange: 34
- teapot → banana: 28
- brown_bear → mushroom: 27
- sports_car → school_bus: 24
- mushroom → brown_bear: 23
- orange → teapot: 22
- golden_retriever → mushroom: 21
- king_penguin → brown_bear: 21
- teapot → golden_retriever: 20
- school_bus → sports_car: 20

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
