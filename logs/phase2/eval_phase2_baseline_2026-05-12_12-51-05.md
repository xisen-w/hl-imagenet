# Eval Run: 2026-05-12_12-51-05

**Tag:** phase2_baseline
**Samples:** 200
**Top-1 Accuracy:** 0.350
**Top-3 Accuracy:** 0.620
**Mean Latency:** 43 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.050 | 1/20 |
| brown_bear | 0.150 | 3/20 |
| golden_retriever | 0.400 | 8/20 |
| jellyfish | 0.550 | 11/20 |
| king_penguin | 0.550 | 11/20 |
| mushroom | 0.000 | 0/20 |
| orange | 0.700 | 14/20 |
| school_bus | 0.650 | 13/20 |
| sports_car | 0.400 | 8/20 |
| teapot | 0.050 | 1/20 |

## Top Confusions

- brown_bear → golden_retriever: 9
- teapot → king_penguin: 7
- banana → school_bus: 6
- banana → orange: 6
- king_penguin → golden_retriever: 6
- golden_retriever → school_bus: 5
- mushroom → golden_retriever: 5
- mushroom → brown_bear: 5
- sports_car → king_penguin: 5
- golden_retriever → orange: 4

## Feature Reuse

- golden_brown_color: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- large_warm_blob: used by 10 classes
- quadruped_like: used by 10 classes
- yellow_dominant: used by 10 classes
- organic_texture: used by 10 classes
- bilateral_symmetry: used by 10 classes
- outdoor_animal_scene: used by 10 classes
- blob_textured_interior: used by 10 classes
- black_white_dominant: used by 10 classes
