# Eval Run: 2026-05-12_13-33-07

**Tag:** phase2_val_baseline
**Samples:** 500
**Top-1 Accuracy:** 0.342
**Top-3 Accuracy:** 0.686
**Mean Latency:** 56 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.000 | 0/50 |
| brown_bear | 0.080 | 4/50 |
| golden_retriever | 0.540 | 27/50 |
| jellyfish | 0.700 | 35/50 |
| king_penguin | 0.620 | 31/50 |
| mushroom | 0.180 | 9/50 |
| orange | 0.340 | 17/50 |
| school_bus | 0.600 | 30/50 |
| sports_car | 0.280 | 14/50 |
| teapot | 0.080 | 4/50 |

## Top Confusions

- banana → golden_retriever: 31
- orange → golden_retriever: 21
- brown_bear → golden_retriever: 21
- sports_car → king_penguin: 21
- teapot → golden_retriever: 19
- teapot → king_penguin: 16
- mushroom → golden_retriever: 13
- brown_bear → king_penguin: 13
- golden_retriever → king_penguin: 12
- king_penguin → golden_retriever: 11

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
