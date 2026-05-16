# hlinet/sensors

<!-- RCC-MINI-README:START -->

## Purpose

Layer-1 classical vision operators that extract typed atoms from raw image pixels.

## S - Formal specification

This folder contains pixel-level sensor modules for color, edges, segmentation, shape, and texture. Sensors should transform raw images into Atom objects without making final class decisions.

## H - Hooks and integration edges

Sensor outputs feed scene graph construction and feature predicates. Sensor changes propagate downstream into hlinet/scene, hlinet/features, hlinet/classifier, hlinet/proof, and hlinet/eval.

## A - Artifacts

color.py, edges.py, segmentation.py, shape.py, texture.py, and __init__.py.

## T - Theory or method basis

Classical computer vision signal extraction is the base representation layer. The Phase 1 ceiling depends partly on what these sensors can extract from 64x64 pixels.

## I - Invariants

- Sensors extract evidence; they do not decide classes.
- Preserve Atom/Region typing.
- Keep output kinds aligned with registry expectations.
- Sensor changes can alter many features and must be evaluated.

## E - Example

After editing a sensor, run python -m hlinet.eval.runner and inspect proof traces for classes affected by the changed signal.

<!-- RCC-MINI-README:END -->
