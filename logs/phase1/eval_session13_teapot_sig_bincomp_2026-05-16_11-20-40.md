# Eval Run: 2026-05-16_11-20-40

**Tag:** session13_teapot_sig_bincomp
**Samples:** 2000
**Top-1 Accuracy:** 0.564
**Top-3 Accuracy:** 0.772
**Mean Latency:** 260 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.550 | 110/200 |
| brown_bear | 0.520 | 104/200 |
| golden_retriever | 0.455 | 91/200 |
| jellyfish | 0.700 | 140/200 |
| king_penguin | 0.580 | 116/200 |
| mushroom | 0.500 | 100/200 |
| orange | 0.615 | 123/200 |
| school_bus | 0.720 | 144/200 |
| sports_car | 0.575 | 115/200 |
| teapot | 0.425 | 85/200 |

## Top Confusions

- teapot → banana: 29
- banana → orange: 25
- sports_car → school_bus: 25
- mushroom → brown_bear: 23
- brown_bear → mushroom: 22
- golden_retriever → brown_bear: 21
- orange → banana: 21
- orange → teapot: 21
- teapot → golden_retriever: 20
- golden_retriever → mushroom: 19

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
