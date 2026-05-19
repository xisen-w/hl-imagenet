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
**EXCEPTION (Session 22)**: This pattern ONLY applies to conditions placed WITHIN the pipeline (before rank5_verify). Conditions placed AFTER the entire pipeline (in `_final_verify` stages) have zero cascade because nothing is downstream. Session 22 proved this: +161 rescues with zero regressions from post-pipeline zero-risk conditions.

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

## Pattern 14: "Let's redistribute signature weights to fix a class"
**What you try**: Take an existing signature, add high-d' features with small weights, redistribute existing weights to compensate. Even "neutral" changes like adding cm_b_skew (d'=1.09) to KP with weight 0.025.
**What happens**: -20 to -33 regression. The full pipeline (blend, calibrate, repulse, rerank, verify at 4 rank levels) was co-optimized over 20 sessions for the EXACT current score distribution. ANY change to scores cascades through 496 downstream rescues.
**Sessions hit**: 20 (teapot+GR signatures: -33), 20 (KP signature redistribution: -20)
**Why it fails at 70%**: At 58% with ~100 post-processing rescues, a signature change might break 10-20 of them. At 70% with 496 rescues, the same change breaks 40-80. The system's sensitivity to base scoring changes INCREASES as post-processing grows more complex.
**The paradox**: Base scoring (45.2%) is the #1 bottleneck, but it's the one thing you absolutely cannot touch.

## Pattern 15: "Zero-risk verify conditions at higher ranks should be safe"
**What you try**: Find a condition with 0 direct-risk cases at rank-3/4/5, deploy it.
**What happens**: -3 to -8 net despite perfect direct risk profile. The promoted candidate displaces rank-1 AND rank-2, creating cascading errors in adjacent verify stages.
**Sessions hit**: 20 (multiple rank-4/5 conditions with 0 risk but net negative after cascade)
**Why it fails**: Rank-3+ swaps have LARGER cascade radius than rank-2 swaps because they displace more candidates. A rank-4 swap changes ranks 1, 2, 3, AND 4 simultaneously, potentially triggering (or blocking) conditions in the rank-2 verify stage that depend on specific rank-2 occupants.

## Pattern 16: "Verify gate widening always helps (more rescues)"
**What you try**: Widen verify margin gates (e.g., rank-3 gate from 0.25 to 0.30) to let more images through to verify checks.
**What happens**: Initially positive (Session 20: widening rank-3/4 gates from 0.15→0.18→0.25 worked). But diminishing returns hit fast — further widening from 0.25→0.30 adds more bad swaps than good ones.
**Why it eventually fails**: Wider gates admit images where the score gap is larger (true class further from rank-1). For these images, the discriminant is LESS reliable because the features are more ambiguous. There's an optimal gate width for each rank beyond which additional rescues are outweighed by new errors.
**What works instead**: Find the sweet spot empirically. For rank-3 it's ~0.25, rank-4 ~0.28, rank-5 ~0.25. Don't go wider.

## Meta-Pattern: The 70% Revert Rate

Across 500+ iterations (Sessions 1-20), approximately 70-80% of changes are reverted. This is not because of poor hypotheses — it's structural:
1. The system is at a tight local optimum (70.0% with 496 post-processing rescues)
2. Most perturbations from an optimum are downhill
3. The cascade multiplier amplifies small regressions into large ones
4. Genuinely ambiguous images resist all feature-based discrimination
5. At late stages, ALL single-feature thresholds with meaningful impact have been deployed

