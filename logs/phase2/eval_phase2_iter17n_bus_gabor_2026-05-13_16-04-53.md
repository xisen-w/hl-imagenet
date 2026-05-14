# Eval Run: 2026-05-13_16-04-53

**Tag:** phase2_iter17n_bus_gabor
**Samples:** 2000
**Top-1 Accuracy:** 0.483
**Top-3 Accuracy:** 0.749
**Mean Latency:** 98 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.590 | 118/200 |
| brown_bear | 0.465 | 93/200 |
| golden_retriever | 0.400 | 80/200 |
| jellyfish | 0.680 | 136/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.495 | 99/200 |
| orange | 0.450 | 90/200 |
| school_bus | 0.450 | 90/200 |
| sports_car | 0.575 | 115/200 |
| teapot | 0.215 | 43/200 |

## Top Confusions

- orange → banana: 53
- teapot → king_penguin: 49
- teapot → banana: 36
- mushroom → banana: 35
- school_bus → sports_car: 31
- brown_bear → mushroom: 30
- brown_bear → king_penguin: 27
- golden_retriever → banana: 24
- golden_retriever → mushroom: 24
- golden_retriever → brown_bear: 23

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
