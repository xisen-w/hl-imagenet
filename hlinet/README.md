# hlinet

<!-- RCC-MINI-README:START -->

## Purpose

Main Python package for the HL-ImageNet symbolic heuristic-learning classifier.

## S - Formal specification

This is the implementation root. It coordinates sensors, scene graph building, feature registration, classifier scoring, proof traces, evaluation harnesses, agent loop components, and visual concept algebra.

## H - Hooks and integration edges

Imports connect subpackages: sensors extract atoms, scene builds relations, features emit predicates, classifier scores/tiebreaks, proof renders explanations, eval measures behavior, agent supports iterative learning.

## A - Artifacts

Python package modules including __init__.py, registry.py, types.py, and subpackages for sensors, scene, features, classifier, proof, eval, agent, and algebra.

## T - Theory or method basis

HL-ImageNet tests heuristic learning for static image classification using classical computer vision, symbolic feature predicates, scoring rules, tiebreakers, proof traces, evaluation logs, and confusion-driven iteration. Preserve the distinction between Phase 1 development-set performance and held-out validation.

## I - Invariants

- Preserve package importability.
- Do not introduce neural-network or gradient-descent dependencies without changing public claims.
- Keep feature and sensor registration coherent.
- Any behavior change should be checked through evaluation commands.

## E - Example

Run python -m hlinet.eval.runner after meaningful classifier, feature, scene, or sensor changes.

<!-- RCC-MINI-README:END -->
