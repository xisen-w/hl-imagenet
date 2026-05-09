# HL-Image-Net: Comprehensive Design Document

## 1. Vision and Motivation

### 1.1 The Core Question

A neural network creates a continuous, distributed, compositional representation space and searches it via gradient descent. Can we build the symbolic equivalent — a typed, relational, hierarchical representation algebra searched by program synthesis?

### 1.2 Why This Matters

- **Interpretability**: Every classification produces a proof trace
- **Editability**: Fix a failure by editing a predicate, not retraining
- **Compositionality**: New classes reuse existing parts (wheels, fur, beaks)
- **Scientific clarity**: Makes explicit what "representation" means
- **Agentic AI**: Tests whether LLMs can externalize visual knowledge into code

### 1.3 The Honest Limitation

Neural networks have three advantages this system must replace:

| Neural Advantage | Symbolic Replacement |
|-----------------|---------------------|
| Smooth optimization (gradients) | Program search / evolutionary search / agent repair |
| Distributed representation | Compositional typed libraries |
| Data-driven feature discovery | Error-driven feature invention |

---

## 2. System Architecture

### 2.1 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT IMAGE                           │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 1: CLASSICAL VISION PARSER                │
│                                                             │
│  Canny edges │ Sobel gradients │ HOG │ Color histograms     │
│  Gabor filters │ LBP │ Watershed segmentation │ Contours    │
│  Hough transforms │ Shape descriptors │ Keypoints           │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│            LAYER 2: SYMBOLIC SCENE GRAPH                     │
│                                                             │
│  Nodes: regions, parts, contours, texture patches           │
│  Edges: above, below, inside, adjacent, symmetric, repeated │
│  Attributes: color, size, elongation, roundness, texture    │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│            LAYER 3: CONCEPT ROUTER                           │
│                                                             │
│  Coarse classification → activate relevant subspaces        │
│  animal? → expand mammal/bird/fish/insect                   │
│  vehicle? → expand car/bus/bike/train                       │
│  Only compute features for activated branches               │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│            LAYER 4: SYMBOLIC CLASSIFIER                      │
│                                                             │
│  Graph matching against class prototypes                    │
│  Compositional predicate evaluation                         │
│  Soft scoring with evidence accumulation                    │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│            LAYER 5: PROOF GENERATOR                          │
│                                                             │
│  Claim: "image contains a zebra"                            │
│  Evidence: quadruped body + stripe texture + outdoor context │
│  Confidence: 0.87                                           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 The Visual Concept Algebra

#### Formal Definition

```
V = (A, O, R, C, S)

A = Atoms       {edge, contour, region, texture_field, blob, keypoint}
O = Operators   {merge, split, compare, repeat, align, abstract, bind, filter}
R = Relations   {above, below, inside, attached, symmetric, parallel, covers, repeated}
C = Composition {Part = O(A, R); Motif = O(Part, R); Concept = O(Motif, Context)}
S = Scoring     {score: Concept × Image → FeatureValue}
```

#### Type System

```
Region → Texture
Region → Shape
Region × Region → Relation
Part × Part × Relation → Motif
Motif × Motif → Object
Object × Context → ClassHypothesis
```

Types prevent invalid compositions:
- `attached_to(leg, torso)` — valid
- `inside(color, symmetry)` — type error

#### Feature Values (Not Booleans)

Every predicate returns a structured value:

```python
@dataclass
class FeatureValue:
    present: bool
    confidence: float        # [0, 1]
    region: BoundingBox      # where in the image
    scale: float             # relative size
    orientation: float       # degrees
    evidence: list[str]      # supporting observations
    relations: list[Relation]
```

This makes symbolic representation approach neural feature-map richness.

---

## 3. Component Design

### 3.1 Classical Vision Parser (`scripts/primitives/`)

The bottom layer converts pixels into symbolic atoms using non-neural methods:

| Category | Operators |
|----------|-----------|
| **Edge detection** | Canny, Sobel, Laplacian, structured edges |
| **Texture** | Gabor bank, LBP, GLCM, Laws' filters |
| **Color** | Histogram (HSV/Lab), dominant colors, color moments |
| **Shape** | Contour detection, Fourier descriptors, Hu moments |
| **Keypoints** | SIFT, ORB, Harris corners, FAST |
| **Segmentation** | Watershed, graph-based (Felzenszwalb), SLIC superpixels |
| **Geometry** | Hough lines/circles, convex hull, skeleton |

