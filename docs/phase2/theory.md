# Theoretical Foundations for Next-Generation Heuristic Learning

*Written after 330+ iterations of building a symbolic image classifier from scratch. These are not speculative ideas — they emerge from specific, documented failures and the structural limits we hit.*

---

## Part I: The Fundamental Problems

### Problem 1: Scalar Features Destroy Spatial Structure

When you compute `yellow_coverage = 0.46`, you've lost *where* the yellow is, what *shape* it forms, and what's *adjacent* to it. Two images with identical scalar feature vectors can look completely different. This is why banana (yellow curve on neutral background) and school_bus (yellow rectangle filling frame) both score high on the same features.

**The core issue:** We're projecting a 64x64x3 = 12,288-dimensional image into ~80 scalars. That's a 150:1 compression ratio. Most of the visual structure lives in what we threw away.

**Empirical evidence from HL-ImageNet:**
- banana `yellow_coverage` mean = 0.46, school_bus mean = 0.24 — but bus scores higher overall because it wins on `grad_mean`, `lap_var`, and `hue_orange`, all of which are *also* scalar summaries that discard spatial layout.
- We tried a 2x2 spatial pyramid (`warm_tl`, `warm_tr`, `warm_bl`, `warm_br`), which helped slightly, but a 2x2 grid is still far too coarse to capture "yellow in a curved shape" vs "yellow in a rectangle."
- The `radial_warm_diff` feature (inner circle vs outer ring warm coverage) was one of our most discriminative features for golden_retriever (d=0.69 vs king_penguin). This hints that spatial structure is where the signal lives — but we only scratched the surface with ad-hoc spatial features.

**What this means for the HL loop:** The agent can tune sigmoid thresholds forever, but if two classes produce the same 80-dimensional feature vector, no amount of parameter adjustment can separate them. The iteration ceiling is set by the *representational bandwidth* of the feature space.

### Problem 2: Additive Independence

```
score = sigmoid(yellow, 0.25, 5) * 0.20 + sigmoid(warm, 0.40, 4) * 0.15 + sigmoid(smooth, 0.15, 5) * 0.15
```

This treats features as **independent evidence**. Each sigmoid contributes its value regardless of what other features say. But "yellow AND smooth AND round" is exponentially more specific than the *sum* of yellow-ness + smooth-ness + round-ness.

**Why this creates sink classes:** A class that *partially* matches on 6 features scores higher than a class that *perfectly* matches on 3. School bus scores 0.538 on average across ALL 2000 images because it partially matches on many general features (edges, warm, gradient). A class like jellyfish, which perfectly matches on 2-3 specific features (blue, translucent, low-edge), scores only 0.320 average. The additive structure rewards breadth over depth.

**The conjunctive insight:** `yellow AND smooth` has a completely different discriminative profile than `yellow + smooth`. Consider:
- `yellow AND smooth`: banana (high), orange (high), school_bus (low — high edge), mushroom (low — textured)
- `yellow + smooth`: banana (high), orange (high), school_bus (medium — yellow helps even though not smooth), mushroom (medium — smooth-ish even though not yellow)

The conjunction eliminates school_bus and mushroom from contention. The sum doesn't. We have a few manually-designed conjunctive features (`smooth_yellow`, `textured_decentered`, `sat_smooth_warm`) and they are among our most discriminative signals. But they were hand-picked — there are C(80,2) = 3,160 possible pairwise conjunctions, and we've explored maybe 10.

**Guard gates as partial fix:** Our `_guarded_score` formula (`pos * (0.5 + 0.5 * min(guards))`) is a step toward conjunctions — a guard that fires zero halves the score. But it's asymmetric: guards can only suppress, never amplify. And the multiplicative interaction is limited to "all positive signals AND all guards pass," not arbitrary feature combinations.

### Problem 3: No Error Attribution

When a mushroom image gets classified as banana, we see the final scores but don't know *which feature* caused the error. Was it because `warm` was too high? Because `edge` was below the guard threshold? Because the histogram blend favored banana? The error is smeared across 80 features, 10 signatures, 24 discriminants, and 2 blending layers.

**Contrast with gradient-based learning:** In a neural network, the gradient tells you exactly which parameter to adjust and by how much: `dL/dw_i` points toward the optimal update for weight `w_i`. This is the fundamental advantage of differentiable systems — error attribution is *automatic*.

