# Hard Confusions

These confusion pairs resist all techniques we've tried. Understanding WHY they're hard prevents wasted iterations.

## Top Confusions at 70.0% (Session 20 end)

| Confusion | Count | Status |
|-----------|:---:|---|
| teapot → banana | 20 | Heavily mined. Residual is copper/brass teapots. |
| sports_car → school_bus | 20 | Heavily mined. Residual is yellow/orange sports cars. |
| mushroom → brown_bear | 17 | Partially mined. Forest-floor brown mushrooms. |
| orange → banana | 16 | Mostly irreducible at 64x64. |
| brown_bear → golden_retriever | 16 | Partially mined. Warm-toned bears in grass. |
| teapot → golden_retriever | 15 | Warm/round teapots. Teapot base too weak. |
| brown_bear → golden_retriever | 14 | (bidirectional with above) |
| golden_retriever → mushroom | 13 | Warm-toned dogs on brown backgrounds. |

## Tier 1: Genuinely Ambiguous (probably irreducible at 64x64)

### banana ↔ orange (16 + ~12 = ~28 mutual errors, down from 60)
**Why hard**: Both are warm-colored, smooth-surfaced, roughly oval objects on neutral backgrounds. At 64x64, the only reliable difference is hue — orange is redder, banana is yellower. But copper-colored bananas and pale oranges overlap completely.
**What's been mined**: Extensive verify conditions across all ranks. The 28 remaining are genuinely feature-indistinguishable at this resolution.
**Verdict**: Irreducible. Would need shape features (curvature, pointed ends vs round) or higher resolution.

### brown_bear ↔ mushroom (17 remaining, down from 42)
**Why hard**: Both are textured, warm-toned, on natural/forest backgrounds.
**What worked**: Exhaustive verify scan found many conditions. Rank-3/4 verify recovered additional cases.
**Residual**: The 17 remaining have smooth brown mushroom caps that produce nearly identical feature vectors to bears in forest settings.
**Verdict**: Near ceiling for current features.

### brown_bear ↔ golden_retriever (16 + 14 = 30 mutual errors, down from 47)
**Why hard**: Both are warm-toned, furry animals. Face structure differs but is invisible at 64x64.
**What worked**: Multiple verify conditions, GR-bear bidirectional verify, channel correlation features.
**Residual**: Golden-brown bears on grass backgrounds vs golden retrievers in parks. Feature vectors indistinguishable.
**Verdict**: Near ceiling. Would need spatial layout features (animal body proportions).

## Tier 2: Structurally Hard (heavily mined, residuals tough)

### sports_car ↔ school_bus (20 remaining, down from 40)
**Why hard**: Both are vehicles with strong edges. Bus has yellow color but some sports cars are yellow/orange.
**What worked**: Extensive verify conditions (dct_high + grad_mean, hue_orange thresholds), rank-3/4 verify for deeper cases.
**Residual**: 20 errors are genuinely ambiguous vehicles — yellow/orange sports cars, unusual bus angles.
**Sports_car cascade sensitivity**: Sports_car shares features with MANY classes. Almost any repulsion/whitelist change causes -2 to -4pp sports_car regression. This makes sports-bus one of the hardest pairs to optimize without side effects.

### teapot → banana (20 remaining, down from 27)
**Why hard**: Copper/brass teapots with banana-like coloring. Most have teapot at rank 3-5 or beyond — pairwise reranking at rank-2 cannot reach them.
**What worked**: Rank-3/4/5 verify invention (Session 19) made previously unreachable errors addressable. cm_center_b, orient_entropy conditions.
**Root cause persists**: Teapot base score is 14.5% (29/200). The 20 remaining have teapot so far down the ranking that even rank-5 verify can't reach them.
**Verdict**: Requires base scoring improvement — which is catastrophic to change.

### teapot → king_penguin (reduced significantly from 42)
**Why hard**: Dark/metallic teapots are feature-indistinguishable from penguins at 64x64.
**What worked**: Many verify conditions deployed via exhaustive scan. Rank-3/4 verify. mid_wider, autocorr_h, horiz_dominance features.
**Best remaining features**: cm_b_skew (d'=1.09), fft_hv_ratio (d'=1.01) — but deploying these in signatures causes -20 cascade.
**Verdict**: Individual condition mining exhausted. Only a structural approach (spatial features) could help further.

## Tier 3: Significantly Reduced (was addressable, now mostly mined)

### GR → mushroom (13 remaining)
**Why hard**: Golden retrievers on brown/natural backgrounds match mushroom's color/texture profile.
**What worked**: Multiple verify conditions through exhaustive scan.
**Residual**: Dogs lying in brown leaf litter — feature-indistinguishable from forest mushrooms.

### teapot → golden_retriever (15 remaining)
**Why hard**: Warm/round teapots with golden coloring. Teapot's base score is too weak to compete.
**Root issue**: Same as teapot-banana — teapot base scoring at 14.5% means most errors have teapot far down rankings.

## Generalization of Confusions (Train → Val)

At 70.0% train / 49.4% val (20.6pp gap), overfitting is severe:

**Pattern**: The more verify conditions we add for a pair on train, the WORSE the gap becomes on val. Each condition fires on 2-10 train images with hard thresholds — these are essentially memorized corrections that don't transfer.

**Stable pairs** (same error rate across splits): sports_car ↔ school_bus, mushroom → brown_bear, banana → orange. These are genuinely hard, not artifacts of overfitting.

**Insight at 70.0%**: The 20.6pp gap means roughly half of the 496 post-processing rescues (~248) don't transfer to val. The base scoring (45.2%) likely generalizes much better (~42-44% on val), meaning it's the verify/reranking layers contributing most of the gap.

## Error Reachability Analysis (at 70.0%)

| True at rank | Errors | Recoverable by |
|:---:|:---:|---|
| 2 | 126 | Local verify — already heavily mined |
| 3 | 95 | Rank-3 verify — already heavily mined |
| 4 | 82 | Rank-4 verify — already heavily mined |
| 5 | 78 | Rank-5 verify — partially mined |
| 6+ | 219 | **NOTHING** — requires base scoring improvement |

The 219 errors at rank 6+ represent a HARD CEILING for the verify/reranking approach. These images have the true class so far from rank 1 that no conditional swap can reach them.

**Per-class base scoring**: teapot 14.5%, GR 26.0%, bear 30.0%, sports 33.5%, mushroom 44.5%, banana 51.0%, orange 52.0%, KP 58.5%, jelly 67.5%, bus 72.0%.

**Implication**: Teapot and GR contribute disproportionately to the rank-6+ pool because their base scores are so low. No amount of verify mining can fix images where the base scorer doesn't even rank the true class in the top 5.
