# Phase 2 Improvement Sessions — Chronological Log

> **Structured knowledge**: See `docs/phase2/understanding/` for distilled, topic-organized knowledge extracted from these sessions. This file is the raw chronological record.

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



## Session 3: Protocol Change — Optimize on Train Only (2026-05-13)

### Protocol
User clarified: do NOT look at val to guide decisions — that's also overfitting on validation.
From now on: all analysis, confusion matrices, and feature distributions use train only.
Val eval runs as a side product for reporting.

### Train Baseline: 47.5% top-1 (949/2000)
Val baseline: 50.1% (val > train by 2.6pp — consistent historical pattern).

Train per-class: banana 56%, bear 42.5%, GR 35.5%, jelly 65%, KP 43.5%, mushroom 42%, 
  orange 42%, bus 78%, sports_car 50.5%, teapot 20%

Top train confusions:
- orange → banana: 53
- sports_car → school_bus: 42
- teapot → king_penguin: 42
- mushroom → banana: 38
- teapot → banana: 34
- golden_retriever → banana: 28
- brown_bear → school_bus: 28

### Analysis — Biggest Bottlenecks (Train)
1. **Teapot at 20%** — worst class by far. 42 → KP, 34 → banana, 24 → GR. Shape-defined class.
2. **GR at 35.5%** — 28 → banana, 21 → bear, 19 → teapot, 16 → bus. Warm-blob overlap.
3. **Banana sink** — receives 186 FPs (38 mushroom, 34 teapot, 28 GR, 53 orange, etc.)
4. **Bus sink** — receives 166 FPs (42 sports_car, 28 bear, 23 banana, etc.)

### Iter 16a: 7 new discriminant pairs → 48.25% (+0.75pp from 47.5% baseline)

Added discriminants for the top uncovered confusion pairs on train:
- banana-mushroom (85% acc): warm_val_mean, smooth_warm, val, hist diff
- GR-teapot (74.5% acc): edge, bot_edge, horiz_dominance, hist diff
- bear-KP (78% acc): textured_decentered, edge, warm_tl, hist diff
- jellyfish-KP (87.5% acc): sat, color_std, sat_br, hist diff
- orange-teapot (82% acc): sat, color_std, sat_bl, hist diff
- bear-teapot (82% acc): edge, textured_decentered, top_edge, hist diff
- GR-KP (80% acc): warm, blob_coverage, hue_red, hist diff

Added 7 new histogram differential features: hist_banana_minus_mushroom, hist_gr_minus_teapot,
hist_bear_minus_kp, hist_jelly_minus_kp, hist_orange_minus_teapot, hist_bear_minus_teapot,
hist_gr_minus_kp.

Result: 48.25% (+0.75pp). KP +7pp, mushroom +2.5pp, BUT GR -2.5pp, bear -4.5pp.
The bear-KP discriminant was pushing bear images TO KP incorrectly.

### Iter 16b-c: Tuned per-pair base thresholds → 48.5% (+1pp)

Raised base thresholds for less accurate discriminants:
- bear-KP: 0.05 → 0.25 (78% acc, was causing bear regression)
- GR-teapot: 0.05 → 0.15 (74.5% acc)
- bear-teapot: 0.0 → 0.10
- GR-KP: 0.05 → 0.10

Result: 48.5% — bear recovered to 40%, KP still at 50%.
Removing bear-KP from rank3 whitelist dropped KP to 47.5% — not worth it.
Restored bear-KP to rank3 whitelist with high base threshold.

### Iter 16f-h: Mean-centered histogram blending → 48.75% (+1.25pp)

Key insight: raw histogram scores have class-level bias. school_bus averages 1.53 
across all images, jellyfish only 0.66. Blending raw scores amplifies sinks.

Solution: `blended = sig * 0.88 + (hist - class_mean * alpha) * 0.12`

Tested alpha values on train:
- alpha=1.0 (full): 48.6% — jelly +4.5pp, KP +1.5pp, bear +2pp, BUT bus -4pp, sports -3pp
- alpha=0.5: 48.6% — bus recovered to 75.5% but still down
- alpha=0.3: 48.75% — best balance. jelly +2.5pp, bear +1pp, bus -1.5pp, sports -1.5pp
- alpha=0.25: 48.75% — same total, bus slightly better

Settled on alpha=0.3 as optimal.

### Current Train State: 48.75% top-1 (975/2000)

Per-class (train): banana 56%, bear 41%, GR 37.5%, jelly 66%, KP 50.5%, mushroom 44.5%, 
  orange 45%, bus 76.5%, sports 49%, teapot 21.5%

Changes from Session 2 end (47.5% train):
1. 7 new discriminant pairs (24 total)
2. 7 new histogram differential features (14 total)
3. Per-pair base threshold calibration for new pairs
4. Mean-centered histogram blending (alpha=0.3)

### Status Quo Analysis

**What's working:**
- Pairwise reranking (24 pairs) is the backbone, responsible for ~4pp over base scoring
- Histogram blending adds another ~0.5-1pp
- Gap-aware gating prevents ~50 reranking regressions per eval

**What's stuck:**
- Teapot at 21% — shape-defined class, fundamentally limited by color/texture features
- GR at 37.5% — warm-blob overlap with banana, mushroom, bear, teapot
- Sink classes (banana 186 FPs, bus 166 FPs) — structural to additive scoring

**Architecture ceiling:**
- ~55% of errors have true class beyond rank 3 → unreachable by reranking
- 24 discriminant pairs cover top confusions; each new one gives <0.3pp
- Parametric tuning (thresholds, weights) gives <0.1pp per iteration now

**Next breakthrough needed:**
- New representation type (frequency domain? multi-scale? spatial relations?)
- Different scoring architecture (multiplicative? attention-weighted?)
- Explicit shape features (Hough transforms for handles/spouts?)


