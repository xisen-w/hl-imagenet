# Zero-Sum Dynamics

The most important pattern in this system. Understanding it is prerequisite to not wasting iterations.

## The Core Problem

When you improve class A's discrimination against class B, you ALSO affect B's discrimination against A. If the discriminant is 80% accurate, it helps A 80% of the time and hurts B 20% of the time. But B also has images confused with A — and there, the discriminant helps B 80% and hurts A 20%.

Net effect across both directions: approximately zero for most pairs.

## Evidence

| Change | Class A | Class B | Net |
|--------|:---:|:---:|:---:|
| Orange-banana discriminant | orange +4pp | banana -2.5pp | +1.5pp |
| Teapot-KP discriminant | KP +6pp | teapot -1.5pp | +4.5pp |
| Bear-mushroom Gabor | bear +7pp | mushroom -10pp | -3pp |
| cm_center_a in banana-orange | banana +0.5pp | orange -0.5pp | 0pp |

**Pattern**: Only asymmetric pairs (where the discriminant is much better for one direction) produce net gains. Symmetric pairs are pure zero-sum.

## Why It Gets Worse Over Time

Early in development, there are "easy wins" — pairs with 2:1 or 3:1 asymmetry in discriminant accuracy. These get harvested first. As accuracy improves, the remaining errors are the genuinely ambiguous images where BOTH classes are plausible. For these images, discriminant accuracy approaches 50% — pure coin flip, pure zero-sum.

**Session progression:**
- Sessions 1-4: +3.9pp (many easy wins available, feature expansion)
- Sessions 5-8: +1.6pp (easy wins exhausted, working on moderate pairs)
- Sessions 9-13: +4.55pp (mostly from conditional logic, not pair tuning — escaped zero-sum)
- Sessions 14-17: +0.55pp (system at local optimum, 25/26 experiments fail)
- Sessions 18-20: +11.85pp (escaped again via new methodology + rank extension — NOT pair tuning)

**Pattern**: Every breakthrough escapes zero-sum by finding a NEW axis that doesn't compete with existing optimizations. Pair tuning, feature tuning, and threshold tuning are all zero-sum at late stages. Only structural innovations escape.

## The Sink Class Mechanism

Additive scoring creates "sink classes" — classes that score high on most images:
- school_bus: mean score 0.539 across ALL images (78% accuracy but 166 FPs)
- banana: mean score 0.46 (51% accuracy but 186 FPs)
- jellyfish: mean score 0.319 (70% accuracy but only 22 FPs)

Sink classes are caused by broad feature overlap: bus partially matches on grad_mean, lap_var, hue_orange, warm, horiz_dominance — all features that fire on many images.

**Why guards don't fix sinks**: Bus signature needs ALL its positive signals. Any guard strong enough to reject FPs also rejects TPs. Bus dropped from 78% to 49-60% with every guard we tried.

## What Escapes Zero-Sum

1. **Global scoring changes** (histogram blending, calibration): affect all classes simultaneously, so the relative ranking can shift without one pair robbing the other.

2. **Conditional logic** (verify conditions, confidence gates): only fires on specific subsets of images, so it doesn't affect the broader score distribution.

3. **Orthogonal features**: features measuring genuinely different properties (LAB vs HSV, Gabor vs edge density, Hu moments vs texture) create separation along a new axis that doesn't participate in existing zero-sum dynamics.

4. **Structural extensions** (rank-4, rank-5 reranking): opens new scoring pathways that don't compete with existing ones.

## How to Predict Zero-Sum Before Deploying

1. Compute cross-class d' (error images from BOTH sides of the confusion pair)
2. If cross-class d' < 0.5: the feature cannot separate the error populations. Pure zero-sum.
3. If cross-class d' 0.5-1.0: marginal. May produce +1 net with careful thresholding.
4. If cross-class d' > 1.0: promising. Deploy with conservative sigmoid.

**Critical distinction**: Within-class d' (correct vs error images of the SAME class) does NOT predict success. A feature can have within-class d'=1.3 but cross-class d'=0.24. Only cross-class d' matters for discriminants.

## The Sports_car Cascade Sensitivity (Sessions 15-20)

Sports_car is the most cascade-sensitive class in the system. In Session 15b, 10 out of 14 experiments caused sports_car to lose 2-4pp, regardless of which pair was modified. The regression occurs because sports_car shares features (warm, hue_orange, grad_mean, edge) with many classes. Any repulsion, whitelist, or threshold change that shifts these shared features propagates to sports_car scoring.

This means most experiments have a hidden -2 to -4 drag from sports_car regression, which must be overcome by gains elsewhere. Successful changes are consistently on "isolated" pairs (bear-mushroom, teapot-KP) where neither class shares heavy feature overlap with sports_car.

## The Verify Accumulation Trap (Sessions 18-20)

At 70.0%, the system has ~90 verify conditions across 4 rank levels. These interact with each other:
- A rank-2 verify swap changes which image appears at rank-1 for rank-3/4/5 stages
- A rank-3 condition can make a rank-2 condition fire differently (or not fire)
- Removing one harmful condition can make 3 other conditions start working correctly

This creates a form of zero-sum WITHIN the verify system itself. Adding a new condition at rank-3 can break an existing condition at rank-2. Session 20 found +21 net from REMOVING 8 bad conditions — the conditions were harming each other.

**Implication**: The system needs periodic "verify audits" — removing conditions that have become net-negative due to interactions with newer conditions. This is a new form of the zero-sum dynamic that didn't exist before Session 18.

## Escaping Zero-Sum: The Historical Pattern

| Escape | Mechanism | How it avoids zero-sum |
|--------|-----------|----------------------|
| Sessions 9-13 | Verify conditions | Fire on specific subsets, don't change global scores |
| Session 18 | Exhaustive scan | Same mechanism as above, just automated/systematic |
| Session 19 | Rank-3/4/5 | New scoring pathway that doesn't compete with rank-2 |
| Session 20 | Bad condition pruning | Removes interference within verify system |

All escapes share one property: they find corrections that DON'T participate in existing score distributions. They operate AFTER the zero-sum scoring is done.

## The Ultimate Zero-Sum: 100% Train (Session 26)

At 100% train accuracy, the ENTIRE system becomes zero-sum. Every change that fixes one image must break another — because there are no "free" correct predictions to absorb regression. This is qualitatively different from earlier zero-sum dynamics:

**Before 100%**: Zero-sum existed between PAIRS (improving A-B hurts B-A). Escapes existed via structural extensions, new features, verify conditions.

**At 100%**: Zero-sum exists across the ENTIRE system. There is no escape within the current architecture because:
1. All structural extensions have been deployed (ranks 2-10)
2. All single-feature thresholds have been claimed
3. Post-pipeline position has been fully exploited (9 waves)
4. Even "safe" changes (discriminant features) cascade through 900+ downstream conditions

**Evidence**: Adding `warm_cool_a_diff > 0.080` to the orange-banana discriminant — a change that would be +1 net in isolation — caused -5 regression (99.75%) because verify conditions calibrated to the previous discriminant output broke.

This is the zero-sum ENDGAME: when the system reaches completeness, zero-sum becomes universal and inescapable within the architecture. The only escape is architectural reset (rebuild with regularization) or improved base scoring (reduce the number of corrections needed).
