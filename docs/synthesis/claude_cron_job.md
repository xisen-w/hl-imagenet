# Claude Cron Job: Generalization-Aware Heuristic Learning

Use this as the next recurring Claude Code job. It is also installed locally in `.claude/scheduled_tasks.json`, which is ignored by git.

```json
{
  "name": "hl_generalization_research_loop",
  "enabled": false,
  "cron": "0 9 * * 1,3,5",
  "timezone": "Europe/London",
  "working_directory": "/Users/wangxiang/Desktop/my_workspace/hl-image-net",
  "command": "claude --dangerously-skip-permissions -p \"Read docs/README.md, docs/synthesis/research_directions.md, docs/phase2/understanding/generalization_gap.md, and docs/phase2/understanding/patch_safety.md. Work only on generalization-aware heuristic learning. Do not optimize train accuracy directly. Pick one small task: inner train/dev split tooling, rule-support instrumentation, base+rerank evaluation isolation, or a region-level representation feature. Run the relevant eval/smoke checks, update docs/synthesis with findings, and stop if the change only improves train while hurting dev/val.\"",
  "objective": "Advance heuristic-learning theory by replacing train-only rule grinding with held-out selection, patch regularization, and reusable visual primitives.",
  "guardrails": [
    "Do not use anycode forests to explain the Phase 2 symbolic result.",
    "Do not add fix-one-image thresholds.",
    "Do not touch final verify waves unless the task is auditing/removing overfit rules.",
    "Prefer measurement tooling over accuracy chasing.",
    "Record every accepted and rejected change in docs/synthesis/research_directions.md or a dated synthesis note."
  ]
}
```

## Operating Frame

The job should treat heuristic rules as model parameters. A code edit is an update step; a threshold is a fitted parameter; a verify rule can be a memorized training correction. The objective is not more training accuracy, but a disciplined update rule for symbolic systems.

Good tasks:

- Add an inner train/dev split so rule patches must survive held-out selection before full validation.
- Add rule-support instrumentation: how many images does each rule affect, by class and split?
- Isolate the base + rerank pipeline so generalizing components can be measured without final verify overfit.
- Prototype reusable visual primitives that explain multiple images, not one-off threshold fixes.

Stop conditions:

- The proposed patch only improves train accuracy.
- The patch fixes a single image or class pair with no reusable feature.
- The patch cannot be evaluated without leaking validation feedback back into the search loop.
