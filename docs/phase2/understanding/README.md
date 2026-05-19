# Phase 2 Understanding: Distilled Knowledge from HL-ImageNet

This folder contains indexable, searchable knowledge about the hand-built Phase 2 symbolic pipeline. It covers the sigmoid-signature, histogram-blending, reranking, and verify-rule system. The anycode forest is documented separately under `../../anycode/`.

**Key Phase 2 states**:
- Session 20/21 hand-built pipeline: 70.0% train, 49.4% val. This is the main no-tree symbolic result.
- Full verify-wave endpoint: 100.0% train (2000/2000), 41.35% val. This is an overfit train memorizer and should not be presented as a generalizing classifier.
- Best documented generalizing hand-pipeline layer stack: base scoring + pairwise reranking at about 51.9% val.

## How to use
- **Before making a change**: read the relevant file to see what's been tried, what worked, and why things fail
- **After a session**: update or add files based on new findings
- **When stuck**: read `pipeline_mechanics.md` and `edit_risk_hierarchy.md` to understand system dynamics before proposing changes
- **When planning the next breakthrough**: read `optimization_trajectory.md` for the phase transition pattern

## Index

### System Architecture
- [pipeline_mechanics.md](pipeline_mechanics.md) — The 7-stage prediction pipeline: score → blend → calibrate → repulse → sort → rerank → verify (4 rank levels)
- [feature_inventory.md](feature_inventory.md) — All feature types: what's orthogonal, what's saturated, what's available
- [edit_risk_hierarchy.md](edit_risk_hierarchy.md) — Which parts of the system are safe to touch, which are dangerous (amplified at 70%)

### What Works
- [techniques_that_work.md](techniques_that_work.md) — Proven techniques ranked by impact, including exhaustive verify scan, rank-3/4/5 invention, bad condition auditing
- [orthogonal_features.md](orthogonal_features.md) — Why representation expansion beats parameter tuning, and which axes remain unexplored

### What Doesn't Work
- [zero_sum_dynamics.md](zero_sum_dynamics.md) — Why most changes are zero-sum, the verify accumulation trap, escaping zero-sum historically
- [failed_patterns.md](failed_patterns.md) — 28 recurring failure modes including ensemble dilution, spatial feature overfit, weak-model ensembling

### Hard Problems
- [hard_confusions.md](hard_confusions.md) — Top confusions at 70.0%, error reachability (219 at rank 6+), generalization of confusions
- [teapot_problem.md](teapot_problem.md) — Shape-defined classes: 58.5% via conditional logic despite 14.5% base score

### Generalization
- [generalization_gap.md](generalization_gap.md) — 58.65pp gap analysis: verify conditions as memorized corrections, the frozen system, layer-by-layer val decomposition

### Meta / Learning System
- [program_induction.md](program_induction.md) — The deeper frame: the codebase is the model, eval is reward, patches are actions. The frozen system: when induction reaches completeness.
- [patch_safety.md](patch_safety.md) — Cascade amplification, safe mutation zones, and the cost of wrong changes
- [optimization_trajectory.md](optimization_trajectory.md) — Sessions 1-26 progression, phases A-L, train optimization COMPLETE at 100%
- [../../anycode/representation_gap.md](../../anycode/representation_gap.md) — Cross-architecture comparison between hand-crafted forests and learned CNN features
