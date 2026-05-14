#!/usr/bin/env python3
"""Predict one image with a saved MLP baseline model."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import joblib
import numpy as np


def image_to_vector(path: Path, image_size: int) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"could not load image: {path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_AREA)
    return (image.astype(np.float32) / 255.0).reshape(1, -1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict with a saved MLP baseline.")
    parser.add_argument("model", type=Path)
    parser.add_argument("image", type=Path)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    payload = joblib.load(args.model)
    model = payload["model"]
    classes = payload["classes"]
    image_size = int(payload["image_size"])

    x = image_to_vector(args.image, image_size)
    proba = model.predict_proba(x)[0]
    order = np.argsort(proba)[::-1][:args.top_k]

    for rank, idx in enumerate(order, start=1):
        print(f"{rank}. {classes[int(idx)]}: {proba[int(idx)]:.4f}")


if __name__ == "__main__":
    main()
