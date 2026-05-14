# Eval Run: 2026-05-13_19-46-48

**Tag:** phase2_session5_val
**Samples:** 2000
**Top-1 Accuracy:** 0.503
**Top-3 Accuracy:** 0.751
**Mean Latency:** 100 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.420 | 84/200 |
| brown_bear | 0.380 | 76/200 |
| golden_retriever | 0.410 | 82/200 |
| jellyfish | 0.650 | 130/200 |
| king_penguin | 0.560 | 112/200 |
| mushroom | 0.435 | 87/200 |
| orange | 0.560 | 112/200 |
| school_bus | 0.750 | 150/200 |
| sports_car | 0.575 | 115/200 |
| teapot | 0.290 | 58/200 |

## Top Confusions

- orange → banana: 38
- teapot → king_penguin: 37
- brown_bear → golden_retriever: 34
- sports_car → school_bus: 34
- teapot → banana: 32
- banana → orange: 29
- brown_bear → mushroom: 29
- golden_retriever → mushroom: 28
- banana → school_bus: 26
- brown_bear → king_penguin: 26

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
