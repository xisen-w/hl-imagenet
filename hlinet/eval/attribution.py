"""Phase 2 sample-level attribution for HL-ImageNet.

This module reads a declared Phase 2 split, runs the current symbolic
classifier, and emits sample-level attribution artifacts.

It does not change classifier behavior.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2

from hlinet.classifier.predict import predict
from hlinet.eval.baselines import make_default_baselines
from hlinet.eval.dataset import PHASE2_CLASSES, Sample, load_dataset


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_ROOT = REPO_ROOT / "data" / "phase2"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "logs" / "phase2" / "attribution"


def _as_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _safe_label_list(prediction) -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = [(prediction.label, _as_float(prediction.confidence))]
    for label, score in prediction.alternatives:
        rows.append((label, _as_float(score)))

    seen: set[str] = set()
    unique: list[tuple[str, float]] = []
    for label, score in rows:
        if label not in seen:
            unique.append((label, score))
            seen.add(label)
    return unique


def _top_features(prediction, limit: int = 12) -> list[dict[str, Any]]:
    rows = []
    for name, val in prediction.feature_activations.items():
        conf = _as_float(getattr(val, "confidence", 0.0))
        present = bool(getattr(val, "present", False))
        evidence = list(getattr(val, "evidence", []) or [])
        if present and conf > 0.05:
            rows.append({
                "name": name,
                "confidence": conf,
                "evidence": evidence[:2],
            })
    rows.sort(key=lambda item: item["confidence"], reverse=True)
    return rows[:limit]


def _outcome(true_label: str, ranked: list[str]) -> str:
    if ranked and ranked[0] == true_label:
        return "correct"
    if true_label in ranked[:3]:
        return "top3_rescue"
    return "miss"


def _prediction_record(sample: Sample, split: str) -> dict[str, Any]:
    image = cv2.imread(str(sample.path))
    if image is None:
        return {
            "path": str(sample.path),
            "split": split,
            "true_label": sample.label,
            "error": "image_load_failed",
        }

    start = time.perf_counter()
    pred = predict(image)
    latency_ms = (time.perf_counter() - start) * 1000.0

    ranked_pairs = _safe_label_list(pred)
    ranked_labels = [label for label, _score in ranked_pairs]
    for cls in PHASE2_CLASSES:
        if cls not in ranked_labels:
            ranked_labels.append(cls)

    top1_score = ranked_pairs[0][1] if ranked_pairs else 0.0
    top2_score = ranked_pairs[1][1] if len(ranked_pairs) > 1 else 0.0
    margin = top1_score - top2_score
    outcome = _outcome(sample.label, ranked_labels)

    return {
        "path": str(sample.path),
        "file": Path(sample.path).name,
        "split": split,
        "true_label": sample.label,
        "predicted_label": pred.label,
        "top3": ranked_labels[:3],
        "top5": ranked_labels[:5],
        "top1_score": top1_score,
        "top2_score": top2_score,
        "margin": margin,
        "outcome": outcome,
        "collapse_path": f"{sample.label}->{pred.label}",
        "latency_ms": latency_ms,
        "route": list(pred.route),
        "activated_features": _top_features(pred),
        "proof": list(pred.proof),
    }


def _fit_baselines(data_root: Path, train_max_per_class: int | None):
    train_samples = load_dataset(
        data_dir=data_root / "train",
        classes=PHASE2_CLASSES,
        split="train",
        max_per_class=train_max_per_class,
    )
    baselines = make_default_baselines(PHASE2_CLASSES)
    for baseline in baselines:
        baseline.fit(train_samples)
    return baselines


def _add_baseline_agreement(records: list[dict[str, Any]], baselines) -> None:
    for record in records:
        path = record.get("path")
        true_label = record.get("true_label")
        if not path or record.get("error"):
            continue

        image = cv2.imread(path)
        if image is None:
            continue

        baseline_rows = {}
        for baseline in baselines:
            pred = baseline.predict(image, path)
            baseline_rows[baseline.name] = {
                "predicted_label": pred.label,
                "top3": pred.ranked_labels[:3],
                "correct": pred.label == true_label,
                "top3_contains_true": true_label in pred.ranked_labels[:3],
            }

        record["baseline_agreement"] = baseline_rows
        record["any_baseline_correct"] = any(row["correct"] for row in baseline_rows.values())
        record["hl_correct"] = record.get("predicted_label") == true_label
        record["baseline_right_hl_wrong"] = bool(record["any_baseline_correct"] and not record["hl_correct"])
        record["hl_right_all_baselines_wrong"] = bool(record["hl_correct"] and not record["any_baseline_correct"])


def _summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [r for r in records if not r.get("error")]
    n = len(valid)
    outcome_counts = Counter(r["outcome"] for r in valid)
    collapse_counts = Counter(r["collapse_path"] for r in valid if r["outcome"] != "correct")

    per_class = {}
    for cls in PHASE2_CLASSES:
        rows = [r for r in valid if r["true_label"] == cls]
        correct = sum(1 for r in rows if r["outcome"] == "correct")
        top3 = sum(1 for r in rows if r["true_label"] in r.get("top3", []))
        misses = [r for r in rows if r["outcome"] != "correct"]
        pred_counts = Counter(r["predicted_label"] for r in misses)
        per_class[cls] = {
            "n": len(rows),
            "correct": correct,
            "recall": correct / len(rows) if rows else 0.0,
            "top3_recall": top3 / len(rows) if rows else 0.0,
            "miss_count": len(misses),
            "top_wrong_predictions": pred_counts.most_common(5),
        }

    feature_counts = Counter()
    for r in valid:
        for feat in r.get("activated_features", []):
            feature_counts[feat["name"]] += 1

    baseline_right_hl_wrong = sum(1 for r in valid if r.get("baseline_right_hl_wrong"))
    hl_right_all_baselines_wrong = sum(1 for r in valid if r.get("hl_right_all_baselines_wrong"))
    margins = [r["margin"] for r in valid]

    return {
        "n_samples": n,
        "accuracy": outcome_counts["correct"] / n if n else 0.0,
        "top3_accuracy": (outcome_counts["correct"] + outcome_counts["top3_rescue"]) / n if n else 0.0,
        "outcome_counts": dict(outcome_counts),
        "mean_margin": statistics.mean(margins) if margins else 0.0,
        "median_margin": statistics.median(margins) if margins else 0.0,
        "top_collapse_paths": [
            {"collapse_path": path, "count": count}
            for path, count in collapse_counts.most_common(20)
        ],
        "per_class": per_class,
        "top_activated_features": [
            {"feature": name, "sample_count": count}
            for name, count in feature_counts.most_common(25)
        ],
        "baseline_right_hl_wrong": baseline_right_hl_wrong,
        "hl_right_all_baselines_wrong": hl_right_all_baselines_wrong,
    }


def _write_csv(records: list[dict[str, Any]], path: Path) -> None:
    fields = [
        "path",
        "split",
        "true_label",
        "predicted_label",
        "top3",
        "top1_score",
        "top2_score",
        "margin",
        "outcome",
        "collapse_path",
        "latency_ms",
        "any_baseline_correct",
        "baseline_right_hl_wrong",
        "hl_right_all_baselines_wrong",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in records:
            writer.writerow({
                key: json.dumps(r.get(key), ensure_ascii=False)
                if isinstance(r.get(key), (list, dict))
                else r.get(key, "")
                for key in fields
            })


def _write_markdown(artifact: dict[str, Any], path: Path) -> None:
    summary = artifact["summary"]
    lines = []
    lines.append("# HL-ImageNet Phase 2 Sample-Level Attribution")
    lines.append("")
    lines.append(f"Generated: `{artifact['generated_at']}`")
    lines.append(f"Split: `{artifact['split']}`")
    lines.append(f"Data root: `{artifact['data_root']}`")
    lines.append(f"Samples: `{summary['n_samples']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Accuracy: `{summary['accuracy']:.3f}`")
    lines.append(f"- Top-3 accuracy: `{summary['top3_accuracy']:.3f}`")
    lines.append(f"- Mean margin: `{summary['mean_margin']:.3f}`")
    lines.append(f"- Median margin: `{summary['median_margin']:.3f}`")
    lines.append(f"- Outcome counts: `{summary['outcome_counts']}`")
    lines.append(f"- Baseline-right / HL-wrong samples: `{summary['baseline_right_hl_wrong']}`")
    lines.append(f"- HL-right / all-baselines-wrong samples: `{summary['hl_right_all_baselines_wrong']}`")
    lines.append("")
    lines.append("## Top collapse paths")
    lines.append("")
    lines.append("| Collapse path | Count |")
    lines.append("|---|---:|")
    for row in summary["top_collapse_paths"][:15]:
        lines.append(f"| {row['collapse_path']} | {row['count']} |")
    lines.append("")
    lines.append("## Per-class attribution summary")
    lines.append("")
    lines.append("| Class | N | Recall | Top-3 recall | Misses | Top wrong predictions |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for cls, row in summary["per_class"].items():
        wrong = ", ".join(f"{label}:{count}" for label, count in row["top_wrong_predictions"])
        lines.append(
            f"| {cls} | {row['n']} | {row['recall']:.3f} | {row['top3_recall']:.3f} | "
            f"{row['miss_count']} | {wrong} |"
        )
    lines.append("")
    lines.append("## Top activated features")
    lines.append("")
    lines.append("| Feature | Sample count |")
    lines.append("|---|---:|")
    for row in summary["top_activated_features"][:20]:
        lines.append(f"| {row['feature']} | {row['sample_count']} |")
    lines.append("")
    lines.append("## Artifact files")
    lines.append("")
    lines.append("- `latest_phase2_attribution.json`")
    lines.append("- `latest_phase2_attribution.csv`")
    lines.append("- `latest_phase2_attribution.md`")
    lines.append("")
    lines.append("## Non-claim lock")
    lines.append("")
    lines.append("- This attribution layer does not change classifier behavior.")
    lines.append("- This attribution layer does not claim accuracy improvement.")
    lines.append("- Validation attribution is not a final test result.")
    lines.append("- Proof traces explain model behavior; they do not prove correctness.")
    lines.append("- Use this artifact to inspect failures before any Phase 2.5 scoring changes.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def run_attribution(
    split: str,
    data_root: Path,
    output_dir: Path,
    eval_max_per_class: int | None,
    train_max_per_class: int | None,
    include_baselines: bool,
) -> dict[str, Any]:
    samples = load_dataset(
        data_dir=data_root / split,
        classes=PHASE2_CLASSES,
        split=split,
        max_per_class=eval_max_per_class,
    )

    if not samples:
        raise FileNotFoundError(f"No samples found under {data_root / split}")

    records = [_prediction_record(sample, split) for sample in samples]

    if include_baselines:
        baselines = _fit_baselines(data_root, train_max_per_class)
        _add_baseline_agreement(records, baselines)

    summary = _summarize(records)

    artifact = {
        "schema": "hl_imagenet_phase2_sample_attribution_v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "split": split,
        "data_root": str(data_root),
        "include_baselines": include_baselines,
        "summary": summary,
        "records": records,
        "non_claim_lock": [
            "This attribution layer does not change classifier behavior.",
            "This attribution layer does not claim accuracy improvement.",
            "Validation attribution is not final test evidence.",
            "Proof traces explain model behavior; they do not prove correctness.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "latest_phase2_attribution.json"
    csv_path = output_dir / "latest_phase2_attribution.csv"
    md_path = output_dir / "latest_phase2_attribution.md"

    json_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    _write_csv(records, csv_path)
    _write_markdown(artifact, md_path)

    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase 2 sample-level attribution.")
    parser.add_argument("--split", default="val", choices=["train", "val", "test"])
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--eval-max-per-class", type=int, default=None)
    parser.add_argument("--train-max-per-class", type=int, default=None)
    parser.add_argument("--no-baselines", action="store_true")
    args = parser.parse_args()

    artifact = run_attribution(
        split=args.split,
        data_root=args.data_root,
        output_dir=args.output_dir,
        eval_max_per_class=args.eval_max_per_class,
        train_max_per_class=args.train_max_per_class,
        include_baselines=not args.no_baselines,
    )

    print("Phase 2 sample-level attribution complete.")
    print(f"Samples: {artifact['summary']['n_samples']}")
    print(f"Accuracy: {artifact['summary']['accuracy']:.3f}")
    print(f"Top-3 accuracy: {artifact['summary']['top3_accuracy']:.3f}")
    print(f"JSON: {args.output_dir / 'latest_phase2_attribution.json'}")
    print(f"CSV: {args.output_dir / 'latest_phase2_attribution.csv'}")
    print(f"Markdown: {args.output_dir / 'latest_phase2_attribution.md'}")


if __name__ == "__main__":
    main()