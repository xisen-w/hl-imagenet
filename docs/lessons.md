# Lessons Learned from Heuristic Learning on Image Classification

330+ iterations of building a symbolic image classifier from scratch. These are the hard-won lessons, ordered from most impactful to most subtle.

---

## 1. Additive scoring creates sink classes — and they're nearly impossible to fix

**The problem:** When class scores are sums of sigmoid activations over shared features (warm color, edge density, saturation), some classes naturally score high on most images. School bus averages 0.59 across ALL images (not just bus images), and banana averages 0.46. These "sink classes" attract false positives from everywhere.

**Evidence:**
- School bus receives 166 false positive predictions on the 2000-image train set
- Banana receives 186 false positive predictions
- Meanwhile, jellyfish (distinctive blue) receives only 22 FPs

**What doesn't work:**
- Guards on the sink class signature: school bus dropped from 78% to 49-60% with any guard we tried. The bus signature needs ALL its positive signals (grad_mean, lap_var, horiz_dominance) — these features genuinely fire on bus images. There's no room for suppression.
- Score normalization (z-score, mean subtraction): disrupts the reranking layer which was tuned for raw score ranges. Full z-score dropped overall accuracy by 4pp.

**What partially works:**
- Mean-centered histogram blending: subtracting 30% of the class's mean histogram score from the blend reduces sink inflation without collapsing the class itself (+0.25pp net)
- Accepting the sink and building pairwise discriminants to rescue specific confusions

**Lesson:** If your scoring formula is additive over shared features, some classes will inevitably dominate. Design the architecture to handle this from the start — don't try to patch it later with guards.

---

## 2. Pairwise reranking is powerful but has a hard ceiling

**The insight:** After initial scoring, if the true class is rank 2 or 3, a specialized pairwise discriminant function can correct the ranking. On our system, ~40-45% of errors have the true class within rescue range (rank 2-3).

**Evidence:**
- Adding the first 17 discriminant pairs improved accuracy from 44.8% to 48.2% (+3.4pp)
- Adding 7 more discriminants (session 3) pushed from 47.5% to 48.75% (+1.25pp)
- But: ~55% of errors have the true class beyond rank 3 — unreachable by reranking

**Key finding on discriminant accuracy:**
| Accuracy | Example pair | Effect |
|:---:|---|---|
| 85%+ | banana-mushroom, jellyfish-KP | Safe to fire with low threshold |
| 75-84% | bear-KP, GR-KP | Needs moderate threshold (0.10-0.15) |
| 70-74% | GR-teapot | Needs high threshold (0.15+) |
| <70% | banana-teapot (58%) | Must be heavily gated (0.30 base) |

**Lesson:** Pairwise reranking is the single most impactful technique available, but its ceiling is structural. Beyond ~24 discriminant pairs, each new one has diminishing or negative returns.

---

## 3. Gap-aware confidence gating prevents reranking from causing errors

**The problem:** 112 out of 1036 errors (5.6%) were CAUSED by reranking — the true class was rank 1 before reranking, then got swapped down by a wrong discriminant call.

**The fix:** Require the discriminant's confidence margin to exceed a threshold that scales with the score gap:

```
swap iff disc_margin > base_threshold + score_gap * gap_scale
```

If class A leads class B by 0.20, the discriminant needs to be VERY confident (margin > 0.35) to justify swapping. If the gap is only 0.02, even modest evidence (margin > 0.08) suffices.

**Evidence:**
- Gap-aware gating alone added +0.8pp (49.0% from 48.2%)
- Per-pair calibration of base thresholds added another +0.2pp
- Total reranking-caused errors dropped from 112 to ~60

**Lesson:** A 70% accurate discriminant helps when the score gap is small but HURTS when the gap is large. Always gate reranking by the confidence of the existing scoring.

---

## 4. Histogram prototype ratios are far more discriminative than raw histogram scores

**The problem:** Raw histogram similarity (chi-squared distance to class prototype) is too correlated across confusable classes. hist_banana and hist_orange both score high on orange images.

**The solution:** Use differential histogram features: `hist_A_minus_B = hist_A - hist_B`. These cancel out shared signal and isolate what distinguishes A from B.

