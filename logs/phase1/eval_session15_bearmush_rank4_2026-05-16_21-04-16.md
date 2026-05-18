# Eval Run: 2026-05-16_21-04-16

**Tag:** session15_bearmush_rank4
**Samples:** 2000
**Top-1 Accuracy:** 0.583
**Top-3 Accuracy:** 0.770
**Mean Latency:** 204 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.550 | 110/200 |
| golden_retriever | 0.490 | 98/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.590 | 118/200 |
| mushroom | 0.520 | 104/200 |
| orange | 0.630 | 126/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.605 | 121/200 |
| teapot | 0.420 | 84/200 |

## Top Confusions

- teapot → banana: 28
- sports_car → school_bus: 27
- banana → orange: 25
- brown_bear → golden_retriever: 22
- teapot → golden_retriever: 21
- orange → banana: 21
- mushroom → brown_bear: 20
- brown_bear → mushroom: 20
- golden_retriever → brown_bear: 19
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
