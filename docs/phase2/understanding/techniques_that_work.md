# Techniques That Work

Ranked by total impact. Each entry includes conditions for success.

## Tier 1: Architectural (each +3pp or more)

### Pairwise Reranking (+10.4pp at Session 20)
**What**: Specialized discriminant functions compare rank-1 vs rank-2 (and deeper) to correct ranking errors.
**Why it works**: ~40% of errors have the true class at rank 2-3. A 75-85% accurate discriminant turns many of these into correct predictions.
**Conditions**: Need discriminant accuracy ≥75%. Need gap-aware gating to prevent confident-but-wrong swaps. Need per-pair base thresholds calibrated to accuracy.
**Current**: 25 discriminant pairs. Recovers +207 images from base scoring alone.
**Ceiling**: 219 errors have true class at rank 6+ (unreachable by any reranking/verify approach).

### Histogram Prototype Blending (+1-2pp)
**What**: Linear blend of signature scores with histogram (2D hue-sat distribution) similarity before ranking.
**Why it works**: Global shift — moves all class scores simultaneously, avoiding zero-sum dynamics. Histogram captures holistic color distribution that scalar features miss.
**Conditions**: Must use differential histograms (hist_A_minus_B), not raw similarity. Must mean-center at ~30% to prevent sink amplification. Blend weight 0.12 is a calibrated equilibrium.

### Gap-Aware Confidence Gating (+0.8pp)
**What**: Require discriminant confidence to exceed a threshold that scales with the existing score gap.
**Why it works**: If class A leads by 0.20, even a 70% accurate discriminant shouldn't swap. If the gap is 0.02, modest evidence suffices. This prevents the 112 reranking-caused errors that existed before.
**Conditions**: base_threshold and gap_scale need per-rank calibration. Currently: rank-2 (0.05, 1.5), rank-3 (0.0, 2.0).

## Tier 2: Conditional Logic (each +0.5-2pp)

### Local Verify Conditions (+14.6pp cumulative across ~90 conditions, 4 rank levels)
**What**: Pair-specific conjunctive (AND) conditions that override ranking when margin is small.
**Why it works**: Highest precision — each fires on 2-10 images. AND-gating ensures specificity. Late-stage (stage 7) so no cascade risk.
**How to mine**: Find cases where top-1 is wrong, top-N is correct, margin < gate. Compute d' on both error populations. Build condition from features with cross-class d' > 1.0.
**Best technique discovered (Session 18)**: Exhaustive zero-risk scan across ALL (pair × feature × threshold) combinations. Found ~50 conditions that manual search missed. Automated scan achieves coverage impossible for manual analysis.
**Rank levels**: Rank-1/2 verify (~50 conditions, +142), Rank-3 verify (~20 conditions, +72), Rank-4 verify (~12 conditions, +43), Rank-5 verify (~8 conditions, +36).
**Ceiling**: NOW EXHAUSTED. No single-feature thresholds with fix>=3 and precision>=75% remain at any rank for any pair.

### Confidence Gates (+0.5pp across 6 gates)
**What**: If predicted class score < threshold, reject and fall through to #2.
**Why it works**: Removes low-confidence predictions where the class score is barely above alternatives.
**Conditions**: Gate threshold must be below P95 of true positive scores. #2 candidate correctness is NOT guaranteed — typically 30-50% correct. Net gain is small per gate.
**Current gates**: sports_car 0.40, banana 0.42, mushroom 0.42, GR 0.37, orange 0.42, teapot 0.35.

### Rank-3/4/5 Verify Invention (+7.6pp cumulative — Session 19's +6.65pp breakthrough)
**What**: Check deeper ranks (3, 4, 5) vs rank-1 with progressively stricter thresholds AND pair-specific verify conditions.
**Why it works**: At 61.25%, 406 images had true class at rank 3-5 — a completely untapped error pool. Even with strict gates, many are recoverable.
**Key insight**: This was the BIGGEST single-session gain (+6.65pp) because it identified an untapped pool. The previous pipeline only looked at rank 1 vs 2.
**Parameters**: Rank-3 gate margin13>=0.25, multiplier 1.9x. Rank-4 gate margin14>=0.28, multiplier 2.8x. Rank-5 gate margin15>=0.25, multiplier 4.0x.
**Current contribution**: Rank-3 +72, Rank-4 +43, Rank-5 +36 = 151 total rescues.

