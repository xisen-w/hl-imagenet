# Eval Run: 2026-05-13_03-58-26

**Tag:** iter14i_better_orange
**Samples:** 2000
**Top-1 Accuracy:** 0.481
**Top-3 Accuracy:** 0.729
**Mean Latency:** 107 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.460 | 92/200 |
| brown_bear | 0.400 | 80/200 |
| golden_retriever | 0.385 | 77/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.470 | 94/200 |
| mushroom | 0.395 | 79/200 |
| orange | 0.515 | 103/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.500 | 100/200 |
| teapot | 0.310 | 62/200 |

## Top Confusions

- orange → banana: 41
- teapot → king_penguin: 37
- sports_car → school_bus: 35
- mushroom → brown_bear: 29
- brown_bear → golden_retriever: 29
- teapot → banana: 26
- golden_retriever → mushroom: 25
- mushroom → banana: 25
- mushroom → golden_retriever: 24
- banana → teapot: 23

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
