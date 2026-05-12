# docs/architecture

<!-- RCC-MINI-README:START -->

## Purpose

Canonical architecture locks and architecture-delta documents for HL-ImageNet repository evolution.

## S - Formal specification

This folder stores architecture documents that define contribution boundaries, software deltas, diagnostic contracts, validation surfaces, falsification surfaces, and non-claim locks before implementation changes are made.

## H - Hooks and integration edges

- `hl_imagenet_rcc_phase2_diagnostic_lens_v1_0.tex` locks the Phase 2.2 diagnostic-lens architecture.
- `hlinet/eval/diagnostics.py` implements the diagnostic lens authorized by that architecture document.
- `logs/phase2/diagnostics/` stores generated diagnostic artifacts.
- Root README and RCC surfaces should reference architecture locks when new major repo layers are added.

## A - Artifacts

- `hl_imagenet_rcc_phase2_diagnostic_lens_v1_0.tex`

## T - Theory or method basis

Architecture locks preserve attribution and prevent implementation drift. In this repo, the architecture layer distinguishes upstream classifier work from RCC/context contributions and diagnostic/evidence tooling.

## I - Invariants

- Architecture documents must preserve original/upstream attribution.
- Architecture documents must say what is and is not being claimed.
- Architecture documents must not imply runtime changes unless such changes are explicitly implemented.
- Diagnostic architecture does not prove classifier correctness or accuracy improvement.
- Future classifier changes should receive their own architecture delta before implementation.

## E - Example

Read the Phase 2 diagnostic architecture before changing diagnostics:

    docs/architecture/hl_imagenet_rcc_phase2_diagnostic_lens_v1_0.tex

<!-- RCC-MINI-README:END -->