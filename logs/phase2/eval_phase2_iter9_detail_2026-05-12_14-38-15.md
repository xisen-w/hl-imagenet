# Eval Run: 2026-05-12_14-38-15

**Tag:** phase2_iter9_detail
**Samples:** 2000
**Top-1 Accuracy:** 0.346
**Top-3 Accuracy:** 0.708
**Mean Latency:** 32 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.650 | 130/200 |
| brown_bear | 0.045 | 9/200 |
| golden_retriever | 0.340 | 68/200 |
| jellyfish | 0.660 | 132/200 |
| king_penguin | 0.675 | 135/200 |
| mushroom | 0.250 | 50/200 |
| orange | 0.165 | 33/200 |
| school_bus | 0.530 | 106/200 |
| sports_car | 0.105 | 21/200 |
| teapot | 0.045 | 9/200 |

## Top Confusions

- sports_car → king_penguin: 100
- orange → banana: 86
- teapot → king_penguin: 81
- golden_retriever → banana: 71
- mushroom → banana: 66
- brown_bear → king_penguin: 61
- brown_bear → banana: 61
- teapot → banana: 49
- orange → golden_retriever: 49
- teapot → golden_retriever: 47

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- yellow_dominant: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- phase2_orange_signature: used by 10 classes
- phase2_brown_bear_signature: used by 10 classes
