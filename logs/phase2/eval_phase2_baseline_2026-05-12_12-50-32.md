# Eval Run: 2026-05-12_12-50-32

**Tag:** phase2_baseline
**Samples:** 100
**Top-1 Accuracy:** 0.230
**Top-3 Accuracy:** 0.630
**Mean Latency:** 70 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.050 | 1/20 |
| golden_retriever | 0.400 | 8/20 |
| mushroom | 0.000 | 0/20 |
| school_bus | 0.650 | 13/20 |
| teapot | 0.050 | 1/20 |

## Top Confusions

- teapot → king_penguin: 7
- banana → school_bus: 6
- banana → orange: 6
- golden_retriever → school_bus: 5
- mushroom → golden_retriever: 5
- mushroom → brown_bear: 5
- golden_retriever → orange: 4
- mushroom → orange: 4
- teapot → golden_retriever: 4
- banana → golden_retriever: 4

## Feature Reuse

- phase2_golden_retriever_signature: used by 5 classes
- golden_brown_color: used by 5 classes
- golden_fur_in_nature: used by 5 classes
- large_warm_blob: used by 5 classes
- quadruped_like: used by 5 classes
- horizontal_window_pattern: used by 5 classes
- yellow_dominant: used by 5 classes
- organic_texture: used by 5 classes
- phase2_school_bus_signature: used by 5 classes
- yellow_body_with_sky: used by 5 classes
