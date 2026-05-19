# Blog Outline: Heuristic Learning Overfits Too

## Working Title

Heuristic Learning Overfits Too: What Happened When a Coding Agent Wrote an Image Classifier Without Neural Networks

## Thesis

The experiment does not prove that symbolic image classification beats neural networks. It proves something more useful: when code is optimized by feedback, the code itself becomes the model, and train-only optimization produces executable memorization.

## Structure

1. **Setup**
   - Jiayi Weng's heuristic-learning frame.
   - The provocation: can a coding agent maintain a non-neural vision system?
   - Tiny ImageNet 10-class, 64x64, no neural nets in the main symbolic pipeline.

2. **Phase 1: Proof The Loop Can Grow Code**
   - 4 real + 6 synthetic classes.
   - 86.1% dev, but with clear methodology caveats.
   - Lesson: the loop can invent useful features and tiebreakers.

3. **Phase 2: Honest 10-Class Setup**
   - Train/val/test split.
   - Architecture: signatures, histogram blending, pairwise reranking, verify.
   - Result: 70.0% train / 49.4% val at Session 20/21.

4. **The Wall**
   - Cascade dynamics.
   - 70-80% revert rate.
   - Verify rules become memorized training corrections.
   - 100% train endpoint drops to 41.35% val.

5. **Anycode As Diagnostic, Not The Main Story**
   - KNN memorizes immediately.
   - GNB lacks conjunctions.
   - Compiled forest reaches 64.4% val.
   - Lesson: feature interactions and regularization matter.

6. **The Deeper Lesson**
   - The codebase is the model.
   - Patches are policy updates.
   - Eval is reward.
   - Heuristic learning needs a theory of generalization, not more train-set grinding.

7. **Next Direction**
   - Generalization-aware HL loop.
   - Held-out update acceptance.
   - Patch regularization.
   - Region-centered visual primitives.
   - Credit assignment for code edits.

## Claims To Avoid

- Do not claim the 70% result came from trees.
- Do not present the 100% train system as a generalizing classifier.
- Do not say "no learned parameters" without caveats; thresholds and prototypes are learned/tuned artifacts.
- Do not compare Phase 1 dev accuracy directly to Phase 2 validation accuracy.

## Strongest Sentence

Train-only heuristic search learns code that memorizes, just like train-only gradient descent learns parameters that memorize.
