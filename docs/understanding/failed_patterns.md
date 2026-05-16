# Failed Patterns

Recurring failure modes. If your proposed change matches one of these patterns, it will almost certainly fail. Read this before implementing.

## Pattern 1: "Let's normalize scores first"
**What you try**: Z-score, mean subtraction, percentile normalization of class scores before ranking.
**What happens**: -1pp to -4.6pp regression. The entire reranking layer (24 discriminants, bases, gap scales) was tuned for raw score distributions. Changing the distribution breaks all downstream thresholds.
**Sessions hit**: 2 (z-score: -4.6pp), 2 (mean sub: -1.3pp), 2 (partial: -0.2pp), 3 (alpha calibration: -0.3pp)
**Why it fails**: Multi-layer systems have emergent calibration. Each layer's parameters encode assumptions about the previous layer's output distribution. Normalization invalidates all those assumptions simultaneously.

## Pattern 2: "Let's add this feature to the signature"
**What you try**: Adding a new sigmoid term to a class's base signature function.
**What happens**: -8 to -28 regression. The target class gains slightly, but all other classes lose because the target's score changes for ALL 2000 images.
**Sessions hit**: 5 (warm_hue_median in GR: -0.6pp), 7 (binary_complexity in teapot: -28), 2 (raw hist in signatures: marginal)
**Why it fails**: Signatures are stage 1 — their output feeds into blending, calibration, repulsion, ranking, reranking, AND verify. A stage-1 change cascades through 6 downstream stages. The cascade multiplier is 2-3x.

## Pattern 3: "This feature has great d' so let's use it"
**What you try**: Feature with d' > 1.0 at class level gets deployed in a discriminant.
**What happens**: Net zero or -2pp. The feature was measured on ALL correct vs error images, but the discriminant only fires on close pairs. Close pairs are the genuinely ambiguous images where even good features fail.
**Sessions hit**: 8 (warm_cool_a_diff d'=0.78: -0.7pp), 13 (hue_entropy cross-d'=1.39: -2 to -4)
**Why it fails**: Within-class d' ≠ cross-class d'. Must compute d' on error images from BOTH sides of the confusion pair. Cross-class d' is typically 30-50% of within-class d'.

## Pattern 4: "Let's apply this change to all classes/all pairs"
**What you try**: A technique works for one pair, so you generalize it to all pairs.
**What happens**: -2pp to -15pp regression. Each pair has different error dynamics. The generalization hurts more pairs than it helps.
**Sessions hit**: 5 (per-class hist blend: -2.5pp), 5 (discriminant vote: -7pp), 6 (LAB in ALL discs: -0.8pp), 9 (proto verify for all pairs: -3pp)
**Why it fails**: Each pairwise intervention is tuned for the specific feature distributions of that pair. "Works for banana-orange" does NOT mean "works for bear-mushroom." Deploy selectively, pair by pair.

## Pattern 5: "Let's boost this struggling class with calibration"
**What you try**: Additive calibration offset (+0.01 to +0.02) for a low-accuracy class.
**What happens**: The target class gains +0.5-1pp but 2-3 other classes lose more. Net -1 to -11.
**Sessions hit**: 4 (teapot +0.01: net +4 but precarious), 13 (teapot +0.01: -11), 7 (banana -0.01: -3), 12 (teapot calibration: -28 after cascade)
**Why it fails**: Calibration changes the score for that class on ALL images. If you boost teapot by 0.01, every image now has teapot 0.01 higher — this moves teapot up in the ranking for non-teapot images too, creating new false positives.

## Pattern 6: "Let's widen the reranking window to catch more"
**What you try**: Increasing verify margin, rank-3/4/5 margin, or adding more pairs to whitelists.
**What happens**: Small gains from margin widening (+1 per step), but catastrophic losses from whitelist expansion (-5 to -16).
**Sessions hit**: 12 (expanded rank-3/4 whitelists: -16), 13 (banana-teapot in rank3: -5), 13 (verify margin 0.15→0.18: -5)
**Why it fails**: Discriminants are 70-85% accurate. At wider margins, they encounter MORE cases where they're wrong. The additional "rescues" are outweighed by additional "corruption." Whitelist expansion is worse because deep-rank discriminants are even less accurate.

## Pattern 7: "Let's add a post-pipeline layer"
**What you try**: Vote counts, ensemble scoring, secondary reranking pass, hist veto.
**What happens**: -3pp to -7pp regression. Double-counts with existing reranking.
**Sessions hit**: 5 (discriminant vote: -5pp to -7pp), 5 (hist veto: net negative), 10 (double verify pass: net negative)
**Why it fails**: The pipeline already extracts all the signal from its features. Adding another layer that reads the SAME features can only add noise. The information is already maximally extracted by the existing pipeline.

## Pattern 8: "Let's add a new discriminant pair"
**What you try**: Build a discriminant for a confusion pair that doesn't have one, add to PAIR_BASE and all whitelists.
**What happens**: Net zero to -3. The new discriminant fires through repulsion and deep-rank reranking, cascading to unrelated classes. Even with good d' (2.34), the cascade eats the gain.
**Sessions hit**: 14 (banana-KP disc: +1 KP, -1 sports_car = 0 net), 14 (mushroom-sports_car disc: -3 net via sports_car cascade)
**Why it fails**: Adding a new discriminant pair is not just a new pair — it's a new participant in the repulsion system AND the deep-rank (3/4/5) reranking. The interaction with existing pairs creates unpredictable cascades. The system was optimized without this pair; adding it changes the equilibrium.
**Mitigation**: If adding a new pair, add ONLY to rank-1/2 reranking (no whitelists, no repulsion) and use pair_base=0.10+ to prevent casual firing.

## Meta-Pattern: The 70% Revert Rate

Across 330+ iterations, approximately 70% of changes are reverted. This is not because of poor hypotheses — it's structural:
1. The system is near a local optimum
2. Most perturbations from an optimum are downhill
3. The cascade multiplier amplifies small regressions into large ones
4. Genuinely ambiguous images resist all feature-based discrimination

**Implication**: Budget for 3-5 experiments per +1 net correct prediction. Plan for reverts. Log everything.
