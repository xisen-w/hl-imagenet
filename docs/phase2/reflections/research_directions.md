# Research Directions

## Goal

Build a heuristic-learning loop that rewards transferable heuristics instead of train-set correction code.

## Non-Negotiable Rules

1. Stop optimizing train accuracy.
2. Use train for proposing rules, a dev split for accepting or rejecting them, and keep val/test untouched.
3. Make base + rerank the real symbolic baseline, around 51-52% val.
4. Treat the 100% train system as an overfitting artifact, not the system to improve.
5. Reject per-image verify rules. No fix-1 thresholds.
6. Accept rules only with support around 10-20 examples, held-out dev precision, and no class collapse.
7. Improve representation before thresholds: object/region-centered features, foreground masks, contours, local patch pooling, "pattern exists somewhere" detectors, and part relations.
8. Maintain [../understanding/](../understanding/) as the reflection memory for every accepted and rejected result.

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

### Completed (Session 29)

1. ~~create a small inner train/dev split from `data/phase2/train`~~ → `hlinet/eval/splits.py` (150/50 per class, seed 2026, crc32-stable)
2. ~~add evaluation modes for base-only, base+rerank, and verify-enabled pipelines~~ → `predict(mode="base"|"base_rerank"|"full")` + `set_verify_whitelist()`
3. ~~add rule-support instrumentation for verify conditions~~ → `hlinet/eval/verify_audit.py` (per-image credit assignment)
4. ~~produce a report ranking existing verify rules by support and dev transfer~~ → `hlinet/eval/rule_credit.py` (per-pair ablation-based credit)
5. First accepted patch: whitelist `{jellyfish, banana}` verify → val 49.4% → 52.7%

### Next

1. Complete rule-level credit report (running)
2. Freeze acceptance rule formally (see `docs/synthesis/acceptance_rule.md`)
3. Begin Direction 3: representation-level features against `base_rerank` baseline
4. Prototype foreground/background separation, contour features, local patch pooling

## Reflection Maintenance

Each run should update Phase 2 knowledge in this order:

1. Update the relevant file in [../understanding/](../understanding/) with the concrete result, including failed patches.
2. Update this file only if the result changes the research program.
3. Update [heuristic_learning_analysis.md](heuristic_learning_analysis.md), [x_thread_drafts.md](x_thread_drafts.md), or [blog_outline.md](blog_outline.md) only when the public story changes.
