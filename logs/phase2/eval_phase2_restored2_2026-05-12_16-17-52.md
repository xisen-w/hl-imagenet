# Eval Run: 2026-05-12_16-17-52

**Tag:** phase2_restored2
**Samples:** 2000
**Top-1 Accuracy:** 0.377
**Top-3 Accuracy:** 0.730
**Mean Latency:** 22 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.500 | 100/200 |
| brown_bear | 0.275 | 55/200 |
| golden_retriever | 0.475 | 95/200 |
| jellyfish | 0.605 | 121/200 |
| king_penguin | 0.525 | 105/200 |
| mushroom | 0.300 | 60/200 |
| orange | 0.205 | 41/200 |
| school_bus | 0.350 | 70/200 |
| sports_car | 0.325 | 65/200 |
| teapot | 0.210 | 42/200 |

## Top Confusions

- orange → banana: 75
- sports_car → king_penguin: 63
- school_bus → sports_car: 58
- teapot → king_penguin: 51
- brown_bear → golden_retriever: 44
- brown_bear → king_penguin: 43
- banana → golden_retriever: 42
- orange → golden_retriever: 41
- mushroom → banana: 36
- jellyfish → teapot: 33

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
