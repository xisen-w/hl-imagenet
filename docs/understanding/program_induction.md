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

The key insight: the agent's action space is patches to source code. Its reward is eval accuracy. Its state is the current codebase + accumulated understanding. This IS reinforcement learning — just with the agent implemented as an LLM instead of a neural policy network.
