# Eval Run: 2026-05-13_03-26-36

**Tag:** iter14c_no_teapot_kp
**Samples:** 2000
**Top-1 Accuracy:** 0.477
**Top-3 Accuracy:** 0.729
**Mean Latency:** 110 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.505 | 101/200 |
| brown_bear | 0.400 | 80/200 |
| golden_retriever | 0.385 | 77/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.410 | 82/200 |
| mushroom | 0.395 | 79/200 |
| orange | 0.475 | 95/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.500 | 100/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- orange → banana: 49
- sports_car → school_bus: 35
- teapot → king_penguin: 33
- teapot → banana: 30
- mushroom → brown_bear: 29
- brown_bear → golden_retriever: 29
- golden_retriever → mushroom: 25
- mushroom → banana: 25
- king_penguin → teapot: 25
- mushroom → golden_retriever: 24

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
