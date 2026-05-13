# Eval Run: 2026-05-12_19-06-04

**Tag:** phase2_iter9e_val
**Samples:** 2000
**Top-1 Accuracy:** 0.444
**Top-3 Accuracy:** 0.730
**Mean Latency:** 112 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.550 | 110/200 |
| brown_bear | 0.275 | 55/200 |
| golden_retriever | 0.425 | 85/200 |
| jellyfish | 0.625 | 125/200 |
| king_penguin | 0.385 | 77/200 |
| mushroom | 0.340 | 68/200 |
| orange | 0.430 | 86/200 |
| school_bus | 0.560 | 112/200 |
| sports_car | 0.500 | 100/200 |
| teapot | 0.345 | 69/200 |

## Top Confusions

- orange → banana: 58
- brown_bear → golden_retriever: 51
- mushroom → golden_retriever: 46
- golden_retriever → banana: 35
- teapot → banana: 34
- king_penguin → teapot: 33
- teapot → king_penguin: 32
- mushroom → banana: 29
- school_bus → sports_car: 29
- jellyfish → teapot: 27

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
