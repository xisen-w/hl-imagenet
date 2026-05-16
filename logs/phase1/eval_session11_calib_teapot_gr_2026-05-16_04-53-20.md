# Eval Run: 2026-05-16_04-53-20

**Tag:** session11_calib_teapot_gr
**Samples:** 2000
**Top-1 Accuracy:** 0.554
**Top-3 Accuracy:** 0.769
**Mean Latency:** 128 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.510 | 102/200 |
| golden_retriever | 0.415 | 83/200 |
| jellyfish | 0.685 | 137/200 |
| king_penguin | 0.555 | 111/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.625 | 125/200 |
| school_bus | 0.730 | 146/200 |
| sports_car | 0.585 | 117/200 |
| teapot | 0.410 | 82/200 |

## Top Confusions

- banana → orange: 34
- teapot → banana: 27
- golden_retriever → brown_bear: 26
- sports_car → school_bus: 24
- mushroom → brown_bear: 23
- brown_bear → mushroom: 23
- king_penguin → teapot: 23
- teapot → golden_retriever: 22
- banana → teapot: 20
- golden_retriever → mushroom: 19

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
