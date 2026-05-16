# Eval Run: 2026-05-16_02-49-21

**Tag:** expanded_whitelist
**Samples:** 2000
**Top-1 Accuracy:** 0.563
**Top-3 Accuracy:** 0.770
**Mean Latency:** 275 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.490 | 98/200 |
| brown_bear | 0.550 | 110/200 |
| golden_retriever | 0.415 | 83/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.570 | 114/200 |
| mushroom | 0.520 | 104/200 |
| orange | 0.615 | 123/200 |
| school_bus | 0.750 | 150/200 |
| sports_car | 0.610 | 122/200 |
| teapot | 0.410 | 82/200 |

## Top Confusions

- banana → orange: 34
- teapot → banana: 28
- golden_retriever → brown_bear: 25
- brown_bear → mushroom: 25
- sports_car → school_bus: 25
- banana → teapot: 22
- mushroom → brown_bear: 21
- teapot → golden_retriever: 21
- orange → teapot: 21
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
