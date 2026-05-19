# Program Induction Under Cascade Risk

The deeper frame: we are not hand-engineering a classifier. We are hand-engineering a scientist that writes classifier code.

## The Mapping

| ML Concept | HL-ImageNet Equivalent |
|-----------|----------------------|
| Model | The codebase (`predict.py`, `phase2_signatures.py`) |
| Weights | Thresholds, sigmoid centers/scales, blend weights, pair bases |
| Training data | Eval logs (JSON + markdown per run) |
| Loss function | Eval runner (`hlinet.eval.runner`) |
| Gradient | Confusion matrix + per-class accuracy delta |
| Optimizer | The agent's iteration loop (think → implement → eval → log → decide) |
| Regularization | Cascade risk awareness, revert policy, edit risk hierarchy |
| Learning rate | Size of parameter changes (±0.01 calibration, ±0.02 margin) |

## Why This Frame Matters

If you treat this as "engineering a classifier," you focus on features, thresholds, and accuracy. You get stuck at local optima because each change is greedy.

If you treat it as "program induction," you focus on:
1. **Action space**: What patches are expressible? (new features, new conditions, parameter tweaks)
2. **Reward signal**: What does the eval runner tell us? (confusion matrix, per-class breakdown)
3. **State representation**: What does the agent observe? (current accuracy, error distribution, feature correlations)
4. **Policy**: How does the agent decide what to try next? (bottleneck analysis → hypothesis → experiment)
5. **Safety**: How do we avoid catastrophic updates? (revert policy, cascade awareness)

## The Heuristic Genome

The codebase has a structure analogous to a biological genome:

**Conserved regions** (must not mutate):
- Pipeline ordering (score → blend → calibrate → repulse → sort → rerank → verify)
- Histogram blend weight (0.88) — everything is calibrated around it
- Existing discriminant pair structure
- Base signature feature sets

**Variable regions** (safe to mutate):
- Local verify conditions (new conditions can be added freely)
- Repulsion pairs (safe to add, small effect)
- Reranking margin/multiplier parameters (move in small steps)

**Regulatory regions** (control expression of other code):
- Confidence gates (determine which predictions pass through)
- Gap scaling parameters (control how aggressively reranking fires)
- Per-pair base thresholds (control sensitivity of each discriminant)

**Mutations in conserved regions are almost always lethal.** This maps perfectly to biological evolution — the regions that everything depends on cannot be changed without breaking downstream systems.

## Safe Mutation Zones

Before making a change, ask: "If this change is wrong, how many images are affected?"

| Zone | Scope | Images affected | Revert cost |
|------|-------|:---:|:---:|
| New verify condition | 1 pair, margin < 0.15 | 2-10 | None (remove condition) |
| New repulsion pair | 1 pair, disc_gap > 1.0 | 5-20 | None (remove pair) |
| Discriminant feature | 1 pair, all candidates | 50-200 | Low (remove feature) |
| Confidence gate | 1 class, score < threshold | 20-100 | Low (remove gate) |
| Pair base threshold | 1 pair, all rankings | 50-200 | Medium (must find old value) |
| Calibration offset | 1 class, all images | 2000 | Medium |
| Signature term | 1 class, all images at stage 1 | 2000 × 6 downstream stages | High |
| Blend weight | All classes, all images | 2000 × 10 classes | Very high |

**Rule**: Prefer mutations in the narrowest-scope zone that can address the problem.

## Cascade Accounting

Every change has a "blast radius" — the number of downstream decisions it affects. Before deploying:

1. **Direct effect**: How many images are directly affected? (e.g., verify fires on 7 images)
2. **Cascade factor**: How many downstream stages reprocess those images? (verify = 0 stages, signature = 6 stages)
3. **Expected regression**: direct_effect × P(wrong) × cascade_factor
4. **Expected gain**: direct_effect × P(correct) × (1 + bonus_from_cascade_alignment)

