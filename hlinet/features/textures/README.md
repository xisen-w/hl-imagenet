# hlinet/features/textures

<!-- RCC-MINI-README:START -->

## Purpose

Texture and pattern feature detectors, including stripes, repeated patterns, and other surface cues.

## S - Formal specification

This folder extracts symbolic texture predicates from scene/image evidence.

## H - Hooks and integration edges

Consumes sensor and scene data; feeds classifier decisions for classes where visual texture matters, such as zebra-like, mushroom-like, fur-like, or patterned surfaces.

## A - Artifacts

patterns.py and __init__.py.

## T - Theory or method basis

Texture features are central to the representation-saturation discussion because some discriminative signals fall below 64x64 resolution.

## I - Invariants

- Preserve texture thresholds with evidence notes when changed.
- Do not claim unresolved micro-texture is captured if the image resolution cannot support it.
- Re-check dog/mushroom/teapot confusions after texture edits.

## E - Example

Run evaluation and inspect confusion involving golden retriever, mushroom, and teapot after texture changes.

<!-- RCC-MINI-README:END -->
