# Eval Run: 2026-05-18_19-22-13

**Tag:** bulk_fix1_deploy
**Samples:** 2000
**Top-1 Accuracy:** 0.820
**Top-3 Accuracy:** 0.861
**Mean Latency:** 33 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.850 | 170/200 |
| brown_bear | 0.840 | 168/200 |
| golden_retriever | 0.770 | 154/200 |
| jellyfish | 0.835 | 167/200 |
| king_penguin | 0.795 | 159/200 |
| mushroom | 0.765 | 153/200 |
| orange | 0.805 | 161/200 |
| school_bus | 0.900 | 180/200 |
| sports_car | 0.850 | 170/200 |
| teapot | 0.790 | 158/200 |

## Top Confusions

- sports_car → school_bus: 14
- orange → banana: 12
- golden_retriever → teapot: 11
- brown_bear → mushroom: 11
- brown_bear → golden_retriever: 11
- banana → orange: 10
- king_penguin → banana: 10
- mushroom → golden_retriever: 9
- orange → king_penguin: 9
- king_penguin → golden_retriever: 9

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
