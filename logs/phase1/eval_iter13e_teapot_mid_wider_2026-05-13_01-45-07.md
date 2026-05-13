# Eval Run: 2026-05-13_01-45-07

**Tag:** iter13e_teapot_mid_wider
**Samples:** 2000
**Top-1 Accuracy:** 0.469
**Top-3 Accuracy:** 0.732
**Mean Latency:** 231 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.520 | 104/200 |
| brown_bear | 0.370 | 74/200 |
| golden_retriever | 0.380 | 76/200 |
| jellyfish | 0.645 | 129/200 |
| king_penguin | 0.410 | 82/200 |
| mushroom | 0.390 | 78/200 |
| orange | 0.450 | 90/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.485 | 97/200 |
| teapot | 0.320 | 64/200 |

## Top Confusions

- orange → banana: 57
- sports_car → school_bus: 39
- brown_bear → golden_retriever: 32
- teapot → banana: 31
- golden_retriever → banana: 30
- teapot → king_penguin: 30
- mushroom → brown_bear: 27
- mushroom → golden_retriever: 27
- golden_retriever → mushroom: 26
- mushroom → banana: 26

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
