# Eval Run: 2026-05-12_19-42-10

**Tag:** phase2_committed_baseline
**Samples:** 2000
**Top-1 Accuracy:** 0.334
**Top-3 Accuracy:** 0.686
**Mean Latency:** 34 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.580 | 116/200 |
| brown_bear | 0.060 | 12/200 |
| golden_retriever | 0.275 | 55/200 |
| jellyfish | 0.655 | 131/200 |
| king_penguin | 0.645 | 129/200 |
| mushroom | 0.220 | 44/200 |
| orange | 0.165 | 33/200 |
| school_bus | 0.575 | 115/200 |
| sports_car | 0.115 | 23/200 |
| teapot | 0.050 | 10/200 |

## Top Confusions

- sports_car → king_penguin: 113
- orange → banana: 83
- golden_retriever → banana: 82
- teapot → king_penguin: 72
- brown_bear → banana: 70
- mushroom → banana: 67
- orange → golden_retriever: 61
- brown_bear → king_penguin: 58
- teapot → golden_retriever: 50
- teapot → banana: 43

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
