# Deep Learning Baseline

This folder contains a small neural baseline for the Phase 2 Tiny ImageNet
10-class split. It is intentionally separate from `hlinet/` so the symbolic
classifier stays unchanged.

PyTorch is not installed in the current environment, so the default baseline is
a scikit-learn MLP trained on resized RGB pixels. This is a real neural network
baseline, but it is not a modern CNN. Treat it as a dependency-light lower bound
for "learned neural model on pixels."

## Data

Expected layout:

```text
data/phase2/
  train/<class>/*.JPEG
  val/<class>/*.JPEG
  test/<class>/*.JPEG
```

The split currently has 2,000 train images, 2,000 val images, and 1,000 test
images.

## Train And Evaluate

Fast smoke run:

```bash
python3 additional_experiments/deep_learning/train_mlp_baseline.py --max-per-class 20 --max-iter 20
```

Full MLP baseline:

```bash
python3 additional_experiments/deep_learning/train_mlp_baseline.py --max-iter 80 --save-model
```

PyTorch CNN baseline, using the local experiment virtualenv:

```bash
python3 -m venv additional_experiments/deep_learning/.venv
additional_experiments/deep_learning/.venv/bin/python -m pip install torch torchvision
additional_experiments/deep_learning/.venv/bin/python \
  additional_experiments/deep_learning/train_cnn_baseline.py \
  --image-size 64 \
  --epochs 10 \
  --batch-size 64 \
  --device cpu \
  --save-model
```

Useful knobs:

```bash
python3 additional_experiments/deep_learning/train_mlp_baseline.py \
  --image-size 32 \
  --hidden-layers 512,128 \
  --max-iter 80 \
  --save-model
```

Reports are saved under `additional_experiments/deep_learning/logs/`.
Saved models go under `additional_experiments/deep_learning/models/`.

## Predict With A Saved Model

```bash
python3 additional_experiments/deep_learning/predict_mlp.py \
  additional_experiments/deep_learning/models/mlp_baseline_latest.joblib \
  path/to/image.JPEG
```

```bash
additional_experiments/deep_learning/.venv/bin/python \
  additional_experiments/deep_learning/predict_cnn.py \
  additional_experiments/deep_learning/models/cnn_baseline_latest.pt \
  path/to/image.JPEG
```

## Interpreting The Gap

The current symbolic Phase 2 result in the root README is:

- Train top-1: 48.75%
- Val top-1: 50.1%
- Val top-3: 74.2%

Compare the MLP's validation top-1/top-3 against those numbers. If this MLP is
below the symbolic system, the symbolic hand-built features are outperforming a
small learned pixel baseline. If it is above, the delta is the approximate gap
to a minimal neural model. A CNN or pretrained model would be a stronger deep
learning baseline, but requires adding PyTorch or another DL framework.

## Current Result

Run:

```bash
python3 additional_experiments/deep_learning/train_mlp_baseline.py \
  --image-size 32 \
  --hidden-layers 256 \
  --max-iter 60 \
  --save-model
```

Report:

```text
additional_experiments/deep_learning/logs/mlp_baseline_20260514_025752.json
```

| Model | Train Top-1 | Val Top-1 | Val Top-3 | Test Top-1 | Test Top-3 |
|---|---:|---:|---:|---:|---:|
| Symbolic Phase 2 | 48.75% | 50.1% | 74.2% | not yet reported here | not yet reported here |
| MLP pixels, 32x32, hidden=256 | 93.7% | 39.4% | 70.65% | 42.7% | 73.5% |
| Small CNN, 64x64, 10 CPU epochs | 76.0% | 71.8% | 92.0% | 71.2% | 91.6% |

Gap on validation top-1: symbolic is **+10.7 percentage points** over this MLP
baseline. The MLP memorizes the train split but generalizes worse, so this is a
useful lower-bound neural baseline rather than a strong CNN comparison.

Gap to the small CNN on validation top-1: CNN is **+21.7 percentage points**
over the symbolic Phase 2 system. This is the more meaningful deep-learning
baseline in this folder.

Top validation confusions for the MLP:

1. orange -> banana: 46
2. banana -> orange: 35
3. brown_bear -> king_penguin: 32
4. king_penguin -> jellyfish: 32
5. golden_retriever -> king_penguin: 30

CNN run:

```text
additional_experiments/deep_learning/logs/cnn_baseline_20260514_032227.json
additional_experiments/deep_learning/models/cnn_baseline_latest.pt
```

CNN top validation confusions are available in the JSON report.

## CNN-Guided Symbolic Feature Mining

Run:

```bash
additional_experiments/deep_learning/.venv/bin/python \
  additional_experiments/deep_learning/mine_cnn_symbolic_gaps.py \
  --split val \
  --max-groups 12 \
  --examples-per-group 3 \
  --device cpu
```

Latest report:

```text
additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_183343/report.md
additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_183343/report.json
```

Outcome counts on validation:

| Outcome | Count |
|---|---:|
| Both correct | 892 |
| CNN correct, symbolic wrong | 544 |
| Symbolic correct, CNN wrong | 109 |
| Both wrong | 455 |

Top cases where the CNN is correct and symbolic is wrong:

| True class | Symbolic prediction | Count | Candidate direction |
|---|---|---:|---|
| orange | banana | 26 | Local high-saturation warm/yellow patch structure, especially lower/central regions |
| sports_car | school_bus | 24 | Local edge-dense/high-texture vehicle structure outside pure yellow-bus cues |
| brown_bear | mushroom | 23 | Local warm, edge-dense, textured animal patches distinct from mushroom caps |
| golden_retriever | banana | 17 | Center warm fur texture/edge evidence to counter banana warm-yellow bias |
| brown_bear | golden_retriever | 17 | Darker local warm texture patches to separate bear fur from retriever fur |
| mushroom | brown_bear | 16 | Bottom/center high-texture cap/stem evidence with green-context handling |
| sports_car | king_penguin | 16 | Local structured vehicle edges/high texture to counter low-saturation penguin bias |
| banana | orange | 15 | Elongated/local yellow structure rather than global orange saturation |
| banana | school_bus | 15 | Local yellow fruit patches plus non-vehicle context/shape cues |
| brown_bear | king_penguin | 15 | Center texture evidence to counter dark/low-saturation penguin confusion |

The script writes annotated images under `visuals/`. Red/orange/yellow boxes mark
patches whose occlusion most reduced the CNN's true-class probability.
