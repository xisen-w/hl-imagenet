"""Phase 2 diagnostic lens for HL-ImageNet evaluation logs.

This module analyzes existing Phase 2 evaluation JSON reports.

It does not:
- run the classifier,
- change classifier behavior,
- modify Phase 2 signatures,
- modify scorer weights,
- claim accuracy improvement.

Diagnostic concepts:
- attractor score: how strongly a predicted class absorbs false positives.
- victim score: how often a true class is lost to other predicted classes.
- confusion gravity well: a high-count off-diagonal true->predicted collapse.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_LOG_DIR = REPO_ROOT / "logs" / "phase2"
DEFAULT_OUTPUT_DIR = PHASE2_LOG_DIR / "diagnostics"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _parse_confusion(confusion: dict[str, Any]) -> dict[tuple[str, str], int]:
    parsed: dict[tuple[str, str], int] = {}

    for raw_key, raw_count in confusion.items():
        key = str(raw_key)
        count = int(raw_count)

        if "->" in key:
            true_label, pred_label = key.split("->", 1)
        elif "→" in key:
            true_label, pred_label = key.split("→", 1)
        else:
            continue

        true_label = true_label.strip()
        pred_label = pred_label.strip()

        if true_label and pred_label:
            parsed[(true_label, pred_label)] = count

    return parsed


def find_latest_phase2_report(log_dir: Path = PHASE2_LOG_DIR) -> Path:
    candidates = sorted(
        log_dir.glob("eval_phase2*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not candidates:
        raise FileNotFoundError(f"No eval_phase2*.json files found in {log_dir}")

    return candidates[0]


def analyze_report(report_path: Path, top_n: int = 15) -> dict[str, Any]:
    report = _load_json(report_path)

    raw_confusion = report.get("confusion_matrix", {})
    if not isinstance(raw_confusion, dict):
        raw_confusion = {}

    confusion = _parse_confusion(raw_confusion)

    classes = sorted(
        set(report.get("per_class_accuracy", {}).keys())
        | {true_label for true_label, _ in confusion.keys()}
        | {pred_label for _, pred_label in confusion.keys()}
    )

    true_totals: dict[str, int] = defaultdict(int)
    pred_totals: dict[str, int] = defaultdict(int)
    correct: dict[str, int] = defaultdict(int)

    for (true_label, pred_label), count in confusion.items():
        true_totals[true_label] += count
        pred_totals[pred_label] += count

        if true_label == pred_label:
            correct[true_label] += count

    per_class: dict[str, Any] = {}

    for cls in classes:
        true_total = true_totals.get(cls, 0)
        pred_total = pred_totals.get(cls, 0)
        cls_correct = correct.get(cls, 0)

        false_negative = max(true_total - cls_correct, 0)
        false_positive = max(pred_total - cls_correct, 0)

        recall = cls_correct / true_total if true_total else 0.0
        precision = cls_correct / pred_total if pred_total else 0.0
        victim_score = false_negative / true_total if true_total else 0.0
        attractor_score = false_positive / pred_total if pred_total else 0.0

        per_class[cls] = {
            "true_total": true_total,
            "pred_total": pred_total,
            "correct": cls_correct,
            "false_negative": false_negative,
            "false_positive": false_positive,
            "recall": recall,
            "precision": precision,
            "victim_score": victim_score,
            "attractor_score": attractor_score,
        }

    off_diagonal = []
    for (true_label, pred_label), count in confusion.items():
        if true_label != pred_label:
            off_diagonal.append(
                {
                    "true": true_label,
                    "pred": pred_label,
                    "count": count,
                }
            )

    off_diagonal.sort(key=lambda item: item["count"], reverse=True)

    attractors = sorted(
        [
            {
                "class": cls,
                "pred_total": data["pred_total"],
                "false_positive": data["false_positive"],
                "attractor_score": data["attractor_score"],
                "precision": data["precision"],
            }
            for cls, data in per_class.items()
            if data["pred_total"] > 0
        ],
        key=lambda item: (item["false_positive"], item["attractor_score"]),
        reverse=True,
    )

    victims = sorted(
        [
            {
                "class": cls,
                "true_total": data["true_total"],
                "false_negative": data["false_negative"],
                "victim_score": data["victim_score"],
                "recall": data["recall"],
            }
            for cls, data in per_class.items()
            if data["true_total"] > 0
        ],
        key=lambda item: (item["victim_score"], item["false_negative"]),
        reverse=True,
    )

    top1 = float(report.get("top1_accuracy", 0.0))
    top3 = float(report.get("top3_accuracy", 0.0))
    top3_rescue_gap = max(top3 - top1, 0.0)

    raw_feature_reuse = report.get("feature_reuse", {})
    if not isinstance(raw_feature_reuse, dict):
        raw_feature_reuse = {}

    high_reuse_features = []

    for name, count in sorted(raw_feature_reuse.items(), key=lambda item: int(item[1]), reverse=True):
        count_i = int(count)
        if count_i >= max(3, int(0.8 * max(len(classes), 1))):
            high_reuse_features.append(
                {
                    "feature": name,
                    "class_count": count_i,
                }
            )

    weak_classes = [
        cls
        for cls, data in per_class.items()
        if data["true_total"] > 0 and data["recall"] < 0.15
    ]

    strong_attractors = [
        item["class"]
        for item in attractors
        if item["false_positive"] >= 25 and item["attractor_score"] >= 0.35
    ]

    warnings: list[str] = []

    if weak_classes:
        warnings.append("Low-recall victim classes detected: " + ", ".join(sorted(weak_classes)))

    if strong_attractors:
        warnings.append("False-positive attractor classes detected: " + ", ".join(strong_attractors[:8]))

    if top3_rescue_gap >= 0.25:
        warnings.append(
            "Large top-3 rescue gap detected; true class may often be near the decision surface but lose top-1."
        )

    if high_reuse_features:
        warnings.append(
            "High feature-reuse counts detected; current feature_reuse may reflect global cache activation rather than class-specific dependence."
        )

    recommendations = [
        "Do not change classifier behavior until attractor and victim classes are inspected.",
        "Inspect top confusion gravity wells before adding new signatures.",
        "Treat feature_reuse as a coarse warning until sample-level/class-node attribution exists.",
        "Preserve train/validation/test labels when summarizing results.",
    ]

    if strong_attractors:
        recommendations.append("Consider future attractor-balanced scoring only after reviewing false-positive attractors.")

    if weak_classes:
        recommendations.append("Prioritize victim-class analysis for: " + ", ".join(sorted(weak_classes[:8])))

    return {
        "schema": "hl_imagenet_phase2_diagnostic_lens_v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_report": str(report_path),
        "source_tag": report.get("tag"),
        "n_samples": report.get("n_samples"),
        "top1_accuracy": top1,
        "top3_accuracy": top3,
        "top3_rescue_gap": top3_rescue_gap,
        "mean_latency_ms": report.get("mean_latency_ms"),
        "classes": classes,
        "per_class": per_class,
        "top_confusion_gravity_wells": off_diagonal[:top_n],
        "top_attractors": attractors[:top_n],
        "top_victims": victims[:top_n],
        "high_reuse_features": high_reuse_features[:top_n],
        "warnings": warnings,
        "recommendations": recommendations,
        "non_claim_lock": [
            "This diagnostic does not prove classifier correctness.",
            "This diagnostic does not change classifier behavior.",
            "This diagnostic does not claim RCC improved classifier accuracy.",
            "This diagnostic should guide inspection before Phase 2.3 scoring or signature changes.",
        ],
    }


def write_markdown(analysis: dict[str, Any], path: Path) -> None:
    lines: list[str] = []

    lines.append("# HL-ImageNet Phase 2 Diagnostic Lens")
    lines.append("")
    lines.append(f"Generated: `{analysis['generated_at']}`")
    lines.append(f"Source report: `{analysis['source_report']}`")
    lines.append(f"Source tag: `{analysis.get('source_tag')}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Samples: `{analysis.get('n_samples')}`")
    lines.append(f"- Top-1 accuracy: `{analysis.get('top1_accuracy'):.3f}`")
    lines.append(f"- Top-3 accuracy: `{analysis.get('top3_accuracy'):.3f}`")
    lines.append(f"- Top-3 rescue gap: `{analysis.get('top3_rescue_gap'):.3f}`")
    lines.append(f"- Mean latency ms: `{analysis.get('mean_latency_ms')}`")
    lines.append("")
    lines.append("## Per-class diagnostic table")
    lines.append("")
    lines.append("| Class | Recall | Precision | Victim Score | Attractor Score | Correct | True Total | Pred Total |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")

    for cls, data in sorted(analysis["per_class"].items()):
        lines.append(
            f"| {cls} | {data['recall']:.3f} | {data['precision']:.3f} | "
            f"{data['victim_score']:.3f} | {data['attractor_score']:.3f} | "
            f"{data['correct']} | {data['true_total']} | {data['pred_total']} |"
        )

    lines.append("")
    lines.append("## Top confusion gravity wells")
    lines.append("")
    lines.append("| True | Predicted | Count |")
    lines.append("|---|---|---:|")

    for item in analysis["top_confusion_gravity_wells"]:
        lines.append(f"| {item['true']} | {item['pred']} | {item['count']} |")

    lines.append("")
    lines.append("## Top false-positive attractors")
    lines.append("")
    lines.append("| Class | Pred Total | False Positive | Attractor Score | Precision |")
    lines.append("|---|---:|---:|---:|---:|")

    for item in analysis["top_attractors"]:
        lines.append(
            f"| {item['class']} | {item['pred_total']} | {item['false_positive']} | "
            f"{item['attractor_score']:.3f} | {item['precision']:.3f} |"
        )

    lines.append("")
    lines.append("## Top victim classes")
    lines.append("")
    lines.append("| Class | True Total | False Negative | Victim Score | Recall |")
    lines.append("|---|---:|---:|---:|---:|")

    for item in analysis["top_victims"]:
        lines.append(
            f"| {item['class']} | {item['true_total']} | {item['false_negative']} | "
            f"{item['victim_score']:.3f} | {item['recall']:.3f} |"
        )

    lines.append("")
    lines.append("## High feature-reuse warnings")
    lines.append("")

    if analysis["high_reuse_features"]:
        lines.append("| Feature | Class Count |")
        lines.append("|---|---:|")
        for item in analysis["high_reuse_features"]:
            lines.append(f"| {item['feature']} | {item['class_count']} |")

    if not analysis["high_reuse_features"]:
        lines.append("No high feature-reuse warnings detected.")

    lines.append("")
    lines.append("## Warnings")
    lines.append("")

    if analysis["warnings"]:
        for warning in analysis["warnings"]:
            lines.append(f"- {warning}")

    if not analysis["warnings"]:
        lines.append("- No diagnostic warnings emitted.")

    lines.append("")
    lines.append("## Recommendations")
    lines.append("")

    for recommendation in analysis["recommendations"]:
        lines.append(f"- {recommendation}")

    lines.append("")
    lines.append("## Non-claim lock")
    lines.append("")

    for lock in analysis["non_claim_lock"]:
        lines.append(f"- {lock}")

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def run(input_path: Path | None, output_dir: Path, top_n: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = input_path or find_latest_phase2_report()
    analysis = analyze_report(report_path, top_n=top_n)

    json_path = output_dir / "latest_phase2_diagnostic.json"
    md_path = output_dir / "latest_phase2_diagnostic.md"

    json_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    write_markdown(analysis, md_path)

    return {
        "json": json_path,
        "markdown": md_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Phase 2 HL-ImageNet eval logs.")
    parser.add_argument("--input", type=Path, default=None, help="Path to eval_phase2*.json. Defaults to latest.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--top-n", type=int, default=15)
    args = parser.parse_args()

    outputs = run(args.input, args.output_dir, args.top_n)

    print("Phase 2 diagnostic lens complete.")
    print(f"JSON: {outputs['json']}")
    print(f"Markdown: {outputs['markdown']}")


if __name__ == "__main__":
    main()
