# Eval Run: 2026-05-18_17-29-08

**Tag:** final_verify_v1
**Samples:** 2000
**Top-1 Accuracy:** 0.725
**Top-3 Accuracy:** 0.810
**Mean Latency:** 51 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.745 | 149/200 |
| brown_bear | 0.785 | 157/200 |
| golden_retriever | 0.640 | 128/200 |
| jellyfish | 0.775 | 155/200 |
| king_penguin | 0.730 | 146/200 |
| mushroom | 0.635 | 127/200 |
| orange | 0.720 | 144/200 |
| school_bus | 0.840 | 168/200 |
| sports_car | 0.745 | 149/200 |
| teapot | 0.630 | 126/200 |

## Top Confusions

- teapot → banana: 20
- sports_car → school_bus: 20
- mushroom → brown_bear: 19
- orange → banana: 17
- golden_retriever → brown_bear: 15
- mushroom → golden_retriever: 15
- teapot → golden_retriever: 15
- brown_bear → golden_retriever: 13
- jellyfish → teapot: 13
- golden_retriever → king_penguin: 12

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
