# Eval Run: 2026-05-16_08-52-57

**Tag:** session13_bear_mush_cbr
**Samples:** 2000
**Top-1 Accuracy:** 0.576
**Top-3 Accuracy:** 0.769
**Mean Latency:** 124 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.535 | 107/200 |
| golden_retriever | 0.480 | 96/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.590 | 118/200 |
| mushroom | 0.505 | 101/200 |
| orange | 0.620 | 124/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.595 | 119/200 |
| teapot | 0.405 | 81/200 |

## Top Confusions

- teapot → banana: 29
- sports_car → school_bus: 26
- banana → orange: 25
- mushroom → brown_bear: 23
- brown_bear → mushroom: 23
- teapot → golden_retriever: 22
- orange → banana: 22
- brown_bear → golden_retriever: 22
- golden_retriever → mushroom: 20
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
