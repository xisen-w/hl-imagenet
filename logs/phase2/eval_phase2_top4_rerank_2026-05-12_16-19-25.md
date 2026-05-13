# Eval Run: 2026-05-12_16-19-25

**Tag:** phase2_top4_rerank
**Samples:** 2000
**Top-1 Accuracy:** 0.355
**Top-3 Accuracy:** 0.729
**Mean Latency:** 22 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.460 | 92/200 |
| brown_bear | 0.315 | 63/200 |
| golden_retriever | 0.360 | 72/200 |
| jellyfish | 0.605 | 121/200 |
| king_penguin | 0.580 | 116/200 |
| mushroom | 0.230 | 46/200 |
| orange | 0.265 | 53/200 |
| school_bus | 0.260 | 52/200 |
| sports_car | 0.305 | 61/200 |
| teapot | 0.175 | 35/200 |

## Top Confusions

- school_bus → sports_car: 75
- sports_car → king_penguin: 71
- orange → banana: 66
- teapot → king_penguin: 63
- brown_bear → king_penguin: 55
- banana → golden_retriever: 41
- mushroom → brown_bear: 38
- mushroom → banana: 37
- orange → golden_retriever: 33
- brown_bear → golden_retriever: 32

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
