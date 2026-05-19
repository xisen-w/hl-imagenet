# The Teapot Problem

Teapot is the system's hardest class (58.5% accuracy at Session 20, up from 40% at Session 13). It illustrates the fundamental limit of classifying shape-defined objects with color/texture features — but also shows how far conditional logic can push a fundamentally weak base scorer.

## Why Teapot Is Shape-Defined

Teapots are identified by spatial configuration: handle on one side, spout on the other, rounded body, often a lid. None of these properties are visible in scalar color/texture statistics. A metallic teapot and a metallic penguin have nearly identical feature vectors:

| Feature | Metallic teapot (lost to KP) | King penguin | d' |
|---------|:---:|:---:|:---:|
| warm | 0.06 | 0.08 | 0.09 |
| sat | 0.14 | 0.12 | 0.15 |
| bw_ratio | 0.72 | 0.68 | 0.22 |
| edge | 0.18 | 0.21 | 0.19 |
| color_std | 0.04 | 0.05 | 0.08 |

**The feature vectors are essentially identical.** No classifier operating in this feature space can separate them.

## The Three Teapot Failure Modes (updated at 70.0%)

### 1. Cold metallic teapots → king_penguin (significantly reduced from 42)
Profile: warm=0.06, sat=0.14, bw=0.72. Silver/dark teapots with low saturation.
**Progress**: Exhaustive verify scan + rank-3/4/5 invention recovered many. Best remaining features: cm_b_skew (d'=1.09), fft_hv_ratio (d'=1.01) — but deploying in signature caused -20 cascade.
**Status**: Individual condition mining exhausted for this pair.

### 2. Warm/copper teapots → banana (20 remaining, down from 27)
Profile: yellow=0.50, warm=0.72, smooth_warm=0.65. Copper/brass teapots.
**Progress**: Rank-3/4/5 verify made previously unreachable errors addressable. cm_center_b + orient_entropy conditions.
**Remaining**: 20 errors have teapot at rank 6+ — completely unreachable by any verify approach.

### 3. Mixed teapots → multiple classes (15 → GR, reduced from 24)
These scatter across all classes because teapot's base score is weak everywhere.
**Progress**: Some recovered via rank-3/4/5 verify targeting teapot-GR, teapot-bear conditions.

## What We've Tried

### Partially worked:
- **mid_wider** (binary: is edge-spread widest in middle third): teapot=0.78, KP=0.39, d=1.17. Used in teapot-KP discriminant: +3pp teapot.
- **orient_entropy** in teapot-banana discriminant: +1.5pp teapot.
- **Local verify conditions**: teapot-banana (cm_b + orient_entropy), teapot-KP (autocorr_h + horiz), teapot-GR (edge + horiz), teapot-bear (hu1). Cumulative +4pp.
- **Confidence gate at 0.35**: catches some FPs but #2 candidate is often wrong.

### Failed:
- **binary_complexity in teapot signature**: -28 regression. Signature changes cascade catastrophically.
- **Calibration boost (+0.01)**: -11 regression. Raises teapot score for ALL images.
- **Horizontal symmetry**: d=0.04 at 64x64. Not discriminative.
- **Foreground center-of-mass, aspect ratio**: d < 0.4.
- **color_purity in teapot-KP disc**: net zero.
- **Teapot hist blend weight**: neutral.

## The Structural Problem

At 64x64 resolution, shape information is severely degraded:
- A teapot handle is ~4-6 pixels wide → barely distinguishable from noise
- Spout is similarly small
- The "rounded body with protrusions" shape is not captured by any of our statistical features

The only shape-adjacent features that work are:
- **mid_wider**: coarse shape proxy (middle wider than top/bottom)
- **horiz_dominance**: horizontal autocorrelation (teapots have horizontal extent)
- **orient_entropy**: gradient direction diversity (teapots have multi-oriented edges)

These provide d = 0.8-1.2, which is enough for marginal reranking gains but not enough to reliably identify teapots as rank 1.

## What HAS Worked for Teapot (40% → 58.5%)

The +18.5pp gain came ENTIRELY from post-processing, not base scoring:
- **Base scoring**: Still only 14.5% (29/200). The signatures are too weak.
- **Reranking**: Teapot-KP, teapot-banana, teapot-GR discriminants recover ~30 images.
- **Verify conditions (4 rank levels)**: ~50 images recovered across all verify stages.
- **Rank-3/4/5 invention**: Made previously unreachable errors (teapot at rank 3-5) addressable for the first time.
- **Confidence gate at 0.35**: Catches some FPs where teapot is falsely ranked #1 with low score.

This proves that conditional logic can push accuracy FAR beyond what base scoring achieves — but at the cost of overfitting (teapot train/val gap is relatively low at +1.5pp only because teapot is bad on BOTH splits).

## What Would Fix Teapot Further

1. **Higher resolution** (128x128 or 256x256): Handle and spout become visible as distinct structures
2. **Spatial features (4x4 grids)**: Teapot has distinctive spatial layout (wider in middle, protrusions on sides). Currently all features are image-global scalars.
3. **Explicit shape detectors**: Hough transform for circles/lines, contour analysis
4. **Template matching**: Spatial correlation with a teapot silhouette template

The fundamental bottleneck is the 14.5% base score. If base scoring could reach 30% for teapot (like bear/GR), then existing verify machinery would push teapot to 70%+. But signature changes cascade catastrophically (-20 to -33 regression).

## Teapot as a Canary

Teapot performance is a proxy for the system's shape-recognition capability. The improvement from 40% to 58.5% came from CONDITIONAL LOGIC, not better representation. Base scoring at 14.5% means the system still cannot reliably IDENTIFY teapots — it can only CORRECT misidentifications after the fact.

Current: 58.5% (117/200 correct on train), base scoring only: 14.5% (29/200)