## Session 4: Breaking the Zero-Sum — Representation Expansion (2026-05-14)

### Starting point: 50.5% train (1010/2000)
(Previous 52.4% was lost — uncommitted code got reverted.)

### Key insight: Zero-sum dynamics in shared feature space

The system has ~140 features in `_stats()`. All 10 class signatures and all discriminants draw 
from this same pool. Boosting one class on any existing feature necessarily creates false positives 
for another. Need **orthogonal** feature axes — dimensions where the target pair separates but 
other classes don't interfere.

### New feature types added to `_stats()`:

**1. DCT frequency band energy** (orthogonal to color/edge features)
- `dct_low`, `dct_mid`, `dct_high`: energy in low/mid/high frequency bands of DCT
- `dct_mid_over_low`: ratio, captures texture complexity
- Key separations: mushroom vs banana (dct_high d=+0.91), GR vs bear (dct_low d=+0.62),
  sports_car vs school_bus (dct_high d=+0.72)

**2. Gabor filter bank** (oriented texture at specific frequencies)
- `gabor_0_04_var`: 0° fine texture variance (school_bus > sports_car, d=0.98)
- `gabor_45_04_var`: 45° fine texture variance (bear > GR, d=0.91)
- `gabor_90_01_mean`: 90° coarse texture mean (banana > mushroom, d=0.96)
- `gabor_dominant_orient`: which orientation has most energy (teapot > KP, d=0.88)

**3. Shape statistics** (for teapot specifically)
- `mid_wider`: is the edge-spread widest in the middle third? (binary)
  - Teapot = 0.78, KP = 0.39 → d=1.17 for cold teapots vs real KP
- `mid_width_ratio`: quantitative version of mid-wider
- `autocorr_x_warm_bl`, `horiz_x_warm_bl`: conjunctive products

**4. Vertical regularity** (FFT of vertical edge profile)
- `vert_regularity`: how periodic are vertical edges (school_bus low, teapot/jellyfish high)

### Deployment results (incremental):

| Change | Train acc | Delta | Key movements |
|--------|-----------|-------|---------------|
| Baseline (50.5%) | 50.50% | — | — |
| +DCT in 4 discriminants | 50.75% | +0.25pp | mushroom+1, sports+0.5, bus+0.5, bear+0.5 |
| +mid_wider in teapot-KP | 50.90% | +0.15pp | teapot +4.5pp (24.5→29), KP -2.5pp |
| +Gabor in teapot-KP, bear-GR | 51.30% | +0.40pp | teapot +3pp (29→32), sports +1.5pp |

**Failed experiments:**
- Conjunctive features (autocorr_x_warm_bl) in teapot-KP disc: threshold calibration wrong, hurt teapot
- Adding mid_wider to teapot **signature**: zero-sum (jellyfish/sports_car also high mid_wider)
- Gabor in mushroom-banana disc: mushroom→banana errors went UP (30→36)
- Gabor in sports-bus disc: bus regressed (76→74%), not worth the sports gain
- Bear-mushroom Gabor: bear +7pp but mushroom -10pp, strongly zero-sum
- sat_tr + hue_orange in banana-orange: orange regressed more than banana gained

### Current best: 51.3% train (1026/2000)

Per-class: banana 50%, bear 45%, GR 38.5%, jelly 66%, KP 49.5%, mushroom 46.5%, 
  orange 58%, bus 76%, sports 51.5%, teapot 32%

Top confusions:
- banana → orange: 36
- sports_car → school_bus: 35
- mushroom → banana: 30
- teapot → banana: 29
- orange → banana: 26
- brown_bear → king_penguin: 23

### Key lesson: Orthogonal features produce non-zero-sum gains

DCT, Gabor, and shape features each added points without stealing from other classes 
because they measure fundamentally different image properties. The gains are small individually 
(+0.15 to +0.40pp per deployment) but cumulative and stable. The old approach of tweaking 
sigmoid thresholds on existing features was near-zero-sum; the new approach of expanding 
the representation space along orthogonal axes is the path forward.

### Iter: warm_hue_median in GR discriminants → 51.4%
Added `warm_hue_median` (median hue in warm pixels) and `warm_sat_cv` (saturation CV in warm region).
GR warm pixels peak at hue~16 (red-orange), banana at ~18 (yellow-orange), KP at ~20.5.
Added to GR-banana and GR-KP discriminants. GR 38.5→39.5%. No regressions.

### Iter: Score calibration → 51.6%
Per-class additive offset: bus=-0.02, jelly=+0.02, KP=+0.01, mushroom=+0.01.
Bus was the biggest sink (mean score 0.539 vs jellyfish 0.319).
Jelly +1.5%, mushroom +1%, KP +1.5%, bus -3% (acceptable trade). Net +4 correct.

### Iter: Potential field repulsion v1-v2 → 51.5% (regression)
Concept: when two classes both score high, penalize the one with weaker discriminant evidence.
Failed because it double-counted with pairwise reranking — both use the same discriminants.

### Iter: Potential field v3 (balanced push/pull) → 51.65%
Changed to symmetric: winner gets +force/2, loser gets -force/2. Only activates when
disc_gap > 1.0 (very high confidence). This spreads scores before ranking without
over-correcting. Sports_car +1%, mushroom +0.5%.

### Current best: 51.65% train (1033/2000)


## Session 5: Reranking Analysis & Rank-4 Extension (2026-05-15)

### Starting point: 51.7% train (1034/2000)

### Deep reranking analysis
Instrumented the pipeline to measure pre-rerank vs post-rerank accuracy:
- Pre-rerank: 44.5% (889/2000)
- Post-rerank: 51.7% (1034/2000)  
- Rerank adds +7.2pp overall

