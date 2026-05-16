# Optimization Trajectory

Historical accuracy progression and the diminishing returns pattern.

## Session-by-Session Progress

| Session | Start | End | Delta | Key Technique |
|:---:|:---:|:---:|:---:|---|
| 1 | 47.2% | 48.2% | +1.0pp | Histogram differential features in discriminants |
| 2 | 48.2% | 50.1% | +1.9pp | Gap-aware gating, per-pair bases, histogram blending |
| 3 | 47.5%* | 48.75% | +1.25pp | 7 new discriminant pairs, mean-centered histogram |
| 4 | 50.5% | 51.65% | +1.15pp | DCT, Gabor, mid_wider, score calibration, repulsion v3 |
| 5 | 51.7% | 52.8% | +1.1pp | Rank-4 reranking, LAB color moments, FFT h/v ratio |
| 6 | 53.1% | 53.5% | +0.4pp | Hu moments, GLCM contrast, warm_sat_std |
| 7 | 53.5% | 53.6% | +0.1pp | orient_entropy in 2 discriminants |
| 8 | 53.6% | 53.6% | 0pp | All experiments failed (color_purity, warm_cool_a_diff) |
| 9 | 53.6% | 55.1% | +1.5pp | Confidence gates, local verify conditions, margin tuning |
| 10 | 55.1% | 56.7% | +1.6pp | Systematic verify mining (6 new conditions) |
| 11 | 56.7% | 56.95% | +0.25pp | 2 verify conditions, 3 confidence gates |
| 12 | 56.95% | 57.35% | +0.40pp | GR-bear verify, bidirectional verify conditions |
| 13 | 57.35% | 58.15% | +0.80pp | Channel correlations, repulsion pairs, margin/multiplier tuning |
| 14 | 58.15% | 58.15% | 0pp | All experiments failed: contour features, calibration, gates, new discriminants, disc enhancements |

*Session 3 switched to train-only optimization; numbers are train accuracy from here.

## Generalization Audit (end of Session 14)

First comprehensive train/val/test comparison:

| Split | Top-1 | Top-3 | N |
|-------|:---:|:---:|:---:|
| Train | 57.9% | 76.9% | 2000 |
| Val | 52.9% | 75.6% | 2000 |
| Test | 51.1% | 74.4% | 1000 |

**Overall train-val gap: 5.0pp top-1, 1.3pp top-3.**
**Overall train-test gap: 6.8pp top-1, 2.5pp top-3.**

The top-3 gap is small, meaning base scoring generalizes well — the overfitting lives in the ranking post-processing (reranking, local verify, confidence gates).

### Per-Class Generalization

| Class | Train | Val | Test | Train-Val gap |
|-------|:---:|:---:|:---:|:---:|
| banana | 56.5% | 46.0% | 43.0% | +10.5pp |
| brown_bear | 54.0% | 42.5% | 41.0% | +11.5pp |
| golden_retriever | 48.5% | 40.5% | 40.0% | +8.0pp |
| jellyfish | 70.5% | 67.0% | 66.0% | +3.5pp |
| king_penguin | 59.0% | 56.5% | 60.0% | +2.5pp |
| mushroom | 51.0% | 48.0% | 43.0% | +3.0pp |
| orange | 62.5% | 62.0% | 62.0% | +0.5pp |
| school_bus | 76.0% | 67.5% | 69.0% | +8.5pp |
| sports_car | 59.5% | 60.0% | 54.0% | -0.5pp |
| teapot | 41.0% | 39.5% | 33.0% | +1.5pp |

**Worst generalizers**: banana (+10.5pp), brown_bear (+11.5pp) — both heavily rely on overfit verify conditions.
**Best generalizers**: orange (+0.5pp), king_penguin (+2.5pp), jellyfish (+3.5pp) — classes with genuinely distinctive features.

## Phase Transitions

The trajectory shows distinct phases with different return profiles:

### Phase A: Architectural Innovation (Sessions 1-2, +2.9pp)
New pipeline stages added: histogram blending, gap-aware gating, per-pair bases.
Each architectural change provided +0.5pp to +1pp.
**Character**: High return per iteration, changes affect all classes.

