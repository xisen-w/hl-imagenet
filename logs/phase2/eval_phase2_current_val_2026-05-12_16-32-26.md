# Eval Run: 2026-05-12_16-32-26

**Tag:** phase2_current_val
**Samples:** 2000
**Top-1 Accuracy:** 0.405
**Top-3 Accuracy:** 0.724
**Mean Latency:** 22 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.460 | 92/200 |
| brown_bear | 0.300 | 60/200 |
| golden_retriever | 0.430 | 86/200 |
| jellyfish | 0.635 | 127/200 |
| king_penguin | 0.460 | 92/200 |
| mushroom | 0.235 | 47/200 |
| orange | 0.360 | 72/200 |
| school_bus | 0.590 | 118/200 |
| sports_car | 0.370 | 74/200 |
| teapot | 0.210 | 42/200 |

## Top Confusions

- orange → banana: 66
- teapot → king_penguin: 49
- sports_car → king_penguin: 44
- mushroom → banana: 41
- brown_bear → banana: 40
- golden_retriever → banana: 38
- mushroom → golden_retriever: 37
- brown_bear → golden_retriever: 36
- orange → golden_retriever: 35
- banana → golden_retriever: 30

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
