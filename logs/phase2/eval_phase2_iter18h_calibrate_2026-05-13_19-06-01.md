# Eval Run: 2026-05-13_19-06-01

**Tag:** phase2_iter18h_calibrate
**Samples:** 2000
**Top-1 Accuracy:** 0.506
**Top-3 Accuracy:** 0.759
**Mean Latency:** 84 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.450 | 90/200 |
| brown_bear | 0.440 | 88/200 |
| golden_retriever | 0.485 | 97/200 |
| jellyfish | 0.695 | 139/200 |
| king_penguin | 0.525 | 105/200 |
| mushroom | 0.465 | 93/200 |
| orange | 0.560 | 112/200 |
| school_bus | 0.690 | 138/200 |
| sports_car | 0.535 | 107/200 |
| teapot | 0.220 | 44/200 |

## Top Confusions

- teapot → king_penguin: 51
- banana → orange: 38
- brown_bear → golden_retriever: 32
- sports_car → school_bus: 32
- brown_bear → king_penguin: 29
- teapot → banana: 26
- school_bus → sports_car: 26
- orange → banana: 25
- teapot → golden_retriever: 24
- orange → teapot: 23

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
