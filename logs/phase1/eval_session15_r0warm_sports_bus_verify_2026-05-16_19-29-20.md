# Eval Run: 2026-05-16_19-29-20

**Tag:** session15_r0warm_sports_bus_verify
**Samples:** 2000
**Top-1 Accuracy:** 0.581
**Top-3 Accuracy:** 0.770
**Mean Latency:** 116 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.545 | 109/200 |
| golden_retriever | 0.475 | 95/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.590 | 118/200 |
| mushroom | 0.505 | 101/200 |
| orange | 0.630 | 126/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.615 | 123/200 |
| teapot | 0.420 | 84/200 |

## Top Confusions

- teapot → banana: 28
- banana → orange: 25
- sports_car → school_bus: 24
- golden_retriever → mushroom: 22
- mushroom → brown_bear: 22
- brown_bear → golden_retriever: 22
- brown_bear → mushroom: 22
- teapot → golden_retriever: 21
- orange → banana: 21
- teapot → king_penguin: 19

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
