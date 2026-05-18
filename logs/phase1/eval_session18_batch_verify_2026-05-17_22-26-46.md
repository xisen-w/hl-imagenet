# Eval Run: 2026-05-17_22-26-46

**Tag:** session18_batch_verify
**Samples:** 2000
**Top-1 Accuracy:** 0.589
**Top-3 Accuracy:** 0.769
**Mean Latency:** 69 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.570 | 114/200 |
| brown_bear | 0.560 | 112/200 |
| golden_retriever | 0.485 | 97/200 |
| jellyfish | 0.710 | 142/200 |
| king_penguin | 0.595 | 119/200 |
| mushroom | 0.515 | 103/200 |
| orange | 0.645 | 129/200 |
| school_bus | 0.765 | 153/200 |
| sports_car | 0.620 | 124/200 |
| teapot | 0.425 | 85/200 |

## Top Confusions

- teapot → banana: 28
- sports_car → school_bus: 27
- banana → orange: 25
- orange → banana: 24
- mushroom → brown_bear: 21
- brown_bear → mushroom: 21
- golden_retriever → brown_bear: 20
- teapot → golden_retriever: 20
- brown_bear → golden_retriever: 20
- teapot → king_penguin: 19

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