Output: a set of typed visual atoms with spatial coordinates.

### 3.2 Scene Graph Builder (`scripts/scene_graph/`)

Converts atoms into a structured graph:

```python
@dataclass
class SceneGraph:
    nodes: list[ObjectCandidate]
    edges: list[SpatialRelation]

@dataclass
class ObjectCandidate:
    region: BoundingBox
    contour: np.ndarray
    texture: TextureDescriptor
    color: ColorDescriptor
    shape: ShapeDescriptor
    size: float
    elongation: float
    roundness: float

@dataclass
class SpatialRelation:
    source: int  # node index
    target: int  # node index
    type: str    # above, below, inside, attached, adjacent, ...
    confidence: float
```

### 3.3 Feature Library (`scripts/features/`)

A growing library of reusable visual predicates, organized hierarchically:

```
features/
├── primitives/
│   ├── edge_density.py
│   ├── color_distribution.py
│   ├── texture_periodicity.py
│   └── shape_compactness.py
├── parts/
│   ├── wheel_like.py
│   ├── eye_like.py
│   ├── beak_like.py
│   ├── leg_like.py
│   ├── handle_like.py
│   └── wing_like.py
├── textures/
│   ├── striped.py
│   ├── spotted.py
│   ├── furry.py
│   ├── metallic.py
│   └── smooth.py
├── relations/
│   ├── bilateral_symmetry.py
│   ├── repeated_pattern.py
│   ├── attached_below.py
│   └── contains.py
└── concepts/
    ├── quadruped.py
    ├── vehicle_like.py
    ├── bird_like.py
    ├── container.py
    └── furniture_like.py
```

Each feature file follows a standard interface:

```python
class Feature:
    name: str
    input_type: Type
    output_type: Type
    description: str

    def evaluate(self, input: SceneGraph) -> FeatureValue:
        ...

    def robustness_score(self) -> float:
        """How well does this survive perturbations?"""
        ...
```

### 3.4 Concept Router (`scripts/algebra/`)

Implements conditional computation — the symbolic analogue of attention:

```python
class ConceptRouter:
    def route(self, scene_graph: SceneGraph) -> list[str]:
        """Determine which concept subspaces to activate."""
        coarse_scores = {
            "animal": self.score_animal_like(scene_graph),
            "vehicle": self.score_vehicle_like(scene_graph),
            "food": self.score_food_like(scene_graph),
            "tool": self.score_tool_like(scene_graph),
            "furniture": self.score_furniture_like(scene_graph),
            ...
        }
        # Only expand branches above threshold
        active = [k for k, v in coarse_scores.items() if v > 0.3]
        return active
```

This prevents computing all 1000 class features for every image.

### 3.5 Hierarchical Classifier (`scripts/classifiers/`)

Classification tree:

```
animal → mammal → dog → breed-level
       → bird → order → species
       → fish → family → species
vehicle → car → model type
        → truck → type
        → bicycle/motorcycle
tool → kitchen → specific tool
     → workshop → specific tool
food → fruit → specific fruit
     → dish → specific dish
```

Each node has specialized predicates. Fine-grained discrimination uses increasingly detailed features:

```python
# Coarse: is it a dog?
dog_like = quadruped AND fur_texture AND snout AND NOT vehicle_features

# Fine: what breed?
husky_vs_malamute = (
    face_mask_pattern
    AND ear_shape(pointy vs rounded)
    AND body_proportion(compact vs stocky)
    AND fur_color_distribution
)
```

### 3.6 Agent Loop (`scripts/agent/`)

The feature invention agent:

```
1. Run classifier on validation set
2. Collect errors (false positives, false negatives)
3. Analyze confusion patterns
4. Propose new symbolic feature (write Python code)
5. Test feature on training images
6. Measure class separation (information gain)
7. If useful: add to library
8. If redundant or weak: discard
9. Recompose affected class rules
10. Repeat
```

The agent's diagnostic questions:

```
- Which classes are most confused?
- What visual property distinguishes them?
- Can I write a predicate for that property?
- Does the predicate generalize across examples?
- Is it robust to perturbations?
```

### 3.7 Proof Generator (`scripts/eval/`)

Every classification emits a reasoning trace:

