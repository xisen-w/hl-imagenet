# Eval Run: 2026-05-12_16-15-45

**Tag:** phase2_multiway
**Samples:** 2000
**Top-1 Accuracy:** 0.367
**Top-3 Accuracy:** 0.734
**Mean Latency:** 22 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.555 | 111/200 |
| brown_bear | 0.170 | 34/200 |
| golden_retriever | 0.585 | 117/200 |
| jellyfish | 0.580 | 116/200 |
| king_penguin | 0.550 | 110/200 |
| mushroom | 0.230 | 46/200 |
| orange | 0.130 | 26/200 |
| school_bus | 0.295 | 59/200 |
| sports_car | 0.370 | 74/200 |
| teapot | 0.205 | 41/200 |

## Top Confusions

- orange → banana: 85
- brown_bear → golden_retriever: 70
- school_bus → sports_car: 54
- sports_car → king_penguin: 53
- mushroom → golden_retriever: 52
- orange → golden_retriever: 49
- teapot → king_penguin: 48
- brown_bear → king_penguin: 48
- teapot → golden_retriever: 47
- banana → golden_retriever: 40

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
