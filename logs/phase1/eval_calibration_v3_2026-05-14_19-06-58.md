# Eval Run: 2026-05-14_19-06-58

**Tag:** calibration_v3
**Samples:** 2000
**Top-1 Accuracy:** 0.514
**Top-3 Accuracy:** 0.759
**Mean Latency:** 253 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.505 | 101/200 |
| brown_bear | 0.440 | 88/200 |
| golden_retriever | 0.395 | 79/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.505 | 101/200 |
| mushroom | 0.470 | 94/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.735 | 147/200 |
| sports_car | 0.515 | 103/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- sports_car → school_bus: 34
- teapot → banana: 33
- banana → orange: 33
- brown_bear → mushroom: 28
- mushroom → banana: 27
- brown_bear → king_penguin: 27
- orange → banana: 26
- teapot → king_penguin: 25
- golden_retriever → mushroom: 23
- golden_retriever → king_penguin: 23

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
