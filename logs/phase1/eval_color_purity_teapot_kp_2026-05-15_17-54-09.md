# Eval Run: 2026-05-15_17-54-09

**Tag:** color_purity_teapot_kp
**Samples:** 2000
**Top-1 Accuracy:** 0.536
**Top-3 Accuracy:** 0.768
**Mean Latency:** 289 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.505 | 101/200 |
| golden_retriever | 0.420 | 84/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.520 | 104/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.575 | 115/200 |
| school_bus | 0.710 | 142/200 |
| sports_car | 0.540 | 108/200 |
| teapot | 0.350 | 70/200 |

## Top Confusions

- sports_car → school_bus: 32
- banana → orange: 30
- orange → banana: 30
- brown_bear → mushroom: 29
- teapot → banana: 27
- teapot → king_penguin: 26
- golden_retriever → brown_bear: 25
- mushroom → banana: 25
- school_bus → sports_car: 23
- golden_retriever → mushroom: 22

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
