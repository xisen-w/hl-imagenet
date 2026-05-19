# Phase 2 Docs

Phase 2 is the main hand-built symbolic pipeline on 10 real Tiny ImageNet classes at 64x64.

## Files

- [phase2_eda.md](phase2_eda.md) — Dataset and class statistics.
- [phase2_experiment_log.md](phase2_experiment_log.md) — Early chronological experiment notes.
- [phase2_local_vision.md](phase2_local_vision.md) — Proposal to move from global statistics to local perception.
- [lessons.md](lessons.md) — Lessons from the hand-built symbolic pipeline.
- [theory.md](theory.md) — Theoretical framing for next-generation heuristic learning.
- [understanding/](understanding/) — Distilled Session 1-26 knowledge about cascade dynamics, overfitting, hard confusions, and patch safety.
- [plots/](plots/) — Phase 2 trajectory plot.
- [logs/composition_architecture.md](logs/composition_architecture.md) — Composition analysis of the symbolic feature/scoring stack.

## Most Important Boundary

The 70.0% train / 49.4% val result belongs here. It is the hand-built symbolic pipeline before the later anycode forest work. No decision trees are responsible for that 70% train result.

The later 100% train / 41.35% val endpoint is also Phase 2, but it should be treated as an overfitting artifact: verify waves memorized training corrections and harmed validation.
