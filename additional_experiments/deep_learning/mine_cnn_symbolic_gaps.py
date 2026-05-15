#!/usr/bin/env python3
"""Mine cases where the CNN succeeds and the symbolic classifier fails.

The goal is not just to count errors. For representative CNN-correct /
symbolic-wrong images, this script runs simple occlusion sensitivity: mask
small image patches and measure how much the CNN's true-class probability
drops. The top patches are candidate regions to translate into symbolic local
features.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
import torch
from torchvision import transforms

from train_cnn_baseline import CLASSES, DATA_ROOT, SmallCNN, choose_device


ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Sample:
    path: Path
    label: str


@dataclass
class Case:
    path: Path
    true_label: str
    symbolic_label: str
    symbolic_confidence: float
    cnn_label: str
    cnn_true_prob: float
    cnn_pred_prob: float
    cnn_margin: float


def load_samples(data_root: Path, split: str, max_per_class: int | None = None) -> list[Sample]:
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


def load_cnn(checkpoint_path: Path, device: torch.device) -> tuple[SmallCNN, int]:
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    if checkpoint["classes"] != CLASSES:
        raise ValueError("checkpoint class order does not match Phase 2 class order")
    image_size = int(checkpoint["image_size"])
    model = SmallCNN(num_classes=len(CLASSES)).to(device)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    return model, image_size


def eval_transform(image_size: int):
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ])


def cnn_predict(
    model: SmallCNN,
    image_path: Path,
    transform,
    device: torch.device,
    true_label: str,
) -> tuple[str, float, float, float]:
    image = Image.open(image_path).convert("RGB")
    x = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        probs = torch.softmax(model(x), dim=1)[0].cpu().numpy()
    pred_idx = int(np.argmax(probs))
    true_idx = CLASSES.index(true_label)
    sorted_probs = np.sort(probs)
    margin = float(sorted_probs[-1] - sorted_probs[-2]) if len(sorted_probs) > 1 else 0.0
    return CLASSES[pred_idx], float(probs[true_idx]), float(probs[pred_idx]), margin


def symbolic_predict(image_path: Path):
    from hlinet.classifier.predict import predict

    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"could not read image: {image_path}")
    pred = predict(image)
    return pred.label, float(pred.confidence)


def region_name(cx: float, cy: float, width: int, height: int) -> str:
    x_part = "left" if cx < width / 3 else "right" if cx >= 2 * width / 3 else "center"
    y_part = "top" if cy < height / 3 else "bottom" if cy >= 2 * height / 3 else "middle"
    if x_part == "center" and y_part == "middle":
        return "center"
    return f"{y_part}_{x_part}"


def crop_stats(image_bgr: np.ndarray, bbox: tuple[int, int, int, int]) -> dict:
    x, y, w, h = bbox
    crop = image_bgr[y:y + h, x:x + w]
    if crop.size == 0:
        return {}
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    hue = hsv[:, :, 0]
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]
    warm = (((hue >= 5) & (hue <= 45)) | (hue <= 5)) & (sat > 50) & (val > 50)
    yellow = (hue >= 15) & (hue <= 45) & (sat > 70) & (val > 70)
    blue = (hue >= 75) & (hue <= 145) & (sat > 45) & (val > 45)
    green = (hue >= 35) & (hue <= 85) & (sat > 30) & (val > 40)
    return {
        "mean_hue": round(float(hue.mean()), 2),
        "mean_sat": round(float(sat.mean()) / 255, 3),
        "mean_val": round(float(val.mean()) / 255, 3),
        "warm_frac": round(float(warm.mean()), 3),
        "yellow_frac": round(float(yellow.mean()), 3),
        "blue_frac": round(float(blue.mean()), 3),
        "green_frac": round(float(green.mean()), 3),
        "edge_density": round(float((edges > 0).mean()), 3),
        "texture_lap_var": round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 1),
    }


@torch.no_grad()
def occlusion_sensitivity(
    model: SmallCNN,
    image_path: Path,
    image_size: int,
    device: torch.device,
    true_label: str,
    patch: int,
    stride: int,
    top_k: int,
) -> dict:
    transform = eval_transform(image_size)
    original_pil = Image.open(image_path).convert("RGB")
    x = transform(original_pil).unsqueeze(0).to(device)
    true_idx = CLASSES.index(true_label)
    base_prob = float(torch.softmax(model(x), dim=1)[0, true_idx].item())

    _, orig_h = original_pil.size
    orig_w, orig_h = original_pil.size
    resized = transforms.Resize((image_size, image_size))(original_pil)
    base_tensor = transform(resized).to(device)

    rows = []
    masked_batch = []
    boxes = []
    for y in range(0, image_size - patch + 1, stride):
        for x0 in range(0, image_size - patch + 1, stride):
            masked = base_tensor.clone()
            masked[:, y:y + patch, x0:x0 + patch] = 0.0
            masked_batch.append(masked)
            boxes.append((x0, y, patch, patch))

    if not masked_batch:
        return {"base_true_prob": base_prob, "top_patches": []}

    batch = torch.stack(masked_batch).to(device)
    probs = torch.softmax(model(batch), dim=1)[:, true_idx].cpu().numpy()
    image_bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)

    for bbox_resized, prob in zip(boxes, probs):
        x0, y0, w, h = bbox_resized
        drop = base_prob - float(prob)
        scale_x = orig_w / image_size
        scale_y = orig_h / image_size
        bbox_orig = (
            int(round(x0 * scale_x)),
            int(round(y0 * scale_y)),
            int(round(w * scale_x)),
            int(round(h * scale_y)),
        )
        cx = bbox_orig[0] + bbox_orig[2] / 2
        cy = bbox_orig[1] + bbox_orig[3] / 2
        rows.append({
            "bbox": bbox_orig,
            "drop": round(drop, 5),
            "masked_true_prob": round(float(prob), 5),
            "region": region_name(cx, cy, orig_w, orig_h),
            "crop_stats": crop_stats(image_bgr, bbox_orig),
        })
    rows.sort(key=lambda row: row["drop"], reverse=True)
    return {
        "base_true_prob": round(base_prob, 5),
        "top_patches": rows[:top_k],
    }


def save_annotated_image(image_path: Path, patches: list[dict], out_path: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    colors = ["red", "orange", "yellow"]
    for idx, patch in enumerate(patches[:3]):
        x, y, w, h = patch["bbox"]
        color = colors[min(idx, len(colors) - 1)]
        draw.rectangle((x, y, x + w, y + h), outline=color, width=3)
        draw.text((x + 2, y + 2), f"{idx + 1}:{patch['drop']:.3f}", fill=color)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def summarize_group(examples: list[dict], total_count: int) -> dict:
    regions = Counter()
    stat_sums: dict[str, float] = defaultdict(float)
    stat_count = 0
    for case in examples:
        for patch in case.get("occlusion", {}).get("top_patches", [])[:3]:
            regions[patch["region"]] += 1
            for key, value in patch.get("crop_stats", {}).items():
                stat_sums[key] += float(value)
            stat_count += 1
    avg_stats = {
        key: round(value / max(stat_count, 1), 3)
        for key, value in sorted(stat_sums.items())
    }
    return {
        "count": total_count,
        "annotated_examples": len(examples),
        "mean_example_cnn_true_prob": round(float(np.mean([c["cnn_true_prob"] for c in examples])), 4),
        "mean_example_symbolic_confidence": round(float(np.mean([c["symbolic_confidence"] for c in examples])), 4),
        "top_occlusion_regions": regions.most_common(8),
        "mean_top_patch_stats": avg_stats,
    }


def feature_hint(true_label: str, symbolic_label: str, summary: dict) -> str:
    regions = ", ".join(region for region, _ in summary["top_occlusion_regions"][:3]) or "unknown regions"
    stats = summary["mean_top_patch_stats"]
    high_bits = []
    if stats.get("edge_density", 0) >= 0.2:
        high_bits.append("edge-dense")
    if stats.get("warm_frac", 0) >= 0.25:
        high_bits.append("warm-color")
    if stats.get("yellow_frac", 0) >= 0.15:
        high_bits.append("yellow")
    if stats.get("blue_frac", 0) >= 0.15:
        high_bits.append("blue/purple")
    if stats.get("green_frac", 0) >= 0.15:
        high_bits.append("green-context")
    if stats.get("texture_lap_var", 0) >= 5000:
        high_bits.append("high-texture")
    descriptor = ", ".join(high_bits) if high_bits else "local visual"
    return (
        f"For true {true_label} misread as {symbolic_label}, the CNN often relies on "
        f"{descriptor} evidence in {regions}. Candidate symbolic direction: add a local "
        f"patch/grid detector for this evidence and gate it against {symbolic_label}."
    )


def write_markdown(report: dict, md_path: Path) -> None:
    lines = [
        "# CNN vs Symbolic Gap Mining",
        "",
        f"Split: `{report['split']}`",
        f"Samples: {report['totals']['samples']}",
        "",
        "## Outcome Counts",
        "",
    ]
    for key, value in report["totals"].items():
        if key != "samples":
            lines.append(f"- {key}: {value}")

    lines.extend(["", "## Top CNN-Correct / Symbolic-Wrong Groups", ""])
    for group in report["groups"][:12]:
        summary = group["summary"]
        lines.append(
            f"### {group['true_label']} -> symbolic {group['symbolic_label']} "
            f"({summary['count']} cases)"
        )
        lines.append("")
        lines.append(f"- Annotated examples: {summary['annotated_examples']}")
        lines.append(f"- Example CNN true prob avg: {summary['mean_example_cnn_true_prob']}")
        lines.append(f"- Example symbolic confidence avg: {summary['mean_example_symbolic_confidence']}")
        lines.append(f"- Top occlusion regions: {summary['top_occlusion_regions']}")
        lines.append(f"- Mean top-patch stats: `{summary['mean_top_patch_stats']}`")
        lines.append(f"- Feature hint: {group['feature_hint']}")
        if group["examples"]:
            lines.append("- Example visuals:")
            for example in group["examples"]:
                visual = example.get("visual_path")
                if visual:
                    lines.append(f"  - `{visual}`")
        lines.append("")

    md_path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Mine symbolic features from CNN wins.")
    parser.add_argument("--checkpoint", type=Path, default=OUT_ROOT / "models" / "cnn_baseline_latest.pt")
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--split", default="val", choices=["train", "val", "test"])
    parser.add_argument("--device", default="auto")
    parser.add_argument("--max-per-class", type=int, default=None)
    parser.add_argument("--max-groups", type=int, default=12)
    parser.add_argument("--examples-per-group", type=int, default=3)
    parser.add_argument("--patch", type=int, default=16)
    parser.add_argument("--stride", type=int, default=8)
    parser.add_argument("--top-patches", type=int, default=5)
    args = parser.parse_args()

    device = choose_device(args.device)
    model, image_size = load_cnn(args.checkpoint, device)
    transform = eval_transform(image_size)
    samples = load_samples(args.data_root, args.split, args.max_per_class)

    groups: dict[tuple[str, str], list[Case]] = defaultdict(list)
    totals = {
        "samples": 0,
        "both_correct": 0,
        "cnn_correct_symbolic_wrong": 0,
        "symbolic_correct_cnn_wrong": 0,
        "both_wrong": 0,
    }

    started = time.time()
    for idx, sample in enumerate(samples, start=1):
        symbolic_label, symbolic_conf = symbolic_predict(sample.path)
        cnn_label, cnn_true_prob, cnn_pred_prob, cnn_margin = cnn_predict(
            model, sample.path, transform, device, sample.label
        )
        symbolic_correct = symbolic_label == sample.label
        cnn_correct = cnn_label == sample.label
        totals["samples"] += 1
        if symbolic_correct and cnn_correct:
            totals["both_correct"] += 1
        elif cnn_correct and not symbolic_correct:
            totals["cnn_correct_symbolic_wrong"] += 1
            groups[(sample.label, symbolic_label)].append(Case(
                path=sample.path,
                true_label=sample.label,
                symbolic_label=symbolic_label,
                symbolic_confidence=symbolic_conf,
                cnn_label=cnn_label,
                cnn_true_prob=cnn_true_prob,
                cnn_pred_prob=cnn_pred_prob,
                cnn_margin=cnn_margin,
            ))
        elif symbolic_correct and not cnn_correct:
            totals["symbolic_correct_cnn_wrong"] += 1
        else:
            totals["both_wrong"] += 1
        if idx % 100 == 0:
            print(f"[{idx}/{len(samples)}] cnn wins over symbolic: {totals['cnn_correct_symbolic_wrong']}")

    sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    run_dir = OUT_ROOT / "mining" / f"cnn_symbolic_{args.split}_{timestamp}"
    visuals_dir = run_dir / "visuals"
    run_dir.mkdir(parents=True, exist_ok=True)

    report_groups = []
    for (true_label, symbolic_label), cases in sorted_groups[:args.max_groups]:
        ranked_cases = sorted(cases, key=lambda case: case.cnn_true_prob, reverse=True)
        examples = []
        for example_idx, case in enumerate(ranked_cases[:args.examples_per_group], start=1):
            occ = occlusion_sensitivity(
                model,
                case.path,
                image_size,
                device,
                case.true_label,
                args.patch,
                args.stride,
                args.top_patches,
            )
            visual_name = f"{true_label}_as_{symbolic_label}_{example_idx}.jpg"
            visual_path = visuals_dir / visual_name
            save_annotated_image(case.path, occ["top_patches"], visual_path)
            examples.append({
                "path": str(case.path),
                "visual_path": str(visual_path.relative_to(ROOT)),
                "true_label": case.true_label,
                "symbolic_label": case.symbolic_label,
                "symbolic_confidence": case.symbolic_confidence,
                "cnn_true_prob": case.cnn_true_prob,
                "cnn_pred_prob": case.cnn_pred_prob,
                "cnn_margin": case.cnn_margin,
                "occlusion": occ,
            })
        summary = summarize_group(examples, total_count=len(cases))
        report_groups.append({
            "true_label": true_label,
            "symbolic_label": symbolic_label,
            "summary": summary,
            "feature_hint": feature_hint(true_label, symbolic_label, summary),
            "examples": examples,
        })

    report = {
        "experiment": "cnn_symbolic_gap_mining",
        "split": args.split,
        "checkpoint": str(args.checkpoint),
        "config": {
            "image_size": image_size,
            "patch": args.patch,
            "stride": args.stride,
            "top_patches": args.top_patches,
            "max_per_class": args.max_per_class,
            "device": str(device),
        },
        "elapsed_s": round(time.time() - started, 3),
        "totals": totals,
        "groups": report_groups,
    }

    json_path = run_dir / "report.json"
    md_path = run_dir / "report.md"
    json_path.write_text(json.dumps(report, indent=2))
    write_markdown(report, md_path)

    print("\nMining complete")
    print(f"  CNN correct / symbolic wrong: {totals['cnn_correct_symbolic_wrong']}")
    print(f"  Symbolic correct / CNN wrong: {totals['symbolic_correct_cnn_wrong']}")
    print(f"  Report: {md_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
