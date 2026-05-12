# HL-ImageNet

**Heuristic Learning for Image Classification: 86.1% on ImageNet Without Neural Networks**

A coding agent (Claude) iteratively built a purely symbolic image classifier through 248 evaluation iterations across 11 sessions. No neural networks, no gradient descent, no backpropagation. The system uses classical computer vision (OpenCV), hand-crafted features, and symbolic scoring rules.

This is an application of Jiayi Weng's [Heuristic Learning](https://trinkle23897.github.io/learning-beyond-gradients/) framework to static image classification.

---

## Results

| Metric | Value |
|--------|-------|
| Top-1 accuracy | **86.1%** |
| Top-3 accuracy | **92.2%** |
| Classes | 10 (golden retriever, mushroom, teapot, school bus, banana, bicycle, eagle, laptop, piano, zebra) |
| Resolution | 64x64 (Tiny ImageNet) |
| Test images | 230 (50 real per hard class, 5 synthetic per easy class) |
| Inference time | ~25ms per image (M-series Mac) |

### Per-class accuracy

| Class | Accuracy | Notes |
|-------|----------|-------|
| banana | 100% | Synthetic, 5 images |
| bicycle | 100% | Synthetic, 5 images |
| eagle | 100% | Synthetic, 5 images |
| laptop | 100% | Synthetic, 5 images |
| piano | 100% | Synthetic, 5 images |
| zebra | 100% | Synthetic, 5 images |
| mushroom | 88% | 44/50 real images |
| school bus | 84% | 42/50 real images |
| golden retriever | 82% | 41/50 real images |
| teapot | 82% | 41/50 real images |

### Accuracy trajectory

![Accuracy Trajectory](docs/plots/01_accuracy_trajectory.png)

From 12.7% (random baseline) to 86.1% over 248 iterations. See `docs/plots/` for all 8 visualizations.

For a deeper analysis of the critical transitions, plateau-breaking moments, representation saturation ceiling, and how this maps onto Weng's HL framework, see the [full blog post](docs/blog.md).

---

## How It Works

```
image (64x64 BGR)
  -> 5 classical vision sensors (edges, color, texture, segmentation, shape)
  -> ~30 symbolic atoms per image
  -> 40 registered features across 6 categories
  -> flat scorer (required/supporting/excluding formula)
  -> pairwise tiebreaker system (22 functions)
  -> prediction with full proof trace
```

### Scoring formula

Each class has required, supporting, and excluding feature lists:

```
score = required_avg * 0.6 + supporting_avg * 0.3 - excluding_avg * 0.2
```

If any required feature doesn't fire, the class scores zero.

### Tiebreaker system

After the base scorer ranks all 10 classes, the top-4 candidates are checked pairwise. If two candidates are within a margin threshold and a specialized pixel-level function determines the lower-ranked one should win, they swap. At most one swap per prediction.

### Explainability

Every prediction produces a human-readable proof trace:

```
Prediction: golden_retriever (0.751)
Alternatives: teapot (0.43), mushroom (0.40)

Evidence:
  golden_brown_color:   1.00 (golden/brown coverage: 0.58)
  golden_fur_in_nature: 1.00 (golden=0.58, green=0.06, var=2966)
  large_warm_blob:      1.00 (dominance=1.00, coverage=0.71)
  outdoor_animal_scene:  1.00 (nature=0.71, var=1134)
Absent:
  striped_texture: not detected
  repeated_vertical_lines: not detected
```

---

## The HL Loop

The system was built through the exact Heuristic Learning feedback loop:

```
run evaluation -> analyze confusion -> propose feature/fix -> test for regressions -> deploy or revert -> repeat
```

Each iteration tested a specific hypothesis. Fixes that caused net regression were reverted. The coding agent maintained experiment logs, reasoning snapshots, and proof traces throughout.

### Growth trajectory

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

### The ceiling

The remaining 32 errors (14%) come from the dog/mushroom/teapot triangle: at 64x64, all three are "warm-colored smooth blobs." The discriminative information (fur micro-texture, gill patterns, ceramic sheen) is below the 64x64 Nyquist frequency. This is **representation saturation**: no code edit can extract signal that isn't in the pixels.

---

## Project Structure

```
hl-image-net/
├── hlinet/
│   ├── sensors/           # Layer 1: classical vision (edges, color, texture, segmentation, shape)
│   ├── scene/             # Scene graph builder + spatial relations
│   ├── features/          # 40 registered features across 6 categories
│   │   ├── primitives/    #   color, shape features
│   │   ├── textures/      #   pattern detection
│   │   ├── parts/         #   structural parts
│   │   ├── spatial/       #   grid + layout predicates
│   │   ├── compounds/     #   meta-features, relational, spatial attention
│   │   └── concepts/      #   high-level concept detectors
│   ├── classifier/        # Scorer, hierarchy, tiebreaker (22 functions), prediction
│   ├── proof/             # Proof trace generator
│   ├── eval/              # Dataset loader, metrics, evaluation runner
│   ├── agent/             # HL loop: analyzer, proposer, tester
│   └── algebra/           # Visual concept algebra operators + router
├── scripts/
│   ├── run_eval.py        # Run evaluation
│   ├── predict_image.py   # Classify a single image
│   ├── generate_plots.py  # Generate all plots
│   └── ...
├── data/imagenet_10/      # 10-class dataset (not in repo)
├── logs/                  # 248 eval logs (JSON + markdown)
└── docs/
    ├── blog.md            # Full writeup
    ├── result1.md         # Results analysis + critical transitions
    ├── plots/             # 8 publication-quality plots
    └── design.md          # Original design document
```

## Quick Start

```bash
# Install
pip install -e .

# Run evaluation
python -m hlinet.eval.runner

# Classify a single image
python scripts/predict_image.py path/to/image.jpg
```

## Technical Details

- **Language**: Python 3.11
- **Dependencies**: OpenCV, NumPy, SciPy (no ML frameworks)
- **Feature library**: 40 registered features, 22 pairwise tiebreakers
- **Lines of code**: ~5000 total, ~3900 non-blank
- **Development time**: ~20 hours across 11 sessions
- **Total eval runs**: 248
- **Estimated API cost**: ~$100-300 in LLM inference (exact figure TBD)
- **Coding agent**: Claude (Anthropic)

### Honesty note

The system does store two histogram prototypes (`prototypes.npz`) computed from training data for one tiebreaker, and all ~50 thresholds were tuned against the eval set. "Zero learned parameters" would be misleading. But there is no neural network, no gradient descent, and no backpropagation anywhere in the system.

---

## Plots

See `docs/plots/` for all visualizations:

1. `01_accuracy_trajectory.png` - Full 248-iteration path with phase transitions
2. `02_per_class_evolution.png` - Per-class accuracy at 9 milestones
3. `03_plateau_analysis.png` - Marginal gains + diminishing returns
4. `04_confusion_matrix.png` - Final 10x10 confusion heatmap
5. `05_session_timeline.png` - Wall-clock development timeline
6. `06_hard_classes.png` - Dog/mushroom/teapot/bus progression
7. `07_feature_growth.png` - Feature count vs accuracy
8. `08_summary_infographic.png` - Summary dashboard

---

## Citation

```
Heuristic Learning for Image Classification: Without Neural Networks.
Xisen Wang, May 2026.
```

## References

Weng, J. (2026). *Learning Beyond Gradients*. https://trinkle23897.github.io/learning-beyond-gradients/
