# Pipeline Mechanics

The prediction pipeline has 7 stages. Every change you make interacts with every downstream stage. Understanding this ordering is prerequisite to understanding why changes cascade.

## The 7 Stages (in execution order)

### 1. Base Scoring
Each of 10 classes gets a sigmoid-weighted score from ~80 features:
```
score = Σ(weight_i * sigmoid(feature_i, center, scale)) * guard_product
```
Guards are multiplicative (0.5 + 0.5 * min(guards)), so a guard firing to 0 halves the score.

**Key property**: This is additive over shared features. Classes that partially match on many features score high everywhere → sink classes.

### 2. Histogram Blending
```
blended = score * 0.88 + (hist_similarity - class_mean * 0.3) * 0.12
```
Histogram prototype scores are 2D hue-sat distribution similarities. Mean-centering at 30% reduces sink amplification.

**Key property**: Global — affects all 10 class scores simultaneously. This is why it can break zero-sum: it shifts the entire ranking, not just one pair.

### 3. Score Calibration
Per-class additive offsets: `{"school_bus": -0.02, "jellyfish": +0.02, "king_penguin": +0.01, "mushroom": +0.01}`

**Key property**: Extremely sensitive. Removing KP's +0.01 caused -19 regression. These offsets compensate for pipeline biases, not just scoring biases.

### 4. Potential Field Repulsion
For whitelisted pairs with discriminant evidence:
```
winner += force/2, loser -= force/2  (force = 0.008-0.012)
```
Only fires when disc_gap > 1.0 (high confidence).

**Key property**: Safest intervention type. Small forces, conservative triggers. Net effect is usually +1 per pair added.

### 5. Ranking (sort by blended score)

### 6. Pairwise Reranking
Checks rank 1 vs rank 2 (and rank 3, 4, 5 with progressively stricter thresholds):
```
swap iff disc_margin > base_threshold + score_gap * gap_scale
```

**Parameters per rank depth:**
| Rank | Margin window | Gap scale | Multiplier |
|------|:---:|:---:|:---:|
| 2 | ≤ 0.30 | 1.5 | 1.3 |
| 3 | ≤ 0.28 | 2.0 | 1.9 |
| 4 | ≤ 0.30 | 3.0 | 2.8 |
| 5 | ≤ 0.15 | 4.0 | 4.0 |

Each depth has a whitelist of allowed pairs. Only high-accuracy discriminants get whitelisted at deeper ranks.

**Key property**: The single most impactful component (+7.2pp over base scoring). Also the most fragile — 112 reranking-caused errors at one point. Gap-aware gating is what makes it safe.

### 7. Local Verify
Pair-specific conjunctive conditions that override the ranking:
```
if pair == {"teapot", "banana"} and margin < 0.15:
    if cm_center_b < 0.57 AND orient_entropy > 2.85: swap to teapot
```

**Key property**: Highest precision, lowest risk. Each condition fires on 2-10 images. Conditions are AND-gated → very specific. This is the most productive optimization axis at the current accuracy level.

## Cascade Dynamics

A change at stage N affects all stages N+1 through 7:
- **Signature change** (stage 1): affects blending, calibration, repulsion, ranking, reranking, AND verify. This is why adding one term to teapot signature caused -28 regression.
- **Calibration change** (stage 3): affects repulsion, ranking, reranking, verify.
- **Reranking parameter change** (stage 6): affects only verify. Relatively safe.
- **Verify condition** (stage 7): affects nothing downstream. Safest.

**The cascade multiplier**: A change expected to affect ±N images in isolation typically causes ±2N to ±3N net change due to cascade interactions. Always assume your estimate is optimistic by 2-3x.

## Current State (Session 13 end)

- 58.15% train (1163/2000)
- 24 discriminant pairs, 14 histogram differentials
- 6 confidence gates, ~15 local verify conditions
- 11 repulsion pairs
- Per-class: banana 112, bear 109, GR 98, jelly 141, KP 118, mush 102, orange 126, bus 152, sports 121, teapot 83
