# Feature Inventory

All features computed in `_stats()` (phase2_signatures.py), organized by type and orthogonality.

## Color Features (HSV-based)
Core features, heavily used in signatures and discriminants. **Saturated** — adding more of this type is zero-sum.

| Feature | What it measures | Key classes |
|---------|-----------------|-------------|
| warm | Warm pixel coverage | banana(0.64), GR(0.52), bear(0.49) |
| yellow | Yellow pixel coverage | banana(0.46), bus(0.24), teapot-copper |
| hue_red | Red-dominant pixel fraction | orange(0.49), bear(0.32), teapot varies |
| hue_orange | Orange hue fraction | orange, bus, banana |
| sat | Mean saturation | jelly(0.32), banana(0.28), KP(0.12) |
| bw_ratio | Black+white pixel fraction | KP(0.68), teapot-metal(0.72) |
| color_std | Color variation | jelly(0.25), mushroom(0.22), KP(0.04) |
| warm_hue_median | Median hue in warm pixels | GR(16), banana(18), KP(20.5) |
| warm_sat_std | Warm saturation std | banana(0.21), orange(0.16) |
| green / green_region_area | Green pixel features | bear, mushroom (natural backgrounds) |
| warm_val_mean | Mean value in warm pixels | general warmth indicator |

## Spatial Color Features (2x2 grid)
Coarse spatial decomposition. **Partially saturated** — useful for specific pairs.

| Feature | What it measures |
|---------|-----------------|
| warm_tl, warm_tr, warm_bl, warm_br | Warm coverage in quadrants |
| sat_tl, sat_tr, sat_bl, sat_br | Saturation in quadrants |
| top_uniformity | How uniform the top strip is |
| radial_warm_diff | Center vs edge warm difference |

## Edge/Texture Features
General structure features. **Partially saturated**.

| Feature | What it measures | Key classes |
|---------|-----------------|-------------|
| edge | Canny edge density | bus(0.28), sports(0.22), banana(0.08) |
| grad_mean | Mean gradient magnitude | bus(high), sports(high) |
| lap_var | Laplacian variance | bus, sports (high-frequency detail) |
| smooth_warm | Warm AND smooth (conjunction) | banana(high), orange(high) |
| blob_coverage | Largest warm blob fraction | banana, orange |
| autocorr_h | Horizontal autocorrelation | bus, sports (repeating structure) |
| horiz_dominance | H/V edge ratio | bus, sports |
| top_edge, bot_edge | Edge density in top/bottom halves | bus(top), teapot(bottom) |

## LAB Color Space
Orthogonal to HSV. **NOT saturated** — room for more LAB features.

| Feature | What it measures | Best pairs |
|---------|-----------------|-----------|
| cm_a_std | Green-red variation | orange-banana (d=1.30) |
| cm_b_std | Blue-yellow variation | banana-GR (d=1.50) |
| cm_center_a | Center green-red value | GR-KP (d=1.31) |
| cm_center_b | Center blue-yellow value | teapot-banana (d=1.62), bear-GR (d=0.91) |

## Frequency Domain
Orthogonal to spatial features. **Partially explored**.

| Feature | What it measures | Best pairs |
|---------|-----------------|-----------|
| dct_low | Low-frequency DCT energy | bear-GR (d=0.62) |
| dct_mid | Mid-frequency energy | general structure |
| dct_high | High-frequency energy | mushroom-banana (d=0.91), sports-bus (d=0.72) |
| dct_mid_over_low | Texture complexity ratio | |
| fft_hv_ratio | H/V FFT energy ratio | bear-KP (d=0.93) |
| vert_regularity | Vertical edge periodicity | bus, sports vs teapot, jelly |

## Gabor Texture
Oriented texture. **Partially explored** — only 4 orientations × 2 frequencies.

| Feature | What it measures | Best pairs |
|---------|-----------------|-----------|
| gabor_0_04_var | 0° fine texture | bus-sports (d=0.98) |
| gabor_45_04_var | 45° fine texture | bear-GR (d=0.91) |
| gabor_90_01_mean | 90° coarse texture | banana-mushroom (d=0.96) |
| gabor_dominant_orient | Dominant orientation | teapot-KP (d=0.88) |

## Shape/Moment Features
Edge shape descriptors. **Not saturated** — higher Hu moments unexplored.

| Feature | What it measures | Best pairs |
|---------|-----------------|-----------|
| hu1 | Shape complexity (log-scale) | mushroom-banana (d=1.09), GR-banana (d=1.11) |
| hu2 | Shape elongation (log-scale) | mushroom-banana (d=1.16) |
| mid_wider | Is middle third widest? (binary) | teapot-KP (d=1.17) |
| mid_width_ratio | Quantitative mid-wider | |
| binary_complexity | Edge complexity measure | teapot(high) — but dangerous in signatures |

## Gradient/Entropy
**Partially explored**.

| Feature | What it measures | Best pairs |
|---------|-----------------|-----------|
| orient_entropy | Gradient direction diversity | sports-teapot (d=1.11) |
| hue_entropy | Hue diversity | bear-mushroom (d=1.39 within, 0.24 cross) |

## Channel Correlations
Recently added. **Not saturated**.

