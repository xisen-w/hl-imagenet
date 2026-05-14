#!/usr/bin/env python3
"""Train a dependency-light neural baseline on the Phase 2 image split."""

from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import cv2
import joblib
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data" / "phase2"
OUT_ROOT = Path(__file__).resolve().parent

CLASSES = [
    "golden_retriever",
    "mushroom",
    "teapot",
    "school_bus",
    "banana",
    "orange",
    "brown_bear",
    "king_penguin",
    "jellyfish",
    "sports_car",
]


@dataclass(frozen=True)
class Sample:
    path: Path
    label: str


def parse_hidden_layers(value: str) -> tuple[int, ...]:
    layers = tuple(int(part.strip()) for part in value.split(",") if part.strip())
    if not layers:
        raise argparse.ArgumentTypeError("hidden layer list cannot be empty")
    if any(layer <= 0 for layer in layers):
        raise argparse.ArgumentTypeError("hidden layer sizes must be positive")
    return layers


def load_samples(
    data_root: Path,
    split: str,
    max_per_class: int | None = None,
) -> list[Sample]:
    samples: list[Sample] = []
    for cls in CLASSES:
        cls_dir = data_root / split / cls
        if not cls_dir.exists():
            raise FileNotFoundError(f"missing class directory: {cls_dir}")
        images = (
            sorted(cls_dir.glob("*.JPEG"))
            + sorted(cls_dir.glob("*.jpg"))
            + sorted(cls_dir.glob("*.png"))
        )
        if max_per_class is not None:
            images = images[:max_per_class]
        samples.extend(Sample(path=path, label=cls) for path in images)
    return samples


def image_to_vector(path: Path, image_size: int) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"could not load image: {path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_AREA)
    return (image.astype(np.float32) / 255.0).reshape(-1)


def build_matrix(samples: list[Sample], image_size: int) -> tuple[np.ndarray, np.ndarray]:
    x = np.empty((len(samples), image_size * image_size * 3), dtype=np.float32)
    y = np.empty(len(samples), dtype=np.int64)
    class_to_idx = {name: idx for idx, name in enumerate(CLASSES)}
    for idx, sample in enumerate(samples):
        x[idx] = image_to_vector(sample.path, image_size)
        y[idx] = class_to_idx[sample.label]
    return x, y


def topk_accuracy(proba: np.ndarray, y_true: np.ndarray, k: int) -> float:
    topk = np.argsort(proba, axis=1)[:, -k:]
    return float(np.mean([target in row for target, row in zip(y_true, topk)]))


