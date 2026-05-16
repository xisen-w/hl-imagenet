# Patch Safety & Cascade Amplification

The most expensive lesson from 330+ iterations: a change that looks like +3 in isolation often becomes -5 after cascade effects. This document codifies how to estimate and mitigate cascade risk.

## The Cascade Amplification Theorem (Empirical)

**Claim**: For any change at pipeline stage N, the actual net effect is:
```
actual = estimated × amplification_factor(N)
```

Where amplification_factor depends on the stage:

| Stage | Factor | Evidence |
|-------|:---:|---------|
| Verify (stage 7) | 1.0x | Verify conditions match predictions within ±1 |
| Reranking params (stage 6) | 1.2-1.5x | Margin widening: estimated +2, actual +1 to +3 |
| Repulsion (stage 4) | 1.0-1.2x | Small forces → small cascade |
| Calibration (stage 3) | 2-3x | Teapot +0.01: estimated +3, actual -11 |
| Blend weight (stage 2) | 3-5x | 0.88→0.90: estimated neutral, actual -17 |
| Signatures (stage 1) | 5-10x | binary_complexity: estimated +3, actual -28 |

**The earlier the stage, the worse the amplification** because more downstream systems need to reprocess under changed conditions.

## Why Cascade Effects Are Asymmetric (Regressions Amplify More)

Positive cascade: a change helps class A → A's improved ranking means A competes better against B → B's ranking drops slightly → but B still wins most of its correct predictions. **Gain is bounded by the direct effect.**

Negative cascade: a change hurts class A → A's worsened ranking means A loses to B more → B now has higher rank in some images → B's discriminants fire differently on those images → C and D are affected through B's changed scoring → ripple continues. **Loss is unbounded by the direct effect.**

This asymmetry means: overestimating gains is common, underestimating losses is dangerous.

## Confidence Gate Estimation Gap

Confidence gates have a specific estimation problem. The "sweep analysis" counts:
- TP in score range [threshold - δ, threshold]: images that would be LOST
- FP in score range [threshold - δ, threshold]: images that would be FIXED

But "FP fixed" assumes the #2 candidate IS the correct class. In practice, #2 is correct only 30-50% of the time. So the actual gain is:
```
actual_gain = FP_in_range × P(#2_correct) ≈ FP_in_range × 0.4
actual_loss = TP_in_range × 1.0
net = FP_in_range × 0.4 - TP_in_range
```

**Session 13 example**: GR gate at 0.39: sweep showed lose 2 TP, fix 4 FP → estimated +2. Actual: -2. Because only ~1 of the 4 "fixed" FPs had correct #2.

## Pre-Deployment Safety Checklist

Before deploying any change:

- [ ] **Scope check**: How many images does this affect? If > 50, extra caution.
- [ ] **Stage check**: What pipeline stage? If stage 1-3, assume 3x amplification.
- [ ] **Failed pattern check**: Does this match a known failed pattern? (See failed_patterns.md)
- [ ] **Correlation check**: Is the feature correlated (|r| > 0.3) with features used in other discriminants?
- [ ] **Cross-class d' check**: For discriminant features, is cross-class d' > 0.8?
- [ ] **Fix/risk ratio**: Is the expected fix count at least 2x the expected risk count?
- [ ] **Revert plan**: Can this be cleanly reverted? (All changes should be.)

## The Code Immune System

Healthy patterns to maintain:

1. **Eval after every change**: Never stack changes. The second change's effect is invisible if the first wasn't evaluated.

2. **One variable at a time**: Change one parameter, one feature, one condition. Multi-variable changes make attribution impossible.

3. **Log before revert**: Write down what you tried, the hypothesis, the result, and why it failed. Then revert. The log is the learning; the code is just the current state.

4. **Preserve the guard rails**: Gap-aware gating, per-pair bases, margin limits — these are the immune system. Don't weaken them to get +1 on one pair.

5. **70% revert rate is normal**: Not a sign of failure. It's the cost of exploring near a local optimum. Budget for it.
