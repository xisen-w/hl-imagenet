# Eval Run: 2026-05-18_01-46-10

**Tag:** session19_rank3_verify
**Samples:** 2000
**Top-1 Accuracy:** 0.624
**Top-3 Accuracy:** 0.769
**Mean Latency:** 100 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.620 | 124/200 |
| brown_bear | 0.595 | 119/200 |
| golden_retriever | 0.555 | 111/200 |
| jellyfish | 0.715 | 143/200 |
| king_penguin | 0.615 | 123/200 |
| mushroom | 0.540 | 108/200 |
| orange | 0.665 | 133/200 |
| school_bus | 0.800 | 160/200 |
| sports_car | 0.660 | 132/200 |
| teapot | 0.475 | 95/200 |

## Top Confusions

- sports_car → school_bus: 27
- teapot → banana: 26
- brown_bear → golden_retriever: 24
- orange → banana: 21
- brown_bear → mushroom: 20
- teapot → golden_retriever: 19
- mushroom → golden_retriever: 18
- banana → orange: 18
- jellyfish → teapot: 18
- golden_retriever → brown_bear: 15

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
