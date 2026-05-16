# Eval Run: 2026-05-15_04-57-39

**Tag:** reduce_rerank_errors
**Samples:** 2000
**Top-1 Accuracy:** 0.516
**Top-3 Accuracy:** 0.761
**Mean Latency:** 148 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.515 | 103/200 |
| brown_bear | 0.440 | 88/200 |
| golden_retriever | 0.395 | 79/200 |
| jellyfish | 0.675 | 135/200 |
| king_penguin | 0.510 | 102/200 |
| mushroom | 0.485 | 97/200 |
| orange | 0.565 | 113/200 |
| school_bus | 0.725 | 145/200 |
| sports_car | 0.530 | 106/200 |
| teapot | 0.325 | 65/200 |

## Top Confusions

- sports_car → school_bus: 33
- teapot → banana: 32
- banana → orange: 32
- brown_bear → mushroom: 30
- orange → banana: 29
- mushroom → banana: 27
- brown_bear → king_penguin: 27
- teapot → king_penguin: 26
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