**Evidence:**
- `hist_sports_minus_bus`: d=2.24 separation (extremely discriminative)
- `hist_gr_minus_banana`: d=1.54
- `hist_orange_minus_banana`: d=1.29
- `hist_teapot_minus_kp`: d=1.28
- Raw `hist_banana`: d=0.3 (barely discriminative between banana and orange)

**Usage:** Added as 5th signal in pairwise discriminants. Contributed to +1pp improvement when first introduced.

**Lesson:** In prototype-matching systems, ratios/differences between prototypes are always more useful than absolute similarities.

---

## 5. Histogram blending works best as a global pre-ranking step, not a per-pair intervention

**The problem:** Adding histogram scores directly into signatures (+0.2pp) or into pairwise discriminants (varied) gave inconsistent results. The zero-sum dynamics meant every improvement for one class hurt its confused partner.

**The breakthrough:** Linear blend of ALL signature scores with ALL histogram scores BEFORE ranking:

```
final = 0.88 * signature + 0.12 * histogram_similarity
```

**Why it works:** It shifts the entire ranking, not just one pair. If school bus's histogram is truly the best match, it moves bus up for ALL comparisons simultaneously. This avoids the zero-sum trap.

**Evidence:**
- Histogram blending added +0.6pp on val (from 49.5% to 50.1%)
- Validated on train (+1pp) — consistent improvement
- School bus +4.5pp, sports car +6pp, orange +2.5pp
- Mean-centering (subtracting 30% of class mean) further improved by +0.25pp on train

**Lesson:** Global scoring adjustments that affect all classes simultaneously avoid the zero-sum dynamics that plague per-pair interventions.

---

## 6. Every pairwise discriminant that helps one class hurts the other

**The phenomenon:** When you add a discriminant between class A and class B:
- Images where A is correct and B was predicted → A gains (good)
- Images where B is correct and A was predicted → B might lose (bad)
- The discriminant has some accuracy <100%, so it sometimes makes the wrong call in both directions

**Evidence:**
- Orange-banana discriminant: orange +4pp, banana -2.5pp
- Teapot-KP discriminant: KP +6pp, teapot -1.5pp
- Bear-mushroom discriminant: mushroom +2.5pp (good), but later bear -1pp

**Why it's fundamental:** With 10 classes sharing overlapping feature space, improving discrimination for pair (A,B) can't magically not affect B. The discriminant IS making claims about B's identity.

