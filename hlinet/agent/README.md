# hlinet/agent

<!-- RCC-MINI-README:START -->

## Purpose

Heuristic-learning loop components for analysis, proposal generation, testing, and iteration orchestration.

## S - Formal specification

This folder contains the agentic maintenance loop: analyze errors, propose changes, test changes, and orchestrate iteration.

## H - Hooks and integration edges

Consumes evaluation results and interacts conceptually with source edits, regression checks, reasoning snapshots, and logs.

## A - Artifacts

analyzer.py, proposer.py, tester.py, loop.py, and __init__.py.

## T - Theory or method basis

This is the HL feedback loop surface: run evaluation, analyze confusion, propose feature/fix, test regressions, deploy or revert.

## I - Invariants

- Agent loop code should not bypass evaluation.
- Proposed changes are not validated until tested.
- Keep reasoning/evidence trails visible.
- Do not let agent iteration inflate claims beyond measured results.

## E - Example

Review analyzer.py and tester.py before changing how the system decides whether a proposed fix is acceptable.

<!-- RCC-MINI-README:END -->
