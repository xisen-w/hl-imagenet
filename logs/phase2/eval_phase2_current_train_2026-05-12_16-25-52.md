# Eval Run: 2026-05-12_16-25-52

**Tag:** phase2_current_train
**Samples:** 2000
**Top-1 Accuracy:** 0.372
**Top-3 Accuracy:** 0.710
**Mean Latency:** 21 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.225 | 45/200 |
| golden_retriever | 0.425 | 85/200 |
| jellyfish | 0.615 | 123/200 |
| king_penguin | 0.450 | 90/200 |
| mushroom | 0.150 | 30/200 |
| orange | 0.305 | 61/200 |
| school_bus | 0.495 | 99/200 |
| sports_car | 0.315 | 63/200 |
| teapot | 0.205 | 41/200 |

## Top Confusions

- orange → banana: 73
- teapot → king_penguin: 53
- mushroom → banana: 51
- brown_bear → golden_retriever: 42
- school_bus → sports_car: 39
- brown_bear → banana: 39
- sports_car → king_penguin: 39
- mushroom → brown_bear: 36
- golden_retriever → banana: 33
- teapot → banana: 32

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
