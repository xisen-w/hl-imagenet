# Phase 1 Docs

Phase 1 was the exploratory setup: 4 real Tiny ImageNet classes plus 6 synthetic placeholder classes, tuned on a shared development/evaluation set.

## Files

- [blog.md](blog.md) — Narrative writeup of the first symbolic classifier experiment.
- [experiment_report.md](experiment_report.md) — Final Phase 1 report with methodology caveats.
- [result1.md](result1.md) — Accuracy trajectory and transition analysis.
- [design.md](design.md) — Early system design for a symbolic visual algebra.
- [plots/](plots/) — Phase 1 accuracy and error visualizations.

## Caveat

The headline 86.1% is a development-set number. The honest held-out 4-real-class validation result was roughly 51-54%, depending duplicate handling. Use Phase 1 as evidence that the heuristic-learning loop can grow code, not as a benchmark claim.
