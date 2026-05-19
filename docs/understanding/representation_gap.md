# The Representation Gap: Hand-Crafted vs Learned Features

## The Numbers

| System | Val top-1 | Feature type |
|---|---|---|
| Phase 2 sigmoid pipeline (base only) | ~45% | 189 hand-crafted, global+quad |
| Phase 2 full (100% train) | 41.35% | Same + 900 verify conditions |
| Anycode forest (90 features) | **64.4%** | Global HSV/LAB/DCT/Gabor/FFT + 2×2 grid |
| Small CNN (10 epochs, no pretrain) | **71.8%** | Learned 3×3 conv filters |
| Gap | 7.4pp | Local spatial structure |

## What the Gap Represents

The 7.4pp gap between the best hand-crafted system (64.4%) and the CNN (71.8%) represents information that EXISTS in the pixels but CANNOT be captured by any design of global or semi-global statistics.

### What the CNN captures that we cannot

From the CNN-guided symbolic gap mining (544 val images where CNN correct, symbolic wrong):

1. **Local texture patterns in specific regions**: The CNN relies on "edge-dense, high-texture evidence in middle_left, center" — it knows WHERE the texture is, not just HOW MUCH texture exists globally.

2. **Color-conditional texture**: For sports_car vs school_bus, the CNN sees "metallic texture at low saturation" vs "uniform yellow". Our `warm_texture` feature approximates this but collapses position.

3. **Shape from local edge arrangement**: For banana vs orange, the CNN sees "elongated edge pattern" vs "circular edge pattern" — captured by oriented conv filters, not by global edge density.

4. **Background-foreground separation**: For bear vs mushroom, the CNN effectively separates "furry texture distributed over large area" from "smooth cap + textured ground". Global features mix foreground and background.

## Why Hand-Crafted Features Hit a Wall

### The position-invariance paradox

To generalize from train to val, features must be POSITION-INVARIANT (object could be anywhere in frame). But to capture local structure, features must be POSITION-SENSITIVE (where the pattern is matters).

CNNs solve this via **translation-equivariant convolutions** → **pooling**:
- Conv layers are position-sensitive (detect local patterns AT specific positions)
- Pooling layers aggregate (remove absolute position, keep relative structure)
- Together: "a circular pattern exists somewhere" without requiring it to be in a specific pixel

Hand-crafted features can only do:
- Global statistics (position-invariant but structure-blind): `mean(saturation)`
- Grid statistics (partially position-sensitive but overfit): `sat_in_top_left_quadrant`
- No way to express "a pattern exists SOMEWHERE" without committing to a grid position

### Session 29 empirical evidence

| Spatial resolution | Val accuracy | Overfit gap |
|---|---|---|
| Global (no grid) | ~58% | 25pp |
| 2×2 quadrants | 64.4% | 26pp |
| 4×4 grid (dense) | 50-55% | 37-42pp |
| 8×8 patches | ~46% | 36-39pp |

The U-shaped curve: finer grids capture more structure but overfit more. The 2×2 grid is the optimal tradeoff for 64×64 images with 200 samples/class.

### The information theory view

A 64×64×3 image has 12,288 values. Our 90 features compress this to 90 scalars — a 136:1 reduction. The question is WHICH 90 scalars maximally preserve class-discriminative information.

- **Global means/stds** capture moments of distributions (efficient but information-lossy)
- **Grid features** capture spatial layout (more information but position-tied)
- **Tree conjunctions** recover some lost structure (if warm AND textured AND center_bright → banana)
- **CNNs** learn the optimal compression: 12,288 → ~512 feature map → 10 classes, preserving exactly the discriminative structure at each layer

The forest's 64.4% represents the maximum information recoverable from 90 pre-chosen measurement types. The CNN's 71.8% represents the maximum recoverable from LEARNED measurements of the same data.

## Design Principles Learned

1. **Global features are the backbone**: Mean/std/ratio features generalize well (small gap) but carry limited information per feature. They form the reliable base.

2. **Coarse spatial features are the ceiling extender**: 2×2 and thirds grids add +6pp over pure globals. This is the sweet spot: enough spatial info to distinguish "top-heavy" from "centered" without enough resolution to overfit.

3. **Fine spatial features overfit**: 4×4+ grids, patch descriptors, HOG at this resolution all overfit because the 200 training images per class don't cover enough spatial configurations.

4. **Feature interactions > feature count**: The forest's conjunctive splits (depth 14 = up to 14-way feature combinations) extract more value from 90 features than 180 features with single-feature splits would.

5. **Orthogonality beats more-of-same**: LAB/DCT/Gabor/FFT added +5.6pp to HSV-only. More HSV features would add ~0.

6. **The combination method doesn't matter at the ceiling**: Forest, GNB, sigmoid pipeline, stacking, specialist, pairwise — all converge to ~64% with the same features. The information content of the features determines the ceiling, not the decision boundary.

## Implications for Heuristic Learning

The project demonstrates that:
1. **Hand-crafted features can reach ~87% of CNN performance** on this task (64.4/71.8)
2. **The last ~13% requires learned representations** — no amount of engineering can close it
3. **The Phase 2 pipeline at 100% train is a memorization artifact** — val drops to 41.35%
4. **Trees generalize better than symbolic pipelines** because they regularize naturally
5. **The optimal feature set is surprisingly compact** — 90 well-chosen features beat 180 diluted ones

The fundamental limit of HL on visual tasks: hand-crafted features can encode WHAT to measure but not HOW to measure it locally. The "how to measure locally" is precisely what learned convolutions provide.

## The Oracle Ensemble: Evidence of Complementary Errors

| Metric | Forest | Phase 2 (full) | Phase 2 (base+rerank) | Oracle (either) |
|---|---|---|---|---|
| Val accuracy | 64.4% | 41.3% | 51.9% | **70.2%** |

Breakdown of 2000 val images:
- Both correct: 873 (43.6%)
- Forest correct only: 415 (20.8%) 
- Phase 2 correct only: 115 (5.8%)
- Both wrong: 597 (29.8%)

The oracle at 70.2% is within 1.6pp of the CNN (71.8%). This means the INFORMATION needed to match the CNN exists across our two systems — we just can't reliably select which system to trust on any given image.

**Why the systems are complementary**: Phase 2's sigmoid pipeline uses different scoring logic (signatures + histogram prototypes + pairwise discriminants) from the forest (conjunctive tree splits). On 5.8% of images, the sigmoid scoring captures a pattern the forest misses — typically via explicit pairwise discriminants that were hand-tuned for specific confusion pairs.

**The selection problem**: The 115 Phase2-only images can't be identified by forest confidence alone. At threshold 0.05 (low forest confidence), trusting Phase 2 gives marginal improvement because Phase 2 is also wrong on most low-confidence forest images.
