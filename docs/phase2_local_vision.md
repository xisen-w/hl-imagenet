# Phase 2.5: From Global Statistics to Local Perception

**Date**: 2026-05-12
**Context**: Global-statistics heuristics hit a ceiling at ~46% val. This document outlines the shift to local, compositional, active perception.

---

## The Problem with Global Statistics

The current system computes 57 scalar features over the entire 64x64 image, then scores 10 classes via weighted sigmoid sums. This is fundamentally:

```
image → fixed vector → classifier
```

This inherits the ML assumption that an image is a point in feature space. But heuristic learning doesn't require this. HL can be:

```
image → symbolic observations → procedures → search → relational constraints → dynamic evidence
```

### Why the ceiling exists

Global stats dilute objects into backgrounds. A brown bear in a green forest averages to "moderate warm, moderate green, moderate edge." A golden retriever on a lawn averages to nearly the same thing. The discriminative information is *where* the warm pixels are relative to the green pixels — spatial structure that global means destroy.

The three hardest classes (mushroom 28%, brown_bear 34%, teapot 32%) all suffer from this: their distinctive features are local (mushroom cap shape, bear fur texture in a nature scene, teapot handle + spout geometry) but get averaged away.

---

## Direction 1: Region Proposals + Local Features

### Classical object segmentation (no NN)
- **Felzenszwalb segmentation**: graph-based oversegmentation into perceptually coherent regions
- **MSER** (Maximally Stable Extremal Regions): finds regions stable across intensity thresholds
- **Superpixels** (SLIC): groups pixels by color+proximity

### Per-region feature extraction
For each candidate region, compute:
- **Shape**: aspect ratio, Hu moments, circularity, convexity, elongation
- **Color**: dominant hue, saturation profile, color uniformity
- **Texture**: edge density, LBP entropy, gradient magnitude — all local to region
- **Position**: centroid, bounding box, relative position (top/bottom/center)

### Why this breaks the ceiling
- `banana = elongated smooth yellow region` (not "image has some yellow somewhere")
- `mushroom = textured cap-region above a vertical stem-region`
- `teapot = compact reflective region with asymmetric side protrusion`
- The object is no longer diluted by background.

---

## Direction 2: Compositional Geometry (Parts + Relationships)

Objects are not feature vectors. Objects are **parts in spatial relationships**.

```
school_bus:
  IF upper_region is blue/bright (sky)
  AND lower_region is elongated warm rectangle
  AND repeated dark vertical slots exist (windows)
  THEN school_bus

king_penguin:
  IF dark_vertical_region exists (body)
  AND white_region exists in center (belly)
  AND small_orange_region near top (beak)
  THEN king_penguin
```

This is grammar-based / symbolic vision: the classifier is a structural pattern matcher, not a distance function.

---

## Direction 3: Active Perception Loops

Instead of extracting all features once (feedforward), do hypothesis-driven inspection:

```
Step 1: Quick global scan → banana is top hypothesis
Step 2: Search for curved contour → found? boost confidence
Step 3: Check for tapering ends → not found? downgrade
Step 4: Verify smooth yellow consistency in candidate region → confirmed
Step 5: Final verdict with evidence chain
```

This is **perception as executable reasoning** — the classifier is a program that actively interrogates the image, not a function that passively maps features to scores.

---

## Direction 4: Feature Programs

Current features are arithmetic expressions:
```python
smooth_yellow = yellow * max(0, 1 - edge * 3)
```

Future features can be executable procedures:
```python
def has_repeated_window_pattern(image, region):
    """Detect evenly-spaced dark rectangles (bus windows)."""
    # threshold to binary
    # find dark rectangular blobs
    # check horizontal spacing regularity
    # return confidence + evidence

def detect_handle_like_structure(image, region):
    """Detect asymmetric protrusion (teapot handle, cup handle)."""
    # find main blob
    # check left-right contour asymmetry
    # measure protrusion aspect ratio
    # return confidence + evidence
```

The classifier becomes a **policy over procedures** — deciding which perceptual programs to run and how to combine their evidence.

---

## Implementation Plan

### Phase 2.5a: Region-based features (immediate)
1. Add Felzenszwalb segmentation to extract candidate regions
2. Compute per-region shape descriptors (Hu moments, aspect ratio, circularity)
3. Compute per-region color/texture features
4. Build region-based class rules (banana = elongated smooth yellow region)
5. Integrate as new features into existing scoring pipeline

### Phase 2.5b: Compositional rules (next)
1. Define part vocabularies per class (cap+stem for mushroom, body+belly+beak for penguin)
2. Implement spatial relationship predicates (above, beside, contains, surrounds)
3. Build compositional matchers that fire when parts exist in correct spatial arrangement

### Phase 2.5c: Active perception (stretch)
1. Implement hypothesis-driven feature extraction (only compute expensive features if hypothesis warrants)
2. Build evidence accumulation loops with early stopping
3. Add contour tracing and curvature analysis for shape-based verification

---

## What This Changes

| Aspect | Current (global stats) | Future (local perception) |
|--------|----------------------|--------------------------|
| Features | 57 scalars per image | Variable per region, per hypothesis |
| Classifier | Weighted sigmoid sum | Compositional rule matching |
| Proof trace | "yellow=0.85, edge=0.12" | "found elongated yellow region (0.7 aspect), smooth interior, curved contour" |
| Ceiling | ~46% (train-val converged) | Unknown — fundamentally richer |
| Interpretability | Feature weights | Structural explanations |
