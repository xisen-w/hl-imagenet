# Session 1: Initial Build + First 3 Iterations

**Date**: 2026-05-09  
**Duration**: ~45 min  
**Starting accuracy**: 0% (no system existed)  
**Ending accuracy**: 18.2% top-1 (best), 9.1% (latest after regression)

---

## What was built

Full pipeline from scratch:
- 10 sensors (classical CV operators for 64x64 Tiny ImageNet images)
- 21 hand-written features (color, shape, texture, parts, concepts)
- Hierarchical classifier with coarse-to-fine routing
- Proof generator
- Evaluation harness

## Dataset

- 4 real classes from Tiny ImageNet (64x64): school_bus, golden_retriever, mushroom, teapot (50 images each)
- 6 synthetic classes (5 images each): zebra, bicycle, eagle, piano, laptop, banana
- Total: 230 images, evaluated on 20 per class = 110 images

## Iteration Results

| Iter | Top-1 | Top-3 | Key Change |
|------|-------|-------|------------|
| Baseline | 12.7% | 40.9% | First run. Eagle massively over-predicted |
| 1 | 15.5% | 40.0% | Tightened bird_like, improved quadruped/vehicle |
| 2 | 18.2% | 32.7% | Tightened striped_texture, handle_spout, color thresholds |
| 3 | 9.1% | 24.5% | REGRESSION — food_like too restrictive, bird_like still dominant |

## Key Findings

1. **64x64 resolution kills most features** — at this size, Gabor/LBP texture features fire on noise. Color detection thresholds need to be much lower. Shape-based features are unreliable because everything is a few pixels.

2. **bird_like was the biggest problem** — it fires on any image with "a compact body + something sticking out", which is basically everything. Fixed aggressively in iter 3 but other gates then fail to open.

3. **The hierarchy gates are the real bottleneck** — if no gate opens strongly, the system falls back to whatever fires weakly, which creates random predictions. Need a "default" fallback or more permissive gates.

4. **Color is the strongest signal at 64x64** — school_bus=yellow, banana=yellow, golden_retriever=golden/brown. But the HSV ranges for "golden" were set too strict (S>80 when actual golden retrievers have S≈39).

5. **Mushroom was easiest to get right** — organic_texture + compact body + green/brown context = mushroom. Got 50% in iter 2.

## What broke in Iter 3

Made `food_like` exclude anything that matches `quadruped_like`. But `quadruped_like` fires on golden_retrievers (correctly!) AND on mushrooms (because organic_texture + body). So food gate closed on mushrooms → mushroom accuracy dropped to 0.

Also tightened bird_like so much it barely fires on synthetic eagles now — but everything else still routes to eagle through the animal gate (quadruped_like still triggers on many images).

## Next Session Plan

1. **Fix the fallback problem**: if no gate fires strongly, classify as "unknown" rather than picking the highest noise signal
2. **Color-first strategy for school_bus and banana**: yellow_dominant should be the primary discriminator, not texture
3. **Separate golden_retriever from eagle**: golden_retriever has golden color + texture; eagle should require specific shape
4. **Get school_bus working**: large yellow body + wheels should be sufficient
5. **Consider a flat classifier as alternative**: at 64x64, the hierarchical approach may not have enough signal to route correctly

## Snapshot

Best result (iter 2, 18.2%):
- zebra: 100% (synthetic)
- bicycle: 100% (synthetic)  
- mushroom: 50%
- teapot: 0% (broke in iter 3)
- school_bus: 0% (yellow not detected)
- golden_retriever: 0% (confused with eagle/mushroom)