Per-class rerank impact:
- Biggest winners: orange +26pp (32→58%), sports_car +11.5pp, bear +10pp, teapot +10pp
- Biggest losers: banana -11.5pp (62.5→51%), jellyfish -1.5pp, KP -3.5pp

Error analysis by pre-rerank rank of true class:
- 112 reranking-caused errors (true was rank 1, got swapped down)
- 217 at rank 2, 160 at rank 3 (reachable)
- 132 at rank 4 (newly targetable)
- 345 at rank 5+ (unreachable by reranking)

Top reranking-caused error pairs:
- banana→orange: 18 (banana-orange disc swaps correct banana to orange)
- KP→sports_car: 9
- mushroom→bear: 7
- GR→bear: 6

### Failed: Raising base thresholds to reduce reranking errors → 51.6% (-0.1pp)
Tried banana-orange 0→0.05, 0→0.10. Orange loses more rescues than banana gains.
Every base threshold increase is zero-sum between the paired classes.

### Failed: GR-mushroom Gabor strengthening → 51.5% (-0.2pp)
Added gabor_45_04_var (d=0.83), green (d=0.70), hist_gr_minus_mushroom to the discriminant.
75.2% accuracy but hurt both classes. Reverted.

### Failed: Calibration v2 (principled alpha=0.2) → 51.4% (-0.3pp)
Penalized high-mean classes (bear, GR, teapot) and boosted low-mean (jelly, KP, orange).
Broke the reranking layer which was tuned for original score distribution.

### Failed: Bear-KP disc with DCT+Gabor → zero-sum
Bear +1pp, KP -1.5pp. Even with conservative base=0.25 threshold.

### Success: Rank-4 reranking → 51.8% (+0.1pp)
Extended pairwise reranking to check rank 4 vs rank 1.
- margin14 ≤ 0.15, gap_scale = 3.0 (strict)
- 11 whitelisted pairs (high-accuracy discriminants only)
- mushroom +1pp, teapot +1pp, bear +0.5pp
- orange -0.5pp, school_bus -0.5pp (minor)

### Current best: 51.8% train (1036/2000)

Key insight: The system is deeply in zero-sum territory for pairwise improvements. The only 
gains that stick are (1) structural changes like rank-4 extension, and (2) truly orthogonal 
features that don't participate in existing zero-sum dynamics.

### Loop Session: Failed experiments (2026-05-15)

**Hist-only vs Sig-only accuracy analysis** (key finding):
- school_bus: hist 75% >> sig 69%  
- orange: hist 49.5% >> sig 26.5%
- banana: hist 21% << sig 64%
- teapot: hist 2% << sig 25%

**Failed: Per-class adaptive histogram blending** → 49.3% (-2.5pp)
Different hist blend weights per class (0.03 to 0.22 based on hist accuracy).
Broke reranking calibration — the discriminant thresholds were tuned for 0.88/0.12 blend.
Even conservative version (0.05 to 0.16) only got 50.4%. Not worth the complexity.

**Failed: GR signature warm_hue_median** → 51.2% (-0.6pp)
Added warm_hue_median (GR lowest at 16.1) to GR signature. GR gained +0.5pp but 
8 other classes regressed because GR's score increased across all images.

**Failed: Discriminant vote as secondary signal** → 44.9-46.1%
Computed weighted vote from all 24 discriminants, added as post-rerank adjustment.
Massive regression — double-counts with reranking, amplifies disc errors.

**Failed: Histogram veto/tiebreaker** → net negative at all thresholds
Hist rank of predicted class is NOT a reliable correctness signal.

