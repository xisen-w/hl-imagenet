# Session Monitor: 2026-05-19 Generalization Loop

## What Ran

Claude Code started a Phase 2 generalization run focused on measurement infrastructure, not train accuracy. The active `python -m hlinet.eval.verify_audit` process completed during monitoring and wrote `logs/generalization/verify_audit_2026-05-19_05-30-21.json`.

Files introduced or modified by the run:

- `hlinet/classifier/predict.py` — added pipeline modes: `full`, `base`, `base_rerank`.
- `hlinet/eval/splits.py` — added inner train/dev split from `data/phase2/train`.
- `hlinet/eval/generalization.py` — added stage-by-stage evaluation across inner train, inner dev, and val.
- `hlinet/eval/verify_audit.py` — compares base+rerank against full verify behavior.
- `logs/generalization/` — stores generalization audit reports.

## What Looks Good

This run is aligned with the new Phase 2 direction because it builds measurement tools rather than adding more train-fixing thresholds.

The first generalization audit supports the central hypothesis:

| Mode | inner_train | inner_dev | val | Reading |
|---|---:|---:|---:|---|
| base | 44.2% | 47.4% | 45.7% | Base scoring is broadly honest. |
| base_rerank | 55.1% | 56.2% | 51.9% | Reranking transfers partially and is the real symbolic baseline. |
| full | 69.4% | 71.8% | 49.4% | Verify improves inner splits much more than val. |

This is exactly the distinction the project needs: not "does code improve train?", but "which code edits transfer?"

The completed verify audit adds a stricter warning:

| Split | verify helped | verify hurt | net |
|---|---:|---:|---:|
| inner_train | 265 | 40 | +225 |
| inner_dev | 84 | 16 | +68 |
| val | 141 | 191 | -50 |

Aggregate inner-dev benefit does not guarantee validation transfer for the verify layer. The next audit needs per-rule and per-class support, not only global top-1.

## Rigor Corrections Made During Monitoring

Two measurement bugs were found and fixed:

1. The inner split used Python `hash(cls)` for class seeds. Python hash randomization made the split change across processes. This was replaced with a stable `zlib.crc32` class seed.
2. `predict(mode=...)` accepted invalid modes silently. A typo behaved like `base_rerank`. Invalid modes now raise `ValueError`.
3. The generalization markdown report mislabeled per-class columns because the header order did not match the mode iteration order. The report writer now uses a fixed display order: `base`, `base_rerank`, `full`.
4. An unused global verify whitelist hook was removed from `predict.py`. It created a tempting class-level pruning path without a disciplined inner-dev acceptance rule.

These are infrastructure fixes only. They do not change the learned classifier rules.

## Main Methodological Warning

Val can be used for reporting and final audit, but not for accepting or pruning rules. A line in the session notes suggested targeting rules that hurt val. That would recreate the same overfitting loop on the validation set.

The correct loop is:

1. propose candidates on inner train;
2. accept or reject on inner dev;
3. keep val/test untouched for periodic reporting only;
4. update `docs/phase2/understanding/` with both accepted and rejected findings.

## Innovative Direction

The promising paradigm is credit assignment over program edits:

- Base scoring is the low-variance representation layer.
- Pairwise rerank is a moderately transferring symbolic correction layer.
- Verify rules are high-variance patch memory unless they show broad support.

This suggests a "backpropagation for heuristic learning" should not mean gradients through pixels. It should mean structured credit assignment over code patches:

`patch utility = dev gain - complexity penalty - low-support penalty - cascade risk`

The next useful work is not more thresholds. It is tooling that measures support, transfer, and marginal contribution for each rule or feature family, then rewards reusable visual primitives: foreground masks, contour descriptors, pooled local patches, pattern-exists-somewhere detectors, and part relations.

## Decision

Do not accept any classifier behavior change from this run. The measurement infrastructure is promising after the split-seed and report-label fixes, but the next run should rerun verify audit with the stable split before making any rule-level decision.
