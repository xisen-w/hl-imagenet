# docs

<!-- RCC-MINI-README:START -->

## Purpose

Human-facing documentation for the HL-ImageNet experiment: blog narrative, design notes, result analysis, experiment reports, Phase 2 exploratory analysis, plots, and documentation logs.

## S - Formal specification

Use this folder as the interpretive documentation surface. Documentation here may summarize source behavior and experimental results, but source files, logs, and generated evaluation artifacts remain the evidence surfaces for implementation and measured claims.

## H - Hooks and integration edges

Root README links into this folder for deeper explanation. docs/blog.md and docs/result1.md explain the experiment; docs/experiment_report.md and docs/phase2_eda.md record evaluation interpretation; docs/plots stores generated visual artifacts.

## A - Artifacts

Markdown reports, design documents, EDA notes, generated plot images, and documentation-side logs.

## T - Theory or method basis

HL-ImageNet tests heuristic learning for static image classification using classical computer vision, symbolic feature predicates, scoring rules, tiebreakers, proof traces, evaluation logs, and confusion-driven iteration. Preserve the distinction between Phase 1 development-set performance and held-out validation.

## I - Invariants

- Do not strengthen claims beyond the README evidence boundaries.
- Keep development-set, validation-folder, non-overlapping validation, and Phase 2 claims separate.
- Treat plots as generated documentation artifacts, not standalone proof.
- When results change, update docs from logs or evaluation outputs rather than memory.

## E - Example

Before editing a result claim, compare README.md, docs/result1.md, docs/experiment_report.md, and the relevant logs under logs/phase1.

<!-- RCC-MINI-README:END -->
