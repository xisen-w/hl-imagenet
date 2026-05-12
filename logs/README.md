# logs

<!-- RCC-MINI-README:START -->

## Purpose

Experiment logs, evaluation outputs, reasoning snapshots, and phase-specific runtime history.

## S - Formal specification

This folder stores generated and historical evidence records. Treat logs as evidence artifacts with methodology boundaries.

## H - Hooks and integration edges

Feeds docs, plots, README summaries, and experiment interpretation. logs/phase1 contains Phase 1 outputs; logs/phase2 stages future split-clean work.

## A - Artifacts

phase1 and phase2 subfolders containing JSON, markdown logs, reasoning snapshots, and placeholders.

## T - Theory or method basis

Logs preserve the HL feedback history: evaluations, iterations, confusion analysis, and reasoning states.

## I - Invariants

- Do not rewrite historical logs to make results look cleaner.
- Distinguish generated logs from curated documentation.
- Use logs as evidence, not as proof outside their methodology.

## E - Example

Before summarizing a result, inspect the relevant log and its phase/methodology context.

<!-- RCC-MINI-README:END -->
