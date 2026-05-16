# Edit Risk Hierarchy

Not all changes carry equal risk. This hierarchy was learned empirically from 330+ iterations.

## Risk Levels (low → high)

### 1. Repulsion pairs — SAFE
- **What**: Adding a new pair to `_REPULSION_PAIRS` with force 0.008-0.012
- **Typical impact**: +0 to +1 per pair
- **Why safe**: Small forces (0.01 typical), conservative triggers (disc_gap > 1.0), symmetric push/pull
- **Worst case seen**: -1 from jellyfish-teapot repulsion (cascade through sports)
- **Guidance**: Just add it and eval. Almost never needs revert.

### 2. Local verify conditions on EXISTING pairs — LOW RISK
- **What**: Adding/relaxing a conjunctive condition for a pair that already has verify logic
- **Typical impact**: +1 to +7 per condition
- **Why safe**: Fires on very few images (margin < 0.15 AND pair match AND feature thresholds). Stage 7 — nothing downstream.
- **Worst case seen**: -0 (conditions are specific enough that bad ones just don't fire, rather than causing harm)
- **Guidance**: Test fix/risk ratio in advance. If fix ≥ risk + 2, deploy.

### 2b. Local verify conditions on NEW pairs — MEDIUM-HIGH RISK
- **What**: Adding verify for a pair that NEVER had verify before
- **Typical impact**: -1 to -25
- **Why risky**: Even 6:1 fix/risk ratios and seemingly safe conditions cause massive cascades. Downstream components (repulsion, reranking) weren't calibrated for these swaps. Session 14: all 3 new-pair verifies failed (-25 combined, -2 standalone).
- **Guidance**: Strongly prefer adding verify to existing pairs (relaxing thresholds). If must add to new pair, test with extreme caution.

### 3. Reranking margin/multiplier tuning — LOW-MEDIUM
- **What**: Changing `margin12`, `margin13`, threshold multipliers
- **Typical impact**: +1 per parameter change
- **Why moderate**: Affects all pairs at that rank depth. Wider margins let more swaps through, including wrong ones.
- **Worst case seen**: -5 from verify margin 0.15→0.18
- **Guidance**: Move in small increments (0.02-0.03). Eval after each step.

### 4. Discriminant feature additions — MEDIUM
- **What**: Adding a new feature signal to an existing `_compute_disc()`
- **Typical impact**: -2 to +2 (highly variable)
- **Why risky**: Changes the discriminant's output for ALL images where that pair is evaluated. Can flip correct predictions.
- **Worst case seen**: -8 from has_dark_bright_contrast in bus-sports disc
- **Guidance**: Check cross-class d' (not within-class d'). Only deploy if cross-class d' > 0.8. Start with conservative sigmoid scale.

### 5. Confidence gates — MEDIUM
- **What**: Adding or tightening `_CONFIDENCE_GATES`
- **Typical impact**: +1 to +3 for new gates, -2 to -13 for tightening
- **Why risky**: Rejects the #1 prediction entirely. If #2 is wrong (which it is 50-70% of the time), you lose.
- **Worst case seen**: -13 from KP gate at 0.38
- **Guidance**: Sweep thresholds before deploying. Count TP-in-range vs FP-in-range, but remember that #2 being correct is NOT guaranteed.

### 6. Discriminant pair bases — MEDIUM-HIGH
- **What**: Changing `_PAIR_DISC_BASE` thresholds
- **Typical impact**: -1 to +2
- **Why risky**: Controls how aggressively a discriminant fires. Lowering a base lets more swaps through (risky). Raising it blocks rescues (costly).
- **Worst case seen**: -3 from lowering bear-KP base
- **Guidance**: Only touch bases for pairs where you have specific evidence of systematic over/under-firing.

### 7. Score calibration — HIGH
- **What**: Changing `_SCORE_CALIBRATION` offsets
- **Typical impact**: -3 to -19 for removal, +1 to +4 for careful additions
- **Why dangerous**: Affects ALL images for that class. Changes score gaps that reranking was tuned for.
- **Worst case seen**: -19 from removing KP +0.01 calibration
- **Guidance**: Never remove existing calibration without understanding why it exists. New offsets: ±0.01 max, one class at a time.

### 8. Base signatures — VERY HIGH
- **What**: Adding/removing features from class signature functions
- **Typical impact**: -8 to -28
- **Why catastrophic**: Changes the score of that class for ALL 2000 images at stage 1. Every downstream stage was calibrated for the previous score distribution.
- **Worst case seen**: -28 from adding binary_complexity to teapot signature
- **Guidance**: Almost never worth it at this stage. The signatures are locally optimal. Any gain for the target class is overwhelmed by cascade regressions.

### 9. Histogram blend weight — VERY HIGH
- **What**: Changing `_HIST_BLEND_W` (currently 0.88)
- **Typical impact**: -17
- **Why catastrophic**: Changes ALL scores simultaneously. Every threshold, every gap, every discriminant was tuned for 0.88/0.12.
- **Worst case seen**: -17 from 0.88→0.90
- **Guidance**: Don't touch it. The current value is a Schelling point that everything else was calibrated around.

## The Pattern

Risk increases with scope:
- **Pair-specific, late-stage** (verify, repulsion): safe
- **Pair-specific, mid-stage** (discriminant features, bases): moderate
- **Class-wide, mid-stage** (gates, calibration): high
- **Global, early-stage** (signatures, blend weights): catastrophic

Always prefer the lowest-risk intervention that addresses the problem.
