# X Thread Drafts

## Thread 1: The Honest Result

Built an image classifier with zero neural networks.

No backprop. No embeddings. No pretrained model.

Just OpenCV, hand-crafted visual features, sigmoid scoring, histogram prototypes, pairwise reranking, and explicit verification rules on 64x64 ImageNet images.

By Session 21, the hand-built symbolic pipeline hit **70.0% train accuracy** across 10 real classes.

No decision trees. No random forest. Every feature, threshold, and rule was readable Python.

But validation was only **49.4%**.

That gap is the whole story.

The system did not just learn vision. It learned the training set.

And because the model was code, the memorization looked like code: narrow threshold rules, special-case swaps, and correction conditions that fired on a few images.

Train-only heuristic search memorizes, just like train-only gradient descent memorizes.

The codebase is the model.

Patches are updates.

Eval accuracy is reward.

If the reward is train accuracy, the agent eventually writes a memorizer made of thresholds.

That feels like the real heuristic-learning lesson.

Not "symbolic vision beats neural nets."

It does not.

The lesson is that heuristic learning needs a generalization theory: held-out selection, patch regularization, reusable feature invention, and a way to distinguish a heuristic from an executable lookup table.

## Thread 2: The Fragile Code Organism

At 70% train accuracy, the symbolic classifier stopped behaving like a clean program.

It behaved like an evolved organism.

The pipeline had 6+ interacting stages:

signature scoring -> histogram blending -> calibration -> repulsion -> reranking -> local verify

A tiny change to one threshold changed score gaps.

Score gaps changed which pairs were compared.

Different pairs triggered different verify rules.

The change meant to fix 3 images broke 5 somewhere else.

Around 70-80% of experiments were reverted.

That revert rate is not noise. It is a property of the search process near a local optimum.

The code had become the learned representation.

The experiment made something very concrete: program induction has overfitting, local minima, cascade dynamics, and reward hacking too.

Heuristic learning needs its own backpropagation-like theory, but not necessarily gradients.

It needs a principled way to assign credit to patches and prefer reusable heuristics over memorized corrections.

## Thread 3: The Phase Boundary

Important correction to the story:

The 70% train result was the hand-built symbolic pipeline.

No trees.

The later compiled forest was a separate anycode experiment.

Why it matters:

The symbolic pipeline showed how far an agent can push readable heuristics by editing code.

The anycode forest showed what happens when you remove architecture constraints: first it memorizes with KNN, then trees generalize better by regularizing feature interactions.

Both are useful, but they answer different questions.

Phase 2 asks: can heuristic learning grow a readable symbolic vision system?

Anycode asks: what program does the optimizer write when the architecture is unconstrained?

The shared conclusion:

Code is not magically immune to overfitting.

If code is the model, code needs regularization.