```
Claim: image contains a zebra (confidence: 0.87)
Evidence:
  1. Main object is quadruped-shaped (0.91)
     - 4 elongated regions below body region
     - body elongation ratio: 1.8
  2. Body texture is striped (0.94)
     - alternating dark/light bands
     - periodicity: 8.2px
     - coverage: 63% of body region
  3. Context suggests outdoor/savanna (0.72)
     - green/brown background regions
     - no indoor indicators
  4. No conflicting features detected
     - no wheel layout
     - no screen/keyboard pattern
Therefore: zebra (0.87)
Alternatives: horse (0.31), donkey (0.18)
```

---

## 4. The Symbolic Nonlinearity

### 4.1 Why Linear Feature Addition Fails

```python
# BAD: linear scoring
score = 0.3 * fur + 0.4 * legs + 0.2 * tail
```

### 4.2 Symbolic Nonlinear Operations

The system uses:

| Operation | Role |
|-----------|------|
| `AND` / `OR` / `NOT` | Logical gating |
| `EXISTS` / `FORALL` | Quantification over regions |
| `COUNT ≥ k` | Cardinality constraints |
| `THRESHOLD` | Soft activation |
| `ARGMAX` / `TOP-K` | Selection |
| `IF-THEN` | Conditional feature expansion |
| `GRAPH_MATCH` | Structural comparison |

### 4.3 Conditional Expansion (Symbolic Attention)

```python
if score("animal_like", image) > 0.7:
    activate(["mammal", "bird", "fish", "insect"])
    # Now compute fur, feathers, scales, exoskeleton
else:
    suppress(["breed_features", "wing_patterns"])
    # Don't waste computation
```

This is the nonlinear route through representation space.

---

## 5. Search and Learning

### 5.1 Permitted Learning Methods

| Method | Use Case |
|--------|----------|
| Decision trees | Class hierarchy nodes |
| Random forests | Ensemble over symbolic features |
| Gradient-boosted trees | Fine-grained discrimination |
| k-NN | Prototype matching over symbolic descriptors |
| Genetic programming | Feature program evolution |
| Program synthesis | Targeted predicate invention |
| MDL search | Concept compression |
| Bayesian classifiers | Probabilistic class scoring |
| Case-based reasoning | Exemplar matching |

### 5.2 Feature Search Constraints

To prevent combinatorial explosion:

1. **Minimum description length** — prefer simpler programs
2. **Information gain** — feature must separate classes
3. **Robustness** — must survive standard perturbations
4. **Reusability** — bonus for features useful across multiple classes
5. **Type safety** — only valid compositions allowed
6. **Curriculum** — start coarse, refine incrementally

### 5.3 The Compression Objective

A good visual concept is a program that compresses positive examples and excludes negatives:

```
minimize:
    description_length(program)
  + errors_on_positive_examples
  + errors_on_negative_examples
```

Example: "zebra" compresses as `horse_body + black_white_stripes`.

---

## 6. Robustness

### 6.1 Perturbation Testing

Every feature is tested under:

- Crop (random 80-100%)
- Rotation (±15 degrees)
- Brightness (±30%)
- Blur (Gaussian σ=1-3)
- Partial occlusion (10-30%)
- Scale (0.7x-1.5x)
- Background variation

A feature is kept only if:
- Stable under irrelevant changes
- Sensitive to concept-relevant changes

### 6.2 Exemplar Diversity

Each class stores multiple symbolic prototypes:

```
golden_retriever:
  prototype_1: yellow fur, floppy ears, outdoor
  prototype_2: lying position, long fur
  prototype_3: head close-up, black nose, golden hair
```

Classification by nearest symbolic match avoids requiring one universal rule.

---

## 7. Ontology Integration

### 7.1 Semantic Prior Knowledge

ImageNet labels have structure. Use it:

```
WordNet / ontology
    ↓
visual attributes (has_fur, has_wheels, has_beak)
    ↓
symbolic detectors (mapped to vision operators)
    ↓
class rules
```

### 7.2 Attribute-to-Detector Mapping

```python
ontology_mapping = {
    "has_wheels": circular_components_near_bottom,
    "has_stripes": repeated_alternating_bands,
    "has_long_neck": elongated_vertical_above_torso,
    "has_beak": triangular_protrusion_from_head,
    "has_handle": loop_attached_to_body,
}
```

---

## 8. Implementation Plan

### Phase 1: Foundation (10 classes)

**Goal**: Prove the algebra works end-to-end.

Classes: zebra, school bus, golden retriever, bicycle, mushroom, teapot, piano, eagle, laptop, banana

