# Eval Run: 2026-05-13_04-17-34

**Tag:** iter14l_new_discs
**Samples:** 2000
**Top-1 Accuracy:** 0.472
**Top-3 Accuracy:** 0.729
**Mean Latency:** 113 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.480 | 96/200 |
| brown_bear | 0.395 | 79/200 |
| golden_retriever | 0.330 | 66/200 |
| jellyfish | 0.665 | 133/200 |
| king_penguin | 0.470 | 94/200 |
| mushroom | 0.415 | 83/200 |
| orange | 0.475 | 95/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.500 | 100/200 |
| teapot | 0.275 | 55/200 |

## Top Confusions

- orange → banana: 47
- teapot → king_penguin: 37
- sports_car → school_bus: 35
- teapot → banana: 31
- golden_retriever → mushroom: 30
- mushroom → brown_bear: 29
- mushroom → golden_retriever: 28
- golden_retriever → teapot: 26
- orange → teapot: 26
- brown_bear → golden_retriever: 26

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
