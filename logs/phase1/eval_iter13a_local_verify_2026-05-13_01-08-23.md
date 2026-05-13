# Eval Run: 2026-05-13_01-08-23

**Tag:** iter13a_local_verify
**Samples:** 2000
**Top-1 Accuracy:** 0.455
**Top-3 Accuracy:** 0.729
**Mean Latency:** 163 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.345 | 69/200 |
| golden_retriever | 0.300 | 60/200 |
| jellyfish | 0.630 | 126/200 |
| king_penguin | 0.370 | 74/200 |
| mushroom | 0.395 | 79/200 |
| orange | 0.495 | 99/200 |
| school_bus | 0.695 | 139/200 |
| sports_car | 0.450 | 90/200 |
| teapot | 0.335 | 67/200 |

## Top Confusions

- orange → banana: 52
- golden_retriever → banana: 46
- teapot → banana: 36
- brown_bear → banana: 35
- king_penguin → teapot: 35
- sports_car → school_bus: 35
- jellyfish → teapot: 30
- mushroom → banana: 28
- teapot → king_penguin: 28
- brown_bear → golden_retriever: 26

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
