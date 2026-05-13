# scripts/metrics

<!-- RCC-MINI-README:START -->

## Purpose

Script surface for generating RCC / AEFL repository-process metrics and charts.

## S - Formal specification

This folder contains metrics scripts that inspect the repository and emit Markdown, JSON, and plot artifacts describing context coverage, evidence coverage, claim-boundary coverage, rejected-delta learning, and controlled-evolution status.

## H - Hooks and integration edges

- `generate_rcc_process_dashboard.py` reads the root README, logs, rejected-delta ledgers, and mini READMEs.
- It writes metrics to `docs/metrics/`.
- It writes charts to `docs/plots/`.
- It updates the root README with the human-facing RCC dashboard section when needed.

## A - Artifacts

- `generate_rcc_process_dashboard.py`

## T - Theory or method basis

RCC process metrics make repository context observable. They track whether the repo is navigable, auditable, bounded, and evidence-linked.

## I - Invariants

- Do not use these metrics as classifier-accuracy claims.
- Do not treat a high RCC score as source correctness.
- Do not silently change classifier runtime behavior from this script.
- Generated plots must remain labeled as repository-process metrics.

## E - Example

Run from the repository root:

    python scripts/metrics/generate_rcc_process_dashboard.py

<!-- RCC-MINI-README:END -->