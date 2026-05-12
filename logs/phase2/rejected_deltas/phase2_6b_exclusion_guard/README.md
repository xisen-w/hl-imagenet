# Phase 2.6B Rejected Delta — Exclusion-Guard Scoring Delta

<!-- RCC-MINI-README:START -->

## Purpose

Preserve the failed Phase 2.6B controlled classifier delta as a rejected evidence artifact without committing the failed classifier behavior change.

## S - Formal specification

This folder stores the rejected-delta comparison output for the Phase 2.6B exclusion-guard scoring experiment.

The attempted delta changed the scoring equation from:

    score = required_score * 0.75 + supporting_score * 0.15 - excluding_score * 0.15 - alt_penalty

to:

    score = required_score * 0.72 + supporting_score * 0.16 - excluding_score * 0.22 - alt_penalty

The regression guard rejected the delta.

## H - Hooks and integration edges

- The rejected result came from the Phase 2.6B local delta comparison.
- This ledger informs future Phase 2.6D class-specific delta design.
- The failed scorer change is not committed.

## A - Artifacts

- `rejected_phase2_6b_delta_compare.json`
- `rejected_phase2_6b_delta_compare.md`

## T - Theory or method basis

The failure teaches that global exclusion pressure is too blunt. It reduced one attractor but increased others and dropped top-1/top-3 below guard thresholds.

## I - Invariants

- Do not commit the failed classifier delta.
- Do not claim improvement from this rejected experiment.
- Preserve the failure because it constrains the next design.
- Future classifier deltas should be class-specific or guarded, not global scorer-pressure changes.

## E - Result

Rejected delta summary:

- Overall status: fail
- Top-1: 0.334 → 0.3255
- Top-3: 0.6865 → 0.681
- HL-unique wins: 68 → 69
- Baseline-right / HL-wrong: 817 → 835
- banana false positives: 416 → 442
- king_penguin false positives: 389 → 410
- golden_retriever false positives: 245 → 211
- teapot recall: 0.050 → 0.065

Decision:

    Revert global scoring delta.
    Preserve failed-delta evidence.
    Next classifier attempt should be class-specific.

<!-- RCC-MINI-README:END -->