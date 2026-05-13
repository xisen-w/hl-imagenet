# Phase 2 Improvement Session — 2026-05-13

## Baseline: iter12h — 47.2% top-1, 72.9% top-3

Top confusions:
- orange → banana: 60
- sports_car → school_bus: 38
- teapot → king_penguin: 33
- teapot → banana: 32
- brown_bear → golden_retriever: 32
- golden_retriever → banana: 30

## Diagnostic: Feature Distribution Analysis (40 samples/class, val set)

Key finding: **hist_* prototype scores are computed but NEVER used in signatures**.
They show strong discrimination:
- sports_car vs school_bus: hist_banana d=1.90, blob_lap_var d=1.62
- orange vs banana: hue_red d=1.10, warm_hue_mean d=0.91
- teapot vs KP: hue_red d=1.41, warm_hue_mean d=1.33
- teapot vs banana: yellow d=1.31, color_std d=1.03

## Iter 14a: Add histogram prototype scores to signatures

Hypothesis: hist_<class> scores are a strong prior — they encode the full
2D hue-sat distribution, not just individual features. Adding the class's
own hist score and suppressing confuser hist should help.

Plan: Add hist_<own_class> as positive signal (weight ~0.10-0.15) to each
signature. For top confusion pairs, add hist_<own> - hist_<confuser> as
a guard or positive.

### Result iter14a (raw hist in all signatures): 47.4% (+0.2pp)
- Marginal. Banana +3pp, GR +3pp, but mushroom -3pp, orange -2pp, KP -2pp.
- Problem: hist_banana high for both banana and orange. Raw hist too correlated.
- **Reverted to iter12h baseline.**

## Iter 14b: Histogram ratio discriminants in pairwise reranking

Added differential features (hist_X_minus_Y) to _stats():
- hist_orange_minus_banana (d=1.29), hist_sports_minus_bus (d=2.24),
  hist_bear_minus_gr (d=0.41), hist_mushroom_minus_bear (d=0.70),
  hist_gr_minus_banana (d=1.54), hist_teapot_minus_kp (d=1.28),
  hist_teapot_minus_banana (d=1.24)

Added these as 5th signal in existing pairwise discriminants.
Added NEW discriminants: teapot-KP, teapot-banana.
Added to rank3 whitelist: teapot-KP, teapot-banana, banana-orange.

### Result: 48.2% (+1.0pp) — new best!
- orange 43.5→47.5 (+4pp), KP 41→47 (+6pp), GR 37→38.5
- BUT teapot 32.5→31 (-1.5pp), banana 53.5→50.5 (-3pp)
- orange→banana 60→49 (great!), GR→banana 30→23 (great!)
- teapot→KP 33→37 (WORSE) — discriminant may fire wrong direction

### iter14c: Removed teapot-KP disc → 47.7%
- KP fell back to 41%. The teapot-KP disc was net positive (+6pp KP, -1.5pp teapot).
- Restored teapot-KP disc.

### iter14d-e: School bus guards → 47.65%, 48.0%
- School bus is the biggest sink class (mean score 0.466 across ALL images).
- Guards suppressed bus too much (71.5→49%). Even light blue_purple guard dropped it to 56.5%.
- **Conclusion:** Guards don't work for school_bus — its high score is structural, not fixable by simple guards.

### iter14f-h: Score normalization experiments → 43.6%, 46.9%, 48.0%
- Z-score: 43.6% (broke everything — signatures were tuned for raw scores)
- Mean subtraction: 46.9% (KP 56.5%! mushroom 49%! but teapot 25%, school_bus 51.5%)
- Partial norm (alpha=0.5): 48.0% (still hurts teapot and school_bus)
- **Lesson:** Full normalization is too disruptive to the reranking layer.

### iter14i: Better orange-banana disc → 48.1%
- Added warm_hue_mean + symmetry. Orange 51.5% (+8pp!) but banana 46% (-7.5pp).
- Net zero. Orange recovery comes at banana's expense — zero-sum at 64×64.

### Teapot deep analysis:
- 37 misclassified as KP: dark/metallic teapots (warm=0.06, sat=0.14)
- 31 misclassified as banana: copper/brass teapots (yellow=0.50, warm=0.72)
- 28/37 KP-confused teapots have teapot at rank ≤ 3 → reranking could help
- 13/31 banana-confused teapots have teapot at rank ≤ 3 → many truly lost
- **Root cause:** Teapot is shape-defined; color features fundamentally can't reach it.

### iter14l: New mushroom-banana + GR-teapot discs → 47.2%
- Both hurt their target classes. Reverted.

### iter14n-o: Margin adjustments → 48.1-48.2%
- Wider rank-3 (0.20): 48.1%, slight regression
- Wider rank-2 (0.30): 48.2%, no change
- Current 0.25/0.15 thresholds are optimal.

