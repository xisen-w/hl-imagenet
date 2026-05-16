# Eval Run: 2026-05-15_08-35-06

**Tag:** disc_elong_gabor_v1
**Samples:** 2000
**Top-1 Accuracy:** 0.522
**Top-3 Accuracy:** 0.764
**Mean Latency:** 144 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.455 | 91/200 |
| golden_retriever | 0.410 | 82/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.515 | 103/200 |
| mushroom | 0.495 | 99/200 |
| orange | 0.560 | 112/200 |
| school_bus | 0.700 | 140/200 |
| sports_car | 0.550 | 110/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- banana → orange: 33
- teapot → banana: 31
- orange → banana: 31
- sports_car → school_bus: 29
- brown_bear → mushroom: 28
- school_bus → sports_car: 27
- teapot → king_penguin: 25
- brown_bear → king_penguin: 24
- mushroom → banana: 23
- golden_retriever → king_penguin: 22

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
