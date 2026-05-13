# Eval Run: 2026-05-12_21-47-52

**Tag:** iter11o_bear_gr_rank3
**Samples:** 2000
**Top-1 Accuracy:** 0.467
**Top-3 Accuracy:** 0.722
**Mean Latency:** 134 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.330 | 66/200 |
| golden_retriever | 0.385 | 77/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.395 | 79/200 |
| mushroom | 0.410 | 82/200 |
| orange | 0.435 | 87/200 |
| school_bus | 0.700 | 140/200 |
| sports_car | 0.465 | 93/200 |
| teapot | 0.335 | 67/200 |

## Top Confusions

- orange → banana: 61
- sports_car → school_bus: 38
- brown_bear → golden_retriever: 37
- teapot → king_penguin: 35
- teapot → banana: 33
- golden_retriever → banana: 30
- golden_retriever → mushroom: 25
- mushroom → brown_bear: 25
- brown_bear → mushroom: 24
- king_penguin → teapot: 24

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
