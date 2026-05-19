# Eval Run: 2026-05-18_04-52-24

**Tag:** session19_val_no_gr_teapot
**Samples:** 2000
**Top-1 Accuracy:** 0.509
**Top-3 Accuracy:** 0.748
**Mean Latency:** 58 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.520 | 104/200 |
| brown_bear | 0.455 | 91/200 |
| golden_retriever | 0.365 | 73/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.480 | 96/200 |
| mushroom | 0.400 | 80/200 |
| orange | 0.595 | 119/200 |
| school_bus | 0.640 | 128/200 |
| sports_car | 0.575 | 115/200 |
| teapot | 0.360 | 72/200 |

## Top Confusions

- orange → banana: 33
- brown_bear → mushroom: 33
- teapot → banana: 30
- mushroom → brown_bear: 29
- golden_retriever → mushroom: 28
- golden_retriever → brown_bear: 28
- sports_car → school_bus: 28
- golden_retriever → teapot: 26
- banana → orange: 24
- king_penguin → brown_bear: 24

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
