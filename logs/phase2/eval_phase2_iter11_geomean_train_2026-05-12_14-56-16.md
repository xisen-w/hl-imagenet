# Eval Run: 2026-05-12_14-56-16

**Tag:** phase2_iter11_geomean_train
**Samples:** 2000
**Top-1 Accuracy:** 0.342
**Top-3 Accuracy:** 0.710
**Mean Latency:** 79 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.090 | 18/200 |
| golden_retriever | 0.410 | 82/200 |
| jellyfish | 0.500 | 100/200 |
| king_penguin | 0.680 | 136/200 |
| mushroom | 0.205 | 41/200 |
| orange | 0.135 | 27/200 |
| school_bus | 0.555 | 111/200 |
| sports_car | 0.230 | 46/200 |
| teapot | 0.080 | 16/200 |

## Top Confusions

- teapot → king_penguin: 86
- orange → banana: 83
- sports_car → king_penguin: 77
- brown_bear → king_penguin: 65
- golden_retriever → king_penguin: 56
- orange → golden_retriever: 54
- mushroom → golden_retriever: 51
- brown_bear → golden_retriever: 51
- mushroom → banana: 50
- jellyfish → teapot: 45

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- yellow_dominant: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- phase2_orange_signature: used by 10 classes
- phase2_brown_bear_signature: used by 10 classes
