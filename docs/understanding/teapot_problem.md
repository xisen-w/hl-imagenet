# The Teapot Problem

Teapot is the system's hardest class (40% accuracy, barely 4x random baseline). It illustrates the fundamental limit of classifying shape-defined objects with color/texture features.

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

## The Three Teapot Failure Modes

### 1. Cold metallic teapots → king_penguin (42 errors)
Profile: warm=0.06, sat=0.14, bw=0.72. These are silver/dark teapots with low saturation.
28/42 have teapot at rank ≤ 3 → partially recoverable by reranking.
Current discriminant uses: hue_red, warm, sat_bl, hist_teapot_minus_kp, mid_wider, color_purity.
Verify conditions catch some (autocorr_h > 0.16 AND horiz > 1.1).

### 2. Warm/copper teapots → banana (27 errors)
Profile: yellow=0.50, warm=0.72, smooth_warm=0.65. Copper/brass teapots with banana-like coloring.
Only 1/27 has teapot as #2. Most have teapot at #3-#5 or unranked.
**This means pairwise reranking cannot fix most of these.** Teapot's base score is too low to even be in contention.

### 3. Mixed teapots → multiple classes (24 → GR, 12 → mushroom, etc.)
These scatter across all classes because teapot's base score is weak everywhere.

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

## What Would Fix Teapot

1. **Higher resolution** (128x128 or 256x256): Handle and spout become visible as distinct structures
2. **Explicit shape detectors**: Hough transform for circles/lines, contour analysis for handle-like protrusions
3. **Template matching**: Spatial correlation with a teapot silhouette template
4. **Exemplar memory**: Store diverse teapot examples and match by spatial similarity

None of these are feasible within the current scalar-feature pipeline. Teapot's ceiling in this architecture is approximately 40-45%.

## Teapot as a Canary

Teapot performance is a proxy for the system's shape-recognition capability. If accuracy improves significantly (say, to 55%+), it would indicate a fundamental advance in the representation. If it stays at 40%, the system remains color/texture-limited.

Current: 40% (83/200 correct on train)