| Feature | What it measures |
|---------|-----------------|
| rb_corr | Red-blue channel correlation |
| gb_corr | Green-blue correlation |
| rg_corr | Red-green correlation |
| mean_ch_corr | Mean of all correlations |
| center_bright_ratio | Center/overall brightness ratio |

## Histogram Prototype Scores
Class-specific histogram similarities. Used in blending and discriminants.

| Feature | What it measures |
|---------|-----------------|
| hist_{class} | Chi-squared similarity to class's hue-sat prototype |
| hist_{A}_minus_{B} | Differential histogram (14 pairs) |

## Features Added But Not Used in Discriminants
These were added to _stats() but failed when deployed. Kept for potential future use.

- **hue_entropy**: Cross-class d' too low despite high within-class d'
- **rb_ratio, gb_ratio**: Correlated with existing color features
- **color_purity**: d' too low for hard cases
- **warm_cool_a_diff**: Hurt both classes when deployed
- **sat_pixels_ratio**: Net negative
- **GLCM contrast**: Only useful in specific pairs, not broadly deployed

## Saturation Status Summary

| Feature Type | Status | Room for growth |
|-------------|--------|:---:|
| HSV color | Saturated | Low |
| Spatial color | Partially saturated | Medium |
| Edge/texture | Partially saturated | Low |
| LAB | Not saturated | High |
| DCT/FFT | Partially explored | Medium |
| Gabor | Partially explored | Medium |
| Shape/moments | Not saturated | Medium |
| Channel correlations | Not saturated | Medium |
| Contour-based | **Unexplored** | High |
| Wavelet | **Unexplored** | High |
| Bilateral/asymmetry | **Unexplored** | Medium |

## The Feature Quality Ceiling (Session 27-28)

Evidence from the anycode forest experiment reveals that 90 hand-crafted features reach a **hard ceiling of ~64% val** regardless of the combination method:

| Combination method | Val accuracy |
|---|---|
| KNN (memorized) | 41.2% |
| GNB (independent) | ~40% |
| Phase 2 sigmoid pipeline (base+reranking only) | 51.9% |
| Compiled forest (101 trees, bagged) | **64.4%** |
| Compiled forest (101 trees, boosted) | 62.9% |
| Compiled forest with TTA | 64.1% |
| Compiled forest with augmented training | 63.5% |
| CNN on raw pixels (for reference) | 71.8% |

**The 64.4% ceiling is feature-quality limited, not architecture-limited.**

### Why features cap out at ~64%

The 90 features are overwhelmingly GLOBAL statistics: `mean(s)`, `mean(h in warm pixels)`, `var(laplacian)`. These collapse a 64×64×3 = 12,288-dimensional input to 90 scalars. The information loss is massive:

1. **Spatial erasure**: `mean(saturation)` is the same whether saturation is concentrated in the center (fruit) or at the edges (vehicle). The tree can't distinguish "yellow top + dark bottom" (bus) from "yellow everywhere" (banana) without explicit spatial features.

2. **Object vs background mixing**: `mean(green_pixels)` mixes foreground and background. A bear in front of green grass and a mushroom with a green background produce similar values.

3. **Composition blindness**: The features can't express "round bright object in center against dark background" (orange) vs "elongated bright object in center" (banana). No combination of global scalars encodes spatial RELATIONSHIPS between regions.

### The 7.4pp gap to CNNs

The CNN achieves 71.8% val on the same task. The extra 7.4pp comes from:
- **Learned spatial filters** that capture local structure
- **Hierarchical composition** (edges → textures → parts → objects)
- **Position-sensitive features** that know WHERE patterns occur

To close this gap with hand-crafted features would require features that encode:
1. Object shape (contour descriptors, skeleton-based features)
2. Spatial relationships (relative positions of colored regions)
3. Part-based composition (structured patches, not global statistics)

These are the features that the Phase 2 system's "spatial grid" partially attempts — but the 2×2 or thirds grid is far too coarse to capture the discriminative structure that a CNN's 3×3 kernels across multiple layers capture.

### Attempted spatial feature sets (Session 29, all worse)

| Feature set | n_features | Val alone | Combined with 90 | Problem |
|---|---|---|---|---|
| HOG-like (4×4 orientation histograms) | 90 | 40.7% | 64.0% | Too noisy at 64×64 |
| Dense spatial grid (4×4 × 5 stats) | 90 | 54.9% | — | Overfits (37.4pp gap) |
| Patch relationships (4×4 + diffs) | 102 | 50.5% | 63.1% | Severe overfit (41.9pp gap) |
| Radial rings + shape | 10 (replacement) | — | 63.9% | Not better than replaced features |

**Why all spatial features fail at 64×64**: Objects are not consistently positioned in the frame. A 4×4 grid (16px cells) is fine enough to be position-sensitive but too coarse to capture actual object structure. The sweet spot (2×2 grid) works precisely because it's coarse enough to be position-invariant while still encoding gross layout (top-heavy vs bottom-heavy).

**The paradox**: To capture spatial information that helps, you need fine spatial resolution. But fine spatial resolution at 64×64 overfits to object placement. CNNs solve this via learned translation-invariant filters — hand-crafted grids cannot.
