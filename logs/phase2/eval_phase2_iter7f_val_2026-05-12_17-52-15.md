# Eval Run: 2026-05-12_17-52-15

**Tag:** phase2_iter7f_val
**Samples:** 2000
**Top-1 Accuracy:** 0.458
**Top-3 Accuracy:** 0.722
**Mean Latency:** 21 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.560 | 112/200 |
| brown_bear | 0.340 | 68/200 |
| golden_retriever | 0.405 | 81/200 |
| jellyfish | 0.640 | 128/200 |
| king_penguin | 0.370 | 74/200 |
| mushroom | 0.285 | 57/200 |
| orange | 0.475 | 95/200 |
| school_bus | 0.685 | 137/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.305 | 61/200 |

## Top Confusions

- orange → banana: 53
- brown_bear → golden_retriever: 50
- golden_retriever → banana: 39
- mushroom → golden_retriever: 38
- teapot → banana: 38
- mushroom → banana: 34
- jellyfish → teapot: 29
- king_penguin → teapot: 28
- teapot → king_penguin: 27
- sports_car → school_bus: 26

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
