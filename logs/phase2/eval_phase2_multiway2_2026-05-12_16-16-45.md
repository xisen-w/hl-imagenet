# Eval Run: 2026-05-12_16-16-45

**Tag:** phase2_multiway2
**Samples:** 2000
**Top-1 Accuracy:** 0.374
**Top-3 Accuracy:** 0.733
**Mean Latency:** 21 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.580 | 116/200 |
| brown_bear | 0.170 | 34/200 |
| golden_retriever | 0.560 | 112/200 |
| jellyfish | 0.595 | 119/200 |
| king_penguin | 0.460 | 92/200 |
| mushroom | 0.225 | 45/200 |
| orange | 0.130 | 26/200 |
| school_bus | 0.360 | 72/200 |
| sports_car | 0.420 | 84/200 |
| teapot | 0.245 | 49/200 |

## Top Confusions

- orange → banana: 86
- brown_bear → golden_retriever: 66
- mushroom → golden_retriever: 53
- school_bus → sports_car: 49
- orange → golden_retriever: 47
- teapot → golden_retriever: 45
- teapot → king_penguin: 41
- jellyfish → teapot: 39
- sports_car → king_penguin: 38
- brown_bear → king_penguin: 36

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
