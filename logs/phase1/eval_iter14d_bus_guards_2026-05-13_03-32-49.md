# Eval Run: 2026-05-13_03-32-49

**Tag:** iter14d_bus_guards
**Samples:** 2000
**Top-1 Accuracy:** 0.476
**Top-3 Accuracy:** 0.732
**Mean Latency:** 105 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.480 | 96/200 |
| golden_retriever | 0.400 | 80/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.470 | 94/200 |
| mushroom | 0.420 | 84/200 |
| orange | 0.475 | 95/200 |
| school_bus | 0.490 | 98/200 |
| sports_car | 0.530 | 106/200 |
| teapot | 0.305 | 61/200 |

## Top Confusions

- orange → banana: 51
- teapot → king_penguin: 38
- teapot → banana: 31
- mushroom → brown_bear: 30
- mushroom → banana: 29
- golden_retriever → brown_bear: 25
- banana → teapot: 25
- golden_retriever → banana: 24
- golden_retriever → mushroom: 24
- brown_bear → golden_retriever: 24

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
