# Eval Run: 2026-05-12_15-32-13

**Tag:** phase2_iter18_pairwise_val
**Samples:** 2000
**Top-1 Accuracy:** 0.378
**Top-3 Accuracy:** 0.702
**Mean Latency:** 73 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.470 | 94/200 |
| brown_bear | 0.135 | 27/200 |
| golden_retriever | 0.425 | 85/200 |
| jellyfish | 0.605 | 121/200 |
| king_penguin | 0.635 | 127/200 |
| mushroom | 0.110 | 22/200 |
| orange | 0.315 | 63/200 |
| school_bus | 0.595 | 119/200 |
| sports_car | 0.270 | 54/200 |
| teapot | 0.220 | 44/200 |

## Top Confusions

- sports_car → king_penguin: 72
- orange → banana: 65
- mushroom → golden_retriever: 55
- brown_bear → golden_retriever: 52
- teapot → king_penguin: 50
- brown_bear → king_penguin: 47
- teapot → golden_retriever: 46
- orange → golden_retriever: 45
- mushroom → banana: 43
- golden_retriever → banana: 41

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
