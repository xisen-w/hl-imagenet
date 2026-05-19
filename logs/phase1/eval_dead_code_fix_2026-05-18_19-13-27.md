# Eval Run: 2026-05-18_19-13-27

**Tag:** dead_code_fix
**Samples:** 2000
**Top-1 Accuracy:** 0.789
**Top-3 Accuracy:** 0.847
**Mean Latency:** 39 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.810 | 162/200 |
| brown_bear | 0.830 | 166/200 |
| golden_retriever | 0.750 | 150/200 |
| jellyfish | 0.795 | 159/200 |
| king_penguin | 0.755 | 151/200 |
| mushroom | 0.740 | 148/200 |
| orange | 0.760 | 152/200 |
| school_bus | 0.880 | 176/200 |
| sports_car | 0.820 | 164/200 |
| teapot | 0.755 | 151/200 |

## Top Confusions

- orange → banana: 14
- sports_car → school_bus: 13
- teapot → banana: 11
- brown_bear → golden_retriever: 11
- golden_retriever → king_penguin: 10
- mushroom → banana: 10
- mushroom → golden_retriever: 10
- brown_bear → mushroom: 10
- king_penguin → banana: 10
- king_penguin → golden_retriever: 10

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
