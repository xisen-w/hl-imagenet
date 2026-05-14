#!/usr/bin/env python3
"""Train a small PyTorch CNN baseline on the Phase 2 image split."""

from __future__ import annotations

import argparse
import json
import random
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms


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
    target: int


class Phase2ImageDataset(Dataset):
    def __init__(
        self,
        data_root: Path,
        split: str,
        transform,
        max_per_class: int | None = None,
    ) -> None:
        self.transform = transform
        self.samples: list[Sample] = []
        for target, cls in enumerate(CLASSES):
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
            self.samples.extend(Sample(path=path, target=target) for path in images)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, int]:
        sample = self.samples[index]
        image = Image.open(sample.path).convert("RGB")
        return self.transform(image), sample.target


class SmallCNN(nn.Module):
    def __init__(self, num_classes: int = len(CLASSES), dropout: float = 0.25) -> None:
        super().__init__()
        self.features = nn.Sequential(
            self._block(3, 32),
            nn.MaxPool2d(2),
            self._block(32, 64),
            nn.MaxPool2d(2),
            self._block(64, 128),
            nn.MaxPool2d(2),
            self._block(128, 256),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(256, num_classes),
        )

    @staticmethod
    def _block(in_channels: int, out_channels: int) -> nn.Sequential:
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def choose_device(requested: str) -> torch.device:
    if requested != "auto":
        return torch.device(requested)
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def make_transforms(image_size: int) -> tuple[transforms.Compose, transforms.Compose]:
    normalize = transforms.Normalize(
        mean=(0.485, 0.456, 0.406),
        std=(0.229, 0.224, 0.225),
    )
    train_tf = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomApply([transforms.ColorJitter(0.15, 0.15, 0.15, 0.04)], p=0.5),
        transforms.ToTensor(),
        normalize,
    ])
    eval_tf = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        normalize,
    ])
    return train_tf, eval_tf


