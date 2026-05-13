# Eval Run: 2026-05-12_17-41-39

**Tag:** phase2_iter7b_val
**Samples:** 2000
**Top-1 Accuracy:** 0.449
**Top-3 Accuracy:** 0.726
**Mean Latency:** 22 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.555 | 111/200 |
| brown_bear | 0.330 | 66/200 |
| golden_retriever | 0.430 | 86/200 |
| jellyfish | 0.640 | 128/200 |
| king_penguin | 0.330 | 66/200 |
| mushroom | 0.280 | 56/200 |
| orange | 0.470 | 94/200 |
| school_bus | 0.635 | 127/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.300 | 60/200 |

## Top Confusions

- brown_bear → golden_retriever: 55
- orange → banana: 53
- mushroom → golden_retriever: 46
- king_penguin → teapot: 41
- golden_retriever → banana: 39
- teapot → banana: 38
- mushroom → banana: 33
- jellyfish → teapot: 32
- teapot → king_penguin: 27
- brown_bear → banana: 25

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
