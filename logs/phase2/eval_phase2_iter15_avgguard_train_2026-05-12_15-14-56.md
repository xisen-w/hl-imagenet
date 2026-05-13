# Eval Run: 2026-05-12_15-14-56

**Tag:** phase2_iter15_avgguard_train
**Samples:** 2000
**Top-1 Accuracy:** 0.348
**Top-3 Accuracy:** 0.713
**Mean Latency:** 103 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.590 | 118/200 |
| brown_bear | 0.095 | 19/200 |
| golden_retriever | 0.465 | 93/200 |
| jellyfish | 0.580 | 116/200 |
| king_penguin | 0.700 | 140/200 |
| mushroom | 0.195 | 39/200 |
| orange | 0.160 | 32/200 |
| school_bus | 0.445 | 89/200 |
| sports_car | 0.155 | 31/200 |
| teapot | 0.095 | 19/200 |

## Top Confusions

- sports_car → king_penguin: 97
- teapot → king_penguin: 83
- orange → banana: 81
- brown_bear → king_penguin: 67
- school_bus → king_penguin: 62
- brown_bear → golden_retriever: 57
- orange → golden_retriever: 55
- mushroom → golden_retriever: 52
- golden_retriever → king_penguin: 47
- teapot → golden_retriever: 45

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
