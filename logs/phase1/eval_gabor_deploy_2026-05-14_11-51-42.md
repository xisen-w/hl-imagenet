# Eval Run: 2026-05-14_11-51-42

**Tag:** gabor_deploy
**Samples:** 2000
**Top-1 Accuracy:** 0.512
**Top-3 Accuracy:** 0.754
**Mean Latency:** 133 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.455 | 91/200 |
| golden_retriever | 0.385 | 77/200 |
| jellyfish | 0.660 | 132/200 |
| king_penguin | 0.495 | 99/200 |
| mushroom | 0.440 | 88/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.740 | 148/200 |
| sports_car | 0.530 | 106/200 |
| teapot | 0.320 | 64/200 |

## Top Confusions

- mushroom → banana: 36
- banana → orange: 36
- sports_car → school_bus: 32
- teapot → banana: 30
- orange → banana: 28
- golden_retriever → banana: 26
- school_bus → sports_car: 25
- brown_bear → mushroom: 24
- teapot → king_penguin: 23
- brown_bear → king_penguin: 23

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
