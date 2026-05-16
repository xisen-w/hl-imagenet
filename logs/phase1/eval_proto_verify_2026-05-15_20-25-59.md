# Eval Run: 2026-05-15_20-25-59

**Tag:** proto_verify
**Samples:** 2000
**Top-1 Accuracy:** 0.540
**Top-3 Accuracy:** 0.768
**Mean Latency:** 123 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.475 | 95/200 |
| golden_retriever | 0.410 | 82/200 |
| jellyfish | 0.710 | 142/200 |
| king_penguin | 0.525 | 105/200 |
| mushroom | 0.500 | 100/200 |
| orange | 0.630 | 126/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.535 | 107/200 |
| teapot | 0.390 | 78/200 |

## Top Confusions

- banana → orange: 34
- sports_car → school_bus: 32
- brown_bear → mushroom: 28
- golden_retriever → mushroom: 27
- teapot → banana: 26
- brown_bear → golden_retriever: 25
- golden_retriever → brown_bear: 22
- teapot → golden_retriever: 22
- teapot → king_penguin: 22
- mushroom → banana: 21

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
