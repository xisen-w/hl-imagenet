# Eval Run: 2026-05-19_01-40-37

**Tag:** val_check_session29
**Samples:** 2000
**Top-1 Accuracy:** 0.413
**Top-3 Accuracy:** 0.688
**Mean Latency:** 73 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.405 | 81/200 |
| brown_bear | 0.345 | 69/200 |
| golden_retriever | 0.325 | 65/200 |
| jellyfish | 0.630 | 126/200 |
| king_penguin | 0.385 | 77/200 |
| mushroom | 0.310 | 62/200 |
| orange | 0.460 | 92/200 |
| school_bus | 0.555 | 111/200 |
| sports_car | 0.440 | 88/200 |
| teapot | 0.280 | 56/200 |

## Top Confusions

- orange → banana: 37
- golden_retriever → mushroom: 36
- mushroom → brown_bear: 36
- brown_bear → mushroom: 34
- brown_bear → golden_retriever: 34
- banana → orange: 31
- king_penguin → brown_bear: 30
- teapot → golden_retriever: 29
- mushroom → golden_retriever: 27
- sports_car → school_bus: 23

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
