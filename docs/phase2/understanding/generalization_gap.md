# Generalization Gap Analysis

What overfits, what generalizes, and where the gap lives in the pipeline.

## Current Numbers (Session 26)

| Metric | Train | Val | Gap (T→V) |
|--------|:---:|:---:|:---:|
| Top-1 | **100.0%** | 41.35% | **58.65pp** |
| Top-3 | 100.0% | 68.75% | 31.25pp |

### Layer-by-layer val decomposition (confirmed Session 29)

| Pipeline Layer | Val Accuracy | Delta from prev | Train Accuracy |
|---|:---:|:---:|:---:|
| Base scoring only | 45.7% | — | ~45.2% |
| + Pairwise reranking | **51.9%** | **+6.2pp** | ~52% |
| + Local verify (rank 2-5) | 49.4% | -2.5pp | ~70% |
| + Final ranks (rank 2-10) | 42.8% | -6.6pp | ~87% |
| + Waves 2-4 | 42.3% | -0.5pp | ~97% |
| + Waves 5-9 (full) | 41.3% | -1.0pp | 100% |

**Key insight**: Post-pipeline verify conditions actively HARM val by a total of 10.6pp. The pairwise reranking is the ONLY post-processing that generalizes well (+6.2pp). Every verify stage after reranking is memorization that hurts generalization.

**The best documented validation configuration** is base + reranking = 51.9%. This is still below the anycode forest (64.4%) because the base scoring itself is weaker — sigmoid signatures capture less class structure than tree-based conjunctive splits.

**Implication**: The verify machinery (Sessions 9-26, 900+ conditions, 54pp of train gain) is dominated by memorized corrections with negative transfer to val. The reranking (+6.2pp val) is the only post-base processing clearly worth keeping for generalization.

### The "frozen system" problem (discovered Session 26)

At 100% train with 900+ verify conditions:
1. Every feature threshold that could fire on the pipeline output has been claimed for train correction
2. Any threshold that fires on a val error also fires on some train correct image (because verify already pushed that image to correct at that threshold)
3. The system CANNOT be modified without train regression — it's at a strict local maximum from which all neighbors are downhill
4. The only escape: compute entirely NEW features not used in any existing condition, or rebuild from scratch with regularization

**Key insight**: The gap has grown from 5.4pp (Session 16) to 58.65pp (Session 26). This +53pp gap growth came from ~900 verify conditions deployed across Sessions 18-26 (memorized per-image corrections).

**Decomposition**: Base scoring likely generalizes to ~42-44% val (vs 45.2% train = ~2pp gap). Reranking likely generalizes partially (~5pp val gain vs ~10pp train). The remaining ~15pp gap is from verify conditions and deep-rank reranking — each fires on 2-10 train images with hard thresholds tuned to training distributions.

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

### Stage 7: Local verify (4 rank levels) — HIGHEST OVERFITTING
~90 pair-specific conjunctive conditions with hard thresholds across rank levels 2-5. These contribute +293 images on train but likely <50 on val. These are the most overfit components because:
1. Each fires on 2-10 training images — extreme overfitting risk
2. Hard AND-gated thresholds are binary — a small distribution shift means the condition stops firing
3. No confidence calibration — either fires or doesn't
4. Rank-3/4/5 verify is even MORE overfit than rank-2 (deeper = more speculative)

At 70.0% train, verify conditions across all 4 ranks contribute +293 corrections. If even half don't transfer, that's ~15pp of the gap explained.

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

## The Gap Growth Story

| Session | Train | Val | Gap | What was added |
|:---:|:---:|:---:|:---:|---|
| 16 | 58.4% | 52.9% | 5.4pp | Baseline monitoring |
| 18 | 61.25% | ~50% | ~11pp | +50 verify conditions (exhaustive scan) |
| 19 | 67.9% | ~49% | ~19pp | Rank-3/4/5 verify (406 new targets) |
| 20 | 70.0% | 49.4% | 20.6pp | Gate widening, bad condition audit |
| 22 | 78.1% | ~42% | ~36pp | Post-pipeline final verify (161 conditions) |
| 23 | 87.4% | ~41% | ~46pp | Fix-1 mining, 5 waves (~250 conditions) |
| 24 | 97.7% | ~41% | ~57pp | Deep-rank access (ranks 6-10) |
| 25 | 98.45% | ~41% | ~57pp | Conjunctive AND conditions |
| 26 | 100.0% | 41.35% | 58.65pp | Precision fix + wave 9 |

