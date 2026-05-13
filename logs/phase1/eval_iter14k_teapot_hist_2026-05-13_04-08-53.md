# Eval Run: 2026-05-13_04-08-53

**Tag:** iter14k_teapot_hist
**Samples:** 2000
**Top-1 Accuracy:** 0.482
**Top-3 Accuracy:** 0.725
**Mean Latency:** 111 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.400 | 80/200 |
| golden_retriever | 0.395 | 79/200 |
| jellyfish | 0.670 | 134/200 |
| king_penguin | 0.460 | 92/200 |
| mushroom | 0.395 | 79/200 |
| orange | 0.475 | 95/200 |
| school_bus | 0.720 | 144/200 |
| sports_car | 0.495 | 99/200 |
| teapot | 0.280 | 56/200 |

## Top Confusions

- orange → banana: 51
- teapot → king_penguin: 37
- sports_car → school_bus: 34
- teapot → banana: 31
- brown_bear → golden_retriever: 30
- mushroom → brown_bear: 29
- mushroom → banana: 27
- golden_retriever → mushroom: 25
- golden_retriever → banana: 23
- mushroom → golden_retriever: 23

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
