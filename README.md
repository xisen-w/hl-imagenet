# HL-ImageNet: Heuristic-Learning Image Classification Without Neural Networks

**A coding agent (Claude) iteratively built a purely symbolic image classifier using classical computer vision. No neural networks, no gradient descent, no backpropagation.**

This is an application of Jiayi Weng's [Heuristic Learning](https://trinkle23897.github.io/learning-beyond-gradients/) framework to static image classification.

---

## Phase 2 (Current): 10-Class Real Image Classification

A proper train/val/test experiment with 10 real Tiny ImageNet classes and 2,000 images per split.

### Results

| Metric | Value |
|--------|-------|
| **Train top-1 accuracy** | **48.75%** (975/2000) |
| **Val top-1 accuracy** | **50.1%** (1003/2000) |
| Val top-3 accuracy | 74.2% (1484/2000) |
| Resolution | 64x64 (Tiny ImageNet) |
| Random baseline | 10% |
| Inference time | ~100ms per image |
| Eval iterations to date | 330+ |

### Per-Class Accuracy

| Class | Train | Val | Difficulty |
|-------|:---:|:---:|-----------|
| school bus | 78.0% | 78.5% | Easiest — yellow+structure is unique |
| jellyfish | 66.0% | 65.5% | Translucent blue is distinctive at 64x64 |
| banana | 56.0% | 51.0% | Confused with orange, school bus |
| sports car | 49.0% | 56.5% | Confused with school bus |
| king penguin | 50.5% | 48.0% | Dark-light contrast helps |
| orange | 45.0% | 50.5% | Confused with banana |
| mushroom | 44.5% | 41.5% | Texture-defined, overlaps with bear/GR |
| brown bear | 41.0% | 40.0% | Confused with GR, mushroom |
| golden retriever | 37.5% | 40.0% | Warm-blob overlap with everything |
| teapot | 21.5% | 30.0% | Shape-defined class in a color system |

### Top Confusions (Train)

| True class | Predicted as | Count | Root cause |
|------------|-------------|:---:|-----------|
| orange | banana | 53 | Both warm-colored round objects |
| sports car | school bus | 42 | Both strong gradients + structure |
| teapot | king penguin | 42 | Both can be dark/desaturated |
| mushroom | banana | 38 | Both warm, textured |
| teapot | banana | 34 | Copper/brass teapots look yellow |

### 10 Classes

| # | Class | wnid | Main confusions |
|---|-------|------|-----------------|
| 1 | golden retriever | n02099601 | banana, brown bear, mushroom |
| 2 | mushroom | n07734744 | banana, brown bear, GR |
| 3 | teapot | n04398044 | king penguin, banana, GR |
| 4 | school bus | n04146614 | sports car |
| 5 | banana | n07753592 | orange, school bus |
| 6 | orange | n07747607 | banana |
| 7 | brown bear | n02132136 | mushroom, GR, school bus |
| 8 | king penguin | n02056570 | brown bear, sports car |
| 9 | jellyfish | n01910747 | king penguin |
| 10 | sports car | n04285008 | school bus, king penguin |

### Data Split

| Split | Images/class | Total | Purpose |
|-------|:---:|:---:|---------|
| **Train** | 200 | 2,000 | HL loop tuning (all decisions based on this) |
| **Val** | 200 | 2,000 | Generalization reporting only (never used for decisions) |
| **Test** | 100 | 1,000 | Touched once at the very end |
| **External** | 50 | 500 | Official Tiny ImageNet val |

### Phase 2 Architecture

```
image (64x64 BGR)
  -> scene graph builder (color masks, edges, texture maps, blobs)
  -> 50+ low-level stats (hue ratios, edge density, gradients, LBP, spatial)
  -> 10 class signatures (weighted sum of sigmoid activations + guards)
  -> mean-centered histogram prototype blending
  -> pairwise reranking (24 discriminant pairs, gap-aware gating)
  -> prediction with proof trace
```

