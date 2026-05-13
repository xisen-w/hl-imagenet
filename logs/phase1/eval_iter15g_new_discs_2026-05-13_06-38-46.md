# Eval Run: 2026-05-13_06-38-46

**Tag:** iter15g_new_discs
**Samples:** 2000
**Top-1 Accuracy:** 0.490
**Top-3 Accuracy:** 0.734
**Mean Latency:** 97 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.500 | 100/200 |
| brown_bear | 0.425 | 85/200 |
| golden_retriever | 0.370 | 74/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.475 | 95/200 |
| mushroom | 0.435 | 87/200 |
| orange | 0.480 | 96/200 |
| school_bus | 0.740 | 148/200 |
| sports_car | 0.505 | 101/200 |
| teapot | 0.310 | 62/200 |

## Top Confusions

- orange → banana: 49
- teapot → king_penguin: 38
- sports_car → school_bus: 36
- teapot → banana: 34
- golden_retriever → mushroom: 30
- mushroom → banana: 28
- brown_bear → golden_retriever: 26
- brown_bear → mushroom: 26
- golden_retriever → banana: 24
- mushroom → brown_bear: 24

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- phase2_jellyfish_signature: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- blob_textured_interior: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- distinct_background: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- horizontal_window_pattern: used by 10 classes
