# Phase 3: From Global Statistics to Local Perception at 128×128

**Date**: 2026-05-13
**Context**: Phase 2 at 64×64 plateaued at 47.2% val top-1. Moving to 128×128 with local region-based verifiers.

---

## Why 128×128

64×64 destroys discriminative structure:
- Object parts collapse into pixel noise
- Contours become compression artifacts
- Shape cues (teapot handle, banana curvature, mushroom cap) are undetectable
- Local region proposals find mostly amorphous blobs

128×128 provides 4× more pixels while remaining computationally cheap. Expected improvements:
- **Shape features** become meaningful (circularity, aspect ratio of actual object parts)
- **Part detection** becomes viable (penguin body+belly+beak, mushroom cap+stem)
- **Color localization** works better (orange_frac on a warm blob that's actually the fruit, not a global average)

---

## Architecture: Global Prior + Local Verifier

```
image (128×128 BGR)
  ├── _stats() → ~80 global features → 10 class signatures → global_score[class]
  │
  └── region proposals → local verifiers → local_score[class]
      ├── largest_warm_blob
      ├── largest_yellow_blob
      ├── largest_dark_blob
      ├── largest_edge_component
      └── center_crop_region

final_score[class] = 0.70 * global_score + 0.30 * local_score
```

Global signatures are NOT deleted — they become a prior. Local verifiers override only when confident.

---

## Phase 3a: Baseline (immediate)

1. Run existing Phase 2 pipeline on 128×128 data as-is
2. Measure per-class accuracy vs Phase 2 at 64×64
3. Identify which classes benefit most from resolution increase

Expected: modest global gain (features compute on more data), largest gains on shape/texture classes.

---

## Phase 3b: Local Region Verifiers (next)

Start with the 3 highest-leverage verifiers:

### Banana Verifier
```
banana_local_score =
    elongated(region.aspect > 2.0)    # banana shape
  + smooth(region.edge_density low)    # fruit texture
  + yellowish(region.hue in yellow)    # banana color
  + curved_contour(curvature cue)      # banana curve
  - circular(region.circularity high)  # NOT orange
```

### Orange Verifier
```
orange_local_score =
    circular(region.circularity high)  # round fruit
  + saturated_warm(region.sat high)    # orange color
  + orange_hue(warm_hue < 18)          # NOT banana yellow
  + compact(region.aspect near 1)      # compact shape
  - elongated(region.aspect high)      # NOT banana
```

### Teapot Verifier
```
teapot_local_score =
    compact_central_object             # centered object
  + handle_protrusion(lr_asymmetry)    # spout/handle shape
  + moderate_edge(not too smooth/textured)
  + low_green(not nature scene)
  - strong_yellow(not fruit)
  - vehicle_structure(not car/bus)
```

---

## Phase 3c: Compositional Rules (stretch)

Part vocabularies per class:
- **mushroom**: cap (dome-shaped top region) + stem (vertical below cap)
- **king_penguin**: dark body + white belly + orange head patch
- **school_bus**: elongated yellow rectangle + dark windows + sky above

Spatial relationship predicates: above, beside, contains, surrounds.

---

## Data

Source: `evanarlian/imagenet_1k_resized_256` on HuggingFace (public)
Resized: 256→128 using INTER_AREA
Split: 200 train, 200 val, 100 test per class (same as Phase 2)
Location: `data/phase3/{train,val,test}/<class_name>/`

---

## Success Criteria

- Phase 3a baseline: expect 50-55% val top-1 from resolution alone
- Phase 3b with local verifiers: target 60% val top-1
- Update README after reaching 55%+ (demonstrating clear resolution benefit)
