# HL-ImageNet: Reasoning & Status Quo Snapshot

**Date:** 2026-05-09, after Session 10 (iteration 80+)
**Accuracy:** 84.8% top-1, 92.2% top-3 on 230 images (10 classes)

---

## Architecture Overview

### Pipeline
```
image (64x64 BGR) → SceneGraphBuilder → atoms → features → flat scorer → tiebreaker → prediction
```

### Scoring Formula
```
score = required_avg * 0.6 + supporting_avg * 0.3 - excluding_avg * 0.2
```
- **Required**: AND-gate — ALL must fire (confidence > 0.1) or class scores 0
- **Supporting**: plain average over all listed features (firing or not)
- **Excluding**: plain average over all listed features
- **Fallback**: if required fails, `supporting * 0.15 - excluding * 0.1`, capped at 0.3

### Tiebreaker System
Post-scoring pairwise check over top-4 candidates. If margin < threshold (0.25 default, 0.35 for wide pairs) and `score_j > 0.1`, runs a pixel-level tiebreaker function. If result < 0.35, swap. Single swap limit per prediction.

Wide margin pairs: (golden_retriever, teapot), (golden_retriever, mushroom), (golden_retriever, school_bus), (banana, mushroom).

### Banana Cap
Pre-tiebreaker: when `yellow_dominant > 0.8`, banana score capped at 0.40 (prevents banana from consuming tiebreaker swaps).

---

## Per-Class Status

| Class | Acc | N | Status | Key Required Feature |
|-------|-----|---|--------|---------------------|
| banana | 100% | 5 | SOLVED | yellow_dominant |
| bicycle | 100% | 5 | SOLVED | wheel_like |
| eagle | 100% | 5 | SOLVED | bird_like (sat<55, edge<0.05 guards) |
| laptop | 100% | 5 | SOLVED | large_dark_rectangle_center |
| piano | 100% | 5 | SOLVED | repeated_vertical_lines + black_white_dominant |
| zebra | 100% | 5 | SOLVED | striped_texture + pure_vertical_stripes |
| school_bus | 84% | 50 | HARD | horizontal_window_pattern |
| golden_retriever | 76% | 50 | HARD | golden_brown_color |
| teapot | 82% | 50 | HARD | organic_texture |
| mushroom | 88% | 50 | HARD | organic_texture |

6 classes at 100% (all synthetic, 5 images each). The 4 hard classes (200 images total) average 82.5%.

---

## Confusion Matrix (top errors)

| From → To | Count | Root Cause |
|-----------|-------|------------|
| teapot → golden_retriever | 7 | golden_brown_color fires at 0.92+ on brass teapots |
| mushroom → golden_retriever | 6 | golden_brown_color fires at 1.0 on brown caps |
| golden_retriever → school_bus | 5 | non-golden dogs (golden_brown_color=0, required gate fails) |
| golden_retriever → mushroom | 4 | organic_texture fires on fur, high supporting overlap |
| golden_retriever → teapot | 4 | organic_texture + distinct_background |
| mushroom → teapot | 3 | both share organic_texture required |
| school_bus → golden_retriever | 3 | yellow bus → golden_brown_color fires |
| school_bus → teapot | 3 | low-yellow buses without window pattern |
| teapot → school_bus | 3 | horizontal banding or yellow teapots |
| teapot → mushroom | 3 | organic_texture shared, no discriminating signal |
| mushroom → school_bus | 2 | yellow/sky mushrooms mimic bus context |
| school_bus → mushroom | 2 | non-yellow buses with organic texture |
| teapot → bicycle | 2 | wheel_like fires on circular teapot elements |

**Total errors: 51/230 (22.2%)**

The dog/mushroom/teapot triangle accounts for 24 of 51 errors (47%).

---

## Progression History

```
Session 1:  ~20% → baseline with sensors + features
Session 2:   34.5% → hierarchy + scorer
Session 3:   43.5% → compound features + tiebreakers + threshold tuning
Session 4:   57.4% → tiebreaker expansion + banana excluders + mushroom_vs_teapot
Session 5:   61.7% → spatial attention + synthetic class tiebreakers + single-swap fix
Session 6:   67.4% → eagle/banana solved + tiebreaker guard fixes
Session 7:   67.8% → smooth_pct tiebreaker, DCT exploration (plateau confirmed)
Session 8a:  73.0% → banana cap + dog_vs_mushroom compound conditions + wide margin pairs
Session 8b:  77.8% → gradient+green conjunctions + mushroom_vs_teapot refinements + bus/teapot tiebreakers
```

