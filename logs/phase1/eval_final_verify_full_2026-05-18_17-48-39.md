# Eval Run: 2026-05-18_17-48-39

**Tag:** final_verify_full
**Samples:** 2000
**Top-1 Accuracy:** 0.768
**Top-3 Accuracy:** 0.839
**Mean Latency:** 69 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.790 | 158/200 |
| brown_bear | 0.810 | 162/200 |
| golden_retriever | 0.710 | 142/200 |
| jellyfish | 0.785 | 157/200 |
| king_penguin | 0.755 | 151/200 |
| mushroom | 0.715 | 143/200 |
| orange | 0.735 | 147/200 |
| school_bus | 0.860 | 172/200 |
| sports_car | 0.800 | 160/200 |
| teapot | 0.720 | 144/200 |

## Top Confusions

- orange → banana: 17
- sports_car → school_bus: 17
- teapot → banana: 16
- mushroom → brown_bear: 14
- golden_retriever → teapot: 13
- jellyfish → teapot: 13
- brown_bear → mushroom: 12
- brown_bear → golden_retriever: 11
- golden_retriever → king_penguin: 10
- teapot → golden_retriever: 10

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
