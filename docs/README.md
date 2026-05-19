# HL-ImageNet Docs

The docs are organized by experiment lineage so the hand-built symbolic pipeline is not mixed with the later compiled-tree side experiment.

## Map

- [phase1/](phase1/) — Exploratory 4-real + 6-synthetic setup. Useful for the first proof that the heuristic-learning loop can grow a symbolic visual system, but not an honest 10-class benchmark.
- [phase2/](phase2/) — Main hand-built symbolic pipeline on 10 real Tiny ImageNet classes. This is the core heuristic-learning story: signatures, histogram blending, pairwise reranking, verify rules, cascade dynamics, overfitting, and the Phase 2 reflection/writing strategy.
- [anycode/](anycode/) — Side experiment that removes architecture constraints and compiles classifiers to code, including KNN memorization and the 64.4% validation random forest.
- [phase3/](phase3/) — Forward plan for higher-resolution local perception.

## Key Numbers

| Track | Train | Val | Status |
|---|---:|---:|---|
| Phase 1 dev system | 86.1% dev | 51-54% held-out subset | Historical proof-of-loop |
| Phase 2 hand-built pipeline, Session 20/21 | 70.0% | 49.4% | Main no-tree symbolic result |
| Phase 2 full verify-wave endpoint | 100.0% | 41.35% | Overfit train memorizer |
| Phase 2 base + pairwise rerank | ~52% train | 51.9% | Best generalizing hand pipeline |
| Anycode compiled forest | 90.2% | 64.4% | Side experiment / phase-3 direction |
| Small CNN baseline | 76.0% | 71.8% | Learned-representation reference |

## Current Research Frame

The central lesson is not that symbolic vision reaches high validation accuracy. It does not. The central lesson is that **train-only heuristic learning over code memorizes just like train-only parameter learning**.

In this project, the codebase is the model, patches are actions, and evaluation accuracy is reward. When the reward is train accuracy, the agent eventually writes a memorizer made of thresholds and special cases. The next research step is a heuristic-learning loop with a generalization reward, explicit regularization, and representation-level feature invention.
