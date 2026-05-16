# Eval Run: 2026-05-15_07-06-28

**Tag:** gr_warm_hue_sig
**Samples:** 2000
**Top-1 Accuracy:** 0.512
**Top-3 Accuracy:** 0.760
**Mean Latency:** 187 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.500 | 100/200 |
| brown_bear | 0.445 | 89/200 |
| golden_retriever | 0.400 | 80/200 |
| jellyfish | 0.670 | 134/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.480 | 96/200 |
| orange | 0.565 | 113/200 |
| school_bus | 0.705 | 141/200 |
| sports_car | 0.530 | 106/200 |
| teapot | 0.315 | 63/200 |

## Top Confusions

- banana → orange: 33
- sports_car → school_bus: 33
- teapot → banana: 31
- brown_bear → mushroom: 29
- teapot → king_penguin: 26
- orange → banana: 26
- brown_bear → king_penguin: 26
- golden_retriever → mushroom: 25
- mushroom → banana: 25
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
