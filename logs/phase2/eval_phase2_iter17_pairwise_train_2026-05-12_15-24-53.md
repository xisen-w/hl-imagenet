# Eval Run: 2026-05-12_15-24-53

**Tag:** phase2_iter17_pairwise_train
**Samples:** 2000
**Top-1 Accuracy:** 0.350
**Top-3 Accuracy:** 0.715
**Mean Latency:** 62 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.560 | 112/200 |
| brown_bear | 0.100 | 20/200 |
| golden_retriever | 0.450 | 90/200 |
| jellyfish | 0.605 | 121/200 |
| king_penguin | 0.645 | 129/200 |
| mushroom | 0.135 | 27/200 |
| orange | 0.165 | 33/200 |
| school_bus | 0.525 | 105/200 |
| sports_car | 0.190 | 38/200 |
| teapot | 0.125 | 25/200 |

## Top Confusions

- sports_car → king_penguin: 84
- orange → banana: 80
- teapot → king_penguin: 76
- brown_bear → king_penguin: 63
- school_bus → king_penguin: 51
- orange → golden_retriever: 51
- brown_bear → golden_retriever: 50
- mushroom → golden_retriever: 49
- golden_retriever → king_penguin: 46
- mushroom → banana: 46

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- golden_fur_in_nature: used by 10 classes
- quadruped_like: used by 10 classes
- phase2_jellyfish_signature: used by 10 classes
- yellow_dominant: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- phase2_orange_signature: used by 10 classes
