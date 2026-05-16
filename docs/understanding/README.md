# Understanding: Distilled Knowledge from HL-ImageNet

This folder contains indexable, searchable knowledge extracted from 14 sessions (640+ iterations) of building a symbolic image classifier from scratch. Each file covers one topic at depth.

## How to use
- **Before making a change**: read the relevant file to see what's been tried, what worked, and why things fail
- **After a session**: update or add files based on new findings
- **When stuck**: read `pipeline_mechanics.md` and `cascade_risk.md` to understand system dynamics before proposing changes

## Index

### System Architecture
- [pipeline_mechanics.md](pipeline_mechanics.md) — The 7-stage prediction pipeline: score → blend → calibrate → repulse → sort → rerank → verify
- [feature_inventory.md](feature_inventory.md) — All feature types: what's orthogonal, what's saturated, what's available
- [edit_risk_hierarchy.md](edit_risk_hierarchy.md) — Which parts of the system are safe to touch, which are dangerous

### What Works
- [techniques_that_work.md](techniques_that_work.md) — Proven techniques ranked by impact, with conditions for success
- [orthogonal_features.md](orthogonal_features.md) — Why representation expansion beats parameter tuning, and which axes are orthogonal

### What Doesn't Work
- [zero_sum_dynamics.md](zero_sum_dynamics.md) — Why most changes are zero-sum, the sink class problem, why reverts dominate
- [failed_patterns.md](failed_patterns.md) — Recurring failure modes: normalization, calibration, signature changes, generic interventions

### Hard Problems
- [hard_confusions.md](hard_confusions.md) — Irreducible confusion pairs, generalization of confusions across splits
- [teapot_problem.md](teapot_problem.md) — Shape-defined classes in a color/texture feature space

### Generalization
- [generalization_gap.md](generalization_gap.md) — Train/val/test gap analysis: what overfits, what generalizes, per-pipeline-stage breakdown

### Meta / Learning System
- [program_induction.md](program_induction.md) — The deeper frame: the codebase is the model, eval is reward, patches are actions
- [patch_safety.md](patch_safety.md) — Cascade amplification, safe mutation zones, and the cost of wrong changes
- [optimization_trajectory.md](optimization_trajectory.md) — Historical accuracy progression, diminishing returns, phase transitions