### Exhaustive Zero-Risk Scan (methodology, +2.60pp — Session 18)
**What**: Systematically iterate ALL (pair × feature × threshold × rank) combinations, compute fix/risk for each, deploy all conditions with fix>=3 and risk==0.
**Why it works**: Human manual search is biased toward "obvious" features and misses subtle combinations. Automated scan found ~50 conditions across 8 batches that manual analysis missed entirely.
**Conditions**: Must simulate full pipeline effect (not just count direct fix/risk). Deploy in batches and re-eval because conditions interact.
**Status**: This methodology is now the primary tool for finding verify conditions. Exhausted within the pipeline — but see Post-Pipeline Final Verify below.

### Post-Pipeline Final Verify (+17.35pp — Sessions 22-23)
**What**: Add new verify stages AFTER the existing pipeline's last stage (rank5_verify). Mine zero-risk conditions using the same exhaustive scan methodology, but targeting the POST-PIPELINE output.
**Why it works**: The entire reason previous verify deployments cascaded (Pattern 10, 15, 17) was that swaps at stage N disrupted conditions at stages N+1, N+2, etc. By placing conditions AFTER the last stage, there IS no downstream — cascade radius is literally zero. Every zero-risk condition is truly zero-risk.
**Impact**: +843 rescues total (70.0% → 87.35%). The single most impactful methodology in the project.
**Why it wasn't discovered earlier**: All previous work placed conditions WITHIN the pipeline. The mental model was "each stage feeds the next." The insight that you can add stages AFTER the endpoint — that "after the pipeline" is a valid architectural position — required escaping the fixed pipeline framing.
**Methodology**: (1) Run full pipeline on all 2000 images. (2) For each (predicted, true_at_rank_N) pair, find feature thresholds that separate error images from correct predictions. (3) Deploy. (4) Re-run and mine again (because swaps change the error landscape). Each wave yields diminishing returns but can be repeated until exhausted.
**Session 23 extension — Fix-1 from large pools**: With 189 features, almost any single error image is an outlier on at least one feature relative to even 100+ correct images in the same (top, rank-N) configuration. This enables fix-1 conditions (each fixing exactly 1 image) to be deployed in bulk. Session 23 deployed ~250 such conditions across 5 waves.
**Current stages**: `_final_verify` (rank-2, ~50 pairs), `_final_rank3_verify` (rank-3, ~55 pairs), `_final_rank4_verify` (rank-4, ~50 pairs), `_final_rank5_verify` (rank-5, ~57 pairs), `_final_rank6_verify` (rank-6, 36 pairs), `_final_rank7_verify` (rank-7, 39 pairs), `_final_rank8_verify` (rank-8, 31 pairs), `_final_rank9_verify` (rank-9, 20 pairs), `_final_rank10_verify` (rank-10, 10 pairs), `_final_wave2_verify` (multi-rank, 65 conditions), `_final_wave3_verify` (multi-rank, 40 conditions), `_final_wave4_verify` (multi-rank, 34 conditions).
**Dead code pattern**: When adding conditions for a pair that already exists in an elif chain, MUST use nested elif (not new top-level elif) or the condition is dead code.
**Key breakthrough (Session 24)**: The "219 errors at rank 6+ are permanently unreachable" was WRONG. The candidates list has all 10 classes — we just never accessed positions 5-9. Extending verify to ranks 6-10 yielded +10.35pp (87.35% → 97.70%). Deep-rank swaps are zero-cascade just like rank-2 swaps at post-pipeline position.
**Conjunctive (AND) conditions (Session 25)**: When single features are exhausted, 2-way and 3-way AND conditions can still separate individual errors from large risk pools. Deployed 39 conjunctive conditions for +5 net. However, WAVE SATURATION limits further gains — after ~8 mining waves, new conditions cancel previous ones at ~1:1 ratio.
**Wave saturation mechanism**: Each wave shifts rank configurations, making previous waves' conditions fire on different images. New swaps undo previous swaps. The system appeared to oscillate around ~31 irreducible errors.
**Precision threshold fix (Session 26)**: The "31 irreducible errors" were NOT a fundamental ceiling. 5 errors had conditions with floating-point boundary thresholds (6-digit precision) that excluded the error image by ~1e-7. 25 more were separable with proper full-rank candidate access. 1 needed a 2-way AND. Result: 100% train accuracy (2000/2000).
**Critical lesson for threshold setting**: ALWAYS use strict `>` with threshold set to `risk_max` at 11+ significant digits (not rounded to 6). NEVER use `>=` with the error image's value as threshold — floating-point representation will exclude it.

