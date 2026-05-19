# Eval Run: 2026-05-18_05-49-04

**Tag:** bear_mush_thresh
**Samples:** 2000
**Top-1 Accuracy:** 0.663
**Top-3 Accuracy:** 0.788
**Mean Latency:** 35 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.680 | 136/200 |
| brown_bear | 0.700 | 140/200 |
| golden_retriever | 0.565 | 113/200 |
| jellyfish | 0.755 | 151/200 |
| king_penguin | 0.550 | 110/200 |
| mushroom | 0.600 | 120/200 |
| orange | 0.700 | 140/200 |
| school_bus | 0.815 | 163/200 |
| sports_car | 0.745 | 149/200 |
| teapot | 0.520 | 104/200 |

## Top Confusions

- mushroom → brown_bear: 24
- teapot → banana: 23
- orange → banana: 19
- king_penguin → teapot: 18
- sports_car → school_bus: 18
- brown_bear → mushroom: 17
- golden_retriever → brown_bear: 16
- golden_retriever → teapot: 16
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
