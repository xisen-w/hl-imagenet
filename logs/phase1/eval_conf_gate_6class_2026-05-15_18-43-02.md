# Eval Run: 2026-05-15_18-43-02

**Tag:** conf_gate_6class
**Samples:** 2000
**Top-1 Accuracy:** 0.532
**Top-3 Accuracy:** 0.768
**Mean Latency:** 125 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.540 | 108/200 |
| brown_bear | 0.515 | 103/200 |
| golden_retriever | 0.415 | 83/200 |
| jellyfish | 0.705 | 141/200 |
| king_penguin | 0.450 | 90/200 |
| mushroom | 0.505 | 101/200 |
| orange | 0.585 | 117/200 |
| school_bus | 0.715 | 143/200 |
| sports_car | 0.535 | 107/200 |
| teapot | 0.360 | 72/200 |

## Top Confusions

- sports_car → school_bus: 32
- banana → orange: 30
- teapot → banana: 28
- orange → banana: 28
- brown_bear → mushroom: 28
- mushroom → banana: 23
- golden_retriever → mushroom: 22
- golden_retriever → brown_bear: 22
- teapot → king_penguin: 22
- king_penguin → teapot: 22

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
