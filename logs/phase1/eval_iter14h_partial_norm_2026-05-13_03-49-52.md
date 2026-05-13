# Eval Run: 2026-05-13_03-49-52

**Tag:** iter14h_partial_norm
**Samples:** 2000
**Top-1 Accuracy:** 0.480
**Top-3 Accuracy:** 0.746
**Mean Latency:** 105 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.395 | 79/200 |
| golden_retriever | 0.360 | 72/200 |
| jellyfish | 0.690 | 138/200 |
| king_penguin | 0.535 | 107/200 |
| mushroom | 0.460 | 92/200 |
| orange | 0.485 | 97/200 |
| school_bus | 0.635 | 127/200 |
| sports_car | 0.470 | 94/200 |
| teapot | 0.260 | 52/200 |

## Top Confusions

- orange → banana: 50
- teapot → king_penguin: 45
- teapot → banana: 34
- sports_car → king_penguin: 31
- golden_retriever → mushroom: 28
- mushroom → banana: 28
- brown_bear → mushroom: 26
- mushroom → brown_bear: 25
- brown_bear → king_penguin: 25
- golden_retriever → banana: 23

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
