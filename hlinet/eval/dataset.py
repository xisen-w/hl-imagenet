"""ImageNet subset loader for evaluation."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path

PHASE2_CLASSES = [
    "golden_retriever", "mushroom", "teapot", "school_bus", "banana",
    "orange", "brown_bear", "king_penguin", "jellyfish", "sports_car",
]

# Kept for archived Phase 1 analysis and plot generation.
PHASE1_CLASSES = [
    "zebra", "school_bus", "golden_retriever", "bicycle",
    "mushroom", "teapot", "piano", "eagle", "laptop", "banana",
]

DATA_DIR = Path(__file__).parent.parent.parent / "data"


@dataclass
class Sample:
    path: Path
    label: str


def load_dataset(
    data_dir: Path | None = None,
    classes: list[str] | None = None,
    split: str = "val",
    max_per_class: int | None = None,
) -> list[Sample]:
    """Load image samples from the dataset directory.

    Expected structure:
        data/phase2/<split>/<class_name>/<image_files>
    """
    data_dir = data_dir or DATA_DIR / "phase2" / split
    classes = classes or PHASE2_CLASSES

    samples = []
    for cls in classes:
        cls_dir = data_dir / cls
        if not cls_dir.exists():
            continue

        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg")) + sorted(cls_dir.glob("*.png"))
        if max_per_class:
            images = images[:max_per_class]

        for img_path in images:
            samples.append(Sample(path=img_path, label=cls))

    return samples


def load_splits(data_dir: Path | None = None) -> dict[str, list[Sample]]:
    """Load train/val/test splits from splits.json if available."""
    data_dir = data_dir or DATA_DIR
    splits_file = data_dir / "splits.json"

    if splits_file.exists():
        with open(splits_file) as f:
            split_data = json.load(f)
        return {
            split_name: [Sample(path=Path(s["path"]), label=s["label"]) for s in samples]
            for split_name, samples in split_data.items()
        }

    phase2_root = data_dir / "phase2"
    if phase2_root.exists():
        return {
            split_name: load_dataset(phase2_root / split_name, classes=PHASE2_CLASSES)
            for split_name in ("train", "val", "test")
        }

    # Legacy fallback for Phase 1-style flat data directories.
    all_samples = load_dataset(data_dir / "imagenet_10", classes=PHASE1_CLASSES)
    random.seed(42)
    random.shuffle(all_samples)

    n = len(all_samples)
    train_end = int(0.7 * n)
    val_end = int(0.85 * n)

    return {
        "train": all_samples[:train_end],
        "val": all_samples[train_end:val_end],
        "test": all_samples[val_end:],
    }
