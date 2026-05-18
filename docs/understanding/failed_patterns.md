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

## Pattern 9: "Let's add a signature guard to suppress false positives"
**What you try**: Adding a guard (e.g., `_sigmoid(sat, 0.58, -2)`) to a class signature to penalize images that look like a confuser class.
**What happens**: -9 to -11pp. The guard suppresses real instances of the target class that happen to have the guarded feature.
**Sessions hit**: 14 (bear signature sat<0.58 guard: -9 net, bear lost 11pp), 14 (bear sat<0.68 guard: still bad)
**Why it fails**: Class prototypes have wide variance. Bears can be highly saturated (colorful backgrounds, wet fur). The guard suppresses these real bears far more than it suppresses mushroom false positives, because there are more real bears than FPs in the affected score range.

## Pattern 10: "Verify with zero risk should be safe"
**What you try**: Add a verify condition with 0/N risk cases (perfect separation on risk images).
**What happens**: -5 net despite zero direct risk. The swapped images change relative score rankings, cascading to adjacent pairs.
**Sessions hit**: 15 (r0_warm verify sports-bus: 0/16 risk, -5 net from banana losing -4pp), 15 (conjunctive r0_warm AND dct_h: net zero, banana still -4pp)
**Why it fails**: Verify operates at stage 7, but its effects propagate FORWARD through adjacent pairs. Sports-bus swaps move bus scores, which changes banana-bus and banana-orange dynamics. The cascade path: sports-bus swap → bus score redistribution → banana-bus margin changes → banana-orange margin changes → banana loses.
**Key insight**: "Zero risk on the direct pair" ≠ "zero risk on the system." Must simulate the full downstream impact, especially for pairs adjacent to high-error pairs (banana-bus, banana-orange).

## Pattern 11: "Verify risk = bidirectional error images only"
**What you try**: Compute verify risk by counting how many reverse-error images (B→A) pass the condition. Find 0 risk, deploy.
**What happens**: -6 net because 48 CORRECT predictions also pass the condition.
**Sessions hit**: 15 (hue_red + color_purity for banana-orange: 0/21 reverse errors pass, but 48/126 correct oranges with banana at rank-2 also pass → 14 correct oranges wrongly swapped)
**Why it fails**: Verify tests ALL images where the pair appears at rank-1/rank-2, not just error images. Correct predictions of the "winner" class that happen to have the "loser" at rank-2 ALSO get tested. For pairs where the winner class's features overlap with the condition (e.g., oranges are inherently red), the condition hits dozens of correct predictions.
**Correct risk analysis**: Must test the condition on: (1) forward errors (fix), (2) reverse errors (risk), AND (3) correct winner-class predictions that have the loser at rank-2. Category (3) is typically 5-20x larger than category (2) and dominates the risk.

## Pattern 12: "Increase repulsion strength for high-confusion pairs"
**What you try**: Scale up repulsion from 0.012 to 0.016 (or higher) on pairs with 20+ confusions.
**What happens**: -3 to -13pp regression on 4 of 6 pairs tried. Only bear-mushroom (+1) and teapot-banana (+2) succeeded.
**Sessions hit**: 15b (sports-bus -3, bear-GR -13, banana-orange -6, mush-banana -4, teapot-GR -4, teapot-KP -6)
**Why it fails**: Repulsion operates on ALL images where both classes score > 0.6 proximity, not just the confused images. Increasing repulsion shifts scores for correct predictions too. Sports_car is especially sensitive — it drops 2-3pp on almost any repulsion change because it shares features (warm, hue_orange, grad_mean) with many classes.
**What works instead**: Very small (+0.004) increases on isolated pairs where the discriminant direction is already correct.

## Pattern 13: "Add more pairs to rank-3/4/5 whitelists"
**What you try**: Add high-confusion pairs missing from rank-3+ whitelists when reachable count is 6+.
**What happens**: -8pp when adding bear-sports_car and KP-sports_car to rank-3 whitelist, despite 6 reachable each.
**Sessions hit**: 15b (rank-3 bear-sports+KP-sports: -8pp despite 12 reachable total)
**Why it fails**: The discriminant may be accurate for rank-2 comparisons but unreliable at rank-3, where the true class scored even lower. Also, rank-3 swaps can cascade — promoting a rank-3 candidate displaces rank-1 AND rank-2, creating knock-on errors.
**Exception**: Bear-mushroom rank-3 worked (+1) because it's an isolated pair whose discriminant is robust.

## Meta-Pattern: The 70% Revert Rate

Across 330+ iterations, approximately 70% of changes are reverted. This is not because of poor hypotheses — it's structural:
1. The system is near a local optimum
2. Most perturbations from an optimum are downhill
3. The cascade multiplier amplifies small regressions into large ones
4. Genuinely ambiguous images resist all feature-based discrimination

**Implication**: Budget for 3-5 experiments per +1 net correct prediction. Plan for reverts. Log everything.
