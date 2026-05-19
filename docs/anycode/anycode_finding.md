# The "Any Code" Experiment: What Happens When You Remove All Architecture Constraints

## Setup

We gave a coding agent one instruction: write `predict(image) -> label` to maximize accuracy on 10-class Tiny ImageNet (64x64). No fixed architecture — no "signatures", no "scorer", no "tiebreaker slots". Any code allowed, only constraint: cv2/numpy/scipy, no neural networks.

## Attempt 1: The agent memorizes immediately

Given unconstrained "any code, optimize train accuracy", the agent's first move was to build a KNN classifier using all 2000 training images as templates. It extracted a 46-dimensional feature vector per image (color histograms + edge density + spatial stats), stored them in `templates.npz`, and did distance-weighted k=5 voting at inference time.

Result: **100% train accuracy in one iteration.** The agent solved the optimization problem in the most direct way possible — by memorizing the answer key.

## Attempt 2: GNB with hand-tuned rules

With the constraint "no stored training data at inference time", the agent wrote a Gaussian Naive Bayes classifier with 46 features and hand-written confusion resolution rules. This hit a ceiling at **49.4% train** because GNB treats features independently.

### Why GNB plateaus

The confusion matrix told the story: brown_bear→golden_retriever (40 errors), banana→orange (38), school_bus→sports_car (32). These are classes that share individual features — brown bears and golden retrievers are both warm-toned and furry, bananas and oranges are both brightly saturated fruit. GNB scores each feature independently, so it can't express "warm AND textured AND dark bottom = brown_bear, NOT golden_retriever." The agent tried hand-writing confusion resolution rules for 12+ class pairs, but each fix introduced new cross-class errors. The approach was fundamentally limited.

## Attempt 3: Compiled Random Forest

### The reasoning

The GNB ceiling forced a rethink. The features weren't the problem — the same 46 features gave KNN 41.2% val, so they carry real discriminative signal. The problem was how features were combined. What we needed was conjunctive logic: "if hue is warm AND saturation is moderate AND texture variance is high AND center-vs-periphery brightness is negative, THEN brown_bear." Decision trees express exactly this.

The bold move: instead of hand-tuning more rules, **auto-generate the entire classifier** by building decision trees from training data, then compiling them to pure Python if/else code. The trees ARE the code — no stored data, no lookup tables.

### Iteration log

**Single tree (depth 18, 701 nodes):** 82.0% train. Immediately jumped +33 points over GNB. Every class above 77%. But a single tree overfits to the training split boundaries.

**Forest of 11 trees (depth 16, bagged):** 86.9% train. Ensemble voting smoothed out individual tree errors. OOB accuracy per tree ~40%, suggesting val would be moderate.

**Forest of 21 deeper trees (depth 20):** 91.1% train. Sports_car 95%, school_bus/golden_retriever/mushroom 93%+. The worst class (orange) still 86.5%. File size: 676KB of pure if/else code.

**Forest of 51 shallow trees (depth 10):** 86.9% train — same as 11 deeper trees. Shallow trees hit a complexity ceiling; depth matters more than count for this problem.

**Decision: keep 21 deep trees.** Highest train accuracy, and the OOB spread suggested the ensemble was capturing complementary patterns, not just redundant memorization.

### Feature engineering for trees

We also expanded the feature set from 46 to 71:
- **Spatial grid (16 features):** 2×2 quadrant means of hue, saturation, value, and edge density. Captures layout — penguins have dark tops and light bellies, school buses have yellow middles and dark wheels.
- **Spatial thirds (9 features):** Top/mid/bottom third statistics. Mushrooms have bright caps and dark stems. Bears have dark backs and lighter underbellies.

These spatial features were nearly useless for GNB (F-ratios <0.1) but highly discriminative in trees, because trees can threshold "top-third value < 100 AND bottom-third saturation > 80" — exactly the kind of conjunction GNB cannot express.

## Results