**Mitigation strategies:**
- High base thresholds for inaccurate discriminants (don't fire unless very confident)
- Only whitelist rank-3 swaps for pairs where the discriminant is >80% accurate
- Accept the trade-off: optimize for net positive across both classes

**Lesson:** Track per-class accuracy before AND after every change. Net positive overall can mask catastrophic regression for one class.

---

## 7. Shape-defined classes hit a fundamental ceiling in color/texture feature spaces

**The problem:** Teapot is defined by SHAPE (handle, spout, body). But at 64x64, the feature space is dominated by color statistics, edge density, and texture measures. A metallic teapot and a king penguin share low saturation, low warmth, low color variation.

**Evidence:**
- Teapot is at 20-21% on train (barely above random 10% baseline)
- Correct teapots have hue_red=0.49, sat=0.33 (warm/colored)
- Lost-to-KP teapots have hue_red=0.10, sat=0.15 (dark/metallic) — feature-indistinguishable from KP
- Lost-to-banana teapots have yellow=0.54, warm=0.79 — feature-indistinguishable from banana

**What we tried and failed:**
- Horizontal symmetry (d=0.04 between teapot and KP — useless)
- Foreground center-of-mass, aspect ratio (d<0.4 — not enough)
- Every texture/shape feature we could compute: all <0.5 separation

**Lesson:** If a class is fundamentally defined by spatial configuration (shape) rather than appearance statistics, a system built on color/texture histograms cannot reliably classify it. Either add explicit shape detectors (e.g., Hough transforms for handles) or accept the ceiling.

---

## 8. Guards must be calibrated at the P95 of the true-positive distribution

**The problem:** A guard sigmoid suppresses a class when a feature exceeds a threshold. But if the threshold is too aggressive, it also suppresses true positives.

**The calibration principle:** The guard threshold should be set so that at most 5% of true positives are suppressed (the P95 of the TP distribution).

**Evidence:**
- GR color_std guard at 0.25: TP mean=0.16, P95=0.23. Threshold at 0.25 suppresses very few TPs. Net effect: GR -2.5pp but mushroom +2pp, bus +1.5pp, bear +0.5pp, orange +1.5pp = net +3pp for others.
- Banana hue_red guard at 0.55: TP P95=0.60, but setting threshold at 0.40 suppressed many TPs. Banana dropped 53→48%. Reverted.
- Bus warm guard at 0.65: Bus TPs frequently have warm>0.65 (mean=0.39 but spread is wide). Dropped bus from 78% to 59%. Reverted.

**Lesson:** Always measure the true-positive distribution before adding a guard. The threshold must be beyond P95 of TPs. A guard that fires on 10%+ of TPs will cause net regression.

---

## 9. Score normalization disrupts downstream systems tuned for raw scores

**The problem:** The reranking layer (discriminants, thresholds, gap scaling) was carefully tuned with signature scores in the 0.3-0.7 range. Normalizing scores (z-score, mean subtraction) changes this range unpredictably.

**Evidence:**
- Z-score normalization: accuracy dropped from 48.2% to 43.6% (-4.6pp)
- Full mean subtraction: dropped to 46.9% (-1.3pp)
- Partial mean subtraction (alpha=0.5): 48.0% (-0.2pp, still negative)
- Only 30% partial centering of histogram scores: +0.25pp (small enough not to disrupt)

**Why:** The reranking layer has 24 discriminant pairs with hand-tuned thresholds and scale parameters. These assume a specific score distribution. Changing the distribution requires retuning ALL parameters simultaneously — which is fragile and expensive.

**Lesson:** If you have a multi-layer system (scoring -> normalization -> reranking), changes to earlier layers cascade unpredictably. Prefer interventions that are additive/small enough not to disrupt downstream calibration.

---

## 10. Train-val gap can be NEGATIVE (val > train) and that's okay

**The phenomenon:** Throughout Phase 2, validation accuracy has been consistently 2-3pp HIGHER than train accuracy. This is the opposite of the usual overfitting pattern.

**Evidence:**
- Train 47.5% vs Val 50.1% (gap = +2.6pp for val)
- This pattern held across all iterations, not just one snapshot

**Why it happens:** The train/val split is images 0-199 vs 200-399 from each Tiny ImageNet class. The earlier-numbered images may be systematically harder (e.g., more atypical examples, different photographers). This is a dataset artifact, not a sign of underfitting.

**Lesson:** Don't assume val < train. Check the actual gap early and treat it as a calibration constant. A consistent gap is fine; a changing gap suggests you're overfitting one split.

---

## 11. The 85% accuracy rule for discriminants

**Finding:** Discriminants below ~75% accuracy tend to cause net harm even with gap-aware gating. The sweet spot is:

| Accuracy range | Recommendation |
|:---:|---|
| 85%+ | Use freely, low base threshold (-0.10 to 0.0) |
| 75-84% | Use with caution, moderate threshold (0.05-0.15) |
| 70-74% | Rank-2 only, high threshold (0.15-0.20) |
| <70% | Don't use, or set base threshold so high (0.25-0.30) it almost never fires |

**Evidence:**
- school_bus-sports_car at 84% accuracy: net +2pp with base=-0.10
- banana-mushroom at 85% accuracy: net +0.5pp with base=0.05
- GR-teapot at 74.5% accuracy: needed base=0.15 to be net neutral
- banana-teapot at 58% accuracy: base=0.30 makes it almost inert (fires on ~5% of pairs)

**Lesson:** Measure discriminant accuracy on the full 200+200 sample BEFORE deploying. If <75%, don't bother — the regression risk exceeds the rescue potential.

---

## 12. Histogram prototypes need mean-centering to avoid amplifying sink classes

**The problem:** Raw histogram similarity scores vary by class: hist_school_bus averages 1.53 across ALL images, while hist_jellyfish averages only 0.66. Blending raw scores amplifies the sink problem.

**The fix:** Subtract a fraction of the class's mean histogram score:
```
adjusted_hist = hist_score - class_mean * 0.3
```

This keeps the relative ordering (images that match bus better than average still get boosted) while removing the class-specific bias.

**Evidence:**
- Without centering: school bus at 78% but contributes to 166 FPs
- Full centering (1.0x): school bus drops to 74% (overcorrected)
- Optimal partial centering (0.3x): +0.25pp net, bus only drops 1.5pp while jelly +2.5pp, bear +1pp

**Lesson:** Any global feature that's used for scoring should be evaluated for class-level bias. If one class systematically scores higher, mean-center before using.

---

## 13. Confusion pairs are NOT symmetric — fixing A→B doesn't fix B→A

**The phenomenon:** orange→banana (53 errors) and banana→orange (23 errors) are different populations of images with different feature profiles. A discriminant tuned to fix orange→banana may not help banana→orange at all.

**Evidence:**
- The orange-banana discriminant: 77% accurate on orange images, 89% on banana images
- Improving it for orange (via hue_red boosting) caused banana regression
- The bear-GR discriminant: 85% on bear images but only 71% on GR images

**Lesson:** Always measure discriminant accuracy SEPARATELY for each class in the pair. The one with lower accuracy determines the risk.

---

## 14. Reverted experiments are as informative as successful ones

**Record of reverted attempts and what they taught:**

| Attempt | Result | What it revealed |
|---------|--------|-----------------|
| School bus guards (5 variants) | All -4 to -20pp for bus | Bus signature has no expendable features |
| Z-score normalization | -4.6pp | Reranking depends on absolute score scale |
| DCT features (Phase 1) | -1pp | Frequency domain doesn't help at 64x64 |
| Raw histogram in signatures | +0.2pp (marginal) | Hist scores too correlated across classes |
| Orange signature weight tuning | -0.1pp | Signature weights are locally optimal |
| Train-computed calibration offsets | -0.5 to -2pp | Global penalties disrupt per-pair tuning |
| Spatial symmetry features for teapot | d<0.1 | Not discriminative at this resolution |

**Lesson:** Log failed experiments as carefully as successful ones. They define the boundaries of what's achievable with the current architecture and prevent repeating the same mistakes.

---

## 15. The most impactful changes are architectural, not parametric

**Ranked by impact (pp improvement):**

| Rank | Change | Impact | Type |
|:---:|--------|:---:|---|
| 1 | Pairwise reranking (initial 17 pairs) | +3.4pp | Architectural |
| 2 | Histogram prototype blending | +0.6pp | Architectural |
| 3 | Gap-aware confidence gating | +0.8pp | Architectural |
| 4 | 7 new discriminant pairs | +1.0pp | Expansion |
| 5 | Per-pair threshold calibration | +0.2pp | Parametric |
| 6 | GR color_std guard | +0.3pp | Parametric |
| 7 | Mean-centered histogram blending | +0.25pp | Parametric |
| 8 | Histogram differential features | +1.0pp | Feature engineering |

**Pattern:** The first 3 architectural changes (+4.8pp total) account for more than all subsequent parametric tuning (~+2.75pp across 70+ iterations). Once the architecture is in place, parametric tuning gives diminishing returns.

**Lesson:** When stuck at a plateau, don't keep tuning thresholds. Look for a new architectural layer or representation. The biggest gains come from adding a new TYPE of computation, not optimizing existing ones.

---

## Summary: The Heuristic Learning Progression

```
Phase 0:  Random baseline (10%)
Phase 1:  Single-feature scoring (20-35%)
Phase 2:  Compound features + flat scoring (35-45%)
Phase 3:  Pairwise reranking (45-48%)
Phase 4:  Histogram blending + gap-aware gating (48-50%)
Phase 5:  Expanded discriminants + centering (48.75% train, 50.1% val)
???:      Next architectural breakthrough needed for 55%+
```

Each phase transition required a fundamentally new idea, not just more of the same type of tuning.
