# Orthogonal Features

The single most reliable way to improve accuracy without zero-sum tradeoffs. A feature is "orthogonal" if it measures a genuinely different image property from existing features, so deploying it in one discriminant doesn't affect other discriminants.

## Why Orthogonality Matters

With ~80 features, all 10 class signatures and all 24 discriminants draw from the same pool. Boosting one class on feature X necessarily creates false positives for another class that also correlates with X. This is the zero-sum trap.

**Orthogonal features break the trap** because they create separation along a NEW axis that doesn't participate in existing zero-sum dynamics. The evidence:

- **LAB features** (+0.6pp, no regressions in non-target pairs): cm_a_std, cm_b_std, cm_center_a, cm_center_b measure green-red and blue-yellow axes. These are mathematically orthogonal to HSV features.
- **Hu moments** (+0.3pp, stable): hu1, hu2 measure edge shape complexity and symmetry — unrelated to edge density or magnitude.
- **DCT frequency bands** (+0.25pp, stable): dct_low/mid/high measure spatial frequency content — unrelated to pixel-level color or edge features.
- **Gabor texture** (+0.4pp, stable): oriented texture at specific frequencies — captures structure invisible to isotropic features.

Contrast with **non-orthogonal additions**: warm_sat_std was correlated with existing warm/sat features → net zero when deployed broadly. hue_entropy was correlated with color_std → failed in discriminants.

## Feature Orthogonality Map

| Feature Type | Orthogonal To | Correlated With |
|-------------|--------------|-----------------|
| **HSV scalars** (warm, sat, yellow, etc.) | DCT, Hu, LAB | Each other, histogram scores |
| **Edge/texture** (edge, lap_var, grad_mean) | LAB, color features | GLCM, Gabor (partially) |
| **Histogram prototypes** (hist_X_minus_Y) | Shape features | HSV (indirectly, via color distributions) |
| **LAB moments** (cm_a_std, cm_center_b) | HSV, edge | Each other (partially) |
| **Hu moments** (hu1, hu2) | Color, HSV | Edge (weakly) |
| **DCT bands** (dct_low, dct_mid, dct_high) | Color, LAB | Edge (weakly) |
| **Gabor** (gabor_*_var, gabor_dominant_orient) | Color, LAB | Edge, DCT (partially) |
| **FFT ratio** (fft_hv_ratio) | Color | Edge (weakly) |
| **Orient entropy** | Color | Edge (moderately) |

## How to Identify Orthogonal Features

1. **Compute correlation with existing feature matrix**: If a candidate feature has |r| < 0.3 with ALL existing features, it's orthogonal.
2. **Check different image property**: If it measures a fundamentally different physical quantity (color vs frequency vs shape vs texture), it's likely orthogonal.
3. **Deploy and check for cascade**: Orthogonal features don't cause cascade regressions in non-target pairs. If you see cascade effects, the feature is correlated with something in the pipeline.

## Unexplored Orthogonal Directions

These feature types have not been fully explored and are likely orthogonal to existing features:

1. **Wavelet coefficients**: Multi-scale decomposition. Captures structure at different spatial scales. Different from DCT (which is fixed-grid, not localized).

