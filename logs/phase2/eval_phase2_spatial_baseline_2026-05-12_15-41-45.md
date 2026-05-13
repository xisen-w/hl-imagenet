# Eval Run: 2026-05-12_15-41-45

**Tag:** phase2_spatial_baseline
**Samples:** 2000
**Top-1 Accuracy:** 0.362
**Top-3 Accuracy:** 0.715
**Mean Latency:** 108 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.125 | 25/200 |
| golden_retriever | 0.435 | 87/200 |
| jellyfish | 0.605 | 121/200 |
| king_penguin | 0.600 | 120/200 |
| mushroom | 0.140 | 28/200 |
| orange | 0.240 | 48/200 |
| school_bus | 0.540 | 108/200 |
| sports_car | 0.245 | 49/200 |
| teapot | 0.165 | 33/200 |

## Top Confusions

- orange → banana: 73
- sports_car → king_penguin: 66
- teapot → king_penguin: 60
- brown_bear → king_penguin: 50
- brown_bear → golden_retriever: 50
- mushroom → golden_retriever: 47
- mushroom → banana: 45
- school_bus → king_penguin: 45
- orange → golden_retriever: 45
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
