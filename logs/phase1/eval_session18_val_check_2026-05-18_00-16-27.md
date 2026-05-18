# Eval Run: 2026-05-18_00-16-27

**Tag:** session18_val_check
**Samples:** 2000
**Top-1 Accuracy:** 0.530
**Top-3 Accuracy:** 0.756
**Mean Latency:** 107 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.410 | 82/200 |
| golden_retriever | 0.410 | 82/200 |
| jellyfish | 0.685 | 137/200 |
| king_penguin | 0.540 | 108/200 |
| mushroom | 0.465 | 93/200 |
| orange | 0.615 | 123/200 |
| school_bus | 0.690 | 138/200 |
| sports_car | 0.610 | 122/200 |
| teapot | 0.365 | 73/200 |

## Top Confusions

- brown_bear → golden_retriever: 38
- orange → banana: 36
- sports_car → school_bus: 30
- golden_retriever → mushroom: 29
- teapot → banana: 29
- brown_bear → mushroom: 28
- golden_retriever → teapot: 22
- golden_retriever → brown_bear: 20
- mushroom → golden_retriever: 20
- mushroom → brown_bear: 20

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
