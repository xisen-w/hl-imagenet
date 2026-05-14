# Eval Run: 2026-05-13_18-02-32

**Tag:** phase2_iter18g_perclass_hist
**Samples:** 2000
**Top-1 Accuracy:** 0.472
**Top-3 Accuracy:** 0.729
**Mean Latency:** 511 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.430 | 86/200 |
| brown_bear | 0.310 | 62/200 |
| golden_retriever | 0.380 | 76/200 |
| jellyfish | 0.685 | 137/200 |
| king_penguin | 0.480 | 96/200 |
| mushroom | 0.440 | 88/200 |
| orange | 0.565 | 113/200 |
| school_bus | 0.795 | 159/200 |
| sports_car | 0.535 | 107/200 |
| teapot | 0.105 | 21/200 |

## Top Confusions

- teapot → king_penguin: 49
- sports_car → school_bus: 48
- banana → school_bus: 40
- banana → orange: 39
- brown_bear → school_bus: 39
- teapot → school_bus: 37
- golden_retriever → school_bus: 32
- mushroom → school_bus: 32
- brown_bear → king_penguin: 32
- brown_bear → mushroom: 31

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
