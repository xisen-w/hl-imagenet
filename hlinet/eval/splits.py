"""Inner train/dev split for generalization-aware heuristic learning.

Creates a deterministic 150/50 split per class from data/phase2/train/,
enabling measurement of whether heuristic rules generalize within training data.
"""

from __future__ import annotations

import random
import zlib
from pathlib import Path

from hlinet.eval.dataset import PHASE2_CLASSES, Sample

DATA_DIR = Path(__file__).parent.parent.parent / "data"
INNER_SEED = 2026
INNER_DEV_SIZE = 50  # per class


def load_inner_split(
    split: str = "inner_train",
    classes: list[str] | None = None,
    max_per_class: int | None = None,
) -> list[Sample]:
    """Load inner train or inner dev split from data/phase2/train/.

    split: "inner_train" (150/class) or "inner_dev" (50/class)
    """
    assert split in ("inner_train", "inner_dev"), f"Unknown split: {split}"
    classes = classes or PHASE2_CLASSES
    train_dir = DATA_DIR / "phase2" / "train"

    samples = []
    for cls in classes:
        cls_dir = train_dir / cls
        if not cls_dir.exists():
            continue

        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg")) + sorted(cls_dir.glob("*.png"))

        class_seed = zlib.crc32(cls.encode("utf-8")) % 10000
        rng = random.Random(INNER_SEED + class_seed)
        shuffled = list(images)
        rng.shuffle(shuffled)

        dev_images = set(str(p) for p in shuffled[:INNER_DEV_SIZE])

        if split == "inner_dev":
            selected = shuffled[:INNER_DEV_SIZE]
        else:
            selected = [p for p in shuffled if str(p) not in dev_images]

        if max_per_class:
            selected = selected[:max_per_class]

        for img_path in selected:
            samples.append(Sample(path=img_path, label=cls))

    return samples


def split_stats() -> dict[str, dict[str, int]]:
    """Report sizes of inner splits per class."""
    stats = {}
    for cls in PHASE2_CLASSES:
        train = load_inner_split("inner_train", classes=[cls])
        dev = load_inner_split("inner_dev", classes=[cls])
        stats[cls] = {"inner_train": len(train), "inner_dev": len(dev)}
    return stats
