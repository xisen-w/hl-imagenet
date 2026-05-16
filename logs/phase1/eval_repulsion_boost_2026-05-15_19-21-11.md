# Eval Run: 2026-05-15_19-21-11

**Tag:** repulsion_boost
**Samples:** 2000
**Top-1 Accuracy:** 0.542
**Top-3 Accuracy:** 0.769
**Mean Latency:** 167 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.530 | 106/200 |
| brown_bear | 0.505 | 101/200 |
| golden_retriever | 0.430 | 86/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.520 | 104/200 |
| mushroom | 0.510 | 102/200 |
| orange | 0.580 | 116/200 |
| school_bus | 0.720 | 144/200 |
| sports_car | 0.535 | 107/200 |
| teapot | 0.390 | 78/200 |

## Top Confusions

- sports_car → school_bus: 32
- banana → orange: 30
- brown_bear → mushroom: 30
- orange → banana: 28
- golden_retriever → brown_bear: 26
- teapot → banana: 26
- mushroom → banana: 22
- teapot → golden_retriever: 22
- golden_retriever → mushroom: 21
- teapot → king_penguin: 21

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
