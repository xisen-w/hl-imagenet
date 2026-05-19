# Claude Cron Job: Generalization-Aware Heuristic Learning

Use this as the next recurring Claude Code job. It is also installed locally in `.claude/scheduled_tasks.json`, which is ignored by git.

```json
{
  "name": "hl_generalization_research_loop",
  "enabled": false,
  "cron": "0 9 * * 1,3,5",
  "timezone": "Europe/London",
  "working_directory": "/Users/wangxiang/Desktop/my_workspace/hl-image-net",
  "command": "claude --dangerously-skip-permissions -p \"Read docs/phase2/README.md, docs/phase2/reflections/research_directions.md, docs/phase2/understanding/README.md, docs/phase2/understanding/generalization_gap.md, and docs/phase2/understanding/patch_safety.md. Work only on Phase 2 generalization-aware heuristic learning. Stop optimizing train accuracy. Use train for proposing rules, an inner dev split for accepting/rejecting them, and keep val/test untouched. Treat base+rerank around 51-52% val as the real symbolic baseline; treat the 100% train system as an overfitting artifact. Do not add fix-1 thresholds or per-image verify rules. Accept rules only with support around 10-20 examples, held-out dev precision, and no class collapse. Prefer representation improvements over threshold tuning: foreground masks, contour descriptors, local patch pooling, pattern-exists-somewhere detectors, and part relations. Maintain docs/phase2/understanding as the reflection memory: update the relevant understanding file with accepted and rejected findings, then update docs/phase2/reflections only if the research story changes. Run relevant eval/smoke checks and stop if a change only improves train while hurting dev/val.\"",
  "objective": "Advance heuristic-learning theory by replacing train-only rule grinding with held-out selection, patch regularization, and reusable visual primitives.",
  "guardrails": [
    "Do not use anycode forests to explain the Phase 2 symbolic result.",
    "Do not add fix-one-image thresholds.",
    "Do not touch final verify waves unless the task is auditing/removing overfit rules.",
    "Prefer measurement tooling over accuracy chasing.",
    "Record every accepted and rejected change in docs/phase2/understanding first, then update docs/phase2/reflections/research_directions.md when strategy changes."
  ]
}
```

## Operating Frame

The job should treat heuristic rules as model parameters. A code edit is an update step; a threshold is a fitted parameter; a verify rule can be a memorized training correction. The objective is not more training accuracy, but a disciplined update rule for symbolic systems.

Good tasks:

- Stop optimizing train accuracy; use train only to propose rules.
- Add an inner train/dev split so rule patches must survive held-out selection before full validation.
- Make base + rerank the real symbolic baseline around 51-52% val.
- Add rule-support instrumentation: how many images does each rule affect, by class and split?
- Isolate the base + rerank pipeline so generalizing components can be measured without final verify overfit.
- Prototype reusable visual primitives that explain multiple images, not one-off threshold fixes.
- Maintain `docs/phase2/understanding/` as the Phase 2 reflection memory before updating public-facing reflection files.

Stop conditions:

- The proposed patch only improves train accuracy.
- The patch fixes a single image or class pair with no reusable feature.
- The patch cannot be evaluated without leaking validation feedback back into the search loop.