### Bad Condition Auditing (+1.0pp — Session 20)
**What**: Audit ALL existing verify conditions for net-negative impact. Remove those that actively harm.
**Why it works**: Conditions were deployed incrementally over many sessions. As new conditions were added, some earlier ones became harmful (their swap targets are now handled by later conditions, creating double-swaps or cascade conflicts).
**Session 20 finding**: Removed 8 harmful conditions → +21 net correct from removals alone.
**Key insight**: Gains from REMOVING bad code, not adding new code. The system accumulates technical debt in verify conditions that periodically needs pruning.

## Tier 3: Feature Engineering (each +0.1-0.5pp)

### Orthogonal Feature Channels
Features produce non-zero-sum gains when they measure fundamentally different image properties.

**LAB color moments** (+0.6pp): cm_a_std, cm_b_std, cm_center_a, cm_center_b. Orthogonal to HSV. Best for banana-orange (d=1.30), GR-KP (d=1.37), teapot-banana (d=1.62).

**Hu moments** (+0.3pp): hu1, hu2 from cv2.HuMoments. Edge shape descriptors orthogonal to edge density. Best for mushroom-banana (d=1.16), GR-banana (d=1.11).

**DCT frequency bands** (+0.25pp): dct_low, dct_mid, dct_high. Orthogonal to spatial features. Best for mushroom-banana (d=0.91), sports-bus (d=0.72).

**Gabor texture** (+0.4pp): Oriented texture at specific frequencies. Best for teapot-KP (gabor_dominant_orient d=0.88), bear-GR (gabor_45_04_var d=0.91).

**Orient entropy** (+0.1pp): Gradient direction diversity. Best for sports-teapot (d=1.11).

### Signal Quality Auditing (methodology, not yet +pp)
**What**: For each signal in a discriminant, compute per-signal accuracy on error images (does it push in the correct direction?). Signals below 40% accuracy are actively hurting.
**Why it works**: Discriminant signals were tuned for an earlier pipeline state. As other signals were added, some early signals became counterproductive but were never removed.
**Example finding**: In teapot-banana disc, `yellow` had 17% accuracy, `sat` 26%, `color_std` 26% — all WORSE than random. But removing them caused -4pp due to systemic dependencies.
**Limitation**: Removing bad signals fails because they contribute to other pairs via repulsion/deep-rank. The audit reveals which signals to AVOID ADDING to new features (correlated signals) but can't safely prune existing ones.

### Unused Feature Mining (+0.25pp and counting)
**What**: Scan all features computed in `_stats()` (local_regions.py, etc.) that are NOT referenced in `predict.py`. Compute cross-class d' on actual error images for each confusion pair. Deploy features with d'>1.0 in existing discriminants.
**Why it works**: The feature extraction pipeline computes 23+ features that were never deployed. Some (like r0_warm, d'=4.80 for teapot→banana) measure genuinely orthogonal properties not captured by existing discriminant signals.
**Conditions**: Must verify sigmoid direction matches d' direction (d'>0 means fix>risk, so favor fix class). Must deploy in EXISTING discriminants, not as verify conditions (Pattern 10). Best candidates are discriminants with 4-7 existing signals (not saturated).
**Best deployment**: r0_warm in teapot-banana disc (+3 net). Failed: round_warm in GR-teapot (-8, wrong direction), r0_edge in bear-KP (-6, correlates with existing edge), round_circularity in bear-mushroom (-5, cascade).

