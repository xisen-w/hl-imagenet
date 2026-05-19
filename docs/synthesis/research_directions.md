# Research Directions

## Goal

Build a heuristic-learning loop that rewards transferable heuristics instead of train-set correction code.

## Direction 1: Generalization-Aware Patch Acceptance

Replace the current rule:

`keep patch if train accuracy improves`

with:

`keep patch if dev accuracy improves and the rule has enough support`

Minimum acceptance criteria:

- train improvement is not required, only allowed;
- dev split improves or is neutral with a strong simplification benefit;
- rule fires on at least 10-20 examples, not one image;
- no single class loses more than a small fixed budget;
- every accepted patch records support, precision, and failure cases.

## Direction 2: Patch Regularization

Score a patch by:

`utility = dev_gain - complexity_penalty - memorization_penalty - cascade_risk`

Possible penalties:

- number of new thresholds;
- number of pair-specific branches;
- support below 10 examples;
- threshold precision with too many significant digits;
- direct dependency on filenames, ranks, or accidental artifacts;
- early-pipeline score distribution shifts.

## Direction 3: Representation-Level Feature Invention

Stop adding narrow verify conditions. Prefer features that expand what can be measured:

- region proposals and foreground/background separation;
- contour descriptors on candidate objects;
- local patch pooling with translation tolerance;
- "pattern exists somewhere" detectors rather than fixed grid cells;
- part relations: cap over stem, body over feet, handle next to body;
- color-conditional texture: warm textured animal vs warm smooth fruit.

## Direction 4: Cross-Validation For Heuristics

Use the 200 train images/class as an inner loop:

- propose on train-a;
- accept on train-b/dev;
- report untouched val;
- periodically rotate splits.

The important measurement is not whether a rule fixes its discovery image. It is whether the rule survives a distribution shift.

## Direction 5: Credit Assignment For Code Edits

The missing "backpropagation for heuristic learning" is credit assignment over patches.

Candidate proxy:

1. instrument each pipeline stage with before/after candidate rankings;
2. record which code branch changed each prediction;
3. compute marginal contribution of each rule by ablation;
4. assign negative credit to rules that help train but hurt dev;
5. prefer patches whose contribution is broad, stable, and low-cascade.

This is not gradient descent, but it is a structured update signal over code.

## Near-Term Work

The next Claude run should not try to improve the 100% train system. It should build tooling for generalization-aware HL:

1. create a small inner train/dev split from `data/phase2/train`;
2. add evaluation modes for base-only, base+rerank, and verify-enabled pipelines;
3. add rule-support instrumentation for verify conditions;
4. produce a report ranking existing verify rules by support and dev transfer;
5. propose only representation-level or regularization patches.
