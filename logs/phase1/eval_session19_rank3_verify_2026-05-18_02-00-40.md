# Eval Run: 2026-05-18_02-00-40

**Tag:** session19_rank3_verify
**Samples:** 2000
**Top-1 Accuracy:** 0.607
**Top-3 Accuracy:** 0.781
**Mean Latency:** 78 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.470 | 94/200 |
| brown_bear | 0.680 | 136/200 |
| golden_retriever | 0.470 | 94/200 |
| jellyfish | 0.715 | 143/200 |
| king_penguin | 0.490 | 98/200 |
| mushroom | 0.560 | 112/200 |
| orange | 0.665 | 133/200 |
| school_bus | 0.800 | 160/200 |
| sports_car | 0.670 | 134/200 |
| teapot | 0.545 | 109/200 |

## Top Confusions

- banana → teapot: 34
- king_penguin → sports_car: 32
- golden_retriever → brown_bear: 30
- mushroom → brown_bear: 27
- sports_car → school_bus: 25
- jellyfish → teapot: 20
- golden_retriever → mushroom: 18
- golden_retriever → teapot: 18
- banana → orange: 18
- king_penguin → teapot: 18

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
