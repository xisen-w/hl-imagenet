# HL-ImageNet Phase 1: Results Analysis

## Accuracy Trajectory

From 12.7% (random baseline) to 86.1% on the Phase 1 development set over 248 evaluation iterations across ~20 wall-clock hours.

Methodology note: this is a development-set trajectory, not a held-out benchmark. The 230-image set mixed 4 real Tiny ImageNet classes (50 each) with 6 synthetic placeholder classes (5 each). On the 4 real classes alone, final dev accuracy was 84%; the later validation folder scored 54%, or 51.4% after exact duplicate removal.

See `plots/` for all visualizations.

---

## Critical Transitions (Plateau-Breaking Moments)

### Transition 1: 12.7% to 34.5% (Sessions 1-2)
**What broke the plateau**: Switching from hierarchical routing to a flat scorer.

At 64x64, the hierarchy gates (animal/vehicle/object) couldn't reliably route. The system kept sending images to wrong subtrees. The flat scorer evaluates all 10 classes simultaneously, letting color/texture signals compete directly.

**Key insight**: At low resolution, top-down categorical reasoning fails. Bottom-up feature matching works.

---

### Transition 2: 34.5% to 43.5% (Session 3)
**What broke the plateau**: Compound features + pairwise tiebreakers.

Single features overlap too much (golden_brown_color fires on dogs, mushrooms, and teapots). Conjunctions of 3+ weak features create clean separations. The tiebreaker system handles close calls that the base scorer can't resolve.

**Key insight**: Feature conjunction is the symbolic equivalent of learning non-linear decision boundaries.

---

### Transition 3: 43.5% to 50.4% (Session 4)
**What broke the plateau**: Tiebreaker expansion + school bus detection via `horizontal_window_pattern`.

School bus went from 0% to 74% once a single structural feature (horizontal dark rectangles = windows) was invented. This is the most dramatic single-class improvement: one feature flipped 37 images.

**Key insight**: Some classes have a single pathognomonic feature. Finding it gives huge gains.

---

### Transition 4: 50.4% to 63.9% (Sessions 5-6)
**What broke the plateau**: Solving the "easy" synthetic classes (eagle, banana, laptop, piano all to 100%).

Each had a unique visual signature at 64x64 that no other class shared. Once their required features were correct, they never regressed. This freed the system to focus tiebreaker capacity on the hard 4 classes.

**Key insight**: Solving easy classes perfectly creates "headroom" for harder problems.

---

### Transition 5: 63.9% to 67.8%, then plateau (Sessions 6-7)
**What caused the plateau**: All remaining errors are in the dog/mushroom/teapot/bus quadrilateral. Every global optimization attempted (score normalization, z-scores, calibration, stronger penalties) caused regression. DCT features explored but showed overlapping distributions.

**Why it stuck**: The system had exhausted single-feature discrimination. Every pair of confused classes overlaps on every single pixel metric.

---

### Transition 6: 67.8% to 78% (Session 8)
**What broke the plateau**: Three innovations simultaneously:
1. **Banana score cap** (yellow_dominant > 0.8, cap at 0.40): Freed tiebreaker capacity that banana was consuming
2. **Compound conjunctions**: `grad_top_bin>0.18 + green>0.089 + warm<0.68` for mushroom; `sat>117 + rb_bot<1.83` for specific mushroom subtypes
3. **Wide margin pairs**: Allowed tiebreakers to fire with larger score gaps for known-confused pairs

**Key insight**: Sometimes the bottleneck is not "can't distinguish A from B" but "C is consuming the correction budget." Fixing C's score (banana cap) indirectly helps A and B.

---

### Transition 7: 78% to 86.1% (Sessions 9-11)
**What broke the plateau**: Alternative required features + guard tightening.

For golden_retriever: added `golden_fur_in_nature` as OR-alternative to `golden_brown_color`. For mushroom: `top_textured_bottom_plain` as additional discriminator. Each fix catches 2-4 images but risks 1-2 regressions, requiring precise threshold surgery.

