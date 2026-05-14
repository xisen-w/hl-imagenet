# Eval Run: 2026-05-14_11-26-17

**Tag:** teapot_shape
**Samples:** 2000
**Top-1 Accuracy:** 0.504
**Top-3 Accuracy:** 0.756
**Mean Latency:** 167 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.500 | 100/200 |
| brown_bear | 0.460 | 92/200 |
| golden_retriever | 0.380 | 76/200 |
| jellyfish | 0.650 | 130/200 |
| king_penguin | 0.505 | 101/200 |
| mushroom | 0.455 | 91/200 |
| orange | 0.575 | 115/200 |
| school_bus | 0.765 | 153/200 |
| sports_car | 0.520 | 104/200 |
| teapot | 0.230 | 46/200 |

## Top Confusions

- teapot → king_penguin: 42
- banana → orange: 35
- sports_car → school_bus: 35
- mushroom → banana: 30
- teapot → banana: 30
- orange → banana: 26
- brown_bear → mushroom: 25
- golden_retriever → banana: 23
- brown_bear → king_penguin: 23
- golden_retriever → brown_bear: 22

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
