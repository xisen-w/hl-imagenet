# Eval Run: 2026-05-14_03-22-33

**Tag:** no_cal_restored
**Samples:** 2000
**Top-1 Accuracy:** 0.484
**Top-3 Accuracy:** 0.754
**Mean Latency:** 148 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.520 | 104/200 |
| brown_bear | 0.435 | 87/200 |
| golden_retriever | 0.290 | 58/200 |
| jellyfish | 0.660 | 132/200 |
| king_penguin | 0.460 | 92/200 |
| mushroom | 0.460 | 92/200 |
| orange | 0.470 | 94/200 |
| school_bus | 0.830 | 166/200 |
| sports_car | 0.415 | 83/200 |
| teapot | 0.305 | 61/200 |

## Top Confusions

- sports_car → school_bus: 56
- orange → banana: 48
- golden_retriever → brown_bear: 37
- teapot → banana: 31
- mushroom → banana: 29
- banana → orange: 28
- brown_bear → school_bus: 27
- brown_bear → mushroom: 25
- teapot → king_penguin: 24
- jellyfish → teapot: 24

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
