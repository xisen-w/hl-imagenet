# Composition Architecture Analysis

## Current Non-Linear Mappings

| Mapping | Where Used | Form |
|---------|-----------|------|
| Threshold gate | `_eval_required` | `all(f > 0.1) else 0` — hard AND |
| Min/max clamping | All compound features | `min(score, 1.0)`, `max(0.3, score)` |
| Conditional branch | Tiebreakers | `if X > T: return Y` — discontinuous |
| Ratio computation | `top_textured_bottom_plain` | `top_var / bot_var` — division |
| Product interaction | `stripes_with_nature` | `(crossings/8) * (green*5) * (amp/60)` — multiplicative |
| Tiered thresholds | `dog_vs_teapot` | Different flip threshold based on context |

## Current Combination Types

| Type | Where | Example |
|------|-------|---------|
| Weighted linear sum | `score_node` | `required*0.6 + supporting*0.3 - excluding*0.2` |
| AND (hard) | `_eval_required` | All required must fire |
| OR/MAX | Feature atoms | `yellow OR golden → yellow_dominant` |
| Spatial binding | Compound features | `sky(top) AND yellow(bottom) → bus` |
| Pairwise comparison | Tiebreakers | Compare signal strength between two classes |

## Current Depth Levels (5)

```
Level 0: Raw pixels (64x64x3 BGR)
Level 1: Transforms (HSV, grayscale, edges, Laplacian, Sobel)
Level 2: Regional statistics (mean, std, ratio, crossings, connected components)
Level 3: Compound features (bind spatial + color + texture → single score)
Level 4: Scoring formula (required gate * weighted sum of Level 3 outputs)
Level 5: Tiebreakers (pairwise class comparison using raw image re-analysis)
```

## Proposed Deeper Chains

### 1. Feature-of-Feature (Level 3.5)

Compose existing features into higher-order detectors:
- `teapot_on_table = top_textured_bottom_plain AND distinct_background`
- `zebra_in_field = pure_vertical_stripes AND stripes_with_nature`
- `indoor_object = distinct_background AND NOT outdoor_animal_scene`

Implementation: new feature class that reads other features from the cache rather than raw pixels.

### 2. Spatial Attention (Level 2→3 feedback)

Find a region of interest, then compute features WITHIN that region:
- Find warm blob (connected component) → compute edge density within blob boundary
- Dogs: low internal edge density (smooth fur)
- Mushrooms: high internal edge density (gilled cap, textured surface)
- Teapots: moderate, concentrated at spout/handle edges

This breaks the global-feature ceiling by conditioning analysis on spatial location.

### 3. Relational Chains (Level 3→4)

Relate properties of distinct spatial regions to each other:
- Object A ABOVE Object B AND A BRIGHTER than B → mushroom (cap over gills)
- Object A WIDER than TALL AND has CONCAVITIES → teapot
- WARM region SURROUNDED by GREEN region → outdoor animal

### 4. Iterative Refinement (Level 5→3 feedback)

Use first-pass classification to select a specialized feature bank:
- Pass 1: rough classification → "likely golden_retriever or teapot"
- Pass 2: run dog-vs-teapot-specific feature bank (blob edge density, symmetry, lateral protrusions)
- Output: refined score that overrides pass 1 if confidence is high

This is architecturally the deepest — it creates a loop in the computation graph.

## Priority Order

1. **Spatial attention** — most promising for the dog/mushroom/teapot plateau (edge-within-blob)
2. **Feature-of-feature** — cheap to implement, composes existing signals
3. **Relational chains** — requires clean region segmentation
4. **Iterative refinement** — highest architectural complexity, biggest potential payoff
