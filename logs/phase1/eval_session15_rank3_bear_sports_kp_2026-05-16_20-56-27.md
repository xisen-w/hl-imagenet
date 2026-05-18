# Eval Run: 2026-05-16_20-56-27

**Tag:** session15_rank3_bear_sports_kp
**Samples:** 2000
**Top-1 Accuracy:** 0.580
**Top-3 Accuracy:** 0.772
**Mean Latency:** 234 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.555 | 111/200 |
| brown_bear | 0.560 | 112/200 |
| golden_retriever | 0.490 | 98/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.540 | 108/200 |
| mushroom | 0.515 | 103/200 |
| orange | 0.630 | 126/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.630 | 126/200 |
| teapot | 0.415 | 83/200 |

## Top Confusions

- teapot → banana: 28
- sports_car → school_bus: 26
- banana → orange: 25
- mushroom → brown_bear: 23
- orange → banana: 22
- brown_bear → golden_retriever: 22
- teapot → golden_retriever: 21
- brown_bear → mushroom: 20
- golden_retriever → brown_bear: 18
- school_bus → sports_car: 18

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