If expected_regression > expected_gain × 0.5, the change is probably not worth it. The 0.5 factor accounts for our consistent overestimation of gains.

## Diagnostics Before Patches

The agent should spend MORE time diagnosing than patching. Current ratio is roughly 30/70 (diagnosis/patch). Optimal is probably 60/40.

**Good diagnostic steps:**
- Compute confusion matrix and identify top-3 error pairs
- For each error pair: count reachable (rank ≤ 3) vs unreachable (rank > 3)
- For reachable errors: compute cross-class d' on error images from BOTH sides
- Compute fix/risk ratio before implementing
- Check if the proposed feature is correlated with existing features (|r| < 0.3?)

**Bad diagnostic steps:**
- Looking at class-level d' (misleading — see failed_patterns.md)
- Counting total errors without checking reachability
- Assuming discriminant accuracy generalizes from class-level to error-level

## The Learning Loop as Science

Each iteration is an experiment:
1. **Hypothesis**: "Adding feature X to discriminant Y will fix errors A, B, C without affecting D, E, F"
2. **Prediction**: "Expected +3 correct, -1 regression, net +2"
3. **Experiment**: Implement and run eval
4. **Observation**: Actual +1 correct, -4 regression, net -3
5. **Update**: "Feature X is correlated with something in D and E's scoring. Cross-class d' was lower than expected. Don't use features with cross-class d' < 0.8."

**The update step is the most important.** Without it, the agent repeats the same mistake with different features. The session reasoning log and these understanding documents ARE the agent's learned knowledge — they prevent re-treading failed paths.

## The Frozen System: When Induction Reaches Completeness

At 100% train accuracy with ~900 verify conditions, the system enters a novel state: **every possible single-feature threshold that could fire on the pipeline output has been claimed**. This is the program induction equivalent of a "fully trained" model — but with a crucial difference:

**In neural networks**, 100% train means the loss landscape has a flat region (zero loss) where gradient descent settles. Small perturbations to weights stay in this flat region.

**In program induction**, 100% train means a FRAGILE equilibrium. Each condition is a hard threshold that either fires or doesn't. There is no "flat region" — any modification to any threshold changes the exact set of images it fires on. Because downstream conditions were calibrated to the EXACT ranking output of all upstream conditions, changing one condition creates a cascade of broken assumptions.

### Why the system cannot be improved without regression

1. **Threshold saturation**: Every feature value that separates an error image from its risk pool has been deployed. New conditions for val errors would fire on some train correct image (because verify already claimed that threshold region).

2. **Condition interference**: The 900+ conditions interact through shared rankings. Image A's rank-7 swap changes what Image B sees at rank-3. This was discovered as "wave saturation" — but it's actually a fundamental property of ANY system where corrections share a global state (the ranking).

3. **No slack in the system**: With 100% accuracy, there are zero "free" images to absorb collateral damage from changes. In a 90% system, a change that fixes 3 and breaks 2 is net positive. In a 100% system, ANY breakage is regression.

### The overfitting-completeness tradeoff

This creates an impossible choice:
- **Keep 100% train**: Accept 41.35% val (58.65pp gap). The system has memorized all 2000 images.
- **Improve val**: Must sacrifice train accuracy by removing verify waves. Best achievable: 51.9% val with base+reranking only (but train drops to ~52% too).
- **No middle ground exists**: You cannot have both high train AND high val because the verify conditions that push train above ~52% are the same conditions that hurt val.

### Implication for program induction theory

The "frozen system" problem suggests that greedy program induction (add conditions one at a time, never break existing ones) necessarily converges to a memorized system when pushed to 100%. The conditions accumulate until they form a lookup table — each image has its own correction path.

This is the program synthesis equivalent of the bias-variance tradeoff: a program that perfectly fits all training data must be complex enough to memorize, and that complexity cannot generalize.