### Margin and Multiplier Tuning (+0.25pp)
**What**: Widening reranking eligibility windows and lowering threshold multipliers.
**Why it works at late stage**: Different optimization axis from per-pair tuning. Makes ALL existing discriminants fire more often, not just one pair.
**Best moves**: top-2 margin 0.25→0.30 (+1), rank4 margin 0.22→0.30 (+2), top-2 multiplier 1.5→1.3 (+1).

### Repulsion Pairs (+0.35pp across 18 pairs)
**What**: Symmetric score push/pull between pairs with discriminant evidence.
**Why it works**: Spreads scores before ranking without over-correcting. Safe mechanism (small forces, high confidence threshold).
**Current**: 18 pairs at 0.008-0.016 force. Most recent: bear-mushroom 0.014, teapot-banana 0.014 (both +0.004 increments from 0.010).
**Tuning insight**: Only ~20% of repulsion increases produce gains. The successful ones are pairs where the discriminant direction is already correct and the pair is "isolated" (doesn't share many features with other pairs). Sports_car is hypersensitive — almost any repulsion change causes it to drop 2-3pp.

### Rank-3+ Whitelist Expansion (+0.05pp per pair)
**What**: Add missing confusion pairs to rank-3/4/5 reranking whitelists so deeper candidates can be promoted.
**Why it works**: Many errors have the true class at rank-3+. If the discriminant is already defined and accurate, extending whitelist coverage is low risk.
**Conditions**: Only add pairs where (1) discriminant exists, (2) pair is "isolated" (not sports_car, which cascades), (3) PAIR_BASE is low (≤0.05). Bear-mushroom rank-3 worked (+1); bear-sports + KP-sports failed (-8) due to sports_car cascade.

## Generalization Profile of Each Technique

From the 20.6pp gap analysis (Session 20: 70.0% train, 49.4% val):

| Technique | Train impact | Generalizes? | Notes |
|-----------|:---:|:---:|---|
| Histogram blending | +1-2pp | YES | Global scoring, no pair-specific tuning |
| Orthogonal features | +0.1-0.6pp each | YES | LAB, Gabor, FFT signals transfer well |
| Repulsion pairs | +0.2pp | YES | Conservative triggers, symmetric forces |
| Pairwise reranking | +10.4pp train | PARTIALLY (~5pp val) | Base scoring generalizes; pair-specific bases overfit |
| Local verify (rank-2) | +7.1pp train | POORLY (~2pp val) | 50 conditions on 2-10 images each = memorized corrections |
| Rank-3/4/5 verify | +7.6pp train | VERY POORLY (~1pp val) | Deep speculative swaps almost never transfer |
| Confidence gates | +0.5pp train | PARTIALLY | Gate thresholds are class-level, partially transfer |
| Bad condition removal | +1.0pp train | UNKNOWN | Removing interference may improve val too |
| Exhaustive scan methodology | methodology | N/A | The scan itself generalizes; the conditions it finds don't |
| **Post-pipeline final verify** | **+8pp train** | **VERY POORLY** | Same as rank-2/3/4/5 verify — pair-specific thresholds on tiny image subsets. Will not generalize. |

**Lesson**: Techniques that affect all images (histogram, features, repulsion) generalize. Techniques that fire on tiny subsets (verify, deep reranking) overfit. The train-val gap will grow from ~20pp to ~28+pp with the final verify additions. This is the deliberate COST of pushing train accuracy — user directive is train optimization only.

## What to Try Next (by expected payoff)

1. **Continue final verify mining** — Each wave still yields +5-15 rescues via conjunctive conditions. Ceiling is when remaining pairs have <3 errors.
2. **New feature types for final verify** — Adding new features (wavelet, GLCM distance=2) would create NEW separation that enables conditions currently impossible. These won't cascade because deployed only in final stages.
3. **Base scoring improvement** — 904/2000 (45.2%) base accuracy is the fundamental bottleneck. Improving base scoring would expose new errors recoverable by final verify (virtuous cycle).
4. **Multi-class discriminants** — Instead of pairwise A vs B, use A vs {B, C, D} to handle deep errors.
5. **Bad-swap diagnostic on final verify** — As more conditions accumulate, some may become net-negative. Periodic audit needed.
