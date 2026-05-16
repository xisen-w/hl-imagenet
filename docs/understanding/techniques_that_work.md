# Techniques That Work

Ranked by total impact. Each entry includes conditions for success.

## Tier 1: Architectural (each +3pp or more)

### Pairwise Reranking (+7.2pp)
**What**: Specialized discriminant functions compare rank-1 vs rank-2 (and deeper) to correct ranking errors.
**Why it works**: ~40% of errors have the true class at rank 2-3. A 75-85% accurate discriminant turns many of these into correct predictions.
**Conditions**: Need discriminant accuracy ≥75%. Need gap-aware gating to prevent confident-but-wrong swaps. Need per-pair base thresholds calibrated to accuracy.
**Ceiling**: ~55% of errors have true class beyond rank 3. Diminishing returns after 24 pairs.

### Histogram Prototype Blending (+1-2pp)
**What**: Linear blend of signature scores with histogram (2D hue-sat distribution) similarity before ranking.
**Why it works**: Global shift — moves all class scores simultaneously, avoiding zero-sum dynamics. Histogram captures holistic color distribution that scalar features miss.
**Conditions**: Must use differential histograms (hist_A_minus_B), not raw similarity. Must mean-center at ~30% to prevent sink amplification. Blend weight 0.12 is a calibrated equilibrium.

### Gap-Aware Confidence Gating (+0.8pp)
**What**: Require discriminant confidence to exceed a threshold that scales with the existing score gap.
**Why it works**: If class A leads by 0.20, even a 70% accurate discriminant shouldn't swap. If the gap is 0.02, modest evidence suffices. This prevents the 112 reranking-caused errors that existed before.
**Conditions**: base_threshold and gap_scale need per-rank calibration. Currently: rank-2 (0.05, 1.5), rank-3 (0.0, 2.0).

## Tier 2: Conditional Logic (each +0.5-2pp)

### Local Verify Conditions (+1.5pp cumulative across ~15 conditions)
**What**: Pair-specific conjunctive (AND) conditions that override ranking when margin is small.
**Why it works**: Highest precision — each fires on 2-10 images. AND-gating ensures specificity. Late-stage (stage 7) so no cascade risk.
**How to mine**: Find cases where top-1 is wrong, top-2 is correct, margin < 0.15. Compute d' on both error populations. Build condition from features with cross-class d' > 1.0.
**Best pairs found**: KP-sports (+6), sports-teapot (+7), bus-mushroom (+5), GR-bear (+5).
**Ceiling**: Most remaining error pairs have insufficient feature separation for high-precision conditions.

### Confidence Gates (+0.5pp across 6 gates)
**What**: If predicted class score < threshold, reject and fall through to #2.
**Why it works**: Removes low-confidence predictions where the class score is barely above alternatives.
**Conditions**: Gate threshold must be below P95 of true positive scores. #2 candidate correctness is NOT guaranteed — typically 30-50% correct. Net gain is small per gate.
**Current gates**: sports_car 0.40, banana 0.42, mushroom 0.42, GR 0.37, orange 0.42, teapot 0.35.

### Rank Extension (rank 3→4→5) (+0.5pp cumulative)
**What**: Check deeper ranks (3, 4, 5) vs rank-1 with progressively stricter thresholds.
**Why it works**: 132 errors at rank 4, ~80 at rank 5. Even with strict gating, some are recoverable.
**Conditions**: Only whitelist high-accuracy pairs (≥80%). Use much stricter multipliers (2.8x for rank4, 4.0x for rank5).

## Tier 3: Feature Engineering (each +0.1-0.5pp)

### Orthogonal Feature Channels
Features produce non-zero-sum gains when they measure fundamentally different image properties.

**LAB color moments** (+0.6pp): cm_a_std, cm_b_std, cm_center_a, cm_center_b. Orthogonal to HSV. Best for banana-orange (d=1.30), GR-KP (d=1.37), teapot-banana (d=1.62).

**Hu moments** (+0.3pp): hu1, hu2 from cv2.HuMoments. Edge shape descriptors orthogonal to edge density. Best for mushroom-banana (d=1.16), GR-banana (d=1.11).

**DCT frequency bands** (+0.25pp): dct_low, dct_mid, dct_high. Orthogonal to spatial features. Best for mushroom-banana (d=0.91), sports-bus (d=0.72).

**Gabor texture** (+0.4pp): Oriented texture at specific frequencies. Best for teapot-KP (gabor_dominant_orient d=0.88), bear-GR (gabor_45_04_var d=0.91).

**Orient entropy** (+0.1pp): Gradient direction diversity. Best for sports-teapot (d=1.11).

### Margin and Multiplier Tuning (+0.25pp)
**What**: Widening reranking eligibility windows and lowering threshold multipliers.
**Why it works at late stage**: Different optimization axis from per-pair tuning. Makes ALL existing discriminants fire more often, not just one pair.
**Best moves**: top-2 margin 0.25→0.30 (+1), rank4 margin 0.22→0.30 (+2), top-2 multiplier 1.5→1.3 (+1).

### Repulsion Pairs (+0.2pp across 11 pairs)
**What**: Symmetric score push/pull between pairs with discriminant evidence.
**Why it works**: Spreads scores before ranking without over-correcting. Safe mechanism (small forces, high confidence threshold).
**Current**: 11 pairs at 0.008-0.012 force.

## Generalization Profile of Each Technique

From the train/val/test audit (Session 14):

| Technique | Train impact | Generalizes? | Notes |
|-----------|:---:|:---:|---|
| Histogram blending | +1-2pp | YES (1.3pp top-3 gap) | Global scoring, no pair-specific tuning |
| Orthogonal features | +0.1-0.6pp each | YES | LAB, Gabor, FFT signals transfer well |
| Repulsion pairs | +0.2pp | YES | Conservative triggers, symmetric forces |
| Pairwise reranking | +7.2pp train | PARTIALLY | Base scoring generalizes; pair-specific bases overfit |
| Local verify | +1.5pp train | POORLY | Hard thresholds on 2-10 images overfit badly (banana +10.5pp gap, bear +11.5pp gap) |
| Confidence gates | +0.5pp train | PARTIALLY | Gate thresholds need cross-val calibration |
| Rank 4/5 extension | +0.5pp train | POORLY | Speculative deep swaps don't transfer |

**Lesson**: Techniques that affect all images (histogram, features, repulsion) generalize. Techniques that fire on tiny subsets (verify, deep reranking) overfit.

## What to Try Next (by expected payoff)

1. **Relax overfit verify conditions** — remove or widen thresholds for conditions that fire on <5 train images. Accept lower train accuracy for better generalization.
2. **Cross-validate confidence gates** — sweep gate thresholds on val, not train.
3. **New orthogonal features** — any genuinely new measurement axis (e.g., GLCM at new distances, wavelet features, contour-based features) can provide +0.1-0.3pp per deployment, and these generalize.
4. **Reduce reranking aggressiveness** — raise pair bases, tighten rank-4/5 margins. The post-processing adds ~4pp on train but only ~1-2pp on val.
