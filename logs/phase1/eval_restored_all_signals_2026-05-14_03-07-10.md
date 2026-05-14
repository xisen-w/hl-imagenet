# Eval Run: 2026-05-14_03-07-10

**Tag:** restored_all_signals
**Samples:** 2000
**Top-1 Accuracy:** 0.483
**Top-3 Accuracy:** 0.758
**Mean Latency:** 222 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.520 | 104/200 |
| brown_bear | 0.415 | 83/200 |
| golden_retriever | 0.295 | 59/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.475 | 95/200 |
| mushroom | 0.460 | 92/200 |
| orange | 0.470 | 94/200 |
| school_bus | 0.815 | 163/200 |
| sports_car | 0.420 | 84/200 |
| teapot | 0.285 | 57/200 |

## Top Confusions

- sports_car → school_bus: 56
- orange → banana: 48
- golden_retriever → brown_bear: 34
- teapot → king_penguin: 31
- teapot → banana: 30
- mushroom → banana: 29
- brown_bear → king_penguin: 29
- banana → orange: 27
- brown_bear → school_bus: 26
- brown_bear → mushroom: 26

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- phase2_jellyfish_signature: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- yellow_dominant: used by 10 classes
- phase2_orange_signature: used by 10 classes
