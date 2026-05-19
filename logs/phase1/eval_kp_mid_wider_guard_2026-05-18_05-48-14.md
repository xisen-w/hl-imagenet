# Eval Run: 2026-05-18_05-48-14

**Tag:** kp_mid_wider_guard
**Samples:** 2000
**Top-1 Accuracy:** 0.650
**Top-3 Accuracy:** 0.782
**Mean Latency:** 39 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.675 | 135/200 |
| brown_bear | 0.645 | 129/200 |
| golden_retriever | 0.550 | 110/200 |
| jellyfish | 0.755 | 151/200 |
| king_penguin | 0.545 | 109/200 |
| mushroom | 0.585 | 117/200 |
| orange | 0.705 | 141/200 |
| school_bus | 0.815 | 163/200 |
| sports_car | 0.725 | 145/200 |
| teapot | 0.505 | 101/200 |

## Top Confusions

- mushroom → brown_bear: 24
- teapot → banana: 23
- king_penguin → teapot: 20
- orange → banana: 19
- sports_car → school_bus: 18
- brown_bear → mushroom: 17
- king_penguin → brown_bear: 17
- golden_retriever → teapot: 15
- teapot → brown_bear: 15
- orange → teapot: 15

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