**In HL, the agent must guess.** Our session logs show: ~70% of iterations were reverts. The agent hypothesizes "mushroom gets misclassified as banana because warm is too high → add warm guard to mushroom." But the real cause might be that banana's signature is just higher overall due to histogram blending. The intervention was wrong because attribution was wrong.

**What would fix this:** If, for each misclassified image, we could decompose the score difference into per-feature contributions — "banana scored 0.55 vs mushroom 0.48, and the 0.07 gap breaks down as: +0.04 from smooth_yellow, +0.02 from warm_band_bot, +0.01 from histogram" — the agent could target the actual culprit. This is possible in principle (the scoring is a sum of known terms) but not currently implemented.

### Problem 4: Symmetric Scoring Architecture

Every class uses the same formula: `weighted_sigmoid_sum * guard_product`. But:
- **Teapots** need *shape* features (handle, spout, body proportions)
- **Jellyfish** need *color* features (blue/purple translucence)
- **School buses** need *structural* features (horizontal lines, window pattern)
- **Golden retrievers** need *texture-in-context* features (fur texture with natural background)

Forcing all classes through the same architecture means each class can only use a fraction of its feature budget effectively. Teapot has 10 sigmoid terms and 5 guards — but at 64x64, no combination of color/texture statistics can reliably distinguish a metallic teapot from a penguin. The architecture can't represent what teapot *needs*.

**Evidence:** Teapot accuracy is 32.5% — barely 3x random baseline. School bus at 73%. The architecture serves some classes far better than others, depending on whether the class's defining properties align with color/texture statistics.

### Problem 5: Greedy Iteration

The HL loop optimizes for the single biggest bottleneck each iteration: find worst confusion, hypothesize fix, implement, eval, keep or revert. But the global optimum sometimes requires making one class *temporarily worse* to enable a structural change that benefits three others.

**Example from our logs:** Adding score calibration (subtracting class-mean scores) improved overall accuracy from 51.9% to 52.4%. But school_bus dropped from 76% to 73%. Under the greedy revert rule, we might have reverted this change because "school_bus regressed." We kept it because the overall gain was clear, but a strict per-class greedy policy would have blocked the best improvement of the session.

**The loss valley problem:** The scoring system has local optima. Moving from one local optimum to a better one may require passing through a valley where accuracy drops. The greedy loop can't navigate these valleys — it always climbs uphill, which means it gets stuck at whatever local optimum it first reaches.

---

## Part II: Five Methods for Breaking Through

### Method 1: Spatial Feature Fields (SFF)

**Intuition:** Instead of computing scalar features globally, compute them on a spatial grid and preserve the *field structure*.

Instead of `yellow_coverage = 0.46`, compute a 4x4 **yellow field** — a 4x4 matrix showing where yellow is concentrated. Do the same for edges, warm pixels, texture, saturation. Now each "feature" is a small spatial map, not a scalar.

**Classification becomes field matching:** Each class has a prototype field (average spatial pattern of yellow, edges, etc. across training images). Comparison uses spatial correlation, not scalar distance.

**Why this is fundamental:** It preserves the spatial structure that scalars destroy. A banana has yellow in the center; a bus has yellow everywhere; an orange has yellow concentrated in a circle. Their scalar yellow coverage may be identical, but their yellow *fields* are distinct.

**Concrete implementation:**
```python
def compute_field(image, mask_fn, grid_size=4):
    """Compute a spatial field: grid_size x grid_size matrix of mask activations."""
    h, w = image.shape[:2]
    field = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            cell = image[i*h//grid_size:(i+1)*h//grid_size, 
                         j*w//grid_size:(j+1)*w//grid_size]
            field[i, j] = mask_fn(cell)
    return field

# Prototype: average field across all training images of a class
banana_yellow_field = np.mean([compute_field(img, yellow_mask) for img in banana_train], axis=0)

# Score: normalized correlation between image field and prototype field
score = np.corrcoef(image_field.ravel(), prototype_field.ravel())[0, 1]
```

**How it changes the HL loop:**
- Error attribution becomes spatial: "the model expected yellow in the top-left but the image had yellow in the center"
- The agent refines prototype fields rather than tuning thresholds
- Grid resolution (4x4, 8x8, 16x16) becomes the key hyperparameter instead of sigmoid steepness
- Multiple field types (yellow, edge, texture, saturation) can be combined, and the combination weights are the learnable parameters

**Estimated impact on HL-ImageNet:** Banana-bus (30+ mutual errors) should drop significantly since their yellow fields are spatially distinct. Banana-orange may not improve much (both have centered yellow). Teapot may benefit from edge fields (teapots have distinctive horizontal edge patterns). Estimated +3-5pp from this alone.

