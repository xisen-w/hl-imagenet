# Eval Run: 2026-05-18_06-18-32

**Tag:** bear_mush_cbr
**Samples:** 2000
**Top-1 Accuracy:** 0.678
**Top-3 Accuracy:** 0.796
**Mean Latency:** 61 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.675 | 135/200 |
| brown_bear | 0.715 | 143/200 |
| golden_retriever | 0.575 | 115/200 |
| jellyfish | 0.745 | 149/200 |
| king_penguin | 0.680 | 136/200 |
| mushroom | 0.590 | 118/200 |
| orange | 0.695 | 139/200 |
| school_bus | 0.825 | 165/200 |
| sports_car | 0.735 | 147/200 |
| teapot | 0.550 | 110/200 |

## Top Confusions

- mushroom → brown_bear: 24
- teapot → banana: 23
- orange → banana: 20
- sports_car → school_bus: 18
- brown_bear → mushroom: 16
- golden_retriever → mushroom: 15
- golden_retriever → brown_bear: 15
- king_penguin → teapot: 15
- golden_retriever → king_penguin: 14
- orange → teapot: 14

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