## Final State: 48.2% top-1, 72.9% top-3 (up from 47.2%)

Changes from iter12h baseline:
1. Histogram differential features added to _stats() (7 new features: hist_X_minus_Y)
2. Hist ratios added as 5th signal to 5 existing pairwise discriminants
   (banana-orange, GR-banana, sports_car-school_bus, bear-GR, mushroom-bear)
3. New discriminant: teapot-king_penguin (hue_red, warm, sat_bl, hist_teapot_minus_kp)
4. New discriminant: teapot-banana (yellow, edge, top_uniformity, hist_teapot_minus_banana)
5. Rank-3 whitelist expanded: +teapot-KP, +banana-orange

Per-class changes vs baseline:
- orange: 43.5→47.5 (+4pp), KP: 41→47 (+6pp), sports_car: 48.5→50 (+1.5pp)
- banana: 53.5→51 (-2.5pp), teapot: 32.5→30.5 (-2pp)
- Others: ~flat

Key lessons:
- Histogram prototype RATIOS (d=1.2-2.2) are far more discriminative than raw scores
- Score normalization is disruptive — the reranking layer is tuned for raw scores
- School bus sink (mean=0.466) isn't fixable by guards — would need architectural change
- Teapot is fundamentally limited by shape-vs-color at 64×64
- Every discriminant that helps one class in a pair hurts the other — zero-sum dynamics


## Session 2: 48.2% → 50.1% (2026-05-13)

### Iter 15: Gap-aware confidence gating → 49.0% (+0.8pp)

Analysis: 112/1036 errors were CAUSED by reranking (true class was rank-1, got swapped down).
Root cause: discriminants with ~70% accuracy were swapping on marginal evidence.

Fix: Require disc_margin > base_threshold + score_gap * gap_scale to swap.
- Rank-2: base=0.05, gap_scale=1.5
- Rank-3: base=0.0, gap_scale=2.0

Result: 49.0% (+0.8pp). Bear +1.5pp, GR +1.5pp, mushroom +2.5pp. Orange -3pp (fewer rescues).

### Iter 15b: Per-pair discriminant thresholds → 49.2% (+0.2pp)

Principle: accurate discriminants get lower thresholds, inaccurate ones higher.
- 84% acc (school_bus-sports_car): base=-0.10
- 58% acc (banana-teapot): base=0.30
- Mapped all 17 discriminant pairs to accuracy-based thresholds.

Train validation: +0.2pp on train (principled version), val-optimized version was neutral on train.

### Iter 15c: GR color_std guard → 49.5% (+0.3pp)

FP analysis: GR has 1022 non-GR images scoring >0.35. GR TPs have low color_std (0.16)
while FPs have high color_std (0.25). Added `_sigmoid(color_std, 0.25, -4)` guard.
GR dropped 42→39.5%, but mushroom +2pp, school_bus +1.5pp, bear +0.5pp, orange +1.5pp.

### Iter 15d-f: Bus guards → reverted
Tried warm guards on school_bus signature. All hurt bus too much (71.5→59-60%).
Bus signature fundamentally needs all its positive signals — no room for guards.

### Iter 15g: New discriminants (GR-bus, banana-mushroom, GR-teapot) → reverted
GR-bus 84% acc, banana-mushroom 59%, GR-teapot 68%. Net -0.5pp.
Only GR-bus was accurate enough but was net neutral. Others removed.

### Iter 15i: Orange signature weight redistribution → reverted
Boosted hue_red weight, added color_std. Net -0.1pp.

### Iter 15j: Histogram score blending → 50.1% (+0.6pp) ← BREAKTHROUGH

Key insight: linear blend of signature scores with hist prototype scores before ranking.
`blended = signature * 0.88 + hist_score * 0.12`

Validated on train: +1pp improvement (46.5→47.5%). Val-train gap = 2.6pp (consistent with
overall val > train pattern in this dataset).

School_bus 74→78.5% (+4.5pp), sports_car 50.5→56.5% (+6pp), orange 48→50.5% (+2.5pp).
Bear 43→40% (-3pp), teapot 32→30% (-2pp). The hist blend helps distinctive-color classes
most and slightly hurts texture/shape-defined ones.

## Final State: 50.1% top-1, 74.2% top-3

Changes from iter14 (48.2%) baseline:
1. Gap-aware confidence gating (base=0.05/0.0, gap_scale=1.5/2.0)
2. Per-pair discriminant base thresholds (12 overrides)
3. GR color_std guard at 0.25/-4
4. Histogram score blending w=0.88 before ranking

Per-class: banana 51%, bear 40%, GR 40%, jelly 65.5%, KP 48%, mushroom 41.5%,
orange 50.5%, bus 78.5%, sports_car 56.5%, teapot 30%

