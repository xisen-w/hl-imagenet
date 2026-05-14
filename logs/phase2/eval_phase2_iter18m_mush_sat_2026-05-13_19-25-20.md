# Eval Run: 2026-05-13_19-25-20

**Tag:** phase2_iter18m_mush_sat
**Samples:** 2000
**Top-1 Accuracy:** 0.511
**Top-3 Accuracy:** 0.754
**Mean Latency:** 105 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.475 | 95/200 |
| brown_bear | 0.445 | 89/200 |
| golden_retriever | 0.445 | 89/200 |
| jellyfish | 0.685 | 137/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.475 | 95/200 |
| orange | 0.565 | 113/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.545 | 109/200 |
| teapot | 0.210 | 42/200 |

## Top Confusions

- teapot → king_penguin: 47
- banana → orange: 38
- sports_car → school_bus: 32
- teapot → banana: 29
- orange → banana: 26
- brown_bear → king_penguin: 25
- mushroom → banana: 23
- brown_bear → mushroom: 23
- school_bus → sports_car: 22
- teapot → golden_retriever: 21

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
