# Eval Run: 2026-05-12_14-06-45

**Tag:** phase2_iter8_enriched
**Samples:** 500
**Top-1 Accuracy:** 0.348
**Top-3 Accuracy:** 0.736
**Mean Latency:** 119 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.680 | 34/50 |
| brown_bear | 0.080 | 4/50 |
| golden_retriever | 0.380 | 19/50 |
| jellyfish | 0.620 | 31/50 |
| king_penguin | 0.560 | 28/50 |
| mushroom | 0.160 | 8/50 |
| orange | 0.280 | 14/50 |
| school_bus | 0.520 | 26/50 |
| sports_car | 0.200 | 10/50 |
| teapot | 0.000 | 0/50 |

## Top Confusions

- golden_retriever → banana: 22
- mushroom → golden_retriever: 20
- orange → banana: 20
- teapot → king_penguin: 19
- sports_car → king_penguin: 19
- teapot → banana: 16
- brown_bear → golden_retriever: 16
- brown_bear → king_penguin: 14
- teapot → golden_retriever: 12
- king_penguin → golden_retriever: 11

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
