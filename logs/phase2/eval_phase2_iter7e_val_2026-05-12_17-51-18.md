# Eval Run: 2026-05-12_17-51-18

**Tag:** phase2_iter7e_val
**Samples:** 2000
**Top-1 Accuracy:** 0.458
**Top-3 Accuracy:** 0.722
**Mean Latency:** 21 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.340 | 68/200 |
| golden_retriever | 0.405 | 81/200 |
| jellyfish | 0.640 | 128/200 |
| king_penguin | 0.365 | 73/200 |
| mushroom | 0.285 | 57/200 |
| orange | 0.470 | 94/200 |
| school_bus | 0.685 | 137/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.310 | 62/200 |

## Top Confusions

- orange → banana: 53
- brown_bear → golden_retriever: 50
- golden_retriever → banana: 39
- mushroom → golden_retriever: 38
- teapot → banana: 38
- mushroom → banana: 34
- jellyfish → teapot: 30
- king_penguin → teapot: 29
- teapot → king_penguin: 27
- king_penguin → brown_bear: 26

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