def evaluate(
    model: Pipeline,
    x: np.ndarray,
    y: np.ndarray,
    samples: list[Sample],
    split: str,
) -> dict:
    start = time.time()
    proba = model.predict_proba(x)
    pred = np.argmax(proba, axis=1)
    elapsed = time.time() - start

    per_class_correct: dict[str, int] = defaultdict(int)
    per_class_total: dict[str, int] = defaultdict(int)
    errors = []
    for idx, (target, guess) in enumerate(zip(y, pred)):
        cls = CLASSES[int(target)]
        pred_cls = CLASSES[int(guess)]
        per_class_total[cls] += 1
        if target == guess:
            per_class_correct[cls] += 1
        elif len(errors) < 30:
            errors.append({
                "path": str(samples[idx].path),
                "true": cls,
                "pred": pred_cls,
            })

    matrix = confusion_matrix(y, pred, labels=list(range(len(CLASSES))))
    confusions = []
    for true_idx, true_name in enumerate(CLASSES):
        for pred_idx, pred_name in enumerate(CLASSES):
            if true_idx != pred_idx and matrix[true_idx, pred_idx]:
                confusions.append({
                    "true": true_name,
                    "pred": pred_name,
                    "count": int(matrix[true_idx, pred_idx]),
                })
    confusions.sort(key=lambda item: item["count"], reverse=True)

    return {
        "split": split,
        "samples": int(len(y)),
        "top1_accuracy": float(np.mean(pred == y)),
        "top3_accuracy": topk_accuracy(proba, y, 3),
        "elapsed_s": round(elapsed, 3),
        "ms_per_image": round((elapsed / max(len(y), 1)) * 1000, 3),
        "per_class": {
            cls: {
                "accuracy": per_class_correct[cls] / max(per_class_total[cls], 1),
                "correct": per_class_correct[cls],
                "total": per_class_total[cls],
            }
            for cls in CLASSES
        },
        "top_confusions": confusions[:15],
        "sample_errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train an MLP pixel baseline.")
    parser.add_argument("--image-size", type=int, default=32)
    parser.add_argument("--hidden-layers", type=parse_hidden_layers, default=(512, 128))
    parser.add_argument("--max-iter", type=int, default=80)
    parser.add_argument("--alpha", type=float, default=1e-4)
    parser.add_argument("--learning-rate-init", type=float, default=1e-3)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--max-per-class", type=int, default=None)
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--save-model", action="store_true")
    args = parser.parse_args()

    train_samples = load_samples(args.data_root, "train", max_per_class=args.max_per_class)
    val_samples = load_samples(args.data_root, "val", max_per_class=args.max_per_class)
    test_samples = load_samples(args.data_root, "test", max_per_class=args.max_per_class)

    print(f"Loading images at {args.image_size}x{args.image_size}...")
    x_train, y_train = build_matrix(train_samples, args.image_size)
    x_val, y_val = build_matrix(val_samples, args.image_size)
    x_test, y_test = build_matrix(test_samples, args.image_size)

    model = Pipeline([
        ("scale", StandardScaler()),
        ("mlp", MLPClassifier(
            hidden_layer_sizes=args.hidden_layers,
            activation="relu",
            solver="adam",
            alpha=args.alpha,
            batch_size=64,
            learning_rate_init=args.learning_rate_init,
            max_iter=args.max_iter,
            early_stopping=True,
            n_iter_no_change=10,
            random_state=args.random_state,
            verbose=True,
        )),
    ])

    print(f"Training MLP on {len(train_samples)} images...")
    started = time.time()
    model.fit(x_train, y_train)
    train_elapsed = time.time() - started

    results = {
        "experiment": "deep_learning_mlp_pixels",
        "classes": CLASSES,
        "config": {
            "image_size": args.image_size,
            "hidden_layers": list(args.hidden_layers),
            "max_iter": args.max_iter,
            "alpha": args.alpha,
            "learning_rate_init": args.learning_rate_init,
            "random_state": args.random_state,
            "max_per_class": args.max_per_class,
            "data_root": str(args.data_root),
        },
        "training": {
            "elapsed_s": round(train_elapsed, 3),
            "mlp_iterations": int(model.named_steps["mlp"].n_iter_),
            "loss": float(model.named_steps["mlp"].loss_),
        },
        "splits": {
            "train": evaluate(model, x_train, y_train, train_samples, "train"),
            "val": evaluate(model, x_val, y_val, val_samples, "val"),
            "test": evaluate(model, x_test, y_test, test_samples, "test"),
        },
    }

    log_dir = OUT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_path = log_dir / f"mlp_baseline_{timestamp}.json"
    report_path.write_text(json.dumps(results, indent=2))

    if args.save_model:
        model_dir = OUT_ROOT / "models"
        model_dir.mkdir(parents=True, exist_ok=True)
        model_path = model_dir / f"mlp_baseline_{timestamp}.joblib"
        latest_path = model_dir / "mlp_baseline_latest.joblib"
        payload = {
            "model": model,
            "classes": CLASSES,
            "image_size": args.image_size,
            "config": results["config"],
        }
        joblib.dump(payload, model_path)
        joblib.dump(payload, latest_path)
        results["model_path"] = str(model_path)
        report_path.write_text(json.dumps(results, indent=2))

    print("\nResults")
    for split in ("train", "val", "test"):
        split_result = results["splits"][split]
        print(
            f"  {split:5s} top1={split_result['top1_accuracy']:.3f} "
            f"top3={split_result['top3_accuracy']:.3f} "
            f"ms/img={split_result['ms_per_image']:.2f}"
        )
    print(f"\nSaved report: {report_path}")


if __name__ == "__main__":
    main()