def topk_correct(logits: torch.Tensor, target: torch.Tensor, k: int) -> int:
    _, pred = logits.topk(k, dim=1)
    return pred.eq(target.view(-1, 1)).any(dim=1).sum().item()


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> dict:
    model.train()
    total_loss = 0.0
    correct = 0
    top3 = 0
    n = 0
    for images, targets in loader:
        images = images.to(device)
        targets = targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        logits = model(images)
        loss = criterion(logits, targets)
        loss.backward()
        optimizer.step()

        batch = targets.size(0)
        total_loss += loss.item() * batch
        correct += (logits.argmax(dim=1) == targets).sum().item()
        top3 += topk_correct(logits, targets, 3)
        n += batch
    return {
        "loss": total_loss / max(n, 1),
        "top1_accuracy": correct / max(n, 1),
        "top3_accuracy": top3 / max(n, 1),
    }


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, device: torch.device, split: str) -> dict:
    model.eval()
    criterion = nn.CrossEntropyLoss()
    total_loss = 0.0
    correct = 0
    top3 = 0
    n = 0
    per_class_correct: dict[str, int] = defaultdict(int)
    per_class_total: dict[str, int] = defaultdict(int)
    confusion: dict[tuple[str, str], int] = defaultdict(int)
    errors = []

    started = time.time()
    for images, targets in loader:
        images = images.to(device)
        targets = targets.to(device)
        logits = model(images)
        loss = criterion(logits, targets)
        preds = logits.argmax(dim=1)

        batch = targets.size(0)
        total_loss += loss.item() * batch
        correct += (preds == targets).sum().item()
        top3 += topk_correct(logits, targets, 3)
        n += batch

        for target, pred in zip(targets.cpu().tolist(), preds.cpu().tolist()):
            true_name = CLASSES[target]
            pred_name = CLASSES[pred]
            per_class_total[true_name] += 1
            if target == pred:
                per_class_correct[true_name] += 1
            else:
                confusion[(true_name, pred_name)] += 1
                if len(errors) < 30:
                    errors.append({"true": true_name, "pred": pred_name})

    elapsed = time.time() - started
    confusions = [
        {"true": true, "pred": pred, "count": count}
        for (true, pred), count in confusion.items()
    ]
    confusions.sort(key=lambda item: item["count"], reverse=True)

    return {
        "split": split,
        "samples": n,
        "loss": total_loss / max(n, 1),
        "top1_accuracy": correct / max(n, 1),
        "top3_accuracy": top3 / max(n, 1),
        "elapsed_s": round(elapsed, 3),
        "ms_per_image": round((elapsed / max(n, 1)) * 1000, 3),
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
    parser = argparse.ArgumentParser(description="Train a small CNN baseline.")
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--image-size", type=int, default=64)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--dropout", type=float, default=0.25)
    parser.add_argument("--max-per-class", type=int, default=None)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--save-model", action="store_true")
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    device = choose_device(args.device)
    train_tf, eval_tf = make_transforms(args.image_size)
    train_ds = Phase2ImageDataset(args.data_root, "train", train_tf, args.max_per_class)
    val_ds = Phase2ImageDataset(args.data_root, "val", eval_tf, args.max_per_class)
    test_ds = Phase2ImageDataset(args.data_root, "test", eval_tf, args.max_per_class)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=0)

    model = SmallCNN(dropout=args.dropout).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(args.epochs, 1))

    print(f"Device: {device}")
    print(f"Train/val/test: {len(train_ds)}/{len(val_ds)}/{len(test_ds)}")
    print(f"Image size: {args.image_size}, epochs: {args.epochs}, batch: {args.batch_size}")

    history = []
    best_val = -1.0
    best_state = None
    started = time.time()
    for epoch in range(1, args.epochs + 1):
        train_metrics = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_metrics = evaluate(model, val_loader, device, "val")
        scheduler.step()
        row = {
            "epoch": epoch,
            "train": train_metrics,
            "val": {
                "loss": val_metrics["loss"],
                "top1_accuracy": val_metrics["top1_accuracy"],
                "top3_accuracy": val_metrics["top3_accuracy"],
            },
            "lr": scheduler.get_last_lr()[0],
        }
        history.append(row)
        print(
            f"epoch {epoch:02d} "
            f"train_top1={train_metrics['top1_accuracy']:.3f} "
            f"val_top1={val_metrics['top1_accuracy']:.3f} "
            f"val_top3={val_metrics['top3_accuracy']:.3f}"
        )
        if val_metrics["top1_accuracy"] > best_val:
            best_val = val_metrics["top1_accuracy"]
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}

    if best_state is not None:
        model.load_state_dict(best_state)

    train_result = evaluate(model, train_loader, device, "train")
    val_result = evaluate(model, val_loader, device, "val")
    test_result = evaluate(model, test_loader, device, "test")
    elapsed = time.time() - started

    results = {
        "experiment": "deep_learning_small_cnn",
        "classes": CLASSES,
        "config": {
            "data_root": str(args.data_root),
            "image_size": args.image_size,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "lr": args.lr,
            "weight_decay": args.weight_decay,
            "dropout": args.dropout,
            "max_per_class": args.max_per_class,
            "device": str(device),
            "seed": args.seed,
        },
        "training": {
            "elapsed_s": round(elapsed, 3),
            "best_val_top1": best_val,
            "history": history,
        },
        "splits": {
            "train": train_result,
            "val": val_result,
            "test": test_result,
        },
    }

    log_dir = OUT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_path = log_dir / f"cnn_baseline_{timestamp}.json"

    if args.save_model:
        model_dir = OUT_ROOT / "models"
        model_dir.mkdir(parents=True, exist_ok=True)
        checkpoint = {
            "model_state": model.state_dict(),
            "classes": CLASSES,
            "image_size": args.image_size,
            "config": results["config"],
        }
        model_path = model_dir / f"cnn_baseline_{timestamp}.pt"
        latest_path = model_dir / "cnn_baseline_latest.pt"
        torch.save(checkpoint, model_path)
        torch.save(checkpoint, latest_path)
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
