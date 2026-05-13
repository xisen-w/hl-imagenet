# Phase 2.6D Rejected Probe — Golden Retriever / Orange Exclusion

<!-- RCC-MINI-README:START -->

## Purpose

Preserve the Phase 2.6D class-specific controlled-delta probe as a rejected near-miss artifact without committing the classifier behavior change.

## S - Formal specification

The probe added one class-specific exclusion:

    golden_retriever excluding_features += phase2_orange_signature

The probe improved top-1, top-3, HL-unique wins, golden_retriever false positives, king_penguin false positives, orange recall, and sports_car recall.

It failed because banana false positives increased.

## H - Hooks and integration edges

- Probe file: `hlinet/classifier/hierarchy.py`
- Comparison artifact: `rejected_phase2_6d_probe_compare.md`
- Next design target: Phase 2.6E paired class-specific probe with banana backstop

## A - Artifacts

- `rejected_phase2_6d_probe_compare.json`
- `rejected_phase2_6d_probe_compare.md`

## T - Theory or method basis

Class-specific deltas are more promising than global scorer pressure, but single exclusions can shift errors into another attractor. The next probe should preserve the golden_retriever/orange benefit while preventing banana spillover.

## I - Invariants

- Do not commit the failed hierarchy change.
- Do not claim improvement from this rejected probe.
- Preserve the failure because it constrains the next probe.
- Future deltas must rerun benchmark, attribution, candidates, and regression guard.

## E - Result

Rejected / near-miss summary:

- Overall status: fail
- Top-1: 0.334 → 0.3345
- Top-3: 0.6865 → 0.6875
- HL-unique wins: 68 → 70
- Baseline-right / HL-wrong: 817 → 818
- banana false positives: 416 → 420
- golden_retriever false positives: 245 → 240
- king_penguin false positives: 389 → 387
- orange recall: 0.165 → 0.185
- sports_car recall: 0.115 → 0.120

Decision:

    Revert hierarchy change.
    Preserve near-miss probe evidence.
    Next classifier attempt should include a banana-spillover backstop.

<!-- RCC-MINI-README:END -->