# Any-Code Experiment

## The premise

What if the entire classifier is just a Python file that gets rewritten each iteration? No fixed architecture (no "signatures", no "scorer", no "tiebreaker slots"). Just: `predict(image) -> label`. Any code allowed, only constraint: cv2/numpy/scipy, no neural networks.

## Attempt 1: Unconstrained "optimize train accuracy"

**Result: 100% train in one move.** The agent immediately built a KNN classifier using all 2000 training images as templates (46-dim color+edge histogram features). Euclidean distance, k=5 weighted vote. Perfect memorization.

### But does it generalize?

| | KNN memorizer | Phase 2 system (200+ hand-engineered iterations) |
|---|---|---|
| **Train** | 100% (memorized) | 48.75% |
| **Val** | 41.2% | 50.1% |

The KNN memorizer is 9 points WORSE on val than the hand-engineered system. This means:

1. **When you say "any code", the first thing an optimizer does is memorize.** This is the trivial solution — and it's what unconstrained optimization always finds first. This is the perfect illustration of why held-out evaluation exists.

2. **The Phase 2 system's 50.1% val is legitimately better than brute-force nearest-neighbor over the same data.** The sigmoid signatures, guard gates, and pairwise discriminants are doing real work — they encode generalizable visual patterns, not memorized instances.

3. **41.2% is a feature-quality baseline.** It tells you that 46 histogram/edge features carry about 41% of the discriminative signal. The Phase 2 system's advantage comes from how it COMBINES features (conjunctions, guards, discriminants), not from having better raw features.

### The insight about HL

Heuristic Learning is not about tuning model parameters. It's about **writing the software environment** — the code that processes images. KNN with memorized templates is parameter tuning (the templates ARE the parameters). HL should produce code that encodes visual knowledge as PROGRAMS, not as stored data.

The test: delete the training data. Does the classifier still work? KNN: no. Phase 2 system: yes (it only has ~50 hardcoded thresholds, not 2000 stored images). That's the difference between memorization and learning.

## Attempt 2: Gaussian Naive Bayes (hand-tuned)

Constraint: no stored training data at inference time. All visual knowledge encoded as code and constants.

- 46 hand-crafted visual features (color histograms, edge stats, texture, spatial)
- Per-class means/stds hardcoded, weighted log-likelihood scoring
- Hand-written confusion resolution rules for 12+ class pairs

**Result: 49.4% train.** Hit a ceiling because GNB treats features independently — it can't capture the conjunctive patterns (e.g., "warm AND textured AND dark bottom = brown_bear") that distinguish visually similar classes.

## Attempt 3: Compiled Random Forest (the bold move)

**Key insight:** instead of hand-tuning rules, auto-generate the entire classifier by building decision trees from training data, then compiling them to pure Python if/else code. The trees ARE the code — no stored data, no lookup tables, no parameters.

- 71 features (original 46 + 16 spatial grid + 9 spatial thirds)
- 21 bagged decision trees, max depth 20, compiled to Python functions
- Majority vote across all trees
- `build_forest.py` generates `predict.py` automatically

### Results

| | KNN memorizer | Phase 2 (hand-eng.) | GNB anycode | Forest v1 | **Forest v2** |
|---|---|---|---|---|---|
| **Train** | 100% | 48.75% | 49.4% | 91.1% | **90.2%** |
| **Val** | 41.2% | 50.1% | ~40% | 58.8% | **64.4%** |
| **Gap** | 58.8pp | -1.4pp | ~9pp | 32.3pp | **25.8pp** |

Forest v2 improvements over v1:
- 90 features (was 71): added LAB color moments, DCT frequency bands, Gabor texture, FFT, Hu moments, GLCM
- 101 trees (was 21): more ensemble diversity
- Depth 14, min_samples 16 (was depth 20, min 8): more regularization trades train for val
- Feature subsampling: sqrt(n)*2 = 18 features per split

