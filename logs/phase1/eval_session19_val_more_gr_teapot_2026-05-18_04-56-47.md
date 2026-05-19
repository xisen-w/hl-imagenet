# Eval Run: 2026-05-18_04-56-47

**Tag:** session19_val_more_gr_teapot
**Samples:** 2000
**Top-1 Accuracy:** 0.514
**Top-3 Accuracy:** 0.748
**Mean Latency:** 52 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.460 | 92/200 |
| golden_retriever | 0.370 | 74/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.495 | 99/200 |
| mushroom | 0.420 | 84/200 |
| orange | 0.590 | 118/200 |
| school_bus | 0.670 | 134/200 |
| sports_car | 0.570 | 114/200 |
| teapot | 0.350 | 70/200 |

## Top Confusions

- orange → banana: 36
- brown_bear → mushroom: 32
- golden_retriever → mushroom: 31
- teapot → banana: 30
- mushroom → brown_bear: 29
- sports_car → school_bus: 27
- golden_retriever → brown_bear: 26
- banana → orange: 24
- brown_bear → golden_retriever: 24
- golden_retriever → teapot: 23

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
