# Eval Run: 2026-05-15_15-26-46

**Tag:** cal_banana_kp
**Samples:** 2000
**Top-1 Accuracy:** 0.530
**Top-3 Accuracy:** 0.761
**Mean Latency:** 243 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.500 | 100/200 |
| brown_bear | 0.500 | 100/200 |
| golden_retriever | 0.415 | 83/200 |
| jellyfish | 0.710 | 142/200 |
| king_penguin | 0.475 | 95/200 |
| mushroom | 0.515 | 103/200 |
| orange | 0.575 | 115/200 |
| school_bus | 0.720 | 144/200 |
| sports_car | 0.550 | 110/200 |
| teapot | 0.345 | 69/200 |

## Top Confusions

- banana → orange: 33
- sports_car → school_bus: 32
- orange → banana: 29
- brown_bear → mushroom: 29
- teapot → banana: 26
- golden_retriever → brown_bear: 25
- golden_retriever → mushroom: 24
- school_bus → sports_car: 23
- mushroom → banana: 21
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
