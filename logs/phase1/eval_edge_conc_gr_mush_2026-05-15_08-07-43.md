# Eval Run: 2026-05-15_08-07-43

**Tag:** edge_conc_gr_mush
**Samples:** 2000
**Top-1 Accuracy:** 0.522
**Top-3 Accuracy:** 0.764
**Mean Latency:** 179 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.510 | 102/200 |
| brown_bear | 0.445 | 89/200 |
| golden_retriever | 0.405 | 81/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.515 | 103/200 |
| mushroom | 0.485 | 97/200 |
| orange | 0.575 | 115/200 |
| school_bus | 0.720 | 144/200 |
| sports_car | 0.530 | 106/200 |
| teapot | 0.330 | 66/200 |

## Top Confusions

- banana → orange: 33
- sports_car → school_bus: 33
- teapot → banana: 32
- brown_bear → mushroom: 30
- orange → banana: 28
- teapot → king_penguin: 25
- brown_bear → king_penguin: 25
- mushroom → banana: 24
- golden_retriever → king_penguin: 22
- school_bus → sports_car: 22

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
