# Eval Run: 2026-05-12_20-56-54

**Tag:** iter11g_rerank3_tight
**Samples:** 2000
**Top-1 Accuracy:** 0.463
**Top-3 Accuracy:** 0.722
**Mean Latency:** 101 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.550 | 110/200 |
| brown_bear | 0.350 | 70/200 |
| golden_retriever | 0.365 | 73/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.375 | 75/200 |
| mushroom | 0.360 | 72/200 |
| orange | 0.455 | 91/200 |
| school_bus | 0.710 | 142/200 |
| sports_car | 0.455 | 91/200 |
| teapot | 0.335 | 67/200 |

## Top Confusions

- orange → banana: 56
- sports_car → school_bus: 37
- teapot → banana: 34
- teapot → king_penguin: 33
- golden_retriever → banana: 32
- brown_bear → golden_retriever: 32
- mushroom → golden_retriever: 28
- mushroom → banana: 27
- king_penguin → teapot: 25
- golden_retriever → mushroom: 24

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
