#!/usr/bin/env python3
"""Predict one image with a saved CNN baseline checkpoint."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image
import torch
from torchvision import transforms

from train_cnn_baseline import SmallCNN, choose_device


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict with a saved CNN baseline.")
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("image", type=Path)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    device = choose_device(args.device)
    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    classes = checkpoint["classes"]
    image_size = int(checkpoint["image_size"])

    model = SmallCNN(num_classes=len(classes)).to(device)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ])

    image = Image.open(args.image).convert("RGB")
    x = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        probs = torch.softmax(model(x), dim=1)[0].cpu()
    values, indices = probs.topk(min(args.top_k, len(classes)))

    for rank, (idx, value) in enumerate(zip(indices.tolist(), values.tolist()), start=1):
        print(f"{rank}. {classes[idx]}: {value:.4f}")


if __name__ == "__main__":
    main()