### Phase B: Feature Expansion (Sessions 3-6, +3.9pp)
New feature types added: DCT, Gabor, LAB, Hu, FFT, histograms.
Each new orthogonal feature channel provided +0.1pp to +0.6pp.
**Character**: Moderate return, requires identifying truly orthogonal features.

### Phase C: Feature Exhaustion (Sessions 7-8, +0.1pp)
Attempted to add more features of existing types. Almost all failed.
**Character**: Zero return. Signal that the feature space is saturated.

### Phase D: Conditional Logic (Sessions 9-12, +3.75pp)
Shifted to conditional interventions: confidence gates, local verify, margin tuning.
Each verify condition provided +1 to +7 net correct.
**Character**: Moderate return, pair-specific, high precision.

### Phase E: Fine Tuning (Session 13, +0.80pp)
Margin widening, multiplier adjustment, new repulsion pairs.
Each change provided +1 net correct.
**Character**: Low return per change, many reverts, near local optimum.

## Diminishing Returns Curve

```
Accuracy vs Cumulative Iterations (approximate):

58% |                                              *
57% |                                         *
56% |                                   *
55% |                              *
54% |                         *
53% |                   * *
52% |              *
51% |         *
50% |     *
49% |   *
48% |  *
47% | *
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--
    0  25  50 75 100 125 150 175 200 225 250 275 300 330
                    Cumulative iterations
```

The curve shows classic logarithmic diminishing returns. Each doubling of iterations adds less than the previous doubling.

## What Predicts the Next Phase Transition

Historical pattern: progress stalls → new technique type discovered → burst of progress → stall again.

| Stall at | Duration | Breakthrough |
|----------|:---:|---|
| 48.2% | ~20 iterations | Gap-aware gating + histogram blending |
| 51.3% | ~15 iterations | LAB color moments (new feature type) |
| 53.5% | ~30 iterations | Confidence gates + local verify (new intervention type) |
| 57.3% | ~20 iterations | Margin/multiplier tuning (new optimization axis) |
| 58.15% | ~15 iterations (Session 14) | Still searching — contour features, new discs, all exhausted |

**Pattern**: Each breakthrough comes from a genuinely new TYPE of intervention, not from more of the same. The next breakthrough requires finding a new optimization axis that hasn't been explored.

## Candidates for Next Phase Transition

1. **Deeper feature engineering**: Wavelet, contour-based, bilateral features (see orthogonal_features.md)
2. **Spatial features**: 4x4 feature grids instead of scalars (preserves WHERE features activate)
3. **Signature restructuring**: Per-class specialized scoring (different architecture for shape-defined vs color-defined classes)
4. **Conjunctive feature search**: Systematic search over feature pairs with information gain objective

## Per-Class Progress Over Time

| Class | Session 3 | Session 6 | Session 9 | Session 13 | Trend |
|-------|:---:|:---:|:---:|:---:|---|
| banana | 56% | 53% | 51% | 56% | Fluctuates (sink class victim) |
| bear | 41% | 50.5% | 52.5% | 54.5% | Steady improvement |
| GR | 37.5% | 42% | 42% | 49% | Improved recently |
| jelly | 66% | 70.5% | 70% | 70.5% | Plateau (already high) |
| KP | 50.5% | 51.5% | 54.5% | 59% | Steady improvement |
| mushroom | 44.5% | 51% | 52.5% | 51% | Plateau |
| orange | 45% | 57.5% | 63.5% | 63% | Major improvement, plateau |
| bus | 76.5% | 71% | 71.5% | 76% | Fluctuates (gives to others) |
| sports | 49% | 54.5% | 53.5% | 60.5% | Improved recently |
| teapot | 21.5% | 34% | 40% | 41.5% | Improved but structural ceiling |

**Observation**: GR, KP, sports, and bear are the classes with the most room to improve. Teapot has a structural ceiling (~45%). Jelly and bus are near their ceilings (70-78%).
