# Eval Run: 2026-05-12_16-26-42

**Tag:** phase2_current_val
**Samples:** 2000
**Top-1 Accuracy:** 0.383
**Top-3 Accuracy:** 0.721
**Mean Latency:** 22 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.465 | 93/200 |
| brown_bear | 0.250 | 50/200 |
| golden_retriever | 0.415 | 83/200 |
| jellyfish | 0.630 | 126/200 |
| king_penguin | 0.485 | 97/200 |
| mushroom | 0.080 | 16/200 |
| orange | 0.360 | 72/200 |
| school_bus | 0.560 | 112/200 |
| sports_car | 0.375 | 75/200 |
| teapot | 0.205 | 41/200 |

## Top Confusions

- orange → banana: 69
- teapot → king_penguin: 51
- mushroom → banana: 49
- mushroom → brown_bear: 44
- brown_bear → banana: 43
- mushroom → golden_retriever: 39
- sports_car → king_penguin: 39
- golden_retriever → banana: 37
- orange → golden_retriever: 34
- teapot → banana: 32

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
