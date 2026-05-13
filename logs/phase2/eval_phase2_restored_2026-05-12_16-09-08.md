# Eval Run: 2026-05-12_16-09-08

**Tag:** phase2_restored
**Samples:** 2000
**Top-1 Accuracy:** 0.378
**Top-3 Accuracy:** 0.721
**Mean Latency:** 27 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.500 | 100/200 |
| brown_bear | 0.130 | 26/200 |
| golden_retriever | 0.430 | 86/200 |
| jellyfish | 0.640 | 128/200 |
| king_penguin | 0.690 | 138/200 |
| mushroom | 0.265 | 53/200 |
| orange | 0.225 | 45/200 |
| school_bus | 0.535 | 107/200 |
| sports_car | 0.255 | 51/200 |
| teapot | 0.110 | 22/200 |

## Top Confusions

- sports_car → king_penguin: 77
- orange → banana: 76
- teapot → king_penguin: 74
- brown_bear → king_penguin: 73
- golden_retriever → king_penguin: 47
- brown_bear → golden_retriever: 40
- orange → golden_retriever: 36
- teapot → golden_retriever: 35
- school_bus → king_penguin: 35
- jellyfish → king_penguin: 35

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
