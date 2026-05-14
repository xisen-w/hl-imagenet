# Any-Code Experiment

## The premise

What if the entire classifier is just a Python file that gets rewritten each iteration? No fixed architecture (no "signatures", no "scorer", no "tiebreaker slots"). Just: `predict(image) -> label`. Any code allowed, only constraint: cv2/numpy/scipy, no neural networks.

## Attempt 1: Unconstrained "optimize train accuracy"

**Result: 100% train in one move.** The agent immediately built a KNN classifier using all 2000 training images as templates (46-dim color+edge histogram features). Euclidean distance, k=5 weighted vote. Perfect memorization.

### But does it generalize?

| | KNN memorizer | Phase 2 system (200+ hand-engineered iterations) |
|---|---|---|
| **Train** | 100% (memorized) | 48.75% |
| **Val** | 41.2% | 50.1% |

The KNN memorizer is 9 points WORSE on val than the hand-engineered system. This means:

1. **When you say "any code", the first thing an optimizer does is memorize.** This is the trivial solution — and it's what unconstrained optimization always finds first. This is the perfect illustration of why held-out evaluation exists.

2. **The Phase 2 system's 50.1% val is legitimately better than brute-force nearest-neighbor over the same data.** The sigmoid signatures, guard gates, and pairwise discriminants are doing real work — they encode generalizable visual patterns, not memorized instances.

3. **41.2% is a feature-quality baseline.** It tells you that 46 histogram/edge features carry about 41% of the discriminative signal. The Phase 2 system's advantage comes from how it COMBINES features (conjunctions, guards, discriminants), not from having better raw features.

### The insight about HL

Heuristic Learning is not about tuning model parameters. It's about **writing the software environment** — the code that processes images. KNN with memorized templates is parameter tuning (the templates ARE the parameters). HL should produce code that encodes visual knowledge as PROGRAMS, not as stored data.

The test: delete the training data. Does the classifier still work? KNN: no. Phase 2 system: yes (it only has ~50 hardcoded thresholds, not 2000 stored images). That's the difference between memorization and learning.

## Attempt 2: Write robust software, not parameters

Constraint: the classifier must work WITHOUT access to training images at inference time. No templates, no stored histograms from training data, no nearest-neighbor lookup. The code itself must encode the visual knowledge.

(In progress)
