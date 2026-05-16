# Generalization Gap Analysis

What overfits, what generalizes, and where the gap lives in the pipeline.

## Current Numbers (Session 14)

| Metric | Train | Val | Test | Gap (T→V) |
|--------|:---:|:---:|:---:|:---:|
| Top-1 | 57.9% | 52.9% | 51.1% | 5.0pp |
| Top-3 | 76.9% | 75.6% | 74.4% | 1.3pp |

**Key insight**: Top-3 generalizes well (1.3pp gap). The base scoring + histogram blending is sound. The 5.0pp top-1 gap means ~3.7pp is lost in the ranking post-processing — reranking, local verify, and confidence gates.

## Where Overfitting Lives (by pipeline stage)

### Stage 1-3: Base scoring + histogram blend — GENERALIZES WELL
The signature scores and histogram prototype blending are computed from feature statistics that transfer. The proto means/stds were computed on train but at weight 0.025 they contribute little. Histogram blending at 0.88/0.12 is a stable equilibrium.

### Stage 4: Score calibration — NEUTRAL
Only 4 classes have offsets (bus -0.02, jelly +0.02, KP +0.01, mush +0.01). These are tiny and class-level, so they transfer.

### Stage 5: Repulsion — LOW OVERFITTING
Small forces (0.008-0.012) with conservative triggers. The discriminant signals used here are the same ones in reranking, so if the discriminant generalizes, repulsion does too.

### Stage 6: Pairwise reranking — MODERATE OVERFITTING
The 24-pair discriminant system. Each pair has a base threshold + gap-aware scaling. The discriminant sigmoid weights and thresholds were tuned on train. Key sources of overfitting:
- `_PAIR_BASE` values (e.g., banana-teapot: 0.30, brown_bear-KP: 0.25) set pair-specific thresholds calibrated to train score distributions
- Rank-3/4/5 whitelists: wider margin windows let speculative swaps through
- Sigmoid centers and scales in `_compute_pair_signals()`: tuned to train feature distributions

### Stage 7: Local verify — HIGHEST OVERFITTING
15+ pair-specific conjunctive conditions with hard thresholds like `cm_b < 0.57`, `hu1 > 2.65`, `acorr < 0.08`. These are the most overfit components because:
1. Each fires on 2-10 training images — extreme overfitting risk
2. Hard AND-gated thresholds are binary — a small distribution shift means the condition stops firing
3. No confidence calibration — either fires or doesn't

### Stage 7b: Confidence gates — MODERATE OVERFITTING
6 per-class gates (e.g., banana: 0.42, sports_car: 0.40). These reject low-confidence predictions. If the score distribution shifts on val, the gate threshold hits different percentiles.

## Per-Class Overfitting Sources

| Class | Gap | Primary overfitting source |
|-------|:---:|---|
| banana | +10.5pp | Local verify for banana-mushroom, banana-school_bus; confidence gate |
| brown_bear | +11.5pp | GR-bear verify (sat < 0.28 AND dct_high < 0.20); bear-mushroom verify |
| school_bus | +8.5pp | Sports-bus reranking with tight dct_high/grad_mean thresholds |
| golden_retriever | +8.0pp | GR-mushroom verify, GR-bear verify bidirectional |
| mushroom | +3.0pp | Moderate — some verify, but mushroom errors are genuinely hard |
| teapot | +1.5pp | Low gap — teapot is bad on train too, not from overfitting |
| jellyfish | +3.5pp | Minimal — jelly features (sat, color_std, blue_purple) transfer well |
| king_penguin | +2.5pp | Minimal — KP features (bw, fft_hv_ratio) are robust |
| orange | +0.5pp | Near-zero gap — orange's color signature is distinctive and stable |
| sports_car | -0.5pp | Negative gap — sports actually does slightly better on val |

## Strategies to Reduce the Gap

### Already proven to generalize
- Histogram blending (stage 2)
- Repulsion with conservative triggers (stage 5)
- Orthogonal features (LAB, Gabor, FFT) in discriminants

### Likely overfit — candidates for relaxation
- Local verify conditions with tight thresholds (relax or remove conditions that fire on <5 train images)
- Rank-4/5 reranking (deeper = more speculative)
- Pair bases tuned on train error analysis

### Unknown — needs cross-validation study
- Per-class histogram weights
- Confidence gate thresholds
- Sigmoid scales in discriminants

## Experiment: Per-Class Histogram Weights (Session 15, Monitor Cycle 1)

Replaced global `_HIST_BLEND_W = 0.88` with per-class weights ranging from teapot=0.05 to bus=0.16.

**Result**: Train dropped 57.9%→55.3%, val unchanged at 52.9%, gap narrowed 5.0pp→2.4pp.

**Lesson**: The train accuracy loss came entirely from teapot (41→27.5%) because weight 0.05 starved the histogram signal. Meanwhile bus/sports gained because their weights were higher. This confirms: the previous 5.0pp gap was ~2.6pp from train-overfit reranking and ~2.4pp from genuinely harder val images. Per-class hist weights are a knob for redistributing score mass between classes but don't improve generalization unless calibrated on val. Minimum hist weight for any class should be ≥0.10.
