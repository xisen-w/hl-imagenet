# Eval Run: 2026-05-16_18-23-56

**Tag:** session14_bear_sig_sat_guard
**Samples:** 2000
**Top-1 Accuracy:** 0.577
**Top-3 Accuracy:** 0.772
**Mean Latency:** 101 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.490 | 98/200 |
| golden_retriever | 0.485 | 97/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.585 | 117/200 |
| mushroom | 0.520 | 104/200 |
| orange | 0.635 | 127/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.615 | 123/200 |
| teapot | 0.415 | 83/200 |

## Top Confusions

- brown_bear → mushroom: 30
- teapot → banana: 29
- banana → orange: 25
- sports_car → school_bus: 25
- brown_bear → golden_retriever: 23
- orange → banana: 21
- mushroom → brown_bear: 20
- teapot → golden_retriever: 20
- golden_retriever → mushroom: 19
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
