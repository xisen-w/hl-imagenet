# hlinet/classifier/classes

<!-- RCC-MINI-README:START -->

## Purpose

Class-level classifier namespace and class organization surface.

## S - Formal specification

This folder is reserved for class-specific classifier organization.

## H - Hooks and integration edges

Connects to classifier scoring and prediction logic when class-specific modules or definitions are added.

## A - Artifacts

__init__.py and any future class-specific files.

## T - Theory or method basis

Class definitions should remain transparent symbolic components, not hidden model weights.

## I - Invariants

- Keep class additions aligned with README methodology.
- Do not add classes without updating evaluation methodology.
- Preserve synthetic-versus-real class distinctions.

## E - Example

When adding a new class surface, update classifier rules, docs, evaluation splits, and this README.

<!-- RCC-MINI-README:END -->