**Layer 1 — Class Signatures:** Each class has a signature — a weighted sum of sigmoid activations over image statistics, with guard gates:

```python
pos = sum(weight_i * sigmoid(stat_i, threshold_i, steepness_i) for each positive signal)
guards = [sigmoid(stat_j, threshold_j, negative_steepness) for each guard]
score = pos * min(guards)  # any guard can suppress the score
```

No hard binary thresholds. Each sigmoid contributes 0-1, and the sum represents soft match strength.

**Layer 2 — Histogram Prototype Blending:** 2D hue-saturation histograms are computed per class from training images. At inference, the image's histogram is compared to each class prototype. Mean-centered blending:

```
final = 0.88 * signature_score + 0.12 * (hist_score - class_mean * 0.3)
```

**Layer 3 — Pairwise Reranking with Gap-Aware Gating:** For the top-2/top-3 candidates, specialized discriminant functions compute evidence. A swap happens only when evidence exceeds a gap-scaled threshold:

```
swap iff disc_margin > base_threshold + score_gap * gap_scale
```

24 pairwise discriminant functions. Per-pair base thresholds calibrated by accuracy (84% -> -0.10, 58% -> 0.30).

### Phase 2 Experiment Logs

- [`logs/session_reasoning.md`](logs/session_reasoning.md) — Full reasoning log: what was tried, why, results per iteration
- [`docs/lessons.md`](docs/lessons.md) — 15 hard-won lessons from 330+ iterations
- [`logs/phase1/`](logs/phase1/) — All eval run logs (JSON + markdown)

---

## Lessons Learned (Both Phases)

330+ iterations produced 15 lessons, documented in full in **[`docs/lessons.md`](docs/lessons.md)**. Highlights:

1. **Additive scoring creates sink classes** — school bus and banana score high on everything. Guards don't fix this; it's structural.
2. **Pairwise reranking is the most impactful technique** (+3.4pp) — but has a hard ceiling since ~55% of errors have the true class beyond rank 3.
3. **Gap-aware gating prevents reranking from causing errors** — 5.6% of errors were CAUSED by the reranking layer before gating was added.
4. **Histogram prototype ratios beat raw scores** — `hist_A - hist_B` (d=1.3-2.2) is far more discriminative than `hist_A` alone (d~0.3).
5. **Shape-defined classes hit a ceiling in color/texture systems** — teapot at 21% is fundamentally limited.
6. **The biggest gains are architectural, not parametric** — top 3 structural changes (+4.8pp) outweigh all subsequent threshold tuning (~+2.75pp across 70+ iterations).

---

## The HL Loop

```
eval on train -> analyze confusion matrix -> hypothesize fix -> implement -> eval -> keep or revert -> repeat
```

Each iteration tests one hypothesis. Regressions are reverted. The coding agent (Claude) maintains experiment logs, reasoning traces, and feature distribution analyses throughout.

---

## Phase 1 (Completed): Exploratory Setup

<details>
<summary>Phase 1 used 4 real + 6 synthetic classes with a shared dev/eval set. Click to expand.</summary>

Phase 1 demonstrated that the HL loop works, but had evaluation methodology issues (tuning and eval on the same images).

### Phase 1 Results

- Dev-set top-1 (all 10 classes): **86.1%** (tuned on same 230 images)
- Held-out validation (4 hard classes): **54%** (216/400)
- Non-overlapping subset: **51.4%** (186/362)
- 248 iterations across 11 sessions (~20 hours)

### Phase 1 Architecture

Phase 1 used a completely different scoring system:

```
score = required_avg * 0.6 + supporting_avg * 0.3 - excluding_avg * 0.2
```

Each class had required, supporting, and excluding feature lists. If any required feature didn't fire, the class scored zero. This was replaced entirely in Phase 2 with the sigmoid-based scoring system.