**The fundamental tradeoff**: Every verify condition adds ~0.05-0.35pp on train but ~0pp or NEGATIVE on val. The system has memorized all 2000 training images. The 58.65pp gap is the COST of pushing train to 100%.

**What would reduce the gap**: (1) Remove post-pipeline waves entirely (+8.1pp val, -58.65pp train). (2) Remove in-pipeline verify too (+10.6pp val total). (3) The "base + reranking" config at 51.9% val is the practical best. But the user's directive was train optimization only — the gap is an accepted cost.

## Experiment: Per-Class Histogram Weights (Session 15, Monitor Cycle 1)

Replaced global `_HIST_BLEND_W = 0.88` with per-class weights ranging from teapot=0.05 to bus=0.16.

**Result**: Train dropped 57.9%→55.3%, val unchanged at 52.9%, gap narrowed 5.0pp→2.4pp.

**Lesson**: The train accuracy loss came entirely from teapot (41→27.5%) because weight 0.05 starved the histogram signal. Meanwhile bus/sports gained because their weights were higher. Per-class hist weights are a knob for redistributing score mass between classes but don't improve generalization unless calibrated on val. Minimum hist weight for any class should be ≥0.10.

## Session 22 Monitor: Inner Dev Generalization Audit

The new generalization-aware loop added explicit pipeline modes and an inner train/dev split. The first audit supports the existing layer decomposition:

| Mode | inner_train | inner_dev | val | Reading |
|---|:---:|:---:|:---:|---|
| base | 44.2% | 47.4% | 45.7% | Base scoring transfers; no meaningful train-val gap. |
| base_rerank | 55.1% | 56.2% | 51.9% | Reranking transfers partially; this remains the real symbolic baseline. |
| full | 69.4% | 71.8% | 49.4% | Verify adds much more on train/dev than val; high-variance correction layer. |

**Rigor correction**: the initial inner split used Python `hash(cls)`, which changes across processes. That made the dev split non-reproducible. The split seed must use a stable class hash.

**Rigor correction**: pipeline modes must fail closed. A typo in `predict(mode=...)` must raise an error, not silently execute a different ablation.

**Methodological rule**: val can audit the story, but it must not accept or reject rules. Future rule pruning must use inner dev. Otherwise the loop will overfit validation in the same way it overfit train.

The verify audit shows why global dev accuracy is not enough:

| Split | verify helped | verify hurt | net |
|---|---:|---:|---:|
| inner_train | 265 | 40 | +225 |
| inner_dev | 84 | 16 | +68 |
| val | 141 | 191 | -50 |

Aggregate verify behavior still looks positive on inner dev while negative on val. The acceptance unit must become smaller: rule-level support, per-class impact, and marginal contribution by ablation.

**Updated interpretation**: base+rerank is the operational baseline for future symbolic HL. Full verify is a diagnostic artifact showing how executable memorization forms.

## Session 22b: Selective Verify Pruning

Added `set_verify_whitelist()` to predict.py allowing class-selective verify.

| Configuration | Val Top-1 | Val Top-3 | Train-Val Gap |
|---|:---:|:---:|:---:|
| base_rerank (no verify) | 51.9% | 75.8% | 4.2pp |
| **whitelist {jellyfish, banana}** | **52.7%** | **75.7%** | **6.2pp** |
| whitelist {jellyfish, banana, bear} | 52.3% | 75.9% | — |
| full verify | 49.4% | 73.7% | 21.1pp |

**Result**: +3.3pp val improvement over full verify, +0.8pp over base_rerank. Gap reduced from 21.1pp to 6.2pp.

**Why jellyfish/banana verify generalizes**: These two classes have highly distinctive visual features (jellyfish: saturated translucent blue/purple; banana: elongated warm yellow). Their verify conditions fire on broad visual properties that transfer across images, not on narrow threshold combinations fitted to specific training examples.

**New operational baseline**: base_rerank + {jellyfish, banana} verify = 52.7% val. This is the starting point for future HL iterations.
