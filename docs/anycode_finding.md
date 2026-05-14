# The "Any Code" Experiment: What Happens When You Remove All Architecture Constraints

## Setup

We gave a coding agent one instruction: write `predict(image) -> label` to maximize train accuracy on 10-class Tiny ImageNet (64x64). No fixed architecture — no "signatures", no "scorer", no "tiebreaker slots". Any code allowed, only constraint: cv2/numpy/scipy, no neural networks.

## Attempt 1: The agent memorizes immediately

Given unconstrained "any code, optimize train accuracy", the agent's first move was to build a KNN classifier using all 2000 training images as templates. It extracted a 46-dimensional feature vector per image (color histograms + edge density + spatial stats), stored them in `templates.npz`, and did distance-weighted k=5 voting at inference time.

Result: **100% train accuracy in one iteration.** The agent solved the optimization problem in the most direct way possible — by memorizing the answer key.

## But does it generalize?

| | KNN memorizer | Phase 2 system (200+ hand-engineered iterations) |
|---|---|---|
| **Train** | 100% (memorized) | 48.75% |
| **Val** | 41.2% | 50.1% |

The KNN memorizer is **9 points worse on val** than the hand-engineered system. This means:

1. **When you say "any code", the first thing an optimizer does is memorize.** This is the trivial solution — and it's what unconstrained optimization always finds first.

2. **The Phase 2 system's 50.1% val is legitimately better than brute-force nearest-neighbor over the same data.** The sigmoid signatures, guard gates, and pairwise discriminants encode generalizable visual patterns, not memorized instances.

3. **41.2% is a feature-quality baseline.** It tells us that 46 histogram/edge features carry about 41% of the discriminative signal. The Phase 2 system's advantage comes from how it combines features (conjunctions, guards, discriminants), not from having better raw features.

## The insight about Heuristic Learning

Heuristic Learning is not about tuning model parameters — it's about writing the software environment. KNN with memorized templates is parameter storage (the templates ARE the parameters). HL should produce code that encodes visual knowledge as programs, not as stored data.

The test: **delete the training data. Does the classifier still work?**
- KNN memorizer: No. It needs `templates.npz` (computed from training images).
- Phase 2 system: Yes. It only has ~50 hardcoded thresholds and decision logic.

That's the difference between memorization and learning. HL produces software that has *understood* something about the visual world, not software that has *remembered* specific images.

## Attempt 2: Robust software (no stored training data)

With the constraint "no stored training data at inference time", the agent must encode visual knowledge as code — decision trees, threshold cascades, spatial reasoning — not as stored feature vectors.

This is the version that tests whether "any code" can discover generalizable visual programs through the HL loop.

(Results in progress)
