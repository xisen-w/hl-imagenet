# Eval Run: 2026-05-18_01-22-35

**Tag:** session19_wide_margin
**Samples:** 2000
**Top-1 Accuracy:** 0.616
**Top-3 Accuracy:** 0.769
**Mean Latency:** 203 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.610 | 122/200 |
| brown_bear | 0.590 | 118/200 |
| golden_retriever | 0.540 | 108/200 |
| jellyfish | 0.715 | 143/200 |
| king_penguin | 0.600 | 120/200 |
| mushroom | 0.530 | 106/200 |
| orange | 0.665 | 133/200 |
| school_bus | 0.795 | 159/200 |
| sports_car | 0.650 | 130/200 |
| teapot | 0.460 | 92/200 |

## Top Confusions

- sports_car → school_bus: 27
- teapot → banana: 26
- brown_bear → golden_retriever: 23
- orange → banana: 21
- brown_bear → mushroom: 21
- teapot → golden_retriever: 20
- mushroom → golden_retriever: 18
- banana → orange: 18
- jellyfish → teapot: 18
- mushroom → brown_bear: 17

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
