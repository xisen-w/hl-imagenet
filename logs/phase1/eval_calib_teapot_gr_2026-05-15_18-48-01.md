# Eval Run: 2026-05-15_18-48-01

**Tag:** calib_teapot_gr
**Samples:** 2000
**Top-1 Accuracy:** 0.534
**Top-3 Accuracy:** 0.765
**Mean Latency:** 138 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.510 | 102/200 |
| golden_retriever | 0.450 | 90/200 |
| jellyfish | 0.680 | 136/200 |
| king_penguin | 0.535 | 107/200 |
| mushroom | 0.505 | 101/200 |
| orange | 0.555 | 111/200 |
| school_bus | 0.680 | 136/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.380 | 76/200 |

## Top Confusions

- banana → orange: 30
- sports_car → school_bus: 30
- orange → banana: 29
- teapot → banana: 28
- brown_bear → mushroom: 27
- golden_retriever → brown_bear: 25
- mushroom → banana: 23
- teapot → golden_retriever: 22
- teapot → king_penguin: 22
- orange → teapot: 22

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
