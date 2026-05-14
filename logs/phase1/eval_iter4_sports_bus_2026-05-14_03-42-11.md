# Eval Run: 2026-05-14_03-42-11

**Tag:** iter4_sports_bus
**Samples:** 2000
**Top-1 Accuracy:** 0.500
**Top-3 Accuracy:** 0.756
**Mean Latency:** 110 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.420 | 84/200 |
| golden_retriever | 0.380 | 76/200 |
| jellyfish | 0.670 | 134/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.445 | 89/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.750 | 150/200 |
| sports_car | 0.520 | 104/200 |
| teapot | 0.220 | 44/200 |

## Top Confusions

- teapot → king_penguin: 45
- sports_car → school_bus: 36
- mushroom → banana: 34
- banana → orange: 33
- teapot → banana: 31
- brown_bear → king_penguin: 29
- brown_bear → mushroom: 27
- orange → banana: 26
- golden_retriever → mushroom: 22
- golden_retriever → banana: 22

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
