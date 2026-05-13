# Eval Run: 2026-05-13_07-38-23

**Tag:** iter15j_hist_blend
**Samples:** 2000
**Top-1 Accuracy:** 0.501
**Top-3 Accuracy:** 0.742
**Mean Latency:** 100 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.400 | 80/200 |
| golden_retriever | 0.400 | 80/200 |
| jellyfish | 0.655 | 131/200 |
| king_penguin | 0.480 | 96/200 |
| mushroom | 0.415 | 83/200 |
| orange | 0.505 | 101/200 |
| school_bus | 0.785 | 157/200 |
| sports_car | 0.565 | 113/200 |
| teapot | 0.300 | 60/200 |

## Top Confusions

- orange → banana: 51
- sports_car → school_bus: 38
- teapot → king_penguin: 37
- teapot → banana: 33
- banana → school_bus: 31
- mushroom → banana: 29
- brown_bear → mushroom: 28
- golden_retriever → banana: 26
- golden_retriever → mushroom: 24
- mushroom → school_bus: 24

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
