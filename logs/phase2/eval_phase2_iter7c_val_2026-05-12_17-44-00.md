# Eval Run: 2026-05-12_17-44-00

**Tag:** phase2_iter7c_val
**Samples:** 2000
**Top-1 Accuracy:** 0.457
**Top-3 Accuracy:** 0.726
**Mean Latency:** 22 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.555 | 111/200 |
| brown_bear | 0.330 | 66/200 |
| golden_retriever | 0.395 | 79/200 |
| jellyfish | 0.640 | 128/200 |
| king_penguin | 0.350 | 70/200 |
| mushroom | 0.280 | 56/200 |
| orange | 0.470 | 94/200 |
| school_bus | 0.685 | 137/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.345 | 69/200 |

## Top Confusions

- orange → banana: 53
- brown_bear → golden_retriever: 50
- golden_retriever → banana: 39
- mushroom → golden_retriever: 38
- teapot → banana: 38
- king_penguin → teapot: 36
- mushroom → banana: 33
- jellyfish → teapot: 30
- golden_retriever → teapot: 25
- teapot → king_penguin: 25

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
