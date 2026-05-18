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
- Sessions 1-4: +37pp (many easy wins available)
- Sessions 5-8: +4pp (easy wins exhausted, working on moderate pairs)
- Sessions 9-13: +4.5pp (mostly from conditional logic, not from pair tuning)

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

## The Sports_car Cascade Sensitivity (Session 15)

Sports_car is the most cascade-sensitive class in the system. In Session 15b, 10 out of 14 experiments caused sports_car to lose 2-4pp, regardless of which pair was modified. The regression occurs because sports_car shares features (warm, hue_orange, grad_mean, edge) with many classes. Any repulsion, whitelist, or threshold change that shifts these shared features propagates to sports_car scoring.

This means most experiments have a hidden -2 to -4 drag from sports_car regression, which must be overcome by gains elsewhere. The 3 changes that succeeded (bear-mush repulsion, teapot-banana repulsion, bear-mush rank-3) were all on "isolated" pairs where neither class shares heavy feature overlap with sports_car.
