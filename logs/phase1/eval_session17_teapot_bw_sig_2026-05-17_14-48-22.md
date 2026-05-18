# Eval Run: 2026-05-17_14-48-22

**Tag:** session17_teapot_bw_sig
**Samples:** 2000
**Top-1 Accuracy:** 0.580
**Top-3 Accuracy:** 0.767
**Mean Latency:** 84 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.560 | 112/200 |
| brown_bear | 0.555 | 111/200 |
| golden_retriever | 0.485 | 97/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.585 | 117/200 |
| mushroom | 0.515 | 103/200 |
| orange | 0.630 | 126/200 |
| school_bus | 0.760 | 152/200 |
| sports_car | 0.590 | 118/200 |
| teapot | 0.410 | 82/200 |

## Top Confusions

- teapot → banana: 29
- sports_car → school_bus: 27
- banana → orange: 25
- brown_bear → golden_retriever: 22
- mushroom → brown_bear: 21
- teapot → golden_retriever: 21
- orange → banana: 21
- brown_bear → mushroom: 20
- golden_retriever → brown_bear: 19
- teapot → king_penguin: 19

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
