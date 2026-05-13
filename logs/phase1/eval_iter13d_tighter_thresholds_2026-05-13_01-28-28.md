# Eval Run: 2026-05-13_01-28-28

**Tag:** iter13d_tighter_thresholds
**Samples:** 2000
**Top-1 Accuracy:** 0.473
**Top-3 Accuracy:** 0.729
**Mean Latency:** 164 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.385 | 77/200 |
| golden_retriever | 0.370 | 74/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.410 | 82/200 |
| mushroom | 0.400 | 80/200 |
| orange | 0.445 | 89/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.485 | 97/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- orange → banana: 58
- sports_car → school_bus: 38
- teapot → king_penguin: 33
- brown_bear → golden_retriever: 32
- teapot → banana: 31
- golden_retriever → banana: 30
- mushroom → banana: 26
- mushroom → brown_bear: 26
- golden_retriever → mushroom: 25
- mushroom → golden_retriever: 25

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
