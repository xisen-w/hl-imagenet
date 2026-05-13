# Eval Run: 2026-05-12_16-28-01

**Tag:** phase2_fixed_mush_bear
**Samples:** 2000
**Top-1 Accuracy:** 0.386
**Top-3 Accuracy:** 0.717
**Mean Latency:** 21 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.535 | 107/200 |
| brown_bear | 0.115 | 23/200 |
| golden_retriever | 0.455 | 91/200 |
| jellyfish | 0.640 | 128/200 |
| king_penguin | 0.495 | 99/200 |
| mushroom | 0.235 | 47/200 |
| orange | 0.305 | 61/200 |
| school_bus | 0.525 | 105/200 |
| sports_car | 0.350 | 70/200 |
| teapot | 0.200 | 40/200 |

## Top Confusions

- orange → banana: 70
- teapot → king_penguin: 58
- mushroom → banana: 48
- sports_car → king_penguin: 46
- brown_bear → golden_retriever: 45
- school_bus → sports_car: 42
- brown_bear → banana: 34
- golden_retriever → banana: 32
- teapot → banana: 31
- brown_bear → king_penguin: 31

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
