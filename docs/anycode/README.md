# Anycode Docs

The anycode track asks what happens when the agent is allowed to write any `predict(image) -> label` program instead of working inside the Phase 2 signature/reranking architecture.

## Files

- [anycode_finding.md](anycode_finding.md) — Narrative of the KNN memorizer, GNB attempt, and compiled random forest.
- [representation_gap.md](representation_gap.md) — Comparison between hand-crafted features, compiled forests, and learned CNN representations.

## Boundary

Anycode is a side experiment / phase-3 direction, not the explanation for Phase 2's 70% train result. It matters because it shows:

- unconstrained code optimization memorizes immediately;
- tree-compiled code generalizes better than hand-written verify rules;
- the feature set contains more signal than the sigmoid pipeline extracts;
- learned convolutions still capture local spatial structure that the hand-crafted feature set misses.
