# Eval Run: 2026-05-12_13-42-20

**Tag:** phase2_iter6_val_full
**Samples:** 2000
**Top-1 Accuracy:** 0.328
**Top-3 Accuracy:** 0.688
**Mean Latency:** 90 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.040 | 8/200 |
| golden_retriever | 0.280 | 56/200 |
| jellyfish | 0.625 | 125/200 |
| king_penguin | 0.630 | 126/200 |
| mushroom | 0.080 | 16/200 |
| orange | 0.300 | 60/200 |
| school_bus | 0.545 | 109/200 |
| sports_car | 0.250 | 50/200 |
| teapot | 0.015 | 3/200 |

## Top Confusions

- orange → banana: 98
- sports_car → king_penguin: 81
- teapot → king_penguin: 80
- golden_retriever → banana: 78
- mushroom → golden_retriever: 65
- brown_bear → golden_retriever: 64
- brown_bear → king_penguin: 52
- brown_bear → banana: 52
- teapot → golden_retriever: 45
- jellyfish → king_penguin: 44

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
