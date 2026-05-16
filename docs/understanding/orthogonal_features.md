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
