# Eval Run: 2026-05-15_18-58-24

**Tag:** local_verify_v2
**Samples:** 2000
**Top-1 Accuracy:** 0.541
**Top-3 Accuracy:** 0.768
**Mean Latency:** 155 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.520 | 104/200 |
| golden_retriever | 0.425 | 85/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.525 | 105/200 |
| mushroom | 0.505 | 101/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.535 | 107/200 |
| teapot | 0.370 | 74/200 |

## Top Confusions

- sports_car → school_bus: 32
- banana → orange: 30
- teapot → banana: 28
- orange → banana: 28
- brown_bear → mushroom: 28
- golden_retriever → brown_bear: 25
- mushroom → banana: 23
- teapot → king_penguin: 23
- golden_retriever → mushroom: 22
- teapot → golden_retriever: 22

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
