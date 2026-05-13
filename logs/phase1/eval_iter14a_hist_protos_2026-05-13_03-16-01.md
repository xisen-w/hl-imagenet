# Eval Run: 2026-05-13_03-16-01

**Tag:** iter14a_hist_protos
**Samples:** 2000
**Top-1 Accuracy:** 0.474
**Top-3 Accuracy:** 0.730
**Mean Latency:** 107 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.565 | 113/200 |
| brown_bear | 0.415 | 83/200 |
| golden_retriever | 0.400 | 80/200 |
| jellyfish | 0.650 | 130/200 |
| king_penguin | 0.390 | 78/200 |
| mushroom | 0.370 | 74/200 |
| orange | 0.415 | 83/200 |
| school_bus | 0.720 | 144/200 |
| sports_car | 0.500 | 100/200 |
| teapot | 0.315 | 63/200 |

## Top Confusions

- orange → banana: 68
- golden_retriever → banana: 34
- teapot → banana: 34
- sports_car → school_bus: 34
- brown_bear → golden_retriever: 31
- mushroom → banana: 30
- teapot → king_penguin: 30
- mushroom → golden_retriever: 28
- mushroom → brown_bear: 27
- king_penguin → teapot: 25

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
