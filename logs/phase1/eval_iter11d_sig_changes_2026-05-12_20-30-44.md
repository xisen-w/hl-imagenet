# Eval Run: 2026-05-12_20-30-44

**Tag:** iter11d_sig_changes
**Samples:** 2000
**Top-1 Accuracy:** 0.456
**Top-3 Accuracy:** 0.722
**Mean Latency:** 109 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.320 | 64/200 |
| golden_retriever | 0.380 | 76/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.395 | 79/200 |
| mushroom | 0.350 | 70/200 |
| orange | 0.435 | 87/200 |
| school_bus | 0.700 | 140/200 |
| sports_car | 0.430 | 86/200 |
| teapot | 0.335 | 67/200 |

## Top Confusions

- orange → banana: 56
- sports_car → school_bus: 41
- brown_bear → golden_retriever: 39
- golden_retriever → banana: 35
- teapot → banana: 35
- teapot → king_penguin: 35
- mushroom → banana: 30
- mushroom → golden_retriever: 30
- king_penguin → teapot: 28
- mushroom → school_bus: 27

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