Phase 1 also used a 22-function pairwise tiebreaker system (different from Phase 2's discriminant-based reranking).

### Phase 1 Growth Trajectory

```
Session 1:   ~20%   baseline sensors + features
Session 2:    35%   flat scorer (replaced broken hierarchy)
Session 3:    44%   compound features + tiebreakers
Session 4:    57%   tiebreaker expansion + school bus window pattern
Session 5:    62%   spatial attention + synthetic class tiebreakers
Session 6:    67%   eagle/banana solved to 100%
Session 7:    68%   plateau (DCT explored, failed)
Session 8:    78%   banana cap + compound conjunctions
Session 9:    80%   gradient/green conjunctions
Session 10:   85%   alt required features + guard tightening
Session 11:   86%   green+warm counter-signals (final)
```

### Phase 1 Ceiling

The remaining 32 errors (14%) came from the dog/mushroom/teapot triangle: at 64x64, all three are "warm-colored smooth blobs."

### Phase 1 Honesty Notes

1. The 86.1% is dev-set accuracy (same images used for tuning).
2. 6 of 10 classes used trivial synthetic images. The evaluation claim should be read as 4-class.
3. The system stores histogram prototypes and ~50 tuned thresholds. Not "zero learned parameters."
4. What Phase 1 demonstrated: the HL loop works. Confusion-driven iteration, feature invention, and representation saturation are real phenomena.

See the [full blog post](docs/blog.md) for trajectory analysis and ceiling discussion.

</details>

---

## Project Structure

```
hl-image-net/
├── hlinet/
│   ├── sensors/           # Classical vision: edges, color, texture, segmentation, shape
│   ├── scene/             # Scene graph builder + spatial relations
│   ├── features/
│   │   ├── primitives/    # Color, shape features
│   │   ├── textures/      # Pattern detection
│   │   ├── parts/         # Structural parts
│   │   ├── spatial/       # Grid + layout predicates
│   │   ├── compounds/     # Phase 2 signatures, histogram prototypes
│   │   └── concepts/      # High-level concept detectors
│   ├── classifier/
│   │   ├── predict.py     # Phase 2: signatures -> blend -> rerank -> predict
│   │   ├── scorer.py      # Phase 1: flat scorer (legacy)
│   │   ├── hierarchy.py   # Class hierarchy
│   │   └── tiebreaker.py  # Phase 1: pairwise tiebreakers (legacy)
│   ├── eval/              # Dataset loader, metrics, evaluation runner
│   └── registry.py        # Feature registry
├── scripts/
│   ├── generate_plots.py  # Generate visualizations
│   └── predict_image.py   # Classify a single image
├── data/phase2/           # Train/val/test splits (not in repo)
├── logs/
│   ├── phase1/            # All eval logs (JSON + markdown), 330+ iterations
│   └── session_reasoning.md  # Detailed reasoning log
└── docs/
    ├── blog.md            # Full Phase 1 writeup
    ├── lessons.md         # Lessons learned across both phases
    └── plots/             # Visualizations
```

## Quick Start

```bash
pip install -e .

# Run evaluation (defaults to val set)
python -m hlinet.eval.runner

# Run on train set
python -m hlinet.eval.runner --data-dir data/phase2/train

# Classify a single image
python scripts/predict_image.py path/to/image.jpg
```

## Technical Details

- **Language**: Python 3.11
- **Dependencies**: OpenCV, NumPy, SciPy (no ML frameworks)
- **Lines of code**: ~6400
- **Phase 1**: 248 eval runs, 11 sessions
- **Phase 2**: 80+ additional eval runs and counting
- **Coding agent**: Claude (Anthropic)

---

## Citation

```
Heuristic Learning for Image Classification: Without Neural Networks.
Xisen Wang, May 2026.
```

## References

Weng, J. (2026). *Learning Beyond Gradients*. https://trinkle23897.github.io/learning-beyond-gradients/
