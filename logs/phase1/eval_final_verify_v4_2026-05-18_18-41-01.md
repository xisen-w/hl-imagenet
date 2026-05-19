# Eval Run: 2026-05-18_18-41-01

**Tag:** final_verify_v4
**Samples:** 2000
**Top-1 Accuracy:** 0.780
**Top-3 Accuracy:** 0.843
**Mean Latency:** 103 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.810 | 162/200 |
| brown_bear | 0.810 | 162/200 |
| golden_retriever | 0.735 | 147/200 |
| jellyfish | 0.785 | 157/200 |
| king_penguin | 0.755 | 151/200 |
| mushroom | 0.730 | 146/200 |
| orange | 0.760 | 152/200 |
| school_bus | 0.880 | 176/200 |
| sports_car | 0.820 | 164/200 |
| teapot | 0.720 | 144/200 |

## Top Confusions

- teapot → banana: 16
- orange → banana: 13
- sports_car → school_bus: 13
- brown_bear → mushroom: 12
- mushroom → brown_bear: 11
- brown_bear → golden_retriever: 11
- king_penguin → mushroom: 11
- jellyfish → teapot: 11
- golden_retriever → king_penguin: 10
- mushroom → banana: 10

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
