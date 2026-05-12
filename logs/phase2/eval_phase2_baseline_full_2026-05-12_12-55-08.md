# Eval Run: 2026-05-12_12-55-08

**Tag:** phase2_baseline_full
**Samples:** 2000
**Top-1 Accuracy:** 0.317
**Top-3 Accuracy:** 0.601
**Mean Latency:** 59 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.065 | 13/200 |
| brown_bear | 0.075 | 15/200 |
| golden_retriever | 0.465 | 93/200 |
| jellyfish | 0.490 | 98/200 |
| king_penguin | 0.570 | 114/200 |
| mushroom | 0.055 | 11/200 |
| orange | 0.560 | 112/200 |
| school_bus | 0.615 | 123/200 |
| sports_car | 0.185 | 37/200 |
| teapot | 0.085 | 17/200 |

## Top Confusions

- brown_bear → golden_retriever: 79
- teapot → king_penguin: 70
- sports_car → king_penguin: 66
- banana → orange: 64
- banana → school_bus: 62
- teapot → golden_retriever: 60
- brown_bear → king_penguin: 46
- mushroom → golden_retriever: 40
- golden_retriever → school_bus: 39
- sports_car → school_bus: 39

## Feature Reuse

- golden_brown_color: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- large_warm_blob: used by 10 classes
- quadruped_like: used by 10 classes
- yellow_dominant: used by 10 classes
- organic_texture: used by 10 classes
- phase2_orange_signature: used by 10 classes
- bilateral_symmetry: used by 10 classes
- phase2_golden_retriever_signature: used by 10 classes
- outdoor_animal_scene: used by 10 classes
