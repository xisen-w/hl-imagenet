# Eval Run: 2026-05-13_06-25-23

**Tag:** iter15e_bus_guard
**Samples:** 2000
**Top-1 Accuracy:** 0.494
**Top-3 Accuracy:** 0.744
**Mean Latency:** 104 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.490 | 98/200 |
| golden_retriever | 0.405 | 81/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.475 | 95/200 |
| mushroom | 0.445 | 89/200 |
| orange | 0.480 | 96/200 |
| school_bus | 0.590 | 118/200 |
| sports_car | 0.530 | 106/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- orange → banana: 51
- teapot → king_penguin: 38
- teapot → banana: 34
- mushroom → banana: 33
- golden_retriever → banana: 30
- mushroom → brown_bear: 27
- brown_bear → golden_retriever: 24
- banana → teapot: 23
- sports_car → king_penguin: 23
- golden_retriever → mushroom: 21

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