### Method 2: Conjunctive Feature Lattice

**Intuition:** Instead of additive scoring, organize features into a lattice of **conjunctions** and score at the conjunction level.

Define atomic features: `warm`, `smooth`, `yellow`, `round_edge`, `low_sat`, etc. (We already have ~80 of these.) Then systematically generate pairwise conjunctions: `warm AND smooth`, `yellow AND round_edge`, etc. Each conjunction is a new binary feature: "both conditions met above their respective thresholds."

For each class, find the **minimal set of conjunctions** that separates it from all confusers:
- Banana: `{yellow AND smooth, warm AND high_persistence, hue_orange AND low_edge}`
- Mushroom: `{textured AND green_surround, round_edge AND center_bright, high_dct AND warm}`
- School bus: `{yellow AND high_grad, warm AND directional, high_lap AND hue_orange}`

**Why this is fundamental:** It directly addresses the additive independence problem. `yellow AND smooth` is far more discriminative than `yellow + smooth`. The conjunctive space is exponentially larger — C(80,2) = 3,160 pairwise, C(80,3) = 82,160 triples — enough to separate 10 classes cleanly if the right conjunctions exist.

**The search algorithm (no gradients needed):**
```
For each confused pair (A, B):
  For each candidate conjunction (f_i AND f_j):
    Compute: P(conjunction fires | class A) and P(conjunction fires | class B)
    Score: mutual_information(conjunction, class) or Fisher discriminant ratio
  Keep top-K conjunctions with highest discriminative power
  Add to class A's conjunction set
```

This is pure information-theoretic search — no gradient, no backpropagation, just counting and ranking. The HL loop becomes "search for discriminative conjunctions" rather than "tune weights."

**Key insight for HL:** The agent doesn't need to *invent* features — it needs to *discover which combinations of existing features are jointly discriminative*. This is a combinatorial search problem, and information gain provides an exact, gradient-free objective function.

**Estimated impact:** The existing conjunctive features (`smooth_yellow`, `textured_decentered`) are among our best. Systematically expanding from ~10 to ~50-100 conjunctions should provide enough representation to break through the 52% plateau. Estimated +4-8pp.

### Method 3: Elimination Cascade (Soft Decision Tree)

**Intuition:** Instead of scoring all 10 classes simultaneously and picking the winner, **sequentially eliminate** classes using the cheapest discriminative features first.

```
Stage 1: "Is it blue/purple?"
  YES → jellyfish (done, ~90% accurate for this stage)
  NO  → continue (9 classes remain)

Stage 2: "Is it low-saturation, high bw_ratio?"
  YES → king_penguin (done)
  NO  → continue (8 classes remain)

Stage 3: "Is it high-gradient with directional structure?"
  YES → {bus, sports_car} → Stage 3a: "yellow dominant?" → bus vs sports
  NO  → {banana, orange, GR, bear, mushroom, teapot} → Stage 4

Stage 4: "Is it high-texture with green context?"
  YES → {mushroom, brown_bear} → Stage 4a: centered vs decentered
  NO  → {banana, orange, GR, teapot} → Stage 5

Stage 5: Fine-grained discrimination within remaining group
```

**Why this is fundamental:** It addresses the symmetric scoring problem. Early stages use broad, cheap features to carve the space. Later stages use expensive, targeted features that only need to separate 2-3 classes. A teapot-vs-bear discriminant doesn't need to worry about jellyfish. The feature budget per decision is much smaller, so each decision can be more accurate.

**Information-theoretic guidance:** At each node, the optimal split feature maximizes information gain:
```
IG(feature, split_point) = H(classes) - Σ_child P(child) * H(classes | child)
```
No gradient needed — just count correct/incorrect on each side. The HL agent has an *exact* objective function for building the tree.

**How it changes the HL loop:**
- Error attribution is *local*: if a bear gets misclassified, you know exactly which node made the wrong split. Was it Stage 3 (wrongly classified as "high-gradient")? Or Stage 4a (confused with mushroom)?
- Each node can be optimized independently without affecting the rest of the tree
- Adding a new feature only needs to help at one specific node, not globally

**Key advantage:** The pairwise reranking system we already have is essentially Stage N of a cascade — it corrects errors between top-2 classes. The cascade generalizes this to ALL stages, not just the final correction.