Tasks:
1. Implement classical vision parser (edge, color, texture, segmentation)
2. Build scene graph constructor
3. Define type system and algebra core
4. Hand-write ~20 primitive features
5. Implement coarse router (animal/vehicle/object/food)
6. Build decision tree classifier
7. Generate proofs
8. Evaluate on 100 images per class

**Success**: >50% accuracy on 10-class subset with interpretable proofs.

### Phase 2: Feature Agent (50 classes)

**Goal**: Test agent-driven feature invention.

Tasks:
1. Implement error analysis module
2. Build feature proposal agent (LLM-assisted)
3. Implement feature testing/scoring pipeline
4. Add part library (eyes, wheels, legs, etc.)
5. Expand class hierarchy (add fine-grained animals, vehicles)
6. Implement prototype matching
7. Add perturbation robustness testing

**Success**: >40% accuracy on 50 classes, library grows to 100+ features.

### Phase 3: Scaling (100 classes)

**Goal**: Stress-test feature reuse and hierarchical routing.

Tasks:
1. Full hierarchical classifier tree
2. Concept router with learned thresholds
3. Feature reuse metrics
4. Evolutionary feature search
5. Fine-grained discrimination predicates
6. Cross-class part sharing analysis

**Success**: >35% accuracy on 100 classes, feature reuse rate >3x per feature.

### Phase 4: Full ImageNet (1000 classes)

**Goal**: Push to the frontier. Answer: when does symbolic collapse?

Tasks:
1. Complete class hierarchy
2. Automated feature generation at scale
3. Scaling law analysis
4. Comparison with neural baselines
5. Identify failure modes and boundaries
6. Write paper

**Success**: Documented scaling curve. Identify the boundary where symbolic representation collapses.

---

## 9. Evaluation Metrics

| Metric | Purpose |
|--------|---------|
| Top-1 accuracy | Standard benchmark comparison |
| Top-5 accuracy | Allow soft symbolic uncertainty |
| Proof validity | % of proofs with grounded evidence |
| Feature reuse | Average classes per feature |
| Library growth | Features added per phase |
| Robustness | Accuracy under perturbation |
| Interpretability | Human agreement with proofs |
| Compression ratio | MDL of class programs |
| Invention rate | Useful features per agent iteration |

---

## 10. The Deep Insight

A non-neural ImageNet solver should not look like:

```
1000 hand-written class heuristics
```

It should look like:

```
a growing symbolic visual operating system
```

With:
- Visual primitives
- Part detectors
- Scene graphs
- Symbolic predicates
- Program search
- Rule learning
- Error-driven feature invention
- Proof-style explanations

The representation space is:
- **Typed** (prevents nonsense)
- **Relational** (captures structure)
- **Hierarchical** (enables reuse)
- **Compositional** (combinatorial richness)
- **Probabilistic** (soft, not brittle)
- **Searchable** (by program synthesis)

The clean comparison with neural nets:

| Dimension | Neural | This System |
|-----------|--------|-------------|
| Representation | Continuous vectors | Typed symbolic objects |
| Composition | Matrix multiplication | Algebraic operators |
| Nonlinearity | Activation functions | Routing / predicates / graph matching |
| Search | Gradient descent | Program synthesis / evolution / agent |
| Memory | Weights | Reusable concept library |
| Interpretability | Opaque | Proof traces |

---

## 11. File Naming Conventions

- Agent logs: `logs/YYYY-MM-DD_HH-MM_<description>.md`
- Feature files: `scripts/features/<category>/<feature_name>.py`
- Class rules: `scripts/classifiers/classes/<class_name>.py`
- Evaluation runs: `logs/eval_<phase>_<date>.json`

---

## 12. Dependencies

Core (Python, no neural networks):
- `numpy` — numerical operations
- `opencv-python` — classical vision operators
- `scikit-image` — segmentation, texture, morphology
- `scipy` — signal processing, spatial operations
- `scikit-learn` — decision trees, forests, k-NN
- `networkx` — graph operations for scene graphs
- `matplotlib` — visualization

Optional (agent/search):
- `deap` — evolutionary algorithms / genetic programming
- `openai` or `anthropic` — LLM for offline feature proposal (not used at inference)

---

## 13. Success Criteria

The project succeeds if it answers:

> **How far can a self-growing symbolic visual program library scale before it collapses?**

Even modest ImageNet accuracy with interpretable proofs would be a significant contribution. The scaling curve itself — where symbolic methods work, where they struggle, where they break — is the core scientific finding.
