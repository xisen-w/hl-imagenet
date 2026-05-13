# Eval Run: 2026-05-12_16-07-35

**Tag:** phase2_competitive
**Samples:** 2000
**Top-1 Accuracy:** 0.371
**Top-3 Accuracy:** 0.714
**Mean Latency:** 25 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.430 | 86/200 |
| brown_bear | 0.200 | 40/200 |
| golden_retriever | 0.355 | 71/200 |
| jellyfish | 0.680 | 136/200 |
| king_penguin | 0.665 | 133/200 |
| mushroom | 0.360 | 72/200 |
| orange | 0.280 | 56/200 |
| school_bus | 0.285 | 57/200 |
| sports_car | 0.285 | 57/200 |
| teapot | 0.175 | 35/200 |

## Top Confusions

- sports_car → king_penguin: 72
- orange → banana: 71
- teapot → king_penguin: 70
- school_bus → sports_car: 65
- brown_bear → king_penguin: 64
- golden_retriever → king_penguin: 47
- mushroom → banana: 32
- banana → golden_retriever: 32
- teapot → banana: 28
- brown_bear → golden_retriever: 28

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
