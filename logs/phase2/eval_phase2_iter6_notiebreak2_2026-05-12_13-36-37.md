# Eval Run: 2026-05-12_13-36-37

**Tag:** phase2_iter6_notiebreak2
**Samples:** 500
**Top-1 Accuracy:** 0.336
**Top-3 Accuracy:** 0.696
**Mean Latency:** 50 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.640 | 32/50 |
| brown_bear | 0.080 | 4/50 |
| golden_retriever | 0.320 | 16/50 |
| jellyfish | 0.680 | 34/50 |
| king_penguin | 0.580 | 29/50 |
| mushroom | 0.100 | 5/50 |
| orange | 0.200 | 10/50 |
| school_bus | 0.520 | 26/50 |
| sports_car | 0.240 | 12/50 |
| teapot | 0.000 | 0/50 |

## Top Confusions

- orange → banana: 23
- teapot → king_penguin: 22
- golden_retriever → banana: 20
- sports_car → king_penguin: 19
- teapot → banana: 16
- brown_bear → golden_retriever: 14
- mushroom → golden_retriever: 13
- mushroom → banana: 12
- brown_bear → king_penguin: 12
- golden_retriever → king_penguin: 11

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
