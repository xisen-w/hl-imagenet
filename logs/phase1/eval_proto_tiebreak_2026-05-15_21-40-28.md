# Eval Run: 2026-05-15_21-40-28

**Tag:** proto_tiebreak
**Samples:** 2000
**Top-1 Accuracy:** 0.520
**Top-3 Accuracy:** 0.770
**Mean Latency:** 110 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.445 | 89/200 |
| golden_retriever | 0.380 | 76/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.535 | 107/200 |
| mushroom | 0.535 | 107/200 |
| orange | 0.650 | 130/200 |
| school_bus | 0.560 | 112/200 |
| sports_car | 0.460 | 92/200 |
| teapot | 0.405 | 81/200 |

## Top Confusions

- banana → orange: 36
- brown_bear → king_penguin: 32
- teapot → banana: 29
- school_bus → sports_car: 29
- brown_bear → mushroom: 28
- sports_car → king_penguin: 28
- golden_retriever → mushroom: 25
- teapot → king_penguin: 25
- sports_car → school_bus: 24
- golden_retriever → banana: 22

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