| | KNN memorizer | Phase 2 base+rerank | Phase 2 full verify | GNB anycode | Forest v1 | **Forest v2** |
|---|---|---|---|---|---|---|
| **Train** | 100% (memorized) | ~52% | 100% | 49.4% | 91.1% | **90.2%** |
| **Val** | 41.2% | 51.9% | 41.35% | ~40% | 58.8% | **64.4%** |

### Per-class val accuracy (Forest v2)

| Class | Val |
|-------|-----|
| school_bus | 79.0% |
| jellyfish | 76.0% |
| sports_car | 74.5% |
| orange | 71.0% |
| king_penguin | 68.0% |
| golden_retriever | 57.0% |
| brown_bear | 56.5% |
| mushroom | 56.0% |
| banana | 54.0% |
| teapot | 52.0% |

## What this tells us

1. **Unconstrained optimization memorizes first.** 100% train / 41.2% val. The trivial solution — and exactly why held-out evaluation exists.

2. **Feature interactions matter more than feature quality.** GNB and the forest use overlapping features, but the forest captures conjunctions ("warm AND textured AND dark bottom") that GNB treats independently. That's the 49.4% → 91.1% train jump, and 13+ points on val.

3. **Hand-engineering hits a ceiling the automated approach doesn't.** Phase 2's best documented generalizing hand-built stack, base scoring plus pairwise reranking, reached 51.9% val after 200+ iterations. The full verify endpoint reached 100% train but collapsed to 41.35% val. The compiled forest reached 64.4% val automatically. The agent's manual confusion resolution rules were discovering the same conjunctive logic that trees find by construction — but doing it one pair at a time, and getting worse as the rule count grew.

4. **Spatial layout is powerful but only in conjunction.** Quadrant and third-split features had low individual F-ratios but became highly discriminative inside tree branches. A mushroom's bright cap means nothing in isolation — it matters when combined with "green in bottom third AND earthy hue AND moderate texture." Trees express this naturally.

5. **41.2% is the raw-feature floor.** KNN over raw features gets 41.2% val. Everything above that is how you combine features. GNB reaches 49.4% train but weak val. Phase 2 base+rerank gets 51.9% val. Trees get 64.4% val. The combination logic is worth 23+ points.

6. **More orthogonal features help, but not indefinitely.** Adding LAB/DCT/Gabor/FFT/Hu features to the forest (+1.7pp val) was productive. But adding MORE spatial/shape features actually hurt — the ensemble's subsampling means each tree sees fewer relevant features as the total grows. The best observed setup is a compact set of diverse, orthogonal features.

## The HL insight

The test: **delete the training data. Does the classifier still work?**
- KNN: No. Needs stored templates.
- GNB: Yes. 46 hardcoded means/stds + hand-written rules.
- Forest: Yes. 34,011 decision nodes encoding visual knowledge.

All three are learned from data. But only the last two produce an executable classifier rather than a nearest-neighbor template database. The forest is strictly better because it captures feature interactions that flat scoring cannot.

The compiled forest is one logical endpoint of the anycode branch: the HL loop (eval → analyze → edit code → test) is fully automated. `build_forest.py` is the learning algorithm. `predict.py` is the learned program. The 34,011 decision nodes are conceptually identical to hand-written rules like "if saturation > 120 and hue in [5,20] and edge density > 0.15, then orange" — but discovered automatically rather than through 200+ manual iterations.

## The generalization lesson

The Phase 2 hand-engineered system achieves 100% train but only 41.35% val (58.65pp gap). The forest achieves 90.2% train and 64.4% val (25.8pp gap). This 33pp gap difference tells us:

- **Trees regularize naturally.** Each split partitions the data into large groups. The 16-sample minimum leaf size means no branch memorizes fewer than 16 images — versus the Phase 2 verify conditions which fire on 1-10 images each.
- **Ensembles smooth errors.** 101 trees voting means a single overfit branch gets outvoted. The Phase 2 system has no ensemble — each condition fires independently with full authority.
- **The cost of perfection.** Pushing from 90.2% → 100% train would require the same kind of per-image memorization that destroyed Phase 2's generalization. The 9.8% train error is the PRICE of 64.4% val accuracy.