### Per-class val accuracy (Forest v2)

| Class | Val accuracy |
|-------|-------------|
| school_bus | 79.0% |
| jellyfish | 76.0% |
| sports_car | 74.5% |
| orange | 71.0% |
| king_penguin | 68.0% |
| golden_retriever | 57.0% |
| mushroom | 56.0% |
| brown_bear | 56.5% |
| banana | 54.0% |
| teapot | 52.0% |

### What this means for Heuristic Learning

The forest approach is a proof that **the HL loop can be automated end-to-end**: extract features → build trees → compile to code → evaluate → iterate. The generated `predict.py` is 2.5MB of pure decision logic — 34,011 nodes across 101 trees that encode visual knowledge discovered from data.

This is still "code that encodes visual knowledge" — the thresholds and feature combinations in the tree branches are conceptually the same as hand-written rules, but discovered automatically rather than manually engineered.

### Key insight: feature interactions > feature count

The jump from 71 to 90 features (adding LAB, DCT, Gabor, FFT, Hu, GLCM) gave +1.7pp val. But adding 27 MORE features (finer spatial grids, shape descriptors) actually HURT by -0.6pp because the fixed feature subsampling ratio means each tree sees fewer relevant features. The optimal feature set is not "as many as possible" but "diverse and orthogonal at the right density for the ensemble's subsampling ratio."

## The 64.4% Ceiling (Sessions 27-29)

Exhaustively confirmed via 25+ experiments across 3 sessions:

| Approach | Val accuracy | Why it fails |
|---|---|---|
| HOG spatial gradients | 40.7% | Too noisy at 64×64 |
| Dense spatial color grid | 54.9% | Overfits to object position |
| Patch relationships | 50.5% | Position-sensitive → overfit |
| Bag-of-Visual-Words (32 clusters) | 43.5% | Local descriptors too weak |
| Bag-of-Visual-Words (64 clusters) | 46.0% | Still too weak |
| Combined features (180) | 63.1-64.0% | Dilution always hurts |
| Stacking meta-forest | 63.0% | Overfits vote patterns |
| Pairwise reranking | <64.4% | Discriminants overfit |
| Per-class specialists | 62.5% | Loses inter-class context |
| Weighted sampling | 62.5% | Reduces diversity |
| More trees (301) | 64.5% | Saturated |
| Mixed regularization | 64.0% | No diversity gain |
| Zero-risk verify mining | 0 rules found | Features overlap in error pool |

**The ceiling is feature-quality limited.** The 90 features encode ~64% of the discriminative signal. The remaining 7.4pp gap to CNN (71.8%) requires learned local spatial structure that no hand-crafted combination can express at 64×64.

## Files

- `predict.py` — The classifier (auto-generated by build_forest.py)
- `eval.py` — Train set evaluator
- `eval_val.py` — Val set evaluator
- `build_forest.py` — Builds random forest and compiles to predict.py
- `build_tree.py` — Builds a single decision tree (earlier experiment)
- `compute_stats.py` — Feature statistics computation
- `build_hog_forest.py` — HOG spatial gradient experiment (40.7% val)
- `build_spatial_forest.py` — Dense spatial color grid (54.9% val)
- `build_patch_forest.py` — Patch relationship features (50.5% val)
- `build_bow_forest.py` — Bag-of-Visual-Words (43.5-46% val)
- `build_combined_forest.py` — Combined features test
- `build_stacked_forest.py` — Stacking meta-learner
- `build_pairwise_rerank.py` — Pairwise discriminant reranking
- `build_specialist_forest.py` — Per-class binary specialists
- `build_weighted_forest.py` — F-ratio weighted feature sampling
- `build_replaced_forest.py` — Feature replacement experiment
- `mine_corrections.py` — Zero-risk correction rule mining
- `eval_ensemble.py` — Multi-forest ensemble evaluation
- `eval_gated_ensemble.py` — Gated ensemble (HOG tiebreaker)
