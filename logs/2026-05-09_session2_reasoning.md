# Session 2: 2026-05-09 — Iteration 7-19 + Architectural Ceiling Analysis

## Starting State
- Previous session hit macOS sandbox permission issue, couldn't access original repo at ~/Desktop
- Cloned fresh from GitHub into /private/tmp/hl-imagenet
- Committed code was pre-flat-scoring (hierarchy-only), ~12% accuracy
- Had to re-apply all improvements from "update" branch that was never pushed

## Key Changes Applied
1. **Flat scoring** — evaluate ALL leaf classes, skip gate filtering (biggest single win)
2. **Updated color ranges** — orange H10-20, golden H20-35, yellow H35-70
3. **Relaxed required features** — school_bus only needs yellow_dominant, golden_retriever only needs golden_brown_color
4. **raw_image stored in SceneGraph** — enables HSV pixel-level analysis in features
5. **Teapot reworked** — required=organic_texture (fires 20/20), excludes yellow/striped/green
6. **Fixed shape_features.py** — removed invalid `raw=` kwarg from FeatureValue.detected()

## Iteration Results

| Iter | Top-1 | Key Change | Result |
|------|-------|-----------|--------|
| 7a | 22.7% | Stricter striped_texture + golden_brown reject orange-dominant | Hurt zebra & retriever |
| 7b | 18.2% | bw_coverage required for stripes | Over-restricted stripes |
| 7c | 25.5% | bird_like made much stricter | Eagle no longer dominates |
| 7d | 17.3% | golden_brown: orange partial (0.3x) | Killed retriever |
| 7e | 19.1% | golden_brown HSV-based (sat<0.45) | Too selective |
| 8 | 19.1% | Fixed raw_image access in golden_brown | golden_brown still fires broadly |
| 9 | 20.0% | Increased excluding penalty to 0.4 | Too harsh |
| 10 | 17.3% | Vivid yellow (sat>140) + coverage thresholds | Still fires on retrievers |
| 11 | 21.8% | Back to simple golden_brown (golden+brown+orange regions) | Baseline recovery |
| 12 | 21.8% | Relaxed striped, golden_brown sat<0.52 | Broad golden fires |
| 13 | **28.2%** | Full revert to simple color_region approach | **Back to baseline** |
| 14 | **30.0%** | Teapot: required=organic_texture, excl=quadruped+golden+etc | **New high!** |
| 15 | 26.4% | golden_brown: orange only 0.3x contribution | Hurt retriever |
| 16 | 29.1% | Removed organic from bus excluding | Slight regression |
| 17 | 25.5% | MAX-based excluding penalty | Killed teapot |
| 18 | 25.5% | Top-2 excluding | Same issue |
| 19 | **30.9%** | Reverted scorer, simplified teapot excludings | **Best!** |

## Best Result: 30.9% Top-1, 54.5% Top-3

| Class | Accuracy | Notes |
|-------|----------|-------|
| zebra | 100% | Synthetic — stripes+bw works |
| bicycle | 100% | Synthetic — wheel_like works |
| golden_retriever | 65% | golden_brown(orange+golden+brown) reliable |
| teapot | 30% | organic_texture + exclusions |
| mushroom | 25% | organic_texture as discriminator |
| school_bus | 0% | yellow_dominant only fires 6-13/20, always beaten |
| eagle | 0% | bird_like too strict (correctly) |
| banana | 0% | yellow+elongated fires on too many things |
| laptop | 0% | screen_rectangle never fires at 64x64 |
| piano | 0% | keyboard_pattern never fires at 64x64 |

## Fundamental Ceiling Analysis

**Why 30% is the ceiling for this approach:**

1. **Texture is non-discriminative at 64x64** — LBP entropy ≈ 2.0 for ALL classes. smooth_texture never fires, organic_texture always fires. Cannot separate teapot from mushroom.

2. **Color overlap is inescapable** — school_bus (H10-20, sat>130) vs golden_retriever (H10-25, sat<80) share warm spectrum. Any threshold catches both.

3. **Shape features broken at 64x64** — wheel_like, handle_spout, rectangular_shape fire 0-1/20 on targets. Not enough resolution for contour/circle detection.

4. **Feature space has low rank** — organic_texture (10/10 classes), bilateral_symmetry (10/10), quadruped_like (9/10) are non-discriminative. The "feature bag" collapses many classes into identical vectors.

## What's Missing: Spatial Binding

Current system: "what features exist?" (v1)
Needed: "how are features arranged?" (v3)

The breakthrough is not more features, it's **relations between features**:
- "yellow body contains dark horizontal windows" = school_bus
- "black-white stripes cover central region" = zebra
- "rounded cap above thin stem" = mushroom

## Next Steps (v2 Architecture)
1. Spatial grid features (3x3 color/edge maps)
2. Layout predicates (yellow_center_mass, dark_band_above_body)
3. Weak evidence pools (wheel_evidence = weighted sum of clues)
4. Pairwise confusion resolvers (bus vs zebra, teapot vs mushroom)
5. Prototype matching (multiple layout signatures per class)
6. Foreground/background split (center crop, non-border colors)
