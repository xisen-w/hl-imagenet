# Eval Run: 2026-05-13_06-46-11

**Tag:** iter15h_gr_bus_only
**Samples:** 2000
**Top-1 Accuracy:** 0.495
**Top-3 Accuracy:** 0.734
**Mean Latency:** 100 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.430 | 86/200 |
| golden_retriever | 0.390 | 78/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.475 | 95/200 |
| mushroom | 0.430 | 86/200 |
| orange | 0.480 | 96/200 |
| school_bus | 0.740 | 148/200 |
| sports_car | 0.505 | 101/200 |
| teapot | 0.320 | 64/200 |

## Top Confusions

- orange → banana: 50
- teapot → king_penguin: 38
- sports_car → school_bus: 36
- teapot → banana: 34
- mushroom → banana: 29
- golden_retriever → banana: 28
- brown_bear → golden_retriever: 28
- mushroom → brown_bear: 24
- sports_car → king_penguin: 23
- golden_retriever → mushroom: 22

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
