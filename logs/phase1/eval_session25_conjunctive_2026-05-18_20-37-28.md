# Eval Run: 2026-05-18_20-37-28

**Tag:** session25_conjunctive
**Samples:** 2000
**Top-1 Accuracy:** 0.979
**Top-3 Accuracy:** 0.981
**Mean Latency:** 29 ms

## Per-Class Accuracy

| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| banana | 0.985 | 197/200 |
| brown_bear | 1.000 | 200/200 |
| golden_retriever | 0.985 | 197/200 |
| jellyfish | 0.960 | 192/200 |
| king_penguin | 0.980 | 196/200 |
| mushroom | 0.965 | 193/200 |
| orange | 0.945 | 189/200 |
| school_bus | 1.000 | 200/200 |
| sports_car | 0.985 | 197/200 |
| teapot | 0.985 | 197/200 |

## Top Confusions

- orange → king_penguin: 5
- orange → banana: 4
- golden_retriever → sports_car: 2
- mushroom → brown_bear: 2
- mushroom → teapot: 2
- king_penguin → brown_bear: 2
- jellyfish → teapot: 2
- jellyfish → school_bus: 2
- jellyfish → banana: 2
- golden_retriever → jellyfish: 1

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
