# Eval Run: 2026-05-18_04-35-16

**Tag:** session19_stable
**Samples:** 2000
**Top-1 Accuracy:** 0.677
**Top-3 Accuracy:** 0.795
**Mean Latency:** 77 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.670 | 134/200 |
| brown_bear | 0.710 | 142/200 |
| golden_retriever | 0.560 | 112/200 |
| jellyfish | 0.745 | 149/200 |
| king_penguin | 0.680 | 136/200 |
| mushroom | 0.585 | 117/200 |
| orange | 0.700 | 140/200 |
| school_bus | 0.825 | 165/200 |
| sports_car | 0.740 | 148/200 |
| teapot | 0.555 | 111/200 |

## Top Confusions

- mushroom → brown_bear: 24
- teapot → banana: 23
- orange → banana: 19
- sports_car → school_bus: 18
- golden_retriever → mushroom: 15
- golden_retriever → brown_bear: 15
- king_penguin → teapot: 15
- golden_retriever → teapot: 14
- golden_retriever → king_penguin: 14
- orange → teapot: 14

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
