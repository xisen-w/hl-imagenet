# Eval Run: 2026-05-16_20-26-32

**Tag:** session15_teapot_kp_repulsion
**Samples:** 2000
**Top-1 Accuracy:** 0.580
**Top-3 Accuracy:** 0.770
**Mean Latency:** 92 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.550 | 110/200 |
| brown_bear | 0.545 | 109/200 |
| golden_retriever | 0.490 | 98/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.590 | 118/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.635 | 127/200 |
| school_bus | 0.760 | 152/200 |
| sports_car | 0.600 | 120/200 |
| teapot | 0.415 | 83/200 |

## Top Confusions

- teapot → banana: 28
- banana → orange: 26
- sports_car → school_bus: 26
- mushroom → brown_bear: 22
- brown_bear → golden_retriever: 22
- brown_bear → mushroom: 22
- teapot → golden_retriever: 21
- golden_retriever → mushroom: 19
- orange → banana: 19
- golden_retriever → brown_bear: 18

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
