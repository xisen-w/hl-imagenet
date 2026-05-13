# Eval Run: 2026-05-13_07-01-40

**Tag:** iter15i_orange_boost
**Samples:** 2000
**Top-1 Accuracy:** 0.494
**Top-3 Accuracy:** 0.734
**Mean Latency:** 123 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.430 | 86/200 |
| golden_retriever | 0.395 | 79/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.475 | 95/200 |
| mushroom | 0.430 | 86/200 |
| orange | 0.475 | 95/200 |
| school_bus | 0.740 | 148/200 |
| sports_car | 0.505 | 101/200 |
| teapot | 0.320 | 64/200 |

## Top Confusions

- orange → banana: 50
- teapot → king_penguin: 38
- sports_car → school_bus: 36
- teapot → banana: 33
- golden_retriever → banana: 29
- mushroom → banana: 29
- brown_bear → golden_retriever: 27
- banana → school_bus: 25
- mushroom → brown_bear: 24
- sports_car → king_penguin: 23

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
