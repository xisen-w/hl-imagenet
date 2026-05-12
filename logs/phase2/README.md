# logs/phase2

<!-- RCC-MINI-README:START -->

## Purpose

Phase 2 evaluation logs and derived diagnostic artifacts for the split-aware 10-real-class Tiny ImageNet experiment.

## S - Formal specification

This folder stores Phase 2 evaluation JSON/Markdown outputs and the derived Phase 2.2 diagnostic reports. Evaluation logs are source evidence artifacts. Diagnostics are derived analysis artifacts generated from those logs.

## H - Hooks and integration edges

- `hlinet/eval/runner.py` writes Phase 2 evaluation reports here when the tag starts with `phase2`.
- `hlinet/eval/diagnostics.py` reads `eval_phase2*.json` files from this folder.
- `scripts/run_phase2_diagnostics.py` writes outputs into `logs/phase2/diagnostics`.
- README and architecture docs may summarize these outputs, but should not strengthen claims beyond the evidence.

## A - Artifacts

- `eval_phase2_*.json`
- `eval_phase2_*.md`
- `diagnostics/latest_phase2_diagnostic.json`
- `diagnostics/latest_phase2_diagnostic.md`
- `diagnostics/README.md`

## T - Theory or method basis

Phase 2 is the split-aware evidence path for the symbolic classifier. The diagnostic lens treats the confusion matrix as a failure-geometry surface where false-positive attractors, victim classes, top-3 rescue gaps, and confusion gravity wells can be measured.

## I - Invariants

- Do not rewrite historical logs to make results look cleaner.
- Preserve tag, split, source report, sample count, and timestamp context.
- Do not treat diagnostic outputs as classifier improvements.
- Do not treat top-3 rescue as top-1 success.
- Do not promote exploratory Phase 2 results into final benchmark claims.

## E - Example

Generate diagnostic reports from the current Phase 2 validation run:

    python scripts/run_phase2_diagnostics.py --input ".\logs\phase2\eval_phase2_iter9_val_2026-05-12_14-37-05.json"

<!-- RCC-MINI-README:END -->