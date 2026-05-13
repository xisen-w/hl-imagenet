# Eval Run: 2026-05-12_18-48-49

**Tag:** phase2_iter9c_val
**Samples:** 2000
**Top-1 Accuracy:** 0.446
**Top-3 Accuracy:** 0.729
**Mean Latency:** 108 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.470 | 94/200 |
| brown_bear | 0.310 | 62/200 |
| golden_retriever | 0.405 | 81/200 |
| jellyfish | 0.630 | 126/200 |
| king_penguin | 0.370 | 74/200 |
| mushroom | 0.405 | 81/200 |
| orange | 0.440 | 88/200 |
| school_bus | 0.625 | 125/200 |
| sports_car | 0.485 | 97/200 |
| teapot | 0.320 | 64/200 |

## Top Confusions

- orange → banana: 52
- brown_bear → golden_retriever: 46
- mushroom → golden_retriever: 45
- teapot → banana: 33
- king_penguin → teapot: 33
- teapot → king_penguin: 32
- golden_retriever → banana: 28
- jellyfish → teapot: 27
- brown_bear → mushroom: 26
- school_bus → sports_car: 25

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
