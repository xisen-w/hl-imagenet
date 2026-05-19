# Heuristic Learning Analysis

## The Core Lesson

Train-only heuristic search learns code that memorizes, just like train-only gradient descent learns parameters that memorize.

In this project, the codebase is the model. A patch is a policy update. The evaluation score is reward. The session logs are memory. Once the reward became train accuracy, the agent optimized toward executable memorization: hundreds of narrow threshold conditions that recover individual training images but do not transfer.

That is not a failure of the heuristic-learning frame. It is evidence that heuristic learning needs the same theory of generalization that neural learning needs.

## The Honest Phase Boundary

Phase 2's hand-built symbolic pipeline reaches **70.0% train / 49.4% val** before the post-pipeline verify waves. That result comes from:

- sigmoid class signatures over hand-crafted visual statistics;
- histogram prototype blending;
- pairwise discriminant reranking;
- local verify rules and rank-3/4/5 correction stages.

No trees are involved in this result.

The later **100% train / 41.35% val** endpoint is the overfitting endpoint of the same Phase 2 pipeline. It proves that code can memorize as effectively as parameters when the loop rewards training accuracy.

Anycode is separate. Its compiled forest reaches **64.4% val**, showing that the feature space contains more generalizable signal than the hand-written pipeline extracted, but it is a different architecture and should not be used to explain the 70% Phase 2 result.

## What Actually Generalized

The evidence points to three layers:

- Base visual statistics generalize moderately.
- Pairwise reranking generalizes best among the post-base interventions.
- Verify rules overfit, especially when they fire on only a few training images.

The best documented hand-built validation configuration is approximately **base + pairwise reranking: 51.9% val**. The full verify-wave system is worse on validation because it optimizes train corrections too specifically.

## What To Do Next

Stop optimizing train accuracy. Use train for proposing rules, a dev split for accepting or rejecting them, and keep val/test untouched. The HL loop needs a generalization reward, not a train reward.

Make base + rerank the real baseline. Treat the 100% train system as an overfitting artifact. The useful symbolic system is the one around 51-52% val.

Move from per-image verify rules to reusable heuristics. Accept rules only if they fire on enough examples, with support around 10-20, precision on held-out dev, and no class collapse. No more fix-1 thresholds.

Improve representation, not thresholds. The current features are too global: mean color, edge density, texture stats. The next useful HL direction is object/region-centered features: foreground masks, contour descriptors, local patch pooling, "pattern exists somewhere" detectors, and part relations.

Maintain [../understanding/](../understanding/) as the reflection memory. Every accepted or rejected direction should update the relevant understanding file before it becomes a public claim.

## Why The System Became Fragile

The pipeline is sequential:

`signature score -> histogram blend -> calibration -> repulsion -> sort -> rerank -> verify`

A small early change changes the score gaps, which changes which pairs get checked, which changes which verify conditions fire. By Session 21, 496 post-processing rescues depended on the exact shape of the ranking. Changes that were locally sensible caused global regressions.

This is cascade dynamics: the codebase behaves like an evolved system under selection pressure, not like a cleanly separable design.

## The Research Claim

The useful claim is not "symbolic image classification beats neural networks." It does not.

The useful claim is:

> Heuristic learning is program induction under feedback. If its reward is train accuracy, it overfits by writing code that memorizes. The next theory needs to explain how to regularize patches, measure heuristic generality, and select updates by held-out transfer.

That is the opening for a new theory of heuristic learning.