**Analysis: Error composition** 
- 112 reranking-caused errors (true was #1, got swapped down)
- 300/963 errors have true class at #2 (31.2%)  
- 477 errors at rank 5+ are unreachable by reranking
- Pipeline (pre-rerank) + disc vote oracle = 57.5% — 5.7pp above current
- Banana produces 271 FPs vs 200 TPs (1.35:1 ratio), biggest sink class

**Key lesson: All post-pipeline adjustments are net negative.** The pipeline (sig→blend→
calibrate→field→sort→rerank) is already well-optimized. Adding layers on top double-counts 
existing signals. The remaining gains must come from (1) new orthogonal features in the 
base signatures, or (2) structural changes that open new scoring pathways.

### Success: FFT h/v ratio in KP discriminants → 51.9% (+0.1pp)
New feature: `fft_hv_ratio` — ratio of horizontal to vertical FFT energy.
KP has highest ratio (1.075), bear lowest (0.913), d=0.93 for bear-KP.
Added to bear-KP discriminant: KP +0.5pp, no regressions.
Also added to GR-KP (neutral — GR and KP closer in this feature, d=0.55).

### Current verified best: 51.9% (1038/2000)

Per-class: banana 51%, bear 44.5%, GR 39.5%, jelly 67.5%, KP 51.5%, 
  mushroom 49%, orange 57.5%, bus 72%, sports 53%, teapot 33.5%

### Success: LAB color moments as orthogonal feature channel → 52.8% (+0.6pp)

**Key discovery**: LAB color space moments (cm_a_std, cm_b_std, cm_center_a, cm_center_b) 
provide genuinely orthogonal information to existing HSV-based features.

New features added to `_stats()`:
- `cm_a_std`: LAB 'a' channel std (green-red axis variation)  
- `cm_b_std`: LAB 'b' channel std (blue-yellow axis variation)
- `cm_center_a`: LAB 'a' mean in center 50%
- `cm_center_b`: LAB 'b' mean in center 50%

Deployed in discriminants:
1. banana-orange: cm_center_a (d=1.30 — orange has higher center_a)
2. GR-KP: cm_center_a (d=1.31) + cm_center_b (d=1.37)
3. teapot-banana: cm_center_b (d=-1.62 — banana has higher center_b)
4. bear-mushroom: cm_a_std (d=-0.93 — mushroom has higher a_std)
5. banana-GR: cm_b_std (d=1.50 — banana has higher b_std)
6. bear-GR: cm_center_b (d=-0.91 — GR has higher center_b)

Results: bear +2pp (44.5→46.5%), GR +1.5pp (40.5→42%), mushroom +2.5pp (49→51.5%),
KP +0.5pp (51.5→52%), banana +0.5pp (51→51.5%).

**Failed extensions**: Adding LAB to ALL discriminants (-0.8pp). The scale=30-40 sigmoids are 
too aggressive for pairs with moderate d-values. Only deploy where d > 0.8 and carefully tune 
the sigmoid center using class means.

### Current verified best: 52.8% (1056/2000)

Per-class: banana 51.5%, bear 46.5%, GR 42%, jelly 70.5%, KP 52%,
  mushroom 51%, orange 57.5%, bus 71.5%, sports 53%, teapot 32.5%


## Session 6: Hu Moments & GLCM Contrast (2026-05-15)

### Starting point: 53.1% train (1062/2000) — verified baseline with LAB + rank-5

### New orthogonal features: Hu moments and GLCM contrast

**Hu moments** (hu1, hu2): Edge shape descriptors from cv2.HuMoments. Orthogonal to 
edge density/magnitude — measure shape complexity, symmetry, compactness.
- hu1: mushroom(2.67), bear(2.68), bus(2.67) >> banana(2.55), jelly(2.49), orange(2.51)
- hu2: mushroom(7.95), bear(7.81) >> banana(6.73), jelly(6.05), sports(6.76)

**GLCM contrast**: Horizontal pixel adjacency texture. Orthogonal to LBP/Gabor.
- mushroom(0.020), bus(0.022), sports(0.019) >> jelly(0.006), orange(0.008), banana(0.011)

### Deployment: Hu1 in 5 discriminants → 53.4% (+0.3pp)

Best configuration (v3): hu1 added to discriminants where d > 0.8:
1. mushroom-banana: +hu1 (d=1.09) +hu2 (d=1.16)
2. GR-banana: +hu1 (d=1.11)
3. bear-KP: +hu1 (d=1.09) — bear gains +2.5pp, KP loses 0.5pp
4. bear-teapot: +hu1 (d=0.98)
5. sports-bus: +hu1 (d=0.84)

Result: 53.4% (1069/2000) — bear +2.5pp, sports +1.5pp, teapot +1pp, KP -0.5pp

### Failed experiments:
- Full deployment (v1: +hu1 in all 6 + jelly-KP glcm/hu2): 53.15% — KP -2pp from jelly-KP additions
- Removing bear-KP hu1 (v3-): 53.0% — bear drops 3pp, not worth the 0.5pp KP recovery
- mushroom-GR glcm+hu2: 53.2% — GR drops 1.5pp, mushroom flat
- 4 new disc pairs (GR-bus, jelly-sports, jelly-orange, mush-sports): 53.0% — bus -2.5pp, jelly -2pp. High-accuracy classes are hurt by new discs.
- Banana hu1 guard (0.64/-8 and 0.66/-5): 53.4% — trades banana TPs for fewer FPs, net zero
- Recalibration (added teapot+0.01, sports+0.01): 53.4% — sports +1pp, teapot +0.5pp but KP -1pp

### Key lessons:
1. Hu moments are genuinely orthogonal and produce stable gains when deployed conservatively
2. High-accuracy classes (jelly 70.5%, bus 71%) can ONLY be hurt by new discriminants
3. Only 19/285 rank-2 errors lack discriminants — the rest have discs that get the wrong answer
4. banana-orange disc accuracy on hard cases: 15.8% — these are genuinely ambiguous images
5. Calibration offsets are near-zero-sum at this accuracy level

### warm_sat_std in banana-orange disc → 53.5% (+0.1pp)
Warm saturation std separates hard banana-orange cases:
- Hard banana→O: warm_sat_std=0.159 (uniform, like orange)
- Hard orange→B: warm_sat_std=0.205 (variable, like banana)
Center=0.18, scale=6 → banana +1.5pp, orange -0.5pp, net +2 correct.

### Current best: 53.5% (1071/2000)

Per-class: banana 53%, bear 50.5%, GR 42%, jelly 70.5%, KP 51.5%, 
  mushroom 51%, orange 57.5%, bus 71%, sports 54.5%, teapot 34%

## Session 7: New features — binary_complexity, orient_entropy

### Analysis phase
- Rank distribution: teapot 104, GR 98, bear 95 reachable errors
- Discriminant accuracy on hard cases: 80-100% get the WRONG answer
- Explored: multi_scale_edge_ratio, vert_horiz_ratio, center_bright_ratio, 
  binary_complexity, orient_entropy, sat_center_edge, color_diversity
- FOUND: orient_entropy (gradient direction diversity) has d=1.11 for sports-teapot

### Experiments
- Calibration offsets (banana -0.04, KP -0.02): 53.0% — breaks reranking calibration
- Per-class histogram blend: 51.4% — catastrophic as expected
- binary_complexity in bear-mushroom: 53.3% — bear +0.5, mush -2.5, net negative
- orient_entropy in sports-teapot disc: +30 net correct discriminant calls!
- orient_entropy in teapot-banana disc: +4-5 net
- Deployed orient_entropy in sports-teapot + teapot-banana → **53.6%** (+0.1pp)
  - Teapot: 34% → 35.5% (+1.5pp), sports: 54.5% → 54.0% (-0.5pp)
- orient_entropy in teapot-KP: net zero (teapot +0.5, KP -1.0) — reverted

### Current best: 53.6% (1071/2000)

Per-class: banana 53%, bear 50.5%, GR 42%, jelly 70.5%, KP 51.5%, 
  mushroom 51%, orange 57.5%, bus 71%, sports 54%, teapot 35.5%

---

## Session 8 — 2026-05-15 (continued)

### New features added
- color_purity: chroma/lightness ratio from LAB space (teapot=0.151, KP=0.095, banana=0.265)
- warm_cool_a_diff: LAB 'a' channel difference between warm-hue and cool-hue pixels (GR=0.031, bear=0.016, d=0.78)

### Experiments
- color_purity in teapot-KP disc (c=0.12, s=5): KP 51.5→52.0, teapot 35.5→35.0. Net zero. Reverted.
- warm_cool_a_diff in bear-GR disc (c=0.023, s=50): 53.3% — bear -2.5pp, GR -1pp. Harmful. Reverted.

### Analysis
Both new features (color_purity, warm_cool_a_diff) failed to improve end-to-end accuracy despite having
meaningful class-level separation (d=0.78 for warm_cool_a_diff). This confirms the zero-sum pattern: 
at this discriminant density, adding more signals to an already-saturated discriminant only introduces
noise for the marginal cases.

### Direction shift needed
Discriminant feature engineering is exhausted. Need structural pipeline changes:
1. Confidence gating: reject low-confidence predictions for certain classes → fall through to #2
2. Ensemble voting: compute multiple independent rankings and vote
3. Signature weight tuning: the relative weights of features within signatures may be suboptimal
4. New discriminant pairs: cover currently unaddressed confusion pairs

Trying: confidence gating for sports_car and mushroom (predicted +6 and +3 respectively)

## Session 9 — Confidence Gating & Local Verify

### Baseline: 53.6% (1071/2000) train top-1

### Confidence gating
- sports_car at 0.40: 53.95% (+7 correct). Sports -0.5pp but KP +1.5pp, bear +1pp, banana +0.5pp, bus +0.5pp
- Added banana at 0.42, mushroom at 0.42: 54.1% (1082/2000). Net +11 over baseline
- Tried expanding to 6 classes (GR, bear, KP also): 53.25% — KP crashed -8pp. Reverted to 3 classes.

### Local verify conditions
- teapot-banana (cm_b < 0.57 AND orient_entropy > 2.85): +2pp teapot  
- teapot-KP (autocorr_h > 0.16 AND horiz > 1.1): +1pp teapot
- Margin 0.15 vs 0.08: 0.15 catches more cases without losing elsewhere
- jelly-teapot (sat > 0.50 AND color_std > 0.20): +0.5pp jelly
- teapot-GR (edge < 0.22 AND horiz > 1.05): +0.5pp teapot
- orange-teapot (sat > 0.55 AND cm_a > 0.56): +0.5pp orange
- mushroom-banana (edge > 0.27 AND hu1 > 2.65): +0.5pp mushroom
- **Best with local verify: 54.35% (1087/2000)**

### Things that DIDN'T work
- Calibration boosts for teapot/GR: teapot gained but bus/jelly/orange lost more (zero-sum)
- Per-class histogram blend weights: 52.4% disaster, teapot crashed to 25%
- Prototype distance blending: 53.55-53.9%. Helped teapot +1.5pp but hurt everything else
- Boosted repulsion strengths: 54.2% — marginal, bear hurt
- Signature weight tuning (teapot): 54.0% — disrupted calibrated balance
- sports_car-school_bus verify: sports +1.5pp but bus -5pp (conditions too aggressive)
- bear-KP verify: net negative (-0.5pp bus)
- Histogram blend at 0.85 instead of 0.88: 53.5% — worse

### Current best verified: 54.35% (1087/2000)
Per-class: banana 53%, bear 52%, GR 42%, jelly 71%, KP 52.5%, mushroom 51%, orange 58%, bus 71.5%, sports 53.5%, teapot 39%

### Key insight
Global score adjustments (calibration, blending, prototypes) are zero-sum.
Conditional logic (confidence gates, local verify) works because it only fires on specific cases.
Each individual condition adds ~1-2 correct predictions. Progress is incremental but cumulative.

### Continued Session 9 — Rank margin tuning + proto verify

**Big wins:**
- Proto verify for orange-banana only: 54.65% (orange +5pp, banana -2pp, net +6)
- Rank-3 margin 0.15→0.25: 54.95% (KP +1pp, teapot +0.5pp, net +2)
- Rank-4 margin 0.15→0.22: 55.05% (bear +0.5pp, teapot +0.5pp, net +2)

**Things that didn't work:**
- Proto verify for jelly-KP: KP crashed -2.5pp (prototypes too close)
- Generic proto tiebreaker (margin < 0.05): 52% catastrophe
- Proto verify for orange-mushroom: net zero
- Rank-5 widening: GR hurt -0.5pp
- Teapot confidence gate: teapot TP hit hard
- Bus-sports base tuning: no effect
- Bear-KP base lowering: KP -1.5pp

**Current best: 55.05% (1101/2000)**
Per-class: banana 51%, bear 52.5%, GR 42%, jelly 70%, KP 54.5%, mushroom 52%, orange 63.5%, bus 71.5%, sports 53.5%, teapot 40%

### Key pattern confirmed
- Selective, pair-specific interventions work (proto for orange-banana: +6 net)  
- Generic interventions backfire (proto for all pairs: -61 net)
- Margin widening for deep ranks works because discriminants are more accurate for larger rank gaps

### Final Session 9 results

**Current best: 55.10% (1102/2000) train top-1**
Per-class: banana 51%, bear 52.5%, GR 42%, jelly 70%, KP 54.5%, mushroom 52.5%, orange 63.5%, bus 71.5%, sports 53.5%, teapot 40%

**All changes from session baseline (53.6%):**
1. Confidence gates: sports_car 0.40, banana 0.42, mushroom 0.42 → +11 correct
2. Local verify conditions:
   - teapot-banana: cm_center_b < 0.57 AND orient_entropy > 2.85
   - teapot-KP: autocorr_h > 0.16 AND horiz_dominance > 1.1
   - jelly-teapot: sat > 0.50 AND color_std > 0.20
   - teapot-GR: edge < 0.22 AND horiz_dominance > 1.05
   - orange-teapot: sat > 0.55 AND cm_center_a > 0.56
   - KP-teapot: bw > 0.70 AND sat < 0.20
   - mushroom-banana: edge > 0.27 AND hu1 > 2.65
   - orange-banana: proto distance (Mahalanobis-like) → +6 net
3. Rank-3 margin 0.15→0.25, rank-4 margin 0.15→0.22 → +4 correct
4. New repulsion pairs: teapot-GR 0.010, GR-mushroom 0.010 → +1 correct

**Total improvement: 53.6% → 55.10% (+31 correct, +1.5pp)**

## Session 10 — Local Verify Mining (2026-05-16)

### Approach: Systematic local verify condition mining
Instead of tuning discriminants (saturated), systematically find top1-wrong/top2-correct cases (margin < 0.15) and craft high-precision verify conditions for each pair.

### Vertical features deployed (neutral)
- edge_vert_mid_ratio in teapot-banana discriminant: neutral
- warm_vert_concentration in sports-bus discriminant: bus -0.5pp, reverted
- warm_vert_top in bear-mushroom and bear-GR discriminants: bear crashed -2pp, reverted

**Lesson: vertical features don't have enough separation in discriminants — too noisy**

### New local verify conditions (all positive net)
1. **sports-bus** (dct_high > 0.20 AND grad_mean > 1.60 → favor sports): +4 net (7 sports gained, 3 bus lost)
2. **bear-mushroom** (green > 0.50 AND color_std > 0.18 → favor bear): +2 net (5 bear gained, 3 mush lost)
3. **KP-sports** (fft_hv_ratio > 1.0 AND edge_vert_mid_ratio < 0.36 → favor KP): +6 net (6 KP gained, 0 sports lost)
4. **bus-mushroom** (autocorr_h > 0.10 AND dct_high < 0.23 → favor bus): +5 net (5 bus gained, 0 mush lost)
5. **sports-teapot** (bw > 0.80 AND horiz_dominance > 1.50 → favor sports): +7 net (9 sports gained, 2 teapot lost)
6. **bus-sports bidirectional** (dct_high < 0.195 AND hue_orange > 0.20 → favor bus): +4 net (7 bus gained, 3 sports lost)

### Things that didn't work
- KP-teapot verify (warm_bl > 0.15 AND color_std > 0.04): +1 net but teapot -1pp, reverted (teapot too fragile)
- Bear-KP verify: all conditions tested were net negative
- GR-mushroom verify: all conditions tested were net zero
- Bear-mushroom with warm_vert_top: zero-sum

### Current best: 56.50% (1130/2000) train top-1
Per-class: banana 51%, bear 55%, GR 42%, jelly 70%, KP 57.5%, mushroom 51%, orange 63.5%, bus 76%, sports 60%, teapot 39%

### Additional verify conditions
7. **banana-bus** (autocorr_h < 0.08 → favor banana): +2 net (3 banana gained, 1 bus lost)
8. **teapot-bus** (autocorr_h < 0.25 AND dct_high > 0.18 → favor teapot): +2 net (2 teapot gained, 0 bus lost)

### Additional experiments
- Verify margin widening (0.15→0.20): FAILED, banana -3.5pp, mushroom -1.5pp
- GR confidence gate at 0.38: NEUTRAL (GR lost 0.5pp)
- GR-banana verify (warm > 0.65 AND yellow > 0.40): only works at margin 0.20, useless at 0.15
- GR-mushroom verify: all conditions net zero
- Bear-KP verify: all conditions net negative
- Mushroom-bear verify: weak separation, net zero

### Updated best: 56.70% (1134/2000) train top-1
Per-class: banana 52.5%, bear 55%, GR 42%, jelly 70%, KP 57.5%, mushroom 51%, orange 63.5%, bus 75.5%, sports 60%, teapot 40%

### Key insight
Local verify condition mining is the most productive approach at this stage. Each pair-specific condition with high-precision thresholds produces net positive gains because:
- The conditions are conjunctive (AND): both features must pass → high precision
- We can test exact recall/FP count before deploying
- Net gain is predictable: (fix_hit - risk_hit)
- Best pairs: KP-sports (+6), sports-teapot (+7), bus-mushroom (+5)
- Worst results come from pairs where both classes share similar feature distributions
- Some pairs (GR-bear, mush-bear, banana-orange) are genuinely hard — features overlap too much

### Things that failed in Session 10
- Vertical profile features in discriminants: all neutral or negative
- Verify margin widening (0.15→0.20): lost banana/mushroom
- GR confidence gate: net zero
- Double verify pass: net negative (re-swaps correct predictions)
- Expanded rank-3/4 whitelists: net -8 (discriminants inaccurate at deep ranks for new pairs)
- Bear-KP, GR-mushroom, mushroom-bear verify: too little feature separation

### Total session improvement: 55.10% → 56.70% (+32 correct, +1.6pp)

### Remaining bottlenecks
- banana→orange (34): genuinely hard, proto distance agrees with wrong answer
- GR→bear (26): insufficient feature separation for verify
- bear→mushroom (24): marginal verify helps (+2) but stubborn core
- GR at 42%: most errors are to bear/mushroom/KP — all hard pairs
- teapot at 40%: signature is too generic, errors spread across all classes

## Session 11 — Verify Mining + Confidence Gates (2026-05-16)

### New verify conditions
1. **teapot-bear**: hu1 < 2.62 → favor teapot: +2 net
2. Fixed dead code: KP-teapot verify at line 504 was unreachable (same frozenset as line 476)

### New confidence gates
- golden_retriever: 0.35, orange: 0.42, teapot: 0.35 → +3 net

### Things that failed
- Unused features in discriminants (color_purity, sat_pixels_ratio, etc.): -15 from 56.80%
- Calibration tuning (teapot +0.02, GR +0.01): -28 from 56.80%
- Gate tuning (removing/adjusting existing gates): net zero
- Unused features in verify conditions: all net zero or negative

### Session 11 result: 56.70% → 56.95% (+5 correct, +0.25pp)

## Session 12 — Verify Mining + Structural Improvements (2026-05-16)

### New verify conditions deployed
1. **GR-bear**: sat < 0.28 AND dct_high < 0.20 → favor GR: +5 net (GR +8, bear -3)
2. **KP-teapot bidirectional**: warm_sat_std > 0.15 → favor KP: +3 net (merged into existing teapot-KP verify as elif)
3. **teapot-bear bidirectional**: hue_red > 0.50 → favor bear: +3 estimated (merged as elif)
4. **banana-mushroom bidirectional**: cm_b_std > 0.045 AND green_region_area < 0.05 → favor banana: +3 estimated
5. Fixed dead code: removed unreachable KP-teapot elif at old line 504

### Structural: replaced orange-banana proto_dist verify (fired 0 times) with the above conditions

### Things that failed (explored but reverted)
- **banana-orange verify conditions**: warm_val_mean < 0.70 AND orient_entropy < 2.80 looked like +8 net in simulation but caused -11 orange regression in full eval. Even tighter (< 0.65) still caused -11 orange. Cascade effects from other changes amplify orange losses.
- **Wider rank-3/4 whitelists**: Added 3 pairs to rank-3, 8 pairs to rank-4 → -16 regression. Discriminants too inaccurate at deep ranks.
- **Confidence gates**: GR gate 0.35→0.40 → -2 GR. Bear gate 0.35 → -1. KP gate 0.38 → -13 KP.
- **Banana-orange pair base**: Raised from 0.0 to 0.10 or 0.20 → net zero or -1.
- **Teapot repulsion increase**: All 4 teapot pairs increased 30-50% → -1 (hurt sports).
- **New feature exploration**: yellow_narrow_ratio (hue 18-32 within warm) had d'=0.63 at class level but only d'=0.24 on error cases. All threshold tests net negative.
- **Discriminant feature vote analysis**: banana-orange discriminant features are 65-85% wrong on BOTH directions of errors. Confirms discriminants are zero-sum at the error boundary.

### Key insights
- **Dead code detection**: frozenset(["teapot", "king_penguin"]) == frozenset(["king_penguin", "teapot"]) — second elif branch never executes. Combined conditions into single branch.
- **Cascade amplification**: A verify condition that shows +X net in isolation can cause -2X or -3X regression when it interacts with confidence gates and other verify conditions.
- **Discriminant analysis on errors**: Features are systematically wrong on error cases because errors are the genuinely ambiguous images. No amount of feature tuning can fix this — the distributions overlap by definition at the error boundary.
- **Hard error ceiling**: 58-80% of errors per class have the true class at rank 4+ (not even in top 3). These can't be fixed by any ranking adjustment.

### Current best: 57.35% (1147/2000) train top-1
Per-class: banana 52.5%, bear 54%, GR 46%, jelly 70.5%, KP 59%, mushroom 51%, orange 64%, bus 75.5%, sports 60%, teapot 41%

### Total session improvement: 56.95% → 57.35% (+8 correct, +0.40pp)

### Remaining bottlenecks
- banana→orange (34): genuinely hard, all verify/discriminant approaches fail
- teapot→banana (27): teapot signature too weak, errors spread across all classes
- sports→bus (25): existing verify catches some, but remaining cases have no separating features
- bear→mushroom (24): feature overlap too high
- GR at 46%: improved +4pp this session but still low

---

## Session 13 (continued) — 2026-05-16

### Starting point: 57.65% (1153/2000) train top-1
From earlier in Session 13: rb_corr in banana-orange disc (+4), gb_corr+rb_corr in GR-banana disc (+2).

### What we tried and results:

1. **center_bright_ratio in GR-KP discriminant**: NEUTRAL. Reverted.

2. **Channel correlation features on NEW confusion pairs** (cross-class error d' analysis):
   - sports→bus: gb_corr d'=1.33, rb_corr d'=1.18
   - bear↔mush: center_bright_ratio d'=1.30/1.36 (within-class), but cross-class d' only 0.55
   - bear↔mush: hue_entropy had cross-class d'=1.39

3. **gb_corr in sports-bus discriminant**: -1 (bus 151→150). Reverted.

4. **center_bright_ratio in bear-mush discriminant**: -3 (banana -1, mush -1, sports -1). Reverted.

5. **hue_entropy (NEW feature) in bear-mush discriminant**: 
   - First try (weight 4, thresh 2.5): -4 total. Bear +5 but mush -7.
   - Second try (weight 2, thresh 2.3): -2 total. Bear ±0, mush -2. Reverted.

6. **rb_ratio in sports-bus discriminant**: -5 total (sports -3, bus -1). Reverted.

7. **hue_entropy in teapot-banana discriminant**: -2 (banana -2). Reverted.

8. **Calibration changes**: 
   - Removing KP +0.01 calibration: -19 DISASTER. KP needs the boost.
   - Adding banana -0.01: -3 (banana -2, bear -2). Reverted.
   
9. **Bus→sports histogram verify condition** (hist_sports_minus_bus < -0.335 AND hist_banana > 2.157):
   fix=6, risk=0. Result: bus +1 but banana -1. Net zero. **KEPT** (improves bus despite cascade).

10. **New repulsion pairs**: 
    - brown_bear↔golden_retriever (0.012): +1 net (bear +1, GR +1, teapot +1, mush -1, sports -1)
    - orange↔teapot (0.008): contributed to the +1.
    **KEPT**. Total: 1154/2000.

11. **jellyfish-teapot repulsion**: -1 (sports cascade). Reverted.

12. **bear-mush repulsion increase** (0.010→0.014): NEUTRAL. Kept at 0.010.

13. **Hist blend weight** (0.88→0.90): -17! Reverted.

14. **Proto weight** (0.025→0.030/0.035): NEUTRAL. Kept at 0.025.

15. **Teapot hist weight** (0.05→0.08/0.12): NEUTRAL.

16. **binary_complexity in teapot signature**: -28! Teapot +3 but every other class -1 to -8. Base signature changes are extremely disruptive. Reverted.

### Key learnings from Session 13:

- **Within-class d' ≠ cross-class d'**: A feature can have d'=1.3 within a class (correct vs error) but only d'=0.55 cross-class (A-errors vs B-errors). Only cross-class d' predicts discriminant success.
- **Calibration is locally optimal**: Removing KP's +0.01 calibration caused -7 KP. The calibration compensates for pipeline biases, not just scoring biases.
- **Base signature changes are 10x more disruptive than discriminant changes**: Adding one term to teapot signature caused -28 regression. Signatures affect ALL 2000 images at the initial scoring stage.
- **Repulsion pairs are a safe, small-gain mechanism**: Adding missing pairs (bear-GR, orange-teapot) gave +1 with minimal cascade risk.
- **hue_entropy, rb_ratio, gb_ratio** added as new features but failed to produce gains in discriminants.

### Current best: 57.70% (1154/2000) train top-1
Per-class: banana 112, bear 108, GR 97, jelly 141, KP 118, mush 101, orange 124, bus 152, sports 119, teapot 82

### Session 13 continued (2026-05-16 context 2)

Starting from 1157/2000 (57.85%). Verified baseline stable.

#### Experiments:
1. **Banana-teapot pair base 0.30→0.20/0.10**: Neutral. Analysis showed only 1 of 29 teapot→banana errors has teapot as #2. Most have teapot in #3-#5 or unranked. Pairwise reranking can't fix this confusion.
2. **GR-mushroom pair base 0.05→0.0**: -1 regression. Reverted.
3. **GR-mushroom local verify (smooth_warm + dct_low)**: Neutral. The 6 eligible GR→mush errors have smooth_warm≈0 — they genuinely look mushroom-like. Reverted.
4. **3 new repulsion pairs** (sports-teapot, bear-sports, banana-KP at 0.012): **+1** (sports 119→120). Kept.
5. **Teapot calibration +0.01**: -11 massive cascade regression. Confirms calibration is extremely dangerous.
6. **Banana-teapot + bear-mush in rank3 whitelist**: -5. Rank3 discriminants not reliable enough at distance.
7. **Bear-mush in rank4 whitelist**: -1. Cascade from bear losses.
8. **has_dark_bright_contrast in bus-sports discriminant**: -8. Modifying existing discriminants is extremely risky.
9. **Banana gate 0.42→0.50**: -4. Gate flips to wrong #2 too often.
10. **GR gate 0.35→0.37**: Neutral. Kept as marginally safer.
11. **GR gate 0.35→0.39**: -2. Too many TP lost.
12. **Mushroom gate 0.42→0.44/0.46**: Neutral (reshuffles classes but net zero).
13. **Repulsion proximity 0.6→0.5**: -2. Fires on non-close pairs.
14. **Repulsion disc_gap 1.0→0.8**: -2. Unreliable discriminants fire.
15. **Reranking margin 0.25→0.30**: **+1** (orange 125→126). Wider window catches one case.
16. **Rank4 margin 0.22→0.25**: **+1** (sports 120→121).
17. **Rank4 margin 0.25→0.27**: **+1** (teapot 82→83).
18. **Rank4 margin 0.27→0.30**: Neutral. Kept at 0.30.
19. **Rank5 margin 0.12→0.15**: Neutral. Kept.
20. **Top-2 multiplier 1.5→1.3**: **+1** (GR 97→98). Lower threshold lets more correct reranking through.
21. **Top-2 multiplier 1.3→1.2**: -2. Too aggressive.
22. **Rank3 multiplier 2.0→1.8**: -3. Rank3 reranking is dangerous at lower thresholds.
23. **Rank4 multiplier 3.0→2.5**: -2. KP drops.
24. **Verify margin 0.15→0.18**: -5. Verify conditions overcorrect at wider margins.
25. **Teapot hist_w 0.05→0.07**: Neutral.

#### Key discovery: margin and multiplier tuning
The biggest gains came from widening the reranking eligibility window and lowering the threshold multiplier for top-1 vs top-2 reranking. This is a different axis of optimization from pair-specific tuning — it makes ALL existing discriminants fire more often.

#### Summary of changes kept:
- 3 new repulsion pairs (sports-teapot, bear-sports, banana-KP at 0.012): +1
- GR gate 0.35→0.37: neutral but safer
- Reranking margin 0.25→0.30: +1
- Rank3 margin 0.25→0.28: neutral
- Rank4 margin 0.22→0.30: +2
- Rank5 margin 0.12→0.15: neutral
- Top-2 multiplier 1.5→1.3: +1

### Current best: 58.10% (1162/2000) train top-1
Per-class: banana 112, bear 108, GR 98, jelly 141, KP 118, mush 102, orange 126, bus 152, sports 121, teapot 83

### Total session improvement: 57.85% → 58.10% (+5 correct, +0.25pp)
Combined with all Session 13 gains: 56.95% → 58.10% (+23 correct, +1.15pp)
