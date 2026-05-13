# Eval Run: 2026-05-12_16-06-14

**Tag:** phase2_calibrated
**Samples:** 2000
**Top-1 Accuracy:** 0.364
**Top-3 Accuracy:** 0.718
**Mean Latency:** 26 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.475 | 95/200 |
| brown_bear | 0.170 | 34/200 |
| golden_retriever | 0.275 | 55/200 |
| jellyfish | 0.760 | 152/200 |
| king_penguin | 0.665 | 133/200 |
| mushroom | 0.385 | 77/200 |
| orange | 0.300 | 60/200 |
| school_bus | 0.195 | 39/200 |
| sports_car | 0.285 | 57/200 |
| teapot | 0.130 | 26/200 |

## Top Confusions

- teapot → king_penguin: 73
- sports_car → king_penguin: 73
- orange → banana: 72
- brown_bear → king_penguin: 69
- school_bus → sports_car: 65
- golden_retriever → king_penguin: 57
- brown_bear → mushroom: 36
- mushroom → banana: 35
- school_bus → banana: 29
- school_bus → king_penguin: 27

## Feature Reuse

- phase2_golden_retriever_signature: used by 10 classes
- phase2_mushroom_signature: used by 10 classes
- phase2_teapot_signature: used by 10 classes
- phase2_school_bus_signature: used by 10 classes
- phase2_banana_signature: used by 10 classes
- phase2_orange_signature: used by 10 classes
- phase2_brown_bear_signature: used by 10 classes
- phase2_jellyfish_signature: used by 10 classes
- phase2_king_penguin_signature: used by 10 classes
- phase2_sports_car_signature: used by 10 classes
