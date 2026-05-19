# HL-ImageNet Phase 2: Experiment Log

**Date**: 2026-05-12
**Current val accuracy**: 45.9% top-1, 72.2% top-3 on 2000 images (10 real Tiny ImageNet classes, 200/class)
**Baseline val accuracy**: 33.4% (initial), 40.5% (after Phase 2 baseline tuning)
**Target**: 50% val top-1 before updating README

---

## Architecture Changes from Phase 1

### Phase 2 scoring pipeline
```
image (64x64 BGR)
  → _stats() extracts ~57 global features (color, texture, spatial, shape)
  → 10 class signatures: score = guarded_score(pos_weighted_sum, min_guards)
  → flat scoring: all classes scored simultaneously
  → pairwise reranking: if top-2 margin < 0.25 and discriminant exists, may swap
  → prediction with proof trace
```

### Key differences from Phase 1
- **No sensors/atoms/scene-graph features** for scoring — all signatures compute directly from `_stats()` which extracts a fixed feature vector from the raw image
- **Guard-gate scoring**: `score = pos * (0.5 + 0.5 * min(guards))` — negative features suppress false positives via min-gate. If any guard fires 0, score halves.
- **Pairwise reranking** replaces the Phase 1 single-swap tiebreaker. Uses targeted discriminant functions for specific class pairs.
- **Conjunctive (multiplicative) features**: `smooth_yellow = yellow * max(0, 1 - edge*3)`, `textured_decentered = edge * max(0, 1 - cs/1.5)`. These capture "smooth yellow object" or "textured non-centered scene" much better than additive combinations.

---

## Iteration History

### Baseline (33.4% → 40.5% val)
- Started with additive sigmoid scoring, no guards, no reranking
- **Problem discovered**: "sink classes" — banana and king_penguin absorb predictions from many other classes because their features (warm/yellow, low-sat) are broadly triggered
- Added guard-gate scoring + P95 calibration
- Added initial pairwise discriminants

### Iter 5 series (40.5% → 45.0% val)
- Added `smooth_yellow` conjunctive feature (7x-62x class separation vs ~1.5x for raw yellow)
- Tuned banana, orange, teapot, king_penguin signatures
- Added/optimized pairwise discriminants
- **Critical discovery**: removing net-negative discriminants was the single biggest improvement (+2.7pp). Bad discriminants actively harm performance more than they help.
- Removed teapot-involved discriminants (all net-negative except sports_car-teapot)
- Overlap-zone tuning for banana-orange discriminant (81.6% accuracy in overlap zone)

### Iter 7 series (45.0% → 45.9% val)
- Added 8 new pairwise discriminants (banana-school_bus, brown_bear-sports_car, sports_car-teapot, GR-school_bus, mushroom-school_bus, GR-teapot, KP-teapot, brown_bear-school_bus)
- **Validated on val**: 4 of 8 were net-negative on val despite 70-89% accuracy on train overlap
- Removed all val-net-negative discriminants (GR-school_bus -7, KP-teapot -6, GR-teapot -2, KP-school_bus -1)
- Also removed previously-added discriminants that turned net-negative (brown_bear-KP, brown_bear-GR, brown_bear-mushroom, banana-brown_bear, banana-mushroom)
- Added `green` guard to teapot signature (P95-calibrated at 0.30/-2)
- Added `textured_decentered` and `warm_blob_count` features to `_stats()`
- Net result: val 45.0% → 45.9%

---

## Key Findings

### 1. Pairwise reranking: high reward but easy to overfit
- **Val reranking stats**: 131 helped, 47 hurt, net +84 (11 active discriminants)
- **Base top-1**: 41.9% → with reranking: 45.9% (captures 22% of rank-1→rank-2 gap)
- **Train-val divergence**: Discriminants at 80%+ accuracy on train overlap often go net-negative on val. The overlap zone (images where two classes are close in score) contains different images on train vs val because base signature scores are noisy.
- **Lesson**: Always validate discriminants on val. Only keep val-net-positive pairs.

### 2. Sink class problem
Banana absorbs 233 FP on val: orange(53), GR(39), teapot(38), mushroom(33), bear(25), KP(17).
Teapot absorbs 186 FP: KP(36), jelly(30), GR(25), mushroom(22), orange(21), banana(20).

These classes have "low-specificity" features — banana triggers on anything warm+yellow, teapot on anything low-edge+low-sat.

### 3. Feature engineering: multiplicative > additive
Conjunctive features that multiply two conditions (`smooth_yellow = yellow * (1-edge*3)`) provide dramatically better class separation than individual features used additively. The key insight: "smooth AND yellow" is much more discriminative than "smooth + yellow" because the former requires both conditions simultaneously.

### 4. Guard calibration at P95
Guard thresholds must be set at the 95th percentile of the TRUE class distribution to avoid self-suppression. Even 10% self-suppression on the positive class can outweigh the FP reduction. Use gentle slopes (-2 to -3) near the threshold.

### 5. Hard confusion pairs (no good discriminant exists)
- brown_bear vs golden_retriever: d < 0.8 for all features in overlap zone. Both are "warm, textured, nature animal." Need spatial structure (shape, pose) to separate.
- king_penguin vs teapot: both "desaturated, low-edge, low-warm." Best discriminant only 70.5% on train, net-negative on val.

---

## Per-Class Analysis (val, current)

| Class | Accuracy | Main losses to | Notes |
|-------|----------|---------------|-------|
| jellyfish | 64.0% | teapot(30) | Strong blue_purple feature, well-isolated |
| school_bus | 68.5% | sports_car(18), banana(12) | Strong blob_lap_var + grad features |
| banana | 55.5% | teapot(20), school_bus(19), GR(16) | smooth_yellow helps but still loses to low-texture classes |
| sports_car | 51.5% | school_bus(25), bear(19), teapot(16) | grad_dir_entropy is key differentiator |
| orange | 47.0% | banana(53), teapot(21), GR(16) | Very hard to separate from banana (both smooth, warm, yellow-ish) |
| golden_retriever | 40.5% | banana(39), teapot(25), bear(21) | radial_warm_diff is unique but GR is diverse |
| king_penguin | 37.0% | teapot(36), bear(24), banana(17) | Low-sat profile overlaps with teapot |
| brown_bear | 34.0% | GR(50), banana(25), school_bus(17) | Hardest — similar to GR in all global features |
| teapot | 32.0% | banana(38), KP(25), GR(16) | Catch-all "low-feature" class |
| mushroom | 28.5% | GR(38), banana(33), teapot(22) | High-texture mushrooms classified correctly; smooth ones lost to banana |

---

## What's Needed for 50%

Current: 45.9%. Need +4.1pp = ~82 more correct predictions.

**Highest-leverage opportunities:**
1. **Improve base signatures** for bear, mushroom, teapot — these three at ~30% drag the average down. Even +5pp each = +30 correct.
2. **New feature types**: spatial shape features (HOG-like), template matching, or color histogram matching could break the bear-GR deadlock.
3. **Better banana guards**: banana absorbs 233 FP. Even modest improvement in banana specificity frees up predictions for other classes.
4. **Careful reranking for remaining high-volume pairs**: banana-school_bus (+4), mushroom-school_bus (+3) are working but could be optimized further.

**What probably won't work:**
- Extending reranking to top-3 (tested: net-negative for almost all pairs)
- Increasing margin threshold beyond 0.25 (tested: ~0 additional benefit)
- Adding guards based on features with d < 0.5 (too much overlap, hurts true positives)
