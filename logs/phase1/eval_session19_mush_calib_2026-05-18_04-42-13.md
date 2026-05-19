# Eval Run: 2026-05-18_04-42-13

**Tag:** session19_mush_calib
**Samples:** 2000
**Top-1 Accuracy:** 0.668
**Top-3 Accuracy:** 0.790
**Mean Latency:** 50 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.665 | 133/200 |
| brown_bear | 0.695 | 139/200 |
| golden_retriever | 0.535 | 107/200 |
| jellyfish | 0.745 | 149/200 |
| king_penguin | 0.675 | 135/200 |
| mushroom | 0.580 | 116/200 |
| orange | 0.700 | 140/200 |
| school_bus | 0.825 | 165/200 |
| sports_car | 0.725 | 145/200 |
| teapot | 0.535 | 107/200 |

## Top Confusions

- mushroom → brown_bear: 26
- teapot → banana: 23
- golden_retriever → mushroom: 21
- sports_car → school_bus: 21
- orange → banana: 19
- brown_bear → mushroom: 18
- golden_retriever → brown_bear: 17
- king_penguin → teapot: 16
- golden_retriever → king_penguin: 14
- teapot → brown_bear: 14

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