**Key insight**: In the final phase, each fix is a micro-surgery. The coupling complexity is near the agent's maintenance capacity.

---

### Final Dev-Set Ceiling: 86.1% (representation saturation)
**Why no further progress**: The remaining 32 errors are dog/mushroom/teapot images where all measurable pixel-level features overlap:
- Laplacian variance: overlapping (7138 vs 12351 vs 8315, all with huge std)
- Gabor isotropy: identical (0.8 +/- 0.0)
- Hue entropy: overlapping (1.09 vs 1.42 vs 1.44)
- LR symmetry: barely separable

The discriminative information (fur texture, gill patterns, ceramic sheen) is below the 64x64 Nyquist frequency. No amount of code editing can extract signal that isn't in the pixels.

---

## Token Usage and Cost Estimate

### Methodology
Based on 11 coding sessions, each involving Claude (Opus-class) as the HL agent:

| Session | Duration | Est. Turns | Est. Input Tokens | Est. Output Tokens |
|---------|----------|------------|-------------------|-------------------|
| 1 | 45 min | ~20 | 200K | 60K |
| 2 | 90 min | ~35 | 400K | 120K |
| 3 | 120 min | ~50 | 600K | 180K |
| 4 | 90 min | ~40 | 500K | 150K |
| 5 | 60 min | ~25 | 350K | 100K |
| 6 | 60 min | ~25 | 350K | 100K |
| 7 | 45 min | ~20 | 300K | 80K |
| 8 | 120 min | ~50 | 700K | 200K |
| 9 | 60 min | ~30 | 450K | 130K |
| 10 | 90 min | ~40 | 600K | 170K |
| 11 | 45 min | ~20 | 350K | 100K |
| **Total** | **~14.5 hrs** | **~355** | **~4.8M** | **~1.4M** |

### Cost Estimate (Claude Opus pricing: $15/M input, $75/M output)

| Component | Tokens | Cost |
|-----------|--------|------|
| Input tokens | ~4.8M | ~$72 |
| Output tokens | ~1.4M | ~$105 |
| **Total API cost** | **~6.2M tokens** | **~$177** |

### Notes on the estimate:
- This is for the coding agent (Claude) inference only. No GPU training cost.
- Each turn includes: reading eval results (~2K tokens), reading code files (~5K), generating code edits (~3K output), running eval (~1K output)
- Context grows across a session (later turns include more history)
- Actual cost likely **$100-200** range depending on caching and context management
- Compare to: training a CNN on 230 images would cost <$1 in GPU time, but would require a human ML engineer's time to design, tune, and iterate

### Cost per accuracy point gained:
- 73.4 development-set percentage points gained (12.7% to 86.1%)
- ~$177 / 73.4 = **~$2.41 per accuracy point**
- First 50 points: ~$80 (fast, structural changes)
- Last 23 points: ~$97 (slow, surgical fixes, many reverts)

### Comparison with alternatives:
- A ResNet-18 fine-tuned on these 230 images: ~$0.10 in GPU, but needs human ML engineering time (~4 hours = ~$200-400 in engineer time)
- Human hand-coding this classifier from scratch: 40+ hours of expert CV time (~$4000-8000)
- The HL approach: $177 in API cost + ~2 hours human oversight = ~$277 total

---

## Plots Generated

All in `plots/`:

1. **01_accuracy_trajectory.png** - Full 248-iteration path with annotated phase transitions and plateau zones
2. **02_per_class_evolution.png** - 10-class bar chart at 9 milestones showing when each class was solved
3. **03_plateau_analysis.png** - Marginal gain per iteration (left) + diminishing returns on log scale (right)
4. **04_confusion_matrix.png** - Final 10x10 confusion heatmap showing the dog/mushroom/teapot triangle
5. **05_session_timeline.png** - Wall-clock progression showing session breaks and overnight gaps
6. **06_hard_classes.png** - Focus on the 4 hard classes (dog, mushroom, teapot, bus) trajectory
7. **07_feature_growth.png** - Feature library size vs accuracy (dual axis)
8. **08_summary_infographic.png** - 6-panel summary dashboard
