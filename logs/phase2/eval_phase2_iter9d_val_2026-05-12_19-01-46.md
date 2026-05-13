# Eval Run: 2026-05-12_19-01-46

**Tag:** phase2_iter9d_val
**Samples:** 2000
**Top-1 Accuracy:** 0.450
**Top-3 Accuracy:** 0.731
**Mean Latency:** 105 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.485 | 97/200 |
| brown_bear | 0.315 | 63/200 |
| golden_retriever | 0.390 | 78/200 |
| jellyfish | 0.625 | 125/200 |
| king_penguin | 0.380 | 76/200 |
| mushroom | 0.420 | 84/200 |
| orange | 0.440 | 88/200 |
| school_bus | 0.625 | 125/200 |
| sports_car | 0.490 | 98/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- orange → banana: 55
- brown_bear → golden_retriever: 47
- mushroom → golden_retriever: 43
- teapot → banana: 33
- teapot → king_penguin: 32
- king_penguin → teapot: 30
- brown_bear → mushroom: 29
- golden_retriever → mushroom: 28
- golden_retriever → banana: 27
- jellyfish → teapot: 27

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
