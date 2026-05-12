# Eval Run: 2026-05-12_13-39-16

**Tag:** phase2_iter6_train_full
**Samples:** 2000
**Top-1 Accuracy:** 0.337
**Top-3 Accuracy:** 0.694
**Mean Latency:** 69 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.635 | 127/200 |
| brown_bear | 0.070 | 14/200 |
| golden_retriever | 0.330 | 66/200 |
| jellyfish | 0.615 | 123/200 |
| king_penguin | 0.645 | 129/200 |
| mushroom | 0.100 | 20/200 |
| orange | 0.275 | 55/200 |
| school_bus | 0.480 | 96/200 |
| sports_car | 0.210 | 42/200 |
| teapot | 0.005 | 1/200 |

## Top Confusions

- teapot → king_penguin: 90
- orange → banana: 84
- sports_car → king_penguin: 75
- golden_retriever → banana: 69
- brown_bear → golden_retriever: 64
- mushroom → banana: 52
- brown_bear → king_penguin: 51
- jellyfish → king_penguin: 50
- mushroom → golden_retriever: 49
- teapot → banana: 46

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- phase2_jellyfish_signature: used by 10 classes
- yellow_dominant: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- phase2_orange_signature: used by 10 classes
