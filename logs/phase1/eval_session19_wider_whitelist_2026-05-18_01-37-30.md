# Eval Run: 2026-05-18_01-37-30

**Tag:** session19_wider_whitelist
**Samples:** 2000
**Top-1 Accuracy:** 0.607
**Top-3 Accuracy:** 0.767
**Mean Latency:** 70 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.560 | 112/200 |
| brown_bear | 0.570 | 114/200 |
| golden_retriever | 0.530 | 106/200 |
| jellyfish | 0.715 | 143/200 |
| king_penguin | 0.595 | 119/200 |
| mushroom | 0.530 | 106/200 |
| orange | 0.665 | 133/200 |
| school_bus | 0.790 | 158/200 |
| sports_car | 0.645 | 129/200 |
| teapot | 0.470 | 94/200 |

## Top Confusions

- sports_car → school_bus: 27
- brown_bear → mushroom: 25
- teapot → banana: 22
- brown_bear → golden_retriever: 21
- teapot → golden_retriever: 20
- banana → teapot: 19
- orange → banana: 19
- jellyfish → teapot: 19
- banana → orange: 18
- golden_retriever → teapot: 16

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
