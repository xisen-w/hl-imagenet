# Hard Confusions

These confusion pairs resist all techniques we've tried. Understanding WHY they're hard prevents wasted iterations.

## Tier 1: Genuinely Ambiguous (probably irreducible at 64x64)

### banana ↔ orange (34 + 26 = 60 mutual errors)
**Why hard**: Both are warm-colored, smooth-surfaced, roughly oval objects on neutral backgrounds. At 64x64, the only reliable difference is hue — orange is redder, banana is yellower. But copper-colored bananas and pale oranges overlap completely.
**Best discriminant accuracy on hard cases**: 15.8% (worse than random). The hard cases genuinely look like either class.
**What we've tried**: warm_hue_mean, sat discriminant, proto distance verify, warm_sat_std, rb_corr, yellow_narrow_ratio. None achieve cross-class d' > 0.5 on the error population.
**Verdict**: Irreducible with current resolution and color-based features. Would need shape features (curvature, pointed ends vs round) or higher resolution.

### brown_bear ↔ mushroom (24 + 18 = 42 mutual errors)
**Why hard**: Both are textured, warm-toned, on natural/forest backgrounds. Brown bears in forest settings have brown coloring and texture similar to mushrooms. 
**Best cross-class d'**: 0.55 (center_bright_ratio), 0.24 (hue_entropy on error cases)
**What we've tried**: hu1/hu2, GLCM, green, color_std, cm_a_std, warm_vert_top, dct_high. GR-bear verify works partially (sat < 0.28 AND dct_high < 0.20: +5 net) but bear-mushroom verify is at ceiling.
**Verdict**: Marginally separable. Best approach is high-precision verify conditions, one at a time.

### brown_bear ↔ golden_retriever (26 + 21 = 47 mutual errors)
**Why hard**: Both are warm-toned, furry animals. Many GR images have natural backgrounds like bears. Face structure differs but is invisible at 64x64.
**What we've tried**: warm_sat_cv, cm_center_b (d=0.91), warm_hue_median. The verify condition (sat < 0.28 AND dct_high < 0.20 → favor GR) catches some but the core overlap is resistant.
**Verdict**: Partially reducible. GR has slightly bluer cast (higher cm_center_b) and bears have coarser texture. +3-5 more rescues may be possible with new features.

## Tier 2: Structurally Hard (addressable with better features)

### sports_car ↔ school_bus (25 + 15 = 40 mutual errors)
**Why hard**: Both are vehicles with strong edges, directional structure, and often fill the frame. Bus has yellow color as primary differentiator but some sports cars are yellow/orange.
**Best discriminant**: hist_sports_minus_bus (d=2.24 at class level). Discriminant accuracy: 84%.
**Current status**: Sports-bus verify conditions (dct_high + grad_mean, dct_high + hue_orange) catch +8 net. The remaining 25 errors are genuinely ambiguous vehicle images.
**Potential**: Vertical regularity (vert_regularity) or window-pattern features could help distinguish bus's repeating structure.

### teapot → banana (27 errors)
**Why hard**: Copper/brass teapots have yellow/warm coloring identical to bananas. Only 1 of 29 errors has teapot as #2 — most have teapot at #3-#5 or unranked. This means pairwise reranking fundamentally cannot fix most of these.
**Root cause**: Teapot's base signature is too weak. It scores low because teapot features (shape-related) don't work well at 64x64.
**Potential**: Need to boost teapot's base score for warm/copper teapots specifically, without affecting other classes. Extremely difficult — see edit_risk_hierarchy.md on signature changes.

### teapot → king_penguin (42 errors on train)
**Why hard**: Dark/metallic teapots (warm=0.06, sat=0.14) are feature-indistinguishable from penguins. Both are low-saturation, centered objects on dark backgrounds.
**Best discriminant features**: hue_red (d=1.41), warm_hue_mean (d=1.33), color_purity, mid_wider. The teapot-KP discriminant + local verify catch some but the cold metallic population is resistant.
**Potential**: autocorr_h (horizontal autocorrelation) and horiz_dominance partially separate (teapots have horizontal structure). Limited by resolution.

## Tier 3: Addressable (just need the right feature)

### GR → banana (23 errors)
**Why hard**: GR images with warm backgrounds (dog on warm-toned floor/furniture) match banana's color profile.
**What works**: cm_center_b (d=1.50), rb_corr. The GR-banana discriminant + verify conditions have reduced this from 28 to 23.
**Remaining**: The 23 remaining are genuinely warm-toned GR images. Need texture-based separation (fur texture vs smooth fruit).

### mushroom → banana (30 errors)
**Why hard**: Warm-colored mushrooms on forest floor. Banana's smooth_yellow and warm features fire on tan/brown mushrooms.
**What works**: hu1 (d=1.16), hu2 (d=1.09), edge, mushroom-banana verify (edge > 0.27 AND hu1 > 2.65).
**Remaining**: Most remaining errors have mushrooms with smooth caps that genuinely look banana-like in feature space.

## Generalization of Confusions (Train → Val → Test)

Key confusion pairs that get significantly worse on unseen data:

| Confusion | Train | Val | Test | Verdict |
|-----------|:---:|:---:|:---:|---|
| brown_bear → GR | 22 | 36 | 21 | VAL +14 — discriminant overfit |
| orange → banana | 21 | 35 | 13 | VAL +14 — discriminant overfit |
| GR → mushroom | 19 | 31 | 11 | VAL +12 |
| brown_bear → mushroom | 22 | 29 | 13 | VAL +7 |
| mushroom → GR | 14 | 23 | 12 | VAL +9 |
| sports_car → KP | 9 | 17 | 4 | VAL +8 |

**Pattern**: Pairs where we added aggressive reranking/verify conditions on train get worse on val. The discriminant thresholds are tuned too tightly to training feature distributions.

**Stable pairs** (same error rate across splits): sports_car ↔ school_bus, mushroom → brown_bear, banana → orange. These are genuinely hard, not artifacts of overfitting.

## Error Reachability Analysis

Per class, percentage of errors where true class is beyond rank 3 (unreachable by standard reranking):

| Class | % at rank 4+ | Count |
|-------|:---:|:---:|
| teapot | 68% | 80 |
| GR | 62% | 64 |
| bear | 58% | 52 |
| banana | 55% | 54 |
| mushroom | 60% | 59 |
| orange | 45% | 33 |
| sports_car | 50% | 40 |
| KP | 42% | 35 |
| jelly | 38% | 23 |
| bus | 35% | 17 |

**Implication**: For teapot (68% unreachable), no amount of reranking can fix most errors. The base scoring must improve. For bus (35% unreachable), reranking is still productive.
