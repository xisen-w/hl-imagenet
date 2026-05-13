# Eval Run: 2026-05-12_21-11-29

**Tag:** iter11i_more_discs
**Samples:** 2000
**Top-1 Accuracy:** 0.464
**Top-3 Accuracy:** 0.722
**Mean Latency:** 99 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.480 | 96/200 |
| brown_bear | 0.355 | 71/200 |
| golden_retriever | 0.360 | 72/200 |
| jellyfish | 0.695 | 139/200 |
| king_penguin | 0.460 | 92/200 |
| mushroom | 0.435 | 87/200 |
| orange | 0.435 | 87/200 |
| school_bus | 0.695 | 139/200 |
| sports_car | 0.450 | 90/200 |
| teapot | 0.270 | 54/200 |

## Top Confusions

- orange → banana: 60
- teapot → king_penguin: 48
- sports_car → school_bus: 37
- golden_retriever → mushroom: 31
- brown_bear → golden_retriever: 30
- teapot → banana: 28
- sports_car → king_penguin: 28
- brown_bear → mushroom: 26
- golden_retriever → banana: 24
- banana → teapot: 24

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
