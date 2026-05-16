# Eval Run: 2026-05-15_21-45-19

**Tag:** proto_extended
**Samples:** 2000
**Top-1 Accuracy:** 0.550
**Top-3 Accuracy:** 0.770
**Mean Latency:** 114 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.525 | 105/200 |
| golden_retriever | 0.420 | 84/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.545 | 109/200 |
| mushroom | 0.520 | 104/200 |
| orange | 0.645 | 129/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.535 | 107/200 |
| teapot | 0.390 | 78/200 |

## Top Confusions

- banana → orange: 34
- sports_car → school_bus: 32
- brown_bear → mushroom: 29
- golden_retriever → brown_bear: 26
- teapot → banana: 26
- golden_retriever → mushroom: 23
- school_bus → sports_car: 22
- teapot → golden_retriever: 21
- teapot → king_penguin: 20
- jellyfish → teapot: 19

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
