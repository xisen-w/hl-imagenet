# Eval Run: 2026-05-12_15-07-31

**Tag:** phase2_iter13_guarded_train
**Samples:** 2000
**Top-1 Accuracy:** 0.353
**Top-3 Accuracy:** 0.694
**Mean Latency:** 82 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.540 | 108/200 |
| brown_bear | 0.130 | 26/200 |
| golden_retriever | 0.465 | 93/200 |
| jellyfish | 0.635 | 127/200 |
| king_penguin | 0.560 | 112/200 |
| mushroom | 0.140 | 28/200 |
| orange | 0.180 | 36/200 |
| school_bus | 0.525 | 105/200 |
| sports_car | 0.220 | 44/200 |
| teapot | 0.140 | 28/200 |

## Top Confusions

- orange → banana: 67
- orange → golden_retriever: 66
- sports_car → king_penguin: 66
- teapot → king_penguin: 60
- brown_bear → golden_retriever: 58
- mushroom → golden_retriever: 57
- teapot → golden_retriever: 55
- brown_bear → king_penguin: 50
- school_bus → king_penguin: 47
- golden_retriever → king_penguin: 43

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