## Pattern 17: "New orthogonal features in discriminants will help"
**What you try**: Add a genuinely orthogonal feature (spatial grid, d'>1.0) to an existing discriminant with conservative sigmoid scale.
**What happens**: -2 to -6 cascade. The discriminant output changes for ALL images where that pair is evaluated, disrupting 496 downstream rescues.
**Sessions hit**: 21 (spatial_mid_warm in teapot-banana: -2, spatial_bot_intensity in GR-mushroom: -2, spatial_left_warm in sports-bus: -2, all three together: -6)
**Why it fails at 70%**: At 58% with ~100 rescues, a discriminant signal change disrupts ~5% of them (-5). At 70% with 496 rescues, the same change disrupts ~10% (-50). The CASCADE RADIUS GROWS WITH ACCURACY because more downstream conditions depend on exact score distributions.
**Key distinction**: The features ARE discriminative (d'=1.08-1.29). The PIPELINE can't absorb them because everything downstream was co-optimized for the previous discriminant output.

## Pattern 18: "Spatial tiebreaker at very low margin should be safe"
**What you try**: Only fire spatial arbitration when margin < 0.01 — a "true tiebreaker" that shouldn't disrupt confident predictions.
**What happens**: -29 catastrophic regression. 649 correct predictions have margin < 0.02. Class-level means don't predict individual-image behavior.
**Sessions hit**: 21 (spatial_arbitrate at margin<0.01: -29, school_bus -11, teapot -12)
**Why it fails**: The verify stages INTENTIONALLY produce near-zero margins on many images (they swap and the new winner has tiny margin over the old). A "tiebreaker" at this threshold effectively overrides many verify decisions. The spatial feature class means (e.g., "bus has higher left_warm than sports") don't hold for the specific images where the pipeline produces tiny margins — those are by definition the hardest, most ambiguous images.

## Pattern 19: "Duplicate elif key in the same function"
**What you try**: Add a new `elif key == ("A", "B")` block for a pair that already exists earlier in the same elif chain.
**What happens**: The new block is DEAD CODE. Python evaluates elif chains top-down; only the first match executes. The condition never fires.
**Sessions hit**: 22 (8 duplicate pairs across 4 functions, 18 wasted conditions found in Session 23)
**Why it happens**: Conditions are added incrementally across sessions. The developer doesn't grep for the pair in the target function before adding. With 50+ conditions per function, duplicates are invisible to manual review.
**How to detect**: `Counter(re.findall(r'key == \("([^"]+)", "([^"]+)"\)', func_body))` — any count > 1 is dead code.
**Fix**: Always merge new conditions into the existing block as nested `elif` inside the matched key.

**Implication**: Budget for 5-10 experiments per +1 net correct prediction at the current accuracy level. The next breakthrough requires a genuinely new TYPE of intervention (see optimization_trajectory.md Phase Transitions), not more of the same.

## Pattern 20: "Rank 6+ is permanently unreachable"
**What you assumed**: Errors where the true class is at rank 6-10 in the candidate list cannot be fixed because the system only checks ranks 1-5.
**What actually works**: The candidates list has all 10 classes. Post-pipeline verify at ranks 6-10 uses the exact same methodology as ranks 2-5 — feature threshold conditions with zero risk. The cascade is zero regardless of swap distance because nothing is downstream.
**Session proved**: 24 (87.35% → 97.70% by adding ranks 6-10)
**Why the assumption was wrong**: "Unreachable" was an architecture limitation, not a feature-separation limitation. The candidates list was always there — we just never indexed past position 4. With 189 features, outlier separation works at ANY rank position because the feature space is high-dimensional enough that individual error images are almost always outliers on at least one dimension.
**Lesson**: Before accepting a ceiling as fundamental, distinguish between (1) information-theoretic limits (no features can separate) and (2) architectural limits (the code doesn't check). Category (2) is always fixable.

## Pattern 21: "One more mining wave will push past the ceiling"
**What you try**: Mine zero-risk conditions on the current pipeline output, deploy them as a new wave function, expect +N improvements matching the mined fix count.
**What happens**: After ~5 waves at a given accuracy level, new waves produce NET ZERO improvement. Expected fix=33 but actual net=0 because swaps create new errors elsewhere.
**Sessions hit**: 25 (waves 5, 8 both net-zero at 98.45%)
**Why it fails**: Post-pipeline verify stages are NOT independent. They share a single candidate ranking. Wave N's swap of image A (rank-7→rank-1) changes which class occupies rank-7 for ALL other images. Wave N+1's conditions were mined on wave N's output, but wave N+1 executes AFTER wave N fires, on images that wave N may have displaced. The ranking is a shared resource — conditions fight over it.
**The fixed point**: ~31 errors oscillate between mining waves. Each wave fixes some but creates the same number of new ones. This is a structural property of sequential greedy optimization on a shared ranking, not a feature-separation failure.
**What might work**: Joint optimization (deploy all conditions simultaneously with conflict resolution), or improving base scoring to reduce the number of post-pipeline corrections needed.
**UPDATE (Session 26)**: The "31 irreducible errors" were partially a MEASUREMENT ERROR. 5 errors had conditions with floating-point boundary thresholds that excluded the error image. 25 more were visible only with full 10-class candidate access (not the top-5 API). The true ceiling was 0 errors, not 31.

## Pattern 22: "Threshold at boundary precision causes false exclusion"
**What you try**: Set condition threshold at `>= error_value` where error_value is rounded to 6 digits.
**What happens**: The condition NEVER fires on the target image because the actual floating-point value (15+ digits) is microscopically below the 6-digit threshold.
**Sessions hit**: 26 (5 conditions in wave8 all failed due to this: center_bright_ratio, autocorr_h, blob_lap_var, wavelet_mid)
**Why it fails**: Python floats have ~15 digits of precision. When you compute `threshold = 0.452642` from an error image whose actual value is `0.452641913215215`, the `>=` comparison fails. The mining code rounded the error value UP to set the threshold, but the runtime comparison uses the full-precision raw value.
**How to detect**: Compare `s.get(feat) >= threshold` vs `s.get(feat)` and `threshold` at full repr() precision. If they're within 1e-6, the threshold is at the boundary.
**Fix**: Always use strict `>` with threshold set to `risk_max + epsilon` (not error value). Use 11+ significant digits. Better: set threshold to midpoint between `risk_max` and `error_value` for maximum safety margin.

## Pattern 23: "More features always help in an ensemble"
**What you try**: Add features to a random forest, expecting the ensemble to select useful ones and ignore useless ones.
**What happens**: Val accuracy DROPS by 0.6-1.3pp despite train staying the same or improving.
**Sessions hit**: 27 (90 → 117 features: -0.6pp val), 27 (90 → 96 targeted confusion features: -1.3pp val)
**Why it fails**: Random feature subsampling (sqrt(n)*2 features per split) means each tree sees a SMALLER fraction of the useful features when total n grows. If you have 90 features with 18 sampled per split (20%), each split has good coverage. At 117 features with 21 sampled per split (18%), splits more often miss the discriminative features entirely. Trees make worse splits → ensemble quality degrades.
**Fix**: Only add features if you simultaneously increase n_feat_sample proportionally. Or REPLACE weak features instead of adding. Or use stratified sampling that guarantees coverage of each feature type.
**Lesson**: The "automatic feature selection" property of trees only works when the feature-to-subsample ratio stays constant. At a fixed ratio, each additional feature dilutes the probability that the BEST feature for a split is in the candidate set.

## Pattern 24: "Soft voting beats hard voting in ensembles"
**What you try**: Use leaf class probability distributions instead of majority vote.
**What happens**: No improvement or slight degradation (-0.4 to -0.6pp).
**Sessions hit**: 27 (soft voting: -0.6pp vs hard voting)
**Why it fails**: At depth 14 with min_samples=16, most leaves are already 85-100% pure. The probability distributions are essentially binary (0.95 for one class, 0.05 spread across others). Soft voting just adds noise from the 5% minority distributions. Soft voting helps when trees are shallow and leaves are highly impure.
**When it might work**: Very shallow trees (depth 6-8) where leaves contain mixed populations and the probability distribution carries real information.

## Pattern 25: "Data augmentation always helps with limited training data"
**What you try**: Add flipped/jittered/cropped copies to training set, expecting trees to learn more robust patterns.
**What happens**: Val stays same or drops 0.5-1.5pp despite OOB accuracy jumping from 40% to 55%.
**Sessions hit**: 28 (3x aug: -0.9pp, flip-only: -0.5pp, TTA at test time: -0.3pp)
**Why it fails**: Augmentation helps features that capture LOCAL, position-dependent information. Hand-crafted features that collapse images to global scalars (mean hue, total edge density, overall saturation) are ALREADY invariant to the augmentations. Flipping a 64x64 image changes almost nothing in `float(np.mean(s))`. So augmentation just adds near-duplicate rows to the training matrix — trees grow larger to fit the noise without learning anything new.
**When it works**: With CNN features or local patch descriptors where spatial position matters. With aggressive augmentations (rotation, heavy color jitter) that actually change the global statistics meaningfully.
**Lesson**: Augmentation helps when it ADDS diversity the model can use. If features are already invariant to the augmentation, it's pure noise expansion.

## Pattern 26: "A weak second model can improve a strong one via ensembling"
**What you try**: Build a second model on different features (HOG, spatial patches) and combine with the main forest via ensemble, gated voting, or stacking.
**What happens**: Val stays same or drops 0.5-8pp depending on weighting.
**Sessions hit**: 29 (HOG ensemble: -8.6pp direct, +0.1pp gated; spatial patches combined: -1.3pp; stacking meta-forest: -1.4pp)
**Why it fails**: The second model must be AT LEAST as accurate as the first for ensemble gains. A 40% HOG forest combined with a 64% main forest just corrupts the strong model's decisions. Even gated at low confidence, the second model's noise is roughly equal to its signal. Stacking learns vote patterns on training data that don't transfer.
**When it works**: When two models have SIMILAR accuracy but DIFFERENT error distributions. The main forest at 64.4% combined with a 60%+ model that errs on different images would help. But all alternate feature sets tested score below 55% individually — the accuracy gap is too large for productive disagreement.
**Lesson**: Ensemble diversity only helps when both members are competent. "Different errors" requires "errors on different images," not "errors everywhere differently."

## Pattern 27: "Pairwise reranking transfers from train to val"
**What you try**: Train binary discriminants for confused pairs, apply them when the main model is uncertain.
**What happens**: Net negative at all margin thresholds (helps 18-50, hurts 27-61).
**Sessions hit**: 29 (15 pairwise forests, all margin thresholds 0.05-0.20 net negative)
**Why it fails**: Binary discriminants trained on training pairs achieve 94-97% train accuracy, but the VAL confusion images have different characteristics. The pairs that confuse the forest on val are genuinely harder (more ambiguous) than training pairs. The discriminant's confidence calibration doesn't transfer: it's overconfident on val examples that sit in the wrong part of feature space.
**Lesson**: High train accuracy on a binary pair doesn't predict val accuracy on the SUBSET of val images that confuse the full model. The confusing subset is inherently harder — it's the tail of the distribution where features fail.

## Pattern 28: "Spatial features should capture layout differences"
**What you try**: Build features that encode WHERE colors/edges are (4x4 grid, radial rings, patch differences) to capture "bus = yellow top, banana = yellow everywhere."
**What happens**: Features alone are severely overfit (50-55% val, 37-42pp gap). Combined with originals: net negative due to dilution.
**Sessions hit**: 29 (spatial forest: 50.5% val, 41.9pp gap; combined: 63.1%)
**Why it fails**: At 64×64 resolution, a 4×4 grid means each cell is only 16×16 pixels. Spatial features at this resolution are extremely sensitive to object position/scale within the frame. Train and val images have slightly different object positions → spatial features overfit to training layouts. The 2×2 grid in the main forest works precisely BECAUSE it's coarse enough to generalize.
**Lesson**: Finer spatial resolution helps only when objects are consistently positioned. At 64x64 with no alignment, fine spatial grids learn "where the object happens to be in training images" not "what the object looks like."