2. **Contour-based features** (PARTIALLY EXPLORED, Session 14): n_contours_norm and contour_fill_ratio computed. High within-class d' but failed in discriminants — adding to bear-GR (d'=+1.54) caused -1 net. Adding to banana-mushroom (d'=-3.0 cross-class) caused -2 net in already-saturated discriminant. **Status**: Features computed in _stats() but not deployed. May work in less saturated contexts.

3. **GLCM at new parameters**: Current GLCM uses horizontal adjacency only. Diagonal and vertical GLCM, or GLCM at distance=2, would capture different texture patterns.

4. **Color co-occurrence**: Which colors appear adjacent to each other. A bus has yellow-next-to-yellow (solid panels) while a banana has yellow-next-to-neutral (fruit on background).

5. **Bilateral features**: Left-half vs right-half asymmetry in various features. Captures objects with distinct sides (sports car profile, teapot with handle on one side).

## Deployment Protocol for Orthogonal Features

1. Compute feature on all 2000 train images
2. Find pairs where cross-class d' > 0.8
3. Add to discriminant for that pair with CONSERVATIVE sigmoid (start with scale=3-5, not 30-40)
4. Eval. If net positive: keep. If net zero: increase scale. If net negative: the feature is correlated with something — remove.
5. Do NOT add to base signatures (cascade risk too high).

## Status at 70.0% (Session 20)

Most profitable orthogonal features have already been deployed:
- LAB moments: deployed in 8+ discriminants
- Hu moments: deployed in 4 discriminants
- DCT bands: deployed in 6 discriminants
- Gabor texture: deployed in 5 discriminants
- FFT ratio: deployed in 3 discriminants
- Orient entropy: deployed in 2 discriminants

**Remaining opportunities**:
1. **Wavelet coefficients** — not yet explored. Multi-scale decomposition captures structure at different spatial scales.
2. **GLCM at distance=2** — current GLCM is horizontal adjacency only. Diagonal/vertical at distance=2 would capture different texture patterns.
3. **Bilateral features** — left/right asymmetry. Useful for sports_car (profile), teapot (handle on one side).
4. **Color co-occurrence** — which colors appear adjacent. Bus has yellow-next-to-yellow vs banana has yellow-next-to-neutral.
5. **Spatial grid features (4x4)** — the biggest untapped direction. Currently ALL features are image-global scalars. A 4x4 grid would preserve WHERE features activate, enabling spatial/shape discrimination that's currently impossible.

The spatial grid approach is the most promising because it addresses the FUNDAMENTAL bottleneck — the system has no spatial awareness at all. Every feature collapses the 64x64 image to a single scalar.

## Session 21 Finding: Spatial Features Are Discriminative But Undeployable

Spatial grid features (4x4 grid of edge/warm/intensity) achieve d'=1.08-1.29 on top confusion pairs. Specifically:
- `spatial_mid_warm`: d'=1.08 for teapot-banana, 0.93 for sports-bus
- `spatial_bot_intensity`: d'=1.11 for GR-mushroom
- `spatial_center_surround` (via grid): d'=1.29 for mushroom-bear

**But all deployment attempts failed**:
- In discriminants: -2 to -6 cascade (every discriminant change affects 496 downstream rescues)
- In verify conditions: -4 cascade (Pattern 10 — adjacent pairs disrupted by swaps)

The features ARE orthogonal and discriminative. The PIPELINE cannot absorb them at 70.0%. Possible solutions:
1. Separate scoring pathway (independent ensemble member)
2. Final arbitration stage that breaks ties without swapping established rankings
3. Complete pipeline rebuild around spatial features as primary scoring
4. Use spatial features only at rank-5+ level where cascade radius is smaller

## Anycode Forest Validation (Session 27)

The anycode compiled forest experiment provides evidence that orthogonal features generalize better when combined via trees than when injected into the saturated sigmoid pipeline:

| Feature set | Forest val accuracy |
|---|---|
| 71 original features (HSV + spatial grid + thirds) | 58.8% |
| + LAB, DCT, Gabor, FFT, Hu, GLCM (= 90 features) | **63.7%** |
| + spatial 3x3 grid + shape + color dist (= 117 features) | 63.1% (WORSE) |

**Key findings**:
1. LAB/DCT/Gabor/FFT are genuinely orthogonal — they give +4.9pp val in a tree ensemble
2. Adding MORE non-orthogonal features (finer spatial grids that overlap with existing spatial features) actually HURTS because it dilutes the feature subsampling
3. The 90-feature sweet spot has high diversity and low redundancy — exactly the "orthogonal and compact" ideal
4. Trees handle feature interactions automatically — no manual discriminant tuning needed

This validates the Phase 2 finding that these feature types are discriminative, while showing that the deployment mechanism (trees vs sigmoid pipeline) determines whether they generalize. The same features that caused cascade regressions in the sigmoid pipeline (+0.25-0.6pp each, carefully) deliver +4.9pp collectively in a tree ensemble because trees handle interactions without cascade risk.

## The Exhaustive Search for Feature Orthogonality (Session 29)

After reaching 64.4%, three additional orthogonal feature types were tested:

| Feature type | Individual val | Orthogonal to existing? | Why it failed |
|---|---|---|---|
| HOG (spatial gradient orientations) | 40.7% | Partially (captures edge direction) | Too noisy at 64×64 resolution |
| Dense spatial color (4×4 grid × 5 stats) | 54.9% | No (overlaps with existing spatial features) | Overfits to object position |
| Patch relationships (adjacent diffs) | 50.5% | Partially (captures spatial transitions) | Position-sensitive → overfit |

**Lesson**: True orthogonality requires both:
1. **Information content**: The feature must carry signal about class membership
2. **Generalization**: The signal must be robust across train/val (position-invariant, scale-invariant)

HOG passes test 1 weakly (40.7%) but FAILS test 2 (93% train → only 40.7% val = 52pp gap!). Spatial color grids FAIL test 2 (92% train → 50-55% val = 37-42pp gap). The existing 90 features represent the rare combination of both: genuinely discriminative AND generalizable at 64×64.

**What would be truly orthogonal AND generalizable?**
- Local features that are position-invariant (histogram of local descriptors, bag-of-words)
- Multi-scale features (wavelet pyramids that pool across positions)
- Learned representations (autoencoders, SimCLR — but these cross into "learned features" territory)

These are the feature directions most likely to attack the 7.4pp gap to CNNs. They all share one property: they capture local structure (what patterns exist) while discarding global position (where in the image), which is exactly what CNNs do via translation-equivariant convolutions + global average pooling.
