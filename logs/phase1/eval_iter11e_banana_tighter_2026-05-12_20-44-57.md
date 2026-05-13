# Eval Run: 2026-05-12_20-44-57

**Tag:** iter11e_banana_tighter
**Samples:** 2000
**Top-1 Accuracy:** 0.456
**Top-3 Accuracy:** 0.723
**Mean Latency:** 97 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.330 | 66/200 |
| golden_retriever | 0.365 | 73/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.395 | 79/200 |
| mushroom | 0.355 | 71/200 |
| orange | 0.430 | 86/200 |
| school_bus | 0.700 | 140/200 |
| sports_car | 0.430 | 86/200 |
| teapot | 0.345 | 69/200 |

## Top Confusions

- orange → banana: 58
- sports_car → school_bus: 41
- brown_bear → golden_retriever: 36
- teapot → king_penguin: 35
- golden_retriever → banana: 33
- teapot → banana: 33
- mushroom → golden_retriever: 32
- mushroom → school_bus: 27
- king_penguin → teapot: 27
- orange → golden_retriever: 26

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
