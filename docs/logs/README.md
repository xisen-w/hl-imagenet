# docs/logs

<!-- RCC-MINI-README:START -->

## Purpose

Documentation-side reasoning and architecture notes. This folder preserves higher-level explanations of how the symbolic system is composed and why design transitions occurred.

## S - Formal specification

Use this folder as derived documentation. It explains architecture and composition but should not override package source, evaluation code, or runtime logs.

## H - Hooks and integration edges

Connects design explanations to hlinet package structure, docs/design.md, docs/blog.md, and root README interpretation.

## A - Artifacts

Architecture notes and reasoning logs, especially composition_architecture.md.

## T - Theory or method basis

HL-ImageNet tests heuristic learning for static image classification using classical computer vision, symbolic feature predicates, scoring rules, tiebreakers, proof traces, evaluation logs, and confusion-driven iteration. Preserve the distinction between Phase 1 development-set performance and held-out validation.

## I - Invariants

- Keep these notes explicitly interpretive.
- Do not treat architecture prose as proof that code still behaves that way.
- Update notes when module topology or scoring flow changes.

## E - Example

Read docs/logs/composition_architecture.md before writing a broad architecture summary.

<!-- RCC-MINI-README:END -->
