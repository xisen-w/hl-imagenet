# Eval Run: 2026-05-18_02-14-55

**Tag:** session19_sportsbus_widemargin
**Samples:** 2000
**Top-1 Accuracy:** 0.636
**Top-3 Accuracy:** 0.781
**Mean Latency:** 60 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.635 | 127/200 |
| brown_bear | 0.660 | 132/200 |
| golden_retriever | 0.530 | 106/200 |
| jellyfish | 0.715 | 143/200 |
| king_penguin | 0.630 | 126/200 |
| mushroom | 0.560 | 112/200 |
| orange | 0.670 | 134/200 |
| school_bus | 0.800 | 160/200 |
| sports_car | 0.660 | 132/200 |
| teapot | 0.500 | 100/200 |

## Top Confusions

- teapot → banana: 25
- sports_car → school_bus: 25
- mushroom → brown_bear: 24
- orange → banana: 21
- banana → orange: 18
- golden_retriever → mushroom: 17
- golden_retriever → teapot: 17
- brown_bear → mushroom: 17
- jellyfish → teapot: 17
- golden_retriever → brown_bear: 16

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
