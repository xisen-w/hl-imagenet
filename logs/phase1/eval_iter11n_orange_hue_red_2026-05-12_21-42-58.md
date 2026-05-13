# Eval Run: 2026-05-12_21-42-58

**Tag:** iter11n_orange_hue_red
**Samples:** 2000
**Top-1 Accuracy:** 0.466
**Top-3 Accuracy:** 0.720
**Mean Latency:** 155 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.350 | 70/200 |
| golden_retriever | 0.360 | 72/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.395 | 79/200 |
| mushroom | 0.410 | 82/200 |
| orange | 0.435 | 87/200 |
| school_bus | 0.705 | 141/200 |
| sports_car | 0.465 | 93/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- orange → banana: 62
- sports_car → school_bus: 38
- teapot → king_penguin: 35
- teapot → banana: 33
- brown_bear → golden_retriever: 32
- golden_retriever → banana: 30
- golden_retriever → mushroom: 25
- brown_bear → school_bus: 25
- mushroom → banana: 24
- mushroom → brown_bear: 24

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