**Possible escapes** (not yet attempted):
1. **Joint optimization**: Rewrite all conditions simultaneously using val as a constraint
2. **Regularization**: Only deploy conditions that fire on ≥N images (where N is large enough to ensure generalization)
3. **Feature improvement**: Improve base scoring so fewer conditions are needed (higher-quality features that capture class-level patterns rather than per-image outliers)
4. **Ensemble of simpler systems**: Multiple prediction paths, each less overfit, combined via voting

## Autonomous Heuristic Scientist (Aspirational)

The ideal architecture for continued improvement:

```
loop:
    state = read_latest_eval_log()
    bottleneck = identify_top_bottleneck(state)
    
    # Diagnosis phase (60% of time)
    error_analysis = analyze_errors(bottleneck)
    reachability = check_reachability(error_analysis)
    feature_scan = scan_orthogonal_features(error_analysis)
    cross_d_prime = compute_cross_class_d_prime(feature_scan, error_analysis)
    
    # Hypothesis generation
    candidates = generate_patch_candidates(cross_d_prime, reachability)
    candidates = filter_by_edit_risk(candidates)
    candidates = filter_by_failed_patterns(candidates)
    
    # Experiment
    best = select_highest_expected_value(candidates)
    implement(best)
    result = eval()
    
    # Learn
    if result.net > 0: commit()
    else: revert()
    log(hypothesis=best, prediction=expected, actual=result)
    update_understanding(best, result)
```

The key insight: the agent's action space is patches to source code. Its reward is eval accuracy. Its state is the current codebase + accumulated understanding. It can be viewed as reinforcement learning over program edits, with the agent implemented as an LLM instead of a neural policy network.

## Optimization Ceilings: Three Types (Session 27)

The project has encountered three distinct types of ceiling, each requiring different escapes:

### Type 1: Architecture ceiling (escapable by structural extension)
- **Example**: 70.0% — adding verify conditions WITHIN the pipeline hit cascade limits
- **Escape**: Place conditions AFTER the pipeline (zero cascade)
- **Signal**: Changes work in isolation but regress due to downstream interactions

### Type 2: Feature ceiling (escapable by new feature types)
- **Example**: 58.8% val (forest v1) — 71 HSV/spatial features max out at this accuracy
- **Escape**: Add orthogonal feature types (LAB, DCT, Gabor, FFT → 64.4% val)
- **Signal**: All parameter combinations plateau at the same accuracy

### Type 3: Completeness ceiling (requires architectural reset)
- **Example**: 100% train (Phase 2 pipeline) — cannot improve train accuracy further because every training image is already corrected
- **Example**: 64.4% val (forest v2) — was not improved by the tried hyperparameter, feature, and voting changes
- **Signal**: Changes in ALL directions lead downhill. No local escape exists.

The distinction matters because each type requires a DIFFERENT kind of intervention. Trying a Type 1 fix (structural extension) on a Type 3 ceiling wastes effort. Trying a Type 3 escape (full reset) on a Type 1 ceiling abandons progress unnecessarily.

**How to diagnose**: If accuracy drops for ALL perturbations (parameters, features, architecture) → Type 3 (feature-quality limited). If accuracy drops for parameter changes but not structural ones → Type 1 (architecture limited). If accuracy drops for same-type features but not orthogonal ones → Type 2 (feature diversity limited).

### Session 29 Confirmation of Type 3 (Completeness Ceiling)

The anycode forest at 64.4% was attacked from 25+ angles over 3 sessions. Every approach—new features, ensemble methods, regularization tuning, stacking, specialization—yielded ≤64.6%. This is strong evidence for a Type 3 ceiling in the tested search space:

The ceiling appears not to be in the combination method but in the information content of the features. No tried architectural variant extracted signal that the features did not contain. To break this ceiling likely requires either:
1. **New measurement tools** (local spatial features that survive position variance — an unsolved problem at 64×64)
2. **Learned features** (CNN/representation learning — a fundamentally different paradigm)

This is analogous to trying to determine 3D shape from a silhouette: once a projection discards information, clever reasoning has limited room unless a new measurement recovers the missing signal.
