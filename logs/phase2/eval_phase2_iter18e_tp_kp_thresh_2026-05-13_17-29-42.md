# Eval Run: 2026-05-13_17-29-42

**Tag:** phase2_iter18e_tp_kp_thresh
**Samples:** 2000
**Top-1 Accuracy:** 0.506
**Top-3 Accuracy:** 0.752
**Mean Latency:** 196 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.470 | 94/200 |
| brown_bear | 0.450 | 90/200 |
| golden_retriever | 0.425 | 85/200 |
| jellyfish | 0.680 | 136/200 |
| king_penguin | 0.520 | 104/200 |
| mushroom | 0.455 | 91/200 |
| orange | 0.560 | 112/200 |
| school_bus | 0.755 | 151/200 |
| sports_car | 0.545 | 109/200 |
| teapot | 0.205 | 41/200 |

## Top Confusions

- teapot → king_penguin: 48
- banana → orange: 38
- sports_car → school_bus: 33
- teapot → banana: 30
- orange → banana: 29
- brown_bear → king_penguin: 25
- mushroom → banana: 24
- brown_bear → mushroom: 24
- school_bus → sports_car: 22
- golden_retriever → mushroom: 21

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