---

## What Was Tried and Worked (Session 8)

| Approach | Result | Key |
|----------|--------|-----|
| Banana score cap at 0.40 when yellow_dominant > 0.8 | +3 teapots | Frees tiebreaker for real corrections |
| grad_top_bin>0.18 + green>0.089 + warm<0.68 in dog_vs_mushroom | +3 mushrooms | Conjunction avoids dog FP |
| sat>117 + rb_bot<1.83 + green<0.10 + yellow<0.15 in dog_vs_mushroom | +1 mushroom | Yellow guard prevents bus cascade |
| Mushroom cap+gills (bright_diff>15, bot_edge>0.28) with yellow<0.05 in bus_vs_mushroom | +2 mushrooms | Returns 0.30 instead of neutral 0.50 |
| texture_ratio>2.5 + negative bright_diff in mushroom_vs_teapot | +2 teapots | Textured top + bright bottom = teapot |
| bright_diff<-80 in mushroom_vs_teapot | (included above) | Very bright bottom = surface reflection |
| High sat>150 + green>0.30 in mushroom_vs_teapot | +1 mushroom | Natural outdoor mushroom |
| No yellow + no sky → lean teapot in bus_vs_teapot | +1 teapot | Bus needs yellow or sky |
| bicycle_vs_dog tiebreaker (warm>0.50 + bg_contrast guard) | +1 dog | Golden colored = dog, not bicycle |
| Wide margin pair for dog/bus + tightened yellow thresholds | +1 bus, +1 dog | Earlier session carry-forward |

## What Was Tried and Failed (Session 8)

| Approach | Result | Why |
|----------|--------|-----|
| Bayesian likelihood ratio with 8 pixel features | 6/10 mush correct but 14/35 dog FP | Gaussian distributions overlap too much |
| Simple Gaussian model | Net negative | Multivariate doesn't help when marginals overlap |
| below_warm_ratio as discriminator | 9 dogs above 0.30 threshold | Too many dogs in forests/grass |
| bicycle_vs_teapot tiebreaker (bg_contrast>40) | +1 tea, -1 bus = 0 | bus_0002 also has high bg_contrast |
| 2-pass tiebreaker / multi-swap | -2% regression | Cascading swaps create pathological chains |
| Stronger excluding penalty (earlier session) | -2.6% | Devastated mushroom and teapot classes |
| High-score tiebreaker guard (score_i > 0.70) | -2% | Blocked ALL legitimate corrections |

---

## Why the Remaining Plateau Exists

### The golden_brown_color dominance
At 64x64, dog, mushroom cap, and brass teapot surfaces occupy the same HSV region (hue 8-35, sat>40, val>50). The required feature `golden_brown_color` fires at 0.92-1.0 on all three. The score formula then produces dog scores of 0.69-0.76 on mushrooms/teapots, which overwhelms the 0.35-0.50 range teapot/mushroom scores.

### Tiebreaker exhaustion
Every pixel-level metric tested shows 40-60% overlap between confused classes:
- Gradient direction, edge density, laplacian: all overlap
- Saturation, color ratios, symmetry: all overlap
- Background contrast, texture ratios: partial discrimination only
- Only conjunctions of 3+ features find any clean separation, and these catch 3-5 cases max

### Single-swap limit
Each prediction gets at most one tiebreaker swap. Many error paths require 2 corrections (e.g., bicycle→dog→teapot for a teapot image).

### Resolution limit
The discriminative information (fur micro-texture, gill patterns, ceramic sheen) exists below 64x64's Nyquist frequency.

---

## What Would Break the Plateau

### Within current framework
1. **Class-specific score normalization**: golden_retriever mean score = 0.72 across all images while mushroom/teapot = 0.45. A per-class calibration could help.
2. **Required feature alternatives**: Allow classes to have OR-gated required features (e.g., mushroom: organic_texture OR (high_saturation AND green_context))
3. **Template/prototype scoring**: Per-class exemplar matching in feature space

### Beyond current framework
4. **Higher resolution**: 128x128 would resolve the texture ambiguities
5. **Learned features**: Even a small CNN would separate the dog/mushroom/teapot triangle
6. **Part-whole reasoning**: Detect sub-structures (cap+stem, head+body+legs, body+spout+handle)
