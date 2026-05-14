# Eval Run: 2026-05-13_19-21-03

**Tag:** phase2_iter18l_grad_hv
**Samples:** 2000
**Top-1 Accuracy:** 0.509
**Top-3 Accuracy:** 0.752
**Mean Latency:** 99 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.475 | 95/200 |
| brown_bear | 0.445 | 89/200 |
| golden_retriever | 0.445 | 89/200 |
| jellyfish | 0.680 | 136/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.460 | 92/200 |
| orange | 0.565 | 113/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.545 | 109/200 |
| teapot | 0.210 | 42/200 |

## Top Confusions

- teapot → king_penguin: 47
- banana → orange: 38
- sports_car → school_bus: 33
- teapot → banana: 30
- orange → banana: 26
- brown_bear → king_penguin: 25
- brown_bear → mushroom: 24
- mushroom → banana: 23
- school_bus → sports_car: 22
- golden_retriever → mushroom: 21

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
