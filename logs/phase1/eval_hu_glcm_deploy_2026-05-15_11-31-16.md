# Eval Run: 2026-05-15_11-31-16

**Tag:** hu_glcm_deploy
**Samples:** 2000
**Top-1 Accuracy:** 0.531
**Top-3 Accuracy:** 0.769
**Mean Latency:** 272 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.500 | 100/200 |
| golden_retriever | 0.420 | 84/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.500 | 100/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.710 | 142/200 |
| sports_car | 0.540 | 108/200 |
| teapot | 0.335 | 67/200 |

## Top Confusions

- banana → orange: 33
- sports_car → school_bus: 32
- orange → banana: 30
- brown_bear → mushroom: 29
- teapot → banana: 26
- golden_retriever → brown_bear: 25
- mushroom → banana: 24
- school_bus → sports_car: 23
- golden_retriever → mushroom: 22
- teapot → king_penguin: 22

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