**Estimated impact:** The cascade can exploit the strong early signals (jellyfish blue, bus yellow+structure) more aggressively, and then spend the full feature budget on hard groups (warm-blob triangle, desaturated objects). Estimated +5-10pp, with the biggest gains on currently-confused clusters.

### Method 4: Exemplar Memory with Learned Metric

**Intuition:** Instead of summarizing each class as a single signature (weighted sigmoid sum), keep a small **library of representative images** per class. Classify by finding the nearest exemplar.

Store 10-20 exemplars per class (chosen to cover the class's visual diversity). At inference, compare the image to all exemplars using a **feature-weighted distance**:

```
d(x, exemplar) = Σ_i w_i * (f_i(x) - f_i(exemplar))^2
```

**Why this is fundamental:** A single signature can't represent multi-modal classes. Our data shows:
- Golden retrievers include "dog on grass" (green background, warm center) AND "dog on couch" (warm everywhere, no green) AND "puppy face close-up" (low edge, high symmetry)
- A single sigmoid sum must compromise: it can't have BOTH "high green" and "low green" as positive signals
- But 10 exemplars can cover 10 visual modes without compromise

**Exemplar selection algorithm:**
```
For each class:
  Start with all 200 training images
  Cluster into K clusters (K=10-20) using feature vectors
  Pick the medoid of each cluster as the exemplar
  
  # Refinement via HL loop:
  For each misclassified image:
    If it's nearest to a wrong-class exemplar:
      Check: would adding this image as a new exemplar fix it?
      If yes, and no other class loses: add it
```

**The metric learning step:** The weights w_i determine which features matter most for distance computation. Initialize uniformly, then adjust:
- If a misclassification happens because feature `f_j` was similar between the image and the wrong exemplar but different from the correct exemplar: increase w_j
- This is a simple, gradient-free update rule: `w_j += learning_rate * |gap_j|`

**Connection to theory:** This is kernel nearest-neighbor classification. Cover & Hart (1967) proved: as the number of exemplars grows, the NN error rate converges to at most 2x the Bayes optimal rate. No other method in our current system has any such guarantee. The guarantee holds regardless of the feature space — it only requires that features be *somewhat* discriminative, not perfectly so.

**How it interacts with existing system:** The exemplar distance can be used as a secondary scoring signal alongside signatures:
```
final_score = 0.7 * signature_score + 0.3 * (1 / (1 + min_exemplar_distance))
```

This allows the existing tuned signatures to remain while adding the exemplar's representational power.

**Estimated impact:** Multi-modal classes (GR, bear, teapot) should benefit most. GR currently at 46% with 50 images beyond rank 3 — these are likely "unusual" GR images that don't match the single prototype. With 10 exemplars, the worst-case exemplar distance should be much smaller. Estimated +3-5pp.

### Method 5: Feature Genesis via Genetic Programming

**Intuition:** Instead of the human agent manually inventing features, use **genetic programming** to automatically evolve new feature functions from primitive operations.

Define primitive operations:
```python
# Leaf nodes (terminals):
mean(channel, region)     # mean of a channel in a region
std(channel, region)      # standard deviation
count(mask, region)       # count of True pixels
area(contour)             # area of largest contour
ratio(a, b)               # a / max(b, epsilon)
diff(a, b)                # a - b

# Regions:
full, center, top_half, bot_half, left_half, right_half, inner_circle, outer_ring

# Channels/masks:
gray, hue, sat, val, warm_mask, yellow_mask, edge_mask, blue_mask
```

A "feature" is a **program tree** composed of these primitives:
```
ratio(
  count(yellow_mask, center),
  count(yellow_mask, full)
)
```
This computes "what fraction of yellow pixels are in the center" — a feature that separates banana (high: yellow in center) from school_bus (low: yellow everywhere). A human might design this, but there are thousands of such features that no human would think to try.

**The GP algorithm:**
```
population = [random_program_tree() for _ in range(100)]

for generation in range(1000):
    # Evaluate each feature's discriminative power
    for program in population:
        values = [program.evaluate(img) for img in train_set]
        program.fitness = mutual_information(values, labels)
    
    # Selection, crossover, mutation
    parents = tournament_select(population, k=3)
    children = crossover(parents) + mutate(parents)
    population = elitism_select(population + children, size=100)
```

After GP finishes, the top-K features (highest fitness) are added to the feature vocabulary and can be used in signatures, discriminants, or conjunctions.

**Why this is fundamental:** It addresses the *fixed feature vocabulary* problem. Our current 80 features were all designed by a human agent (Claude) based on intuition about what might discriminate classes. But human intuition is bounded — we can't explore 100,000 possible feature computations. GP can.

**What GP can discover that humans can't:**
- `ratio(std(hue, top_half), std(hue, bot_half))` — hue consistency asymmetry between top and bottom (catches outdoor scenes with sky above and objects below)
- `diff(mean(sat, inner_circle), mean(sat, outer_ring))` — saturation center-surround difference (catches objects-on-background)
- `ratio(count(edge_mask, left_half), count(edge_mask, right_half))` — edge bilateral asymmetry (catches asymmetric objects like cars viewed from the side)

These are all computable from existing image data but not in our feature vocabulary.

**How it changes the HL loop:** The agent's role shifts fundamentally:
- **Before GP:** "I need a feature that separates banana from bus. Let me try... yellow coverage? No. Warm blob extent? Partially. Edge persistence? No."
- **After GP:** "GP found that `ratio(count(yellow, center), area(largest_warm_contour))` has MI=0.43 with class labels. Let me add it to the banana signature and evaluate."

The iteration is no longer about *inventing* representations — it's about *evaluating and integrating* automatically-discovered representations. The search space moves from "which threshold to tweak" to "which discovered features to deploy."

**Connection to theory:** GP is a universal function approximator over programs (Koza, 1992). With sufficient generations, it can discover any computable feature of bounded complexity. The practical question is efficiency — but even a modest GP run (1000 generations x 100 population) explores ~100K feature programs, far more than a human can design in 330 iterations.

**Estimated impact:** Hard to predict precisely because it depends on what GP discovers. But if even 5 new features have d > 1.0 for currently-confused pairs, they could break through the representation ceiling. Estimated +3-8pp.

---

## Part III: The Meta-Insight

All five methods share one deep principle: **the ceiling of heuristic learning is set by the representation, not the optimizer**. 

We've spent 330+ iterations tuning sigmoid thresholds, guard gates, and pairwise discriminants. The gains trajectory tells the story:
- Sessions 1-4: +37pp (new features, new architecture)
- Sessions 5-8: +11pp (compound features, reranking)
- Sessions 9-11: +3pp (guard tightening, threshold tuning)
- Phase 2 iterations 1-330: +5pp (discriminant expansion, calibration)

Each phase delivered smaller returns because it was *optimizing within a fixed representation*. The diminishing returns are not because we ran out of ideas — it's because the representation cannot separate the classes.

**The formal argument:** Consider the 80-dimensional feature space F. If the class-conditional distributions P(F|class_A) and P(F|class_B) overlap substantially, no classifier operating on F can separate them — whether it's sigmoid sums, decision trees, nearest neighbors, or anything else. The Bayes error rate on F is a hard lower bound. To reduce this bound, you must *expand* F — add features that push the distributions apart.

**The path forward:** Change WHAT we measure, not HOW we combine measurements:
- **Spatial fields** preserve structure that scalars discard
- **Conjunctions** capture interactions that sums can't
- **Cascades** focus measurement where it's needed
- **Exemplars** represent diversity that prototypes compress away
- **GP** discovers measurements no human would design

### The Recommended Combination: Cascade + Conjunctions + Fields

The most impactful approach combines methods 3, 2, and 1:

1. **Build an elimination cascade** (Method 3) to decompose the 10-class problem into a tree of binary/ternary decisions. Information gain guides the tree structure.

2. **At each node**, use **conjunctive features** (Method 2) instead of individual sigmoids. The conjunction search is scoped to only the classes remaining at that node — much smaller search space.

3. **Within each conjunction**, features can be **spatial fields** (Method 1) instead of scalars. `yellow_field(center) AND low_edge_field(top)` is far more specific than `yellow AND low_edge`.

This combination addresses Problems 1 (spatial fields), 2 (conjunctions), 3 (cascade gives local error attribution), and 4 (each node has class-specific features). Problem 5 (greedy iteration) is partially addressed because each node can be optimized independently.

**Why this combination is synergistic:**
- The cascade reduces the search space for conjunctions (only need to separate 2-3 classes at each node, not 10)
- Spatial fields make conjunctions more discriminative (spatial interactions are richer than scalar interactions)
- Each layer compensates for the others' weaknesses

### Implications for Heuristic Learning Theory

These methods suggest a broader principle for HL systems:

**The Representation Progression Hypothesis:** In any HL system, the agent should follow a progression of:
1. **Feature invention** (what to measure) — most impactful but hardest
2. **Feature combination** (how to combine measurements) — moderate impact
3. **Parameter tuning** (precise calibration) — least impactful, easiest

Most HL effort naturally gravitates to (3) because it's concrete and measurable. But the biggest gains come from (1). Methods 1, 4, and 5 above automate feature invention. Methods 2 and 3 automate feature combination. Together, they could make HL systems self-improving in the highest-impact dimension.

**The Error Attribution Principle:** HL systems improve fastest when the agent can *decompose* errors into attributable causes. The cascade provides this naturally (which node failed?). Spatial fields provide this for representation errors (which spatial region was wrong?). Without error attribution, the agent is reduced to random search over a large hypothesis space.

**The Representation Saturation Theorem (informal):** For a fixed feature space of dimension D with K classes, there exists a maximum accuracy achievable by *any* classifier. This maximum is the Bayes optimal rate on that feature space. Once the HL system approaches this rate, further iteration cannot improve accuracy — only representation expansion can. The practical signature of saturation is: many iterations with small or zero gain, frequent reverts, and gains that are robbed from other classes (zero-sum dynamics).

We believe HL-ImageNet is near saturation in its current 80-scalar feature space. The evidence: 70% revert rate, zero-sum dynamics on confused pairs, diminishing returns per iteration. The methods above are designed specifically to break through this saturation by expanding the representational space.

---

## Part IV: How Each Method Changes the HL Iteration Speed

A key question: does the method make the HL *loop itself* faster, or just provide a higher ceiling?

| Method | Ceiling increase | Iteration speed | Why |
|--------|:---:|:---:|-----|
| Spatial Fields | +3-5pp | 1.5x faster | Error attribution becomes spatial — agent can see WHERE the feature fails, not just THAT it fails |
| Conjunctive Lattice | +4-8pp | 3x faster | Information gain provides exact guidance — no guessing which conjunction to try |
| Elimination Cascade | +5-10pp | 5x faster | Each node is independent — errors are localized, changes don't cascade, parallel optimization possible |
| Exemplar Memory | +3-5pp | 2x faster | Adding/removing exemplars is O(1) — no weight retuning needed |
| Feature Genesis (GP) | +3-8pp | 10x faster for feature invention | Automates the hardest part — human designs ~1 feature/hour, GP evaluates ~100K/hour |

**The cascade provides the biggest speed improvement** because it breaks the monolithic scoring problem into independent subproblems. Currently, changing one signature affects ALL 10 classes through score competition. In a cascade, changing the bear-vs-mushroom node only affects those two classes.

**GP provides the biggest ceiling increase per unit effort** because it searches a vastly larger feature space than human intuition can.

**The recommended starting point:** Implement Method 3 (cascade) first, because it provides both the largest absolute ceiling increase AND the largest iteration speed improvement. Then add Method 2 (conjunctions) at each node. Then optionally add Method 1 (spatial fields) or Method 5 (GP) for further gains.

---

## Appendix: Empirical Evidence Supporting These Claims

All claims above are grounded in specific observations from HL-ImageNet Phase 2:

**Re: Scalar features destroying structure (P1):**
- banana `warm_coverage` = 0.638, GR `warm_coverage` = 0.515 — only d=0.46 separation
- But banana has warm concentrated in center-bottom, GR has warm everywhere-center — visible in images but invisible in scalars

**Re: Additive independence (P2):**
- `smooth_yellow` (conjunction) has d=0.96 between banana and school_bus
- `yellow` alone has d=0.98 and `smooth_warm` alone has d=0.78 — but the SUM yellow+smooth_warm gives only d=0.71 because they're correlated

**Re: No error attribution (P3):**
- Session 6 alone: 12 attempted changes, 8 reverted — 67% wasted effort
- Most common revert reason: "the real cause was different from what I hypothesized"

**Re: Symmetric architecture (P4):**
- Teapot at 32.5% uses 10 positive signals and 5 guards — same architecture as school_bus at 73%
- The problem is not that teapot has fewer features — it's that shape-relevant features (mid_wider, symmetry, autocorr_h) are weak predictors in a color-dominant system

**Re: Greedy iteration (P5):**
- Score calibration: school_bus -3pp, teapot -1.5pp, but overall +0.5pp — a greedy per-class policy would have reverted
- Histogram blending: banana -0.5pp initially, but after reranking settled: overall +0.6pp

---

*This document should be updated as we implement these methods and gather evidence for or against the theoretical claims.*
