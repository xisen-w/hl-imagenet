# HL-Image-Net

**A Self-Growing Symbolic Visual Algebra for ImageNet Classification**

Non-neural image recognition through agentic program synthesis, compositional feature libraries, and typed visual concept algebras.

---

## Thesis

Neural networks succeed because they learn high-dimensional compositional representations. This project asks:

> Can agentic program synthesis construct an explicit symbolic representation space with comparable compositional richness?

The system does not hand-code ImageNet heuristics. It **grows the language** in which images can be classified.

## Core Idea

```
Image
 → Classical vision parser (edges, contours, textures, keypoints)
 → Symbolic scene graph (parts, attributes, relations)
 → Feature invention agent (writes & tests Python predicates)
 → Hierarchical classifier (coarse → fine)
 → Proof/explanation generator (visual reasoning trace)
```

The "parameters" are not matrix weights. They are:
- Functions and thresholds
- Typed symbolic objects
- Relations and compositions
- Class prototypes
- A growing library of reusable visual predicates

## Architecture

```
Primitive Visual Operators
        ↓
   Scene Graph Builder
        ↓
  Visual Concept Algebra
   (atoms → parts → motifs → concepts)
        ↓
   Concept Router
   (coarse-to-fine, conditional expansion)
        ↓
   Symbolic Classifier
   (graph matching + rule composition)
        ↓
   Proof Generator
```

### The Visual Concept Algebra

A typed algebra `V = (A, O, R, C, S)`:

| Component | Role |
|-----------|------|
| **A** — Atoms | color patches, edges, contours, texture fields, regions |
| **O** — Operators | merge, split, compare, repeat, align, abstract, bind |
| **R** — Relations | above, below, inside, attached, symmetric, parallel, covers |
| **C** — Composition Rules | Part = op(atoms, relations); Motif = op(parts, relations) |
| **S** — Scoring Functions | score(concept, image) → [0, 1] with confidence + evidence |

### Representation Layers

```
Level 0: Pixels
Level 1: Edges, corners, blobs, gradients, textures
Level 2: Parts — eyes, wheels, wings, legs, handles, beaks
Level 3: Objects — bird, dog, bicycle, cup (graph families)
Level 4: Fine classes — husky, malamute, golden retriever
```

## Key Design Principles

1. **Library, not model** — Knowledge lives in a growing code library, not frozen weights
2. **Typed composition** — Types prevent nonsense compositions and control explosion
3. **Soft predicates** — Features return confidence + region + evidence, not just booleans
4. **Conditional routing** — Only expand relevant subspaces per image (symbolic attention)
5. **Error-driven invention** — The agent writes new features to fix classification failures
6. **Hierarchical classification** — Coarse-to-fine, never flat 1000-way

## Project Structure

```
hl-image-net/
├── README.md
├── docs/
│   └── design.md           # Comprehensive design document
├── scripts/
│   ├── primitives/         # Level 1: classical vision operators
│   ├── scene_graph/        # Scene graph construction
│   ├── algebra/            # Visual concept algebra core
│   ├── features/           # Agent-invented feature library
│   ├── classifiers/        # Hierarchical symbolic classifiers
│   ├── agent/              # Feature invention agent loop
│   └── eval/               # Evaluation and benchmarking
└── logs/                   # Agent run logs and experiment records
```

## Research Questions

1. **Basis sufficiency** — What minimal set of visual primitives generates a rich enough concept space?
2. **Search efficiency** — How to find useful compositions without combinatorial explosion?
3. **Scaling laws** — When does the symbolic library collapse under class complexity?
4. **Generalization** — How do symbolic programs survive viewpoint, lighting, and occlusion?
5. **Comparison** — At what class count does neural representation become strictly necessary?

## Scaling Plan

```
Phase 1:  10 classes  — Prove the algebra works
Phase 2:  50 classes  — Test hierarchical routing
Phase 3: 100 classes  — Stress-test feature reuse
Phase 4: 1000 classes — Full ImageNet (the frontier)
```

## Non-Neural, But Not Anti-Learning

The system bans neural networks at inference time. It permits:

- Decision trees and random forests
- k-NN over symbolic features
- Genetic programming / evolutionary search
- Program synthesis
- Minimum description length search
- Bayesian classifiers
- Rule learning

The agent (which may use an LLM) generates candidate code **offline**. At inference: `image → pure Python symbolic pipeline → label`.

## The Beautiful Punchline

The agent's job is not to classify images directly.

**The agent's job is to grow the language in which images can be classified.**

---

*A research project exploring the frontier between symbolic AI and representation learning.*
