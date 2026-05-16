
---

## Session 15 (2026-05-16)

**Baseline**: 58.15% (1163/2000) train top-1

### Session 14 Summary
- 12+ experiments, ALL failed or net-zero
- Exhausted: contour features (d'=1.54 but cascade), new discriminant pairs (cascade through repulsion), signature guards (-9 to -11), calibration (-7 to -2), gate tuning (-2 to -14), multiplier tuning (-1 to -2), histogram weight changes (net zero), pair base changes (-2)
- Pattern: system is deeply in a local optimum. Every change is zero-sum.

### Session 15 Strategy: Think out of the box

Session 14 tried every INCREMENTAL change: tweak thresholds, add features to existing discriminants, add new discriminants, tune parameters. ALL failed because the cascade amplification eats any local gain.

**New hypothesis**: The problem isn't that individual changes are bad — it's that the pipeline is too tightly coupled. Changes at any one point ripple through 6 downstream stages. The solution may need to be a COORDINATED multi-point change.

Specifically:
1. The biggest confusion pairs (banana-orange 46, bear-mushroom 44, banana-teapot 42, sports-bus 42) resist individual pair improvements because the discriminants are saturated AND the verify conditions are overfit
2. Instead of targeting one pair, what if I improve the BASE SCORING for underperforming classes by finding features that aren't used by signatures at all?
3. Or: what about a "consensus" approach — if the discriminant, the histogram, AND the signature all agree, boost confidence?

**Plan for this session**: Try 2-3 creative approaches that haven't been tried before:
1. Check if there are features with high d' that aren't used in ANY part of the pipeline
2. Try a "soft verify" that nudges scores instead of hard-swapping (reduce cascade risk)
3. Look for compound conditions (A AND B AND C) that are highly specific

### Monitor Cycle 1 — Uncommitted changes detected

**Changes found** (not yet committed):
- Per-class histogram blend weights used instead of global 0.88/0.12
- Reranking margins widened (rank-2: 0.25→0.30, rank-3: 0.25→0.28, rank-4: 0.22→0.30, rank-5: 0.12→0.15)
- Multipliers lowered (rank-2: 1.5→1.3, rank-3: 2.0→1.9, rank-4: 3.0→2.8)
- banana-teapot pair base raised 0.10→0.30
- 3 new repulsion pairs, GR gate 0.35→0.37
- 3 new rank-5 whitelist pairs
- New contour features (n_contours_norm, contour_fill_ratio)

**Result**:
| Split | Previous | Current | Delta |
|-------|:---:|:---:|:---:|
| Train top-1 | 57.9% | 55.3% | −2.6pp |
| Val top-1 | 52.9% | 52.9% | 0.0pp |
| Train-Val gap | 5.0pp | 2.4pp | −2.6pp (improved!) |
| Train top-3 | 76.9% | 74.7% | −2.2pp |
| Val top-3 | 75.6% | 75.7% | +0.1pp |

**Analysis**: Val is completely unchanged. Train dropped because per-class hist weights starve teapot (0.05 vs old 0.12) — teapot collapsed 41→27.5% on train. School_bus and sports_car gained because their hist weights are high (0.16, 0.14). The wider reranking margins and lower multipliers let more swaps through on train, but these don't transfer to val.

**Key insight**: The train-val gap narrowed from 5.0pp to 2.4pp. The previous system was overfitting to train by ~2.6pp via aggressive reranking. These changes de-overfit without improving val — they're neutral, not helpful.

**Verdict**: These changes should NOT be committed. They don't improve val, and they destroy teapot on train. The per-class hist weights need teapot to be at least 0.10-0.12 to avoid starving it.

