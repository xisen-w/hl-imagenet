"""Phase 2 regression guard for HL-ImageNet.

Reads Phase 2 benchmark, attribution, and candidate-selection artifacts and
emits a regression baseline/guard contract for future controlled classifier
changes.

This module does not change classifier behavior.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_BENCHMARK = REPO_ROOT / "logs" / "phase2" / "benchmarks" / "latest_phase2_benchmark.json"
DEFAULT_ATTRIBUTION = REPO_ROOT / "logs" / "phase2" / "attribution" / "latest_phase2_attribution.json"
DEFAULT_CANDIDATES = REPO_ROOT / "logs" / "phase2" / "candidates" / "latest_phase2_candidate_plan.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "logs" / "phase2" / "regression_guard"


MAJOR_ATTRACTORS = ["banana", "king_penguin", "golden_retriever"]
VICTIM_CLASSES = ["teapot", "brown_bear", "sports_car", "orange", "mushroom"]


def _load_json(path: Path, required: bool = True) -> dict[str, Any]:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Required file not found: {path}")
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_hl_benchmark(benchmark: dict[str, Any]) -> dict[str, Any]:
    models = benchmark.get("models") or {}
    hl = models.get("hl_symbolic_classifier") or {}

    leaderboard = benchmark.get("leaderboard") or []
    rank = None
    for idx, row in enumerate(leaderboard, start=1):
        if row.get("name") == "hl_symbolic_classifier":
            rank = idx
            break

    return {
        "top1": float(hl.get("top1_accuracy") or hl.get("top1") or 0.0),
        "top3": float(hl.get("top3_accuracy") or hl.get("top3") or 0.0),
        "mean_latency_ms": float(hl.get("mean_latency_ms") or 0.0),
        "leaderboard_rank": rank,
        "leaderboard_size": len(leaderboard),
    }


def _extract_attribution_baseline(attribution: dict[str, Any]) -> dict[str, Any]:
    summary = attribution.get("summary") or {}
    records = attribution.get("records") or []

    attractor_counts = Counter()
    for row in records:
        if row.get("outcome") == "correct":
            continue
        true_label = row.get("true_label")
        pred_label = row.get("predicted_label")
        if pred_label and pred_label != true_label:
            attractor_counts[pred_label] += 1

    per_class = summary.get("per_class") or {}

    victims = {}
    for cls in VICTIM_CLASSES:
        payload = per_class.get(cls) or {}
        victims[cls] = {
            "recall": float(payload.get("recall") or 0.0),
            "top3_recall": float(payload.get("top3_recall") or 0.0),
            "miss_count": int(payload.get("miss_count") or 0),
            "top_wrong_predictions": payload.get("top_wrong_predictions") or [],
        }

    major_attractors = {
        label: int(attractor_counts.get(label, 0))
        for label in MAJOR_ATTRACTORS
    }

    return {
        "samples": int(summary.get("n_samples") or 0),
        "accuracy": float(summary.get("accuracy") or 0.0),
        "top3_accuracy": float(summary.get("top3_accuracy") or 0.0),
        "outcome_counts": summary.get("outcome_counts") or {},
        "baseline_right_hl_wrong": int(summary.get("baseline_right_hl_wrong") or 0),
        "hl_right_all_baselines_wrong": int(summary.get("hl_right_all_baselines_wrong") or 0),
        "major_attractor_false_positives": major_attractors,
        "victim_classes": victims,
    }


def _extract_candidate_context(candidates: dict[str, Any]) -> dict[str, Any]:
    candidate_sets = candidates.get("candidate_sets") or {}
    feature_warnings = candidate_sets.get("feature_overactivation_warnings") or []
    attractor_targets = candidate_sets.get("attractor_suppression_targets") or []
    victim_targets = candidate_sets.get("victim_rescue_targets") or []

    return {
        "feature_overactivation_warning_count": len(feature_warnings),
        "top_feature_overactivation_warnings": feature_warnings[:10],
        "top_attractor_targets": attractor_targets[:5],
        "top_victim_targets": victim_targets[:5],
        "phase2_6_recommendation": candidates.get("phase2_6_recommendation") or {},
    }


def _make_guard_contract(hl: dict[str, Any], attr: dict[str, Any]) -> dict[str, Any]:
    top1 = attr.get("accuracy") or hl.get("top1") or 0.0
    top3 = attr.get("top3_accuracy") or hl.get("top3") or 0.0
    unique = attr.get("hl_right_all_baselines_wrong") or 0

    return {
        "mode": "baseline_lock_before_classifier_delta",
        "minimum_top1_accuracy": round(max(0.0, top1 - 0.005), 6),
        "minimum_top3_accuracy": round(max(0.0, top3 - 0.005), 6),
        "minimum_hl_unique_wins": max(0, int(unique * 0.90)),
        "maximum_allowed_major_attractor_increase": 0,
        "required_major_attractor_decrease_for_success": 1,
        "required_victim_class_improvement_for_success": 1,
        "required_reruns_after_classifier_change": [
            "python scripts/run_phase2_diagnostics.py --input <new_phase2_eval_json>",
            "python scripts/run_phase2_benchmarks.py --data-root \".\\data\\phase2\" --split val",
            "python scripts/run_phase2_attribution.py --data-root \".\\data\\phase2\" --split val",
            "python scripts/run_phase2_candidates.py",
            "python scripts/run_phase2_regression_guard.py",
        ],
    }


def _current_status(hl: dict[str, Any], attr: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    checks = []

    top1 = attr.get("accuracy") or hl.get("top1") or 0.0
    top3 = attr.get("top3_accuracy") or hl.get("top3") or 0.0
    unique = attr.get("hl_right_all_baselines_wrong") or 0

    checks.append({
        "name": "top1_accuracy_baseline",
        "value": top1,
        "threshold": contract["minimum_top1_accuracy"],
        "status": "pass" if top1 >= contract["minimum_top1_accuracy"] else "fail",
    })

    checks.append({
        "name": "top3_accuracy_baseline",
        "value": top3,
        "threshold": contract["minimum_top3_accuracy"],
        "status": "pass" if top3 >= contract["minimum_top3_accuracy"] else "fail",
    })

    checks.append({
        "name": "hl_unique_wins_baseline",
        "value": unique,
        "threshold": contract["minimum_hl_unique_wins"],
        "status": "pass" if unique >= contract["minimum_hl_unique_wins"] else "fail",
    })

    fail_count = sum(1 for c in checks if c["status"] == "fail")
    warning_count = sum(1 for c in checks if c["status"] == "warning")

    overall = "pass"
    if fail_count:
        overall = "fail"
    elif warning_count:
        overall = "warning"

    return {
        "overall_status": overall,
        "checks": checks,
        "note": "This baseline should pass because it is the locked pre-change state.",
    }


def build_regression_guard(
    benchmark_path: Path,
    attribution_path: Path,
    candidates_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    benchmark = _load_json(benchmark_path, required=True)
    attribution = _load_json(attribution_path, required=True)
    candidates = _load_json(candidates_path, required=True)

    hl = _extract_hl_benchmark(benchmark)
    attr = _extract_attribution_baseline(attribution)
    candidate_context = _extract_candidate_context(candidates)
    contract = _make_guard_contract(hl, attr)
    status = _current_status(hl, attr, contract)

    artifact = {
        "schema": "hl_imagenet_phase2_regression_guard_v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_files": {
            "benchmark": str(benchmark_path),
            "attribution": str(attribution_path),
            "candidates": str(candidates_path),
        },
        "baseline": {
            "benchmark": hl,
            "attribution": attr,
            "candidate_context": candidate_context,
        },
        "guard_contract": contract,
        "current_status": status,
        "phase2_6b_gate": {
            "allowed_next_step": "one controlled classifier delta only",
            "preferred_target": "tighten globally overactive Phase 2 signatures or add regression guards before attractor suppression",
            "forbidden_moves": [
                "broad scorer rewrite",
                "multiple simultaneous classifier changes",
                "validation-only tuning without reruns",
                "claiming improvement without benchmark/attribution comparison",
            ],
        },
        "non_claim_lock": [
            "This regression guard does not change classifier behavior.",
            "This regression guard does not claim accuracy improvement.",
            "This regression guard does not prove classifier correctness.",
            "Validation regression checks are not final test evidence.",
            "Any future classifier change must rerun diagnostics, benchmarks, attribution, candidates, and regression guard.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "latest_phase2_regression_guard.json"
    md_path = output_dir / "latest_phase2_regression_guard.md"

    json_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    _write_markdown(artifact, md_path)

    return artifact


def _write_markdown(artifact: dict[str, Any], path: Path) -> None:
    baseline = artifact["baseline"]
    attr = baseline["attribution"]
    bench = baseline["benchmark"]
    contract = artifact["guard_contract"]
    status = artifact["current_status"]

    lines = []
    lines.append("# HL-ImageNet Phase 2 Regression Guard")
    lines.append("")
    lines.append(f"Generated: `{artifact['generated_at']}`")
    lines.append("")
    lines.append("## Baseline lock")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| HL top-1 accuracy | {float(attr.get('accuracy') or 0.0):.3f} |")
    lines.append(f"| HL top-3 accuracy | {float(attr.get('top3_accuracy') or 0.0):.3f} |")
    lines.append(f"| Benchmark top-1 | {float(bench.get('top1') or 0.0):.3f} |")
    lines.append(f"| Benchmark top-3 | {float(bench.get('top3') or 0.0):.3f} |")
    lines.append(f"| Correct | {attr.get('outcome_counts', {}).get('correct')} |")
    lines.append(f"| Top-3 rescue | {attr.get('outcome_counts', {}).get('top3_rescue')} |")
    lines.append(f"| Miss | {attr.get('outcome_counts', {}).get('miss')} |")
    lines.append(f"| Baseline-right / HL-wrong | {attr.get('baseline_right_hl_wrong')} |")
    lines.append(f"| HL-right / all-baselines-wrong | {attr.get('hl_right_all_baselines_wrong')} |")
    lines.append("")
    lines.append("## Major attractor false positives")
    lines.append("")
    lines.append("| Attractor | False positives |")
    lines.append("|---|---:|")
    for label, count in attr.get("major_attractor_false_positives", {}).items():
        lines.append(f"| {label} | {count} |")
    lines.append("")
    lines.append("## Victim class baseline")
    lines.append("")
    lines.append("| Class | Recall | Top-3 recall | Misses |")
    lines.append("|---|---:|---:|---:|")
    for label, row in attr.get("victim_classes", {}).items():
        lines.append(
            f"| {label} | {float(row.get('recall') or 0.0):.3f} | "
            f"{float(row.get('top3_recall') or 0.0):.3f} | {row.get('miss_count')} |"
        )
    lines.append("")
    lines.append("## Guard contract")
    lines.append("")
    lines.append("| Guard | Threshold |")
    lines.append("|---|---:|")
    lines.append(f"| Minimum top-1 accuracy | {contract['minimum_top1_accuracy']:.3f} |")
    lines.append(f"| Minimum top-3 accuracy | {contract['minimum_top3_accuracy']:.3f} |")
    lines.append(f"| Minimum HL-unique wins | {contract['minimum_hl_unique_wins']} |")
    lines.append(f"| Maximum major-attractor increase | {contract['maximum_allowed_major_attractor_increase']} |")
    lines.append(f"| Required major-attractor decrease | {contract['required_major_attractor_decrease_for_success']} |")
    lines.append(f"| Required victim-class improvement | {contract['required_victim_class_improvement_for_success']} |")
    lines.append("")
    lines.append("## Current guard status")
    lines.append("")
    lines.append(f"Overall status: `{status['overall_status']}`")
    lines.append("")
    lines.append("| Check | Value | Threshold | Status |")
    lines.append("|---|---:|---:|---|")
    for check in status["checks"]:
        lines.append(
            f"| {check['name']} | {float(check['value']):.3f} | "
            f"{float(check['threshold']):.3f} | {check['status']} |"
        )
    lines.append("")
    lines.append("## Phase 2.6B gate")
    lines.append("")
    gate = artifact["phase2_6b_gate"]
    lines.append(f"- Allowed next step: {gate['allowed_next_step']}")
    lines.append(f"- Preferred target: {gate['preferred_target']}")
    lines.append("")
    lines.append("Forbidden moves:")
    lines.append("")
    for item in gate["forbidden_moves"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Required reruns after any classifier change:")
    lines.append("")
    for cmd in contract["required_reruns_after_classifier_change"]:
        lines.append(f"    {cmd}")
    lines.append("")
    lines.append("## Non-claim lock")
    lines.append("")
    for lock in artifact["non_claim_lock"]:
        lines.append(f"- {lock}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase 2 regression guard.")
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--attribution", type=Path, default=DEFAULT_ATTRIBUTION)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    artifact = build_regression_guard(
        benchmark_path=args.benchmark,
        attribution_path=args.attribution,
        candidates_path=args.candidates,
        output_dir=args.output_dir,
    )

    print("Phase 2 regression guard complete.")
    print(f"Status: {artifact['current_status']['overall_status']}")
    print(f"Top-1 baseline: {artifact['baseline']['attribution']['accuracy']:.3f}")
    print(f"Top-3 baseline: {artifact['baseline']['attribution']['top3_accuracy']:.3f}")
    print(f"JSON: {args.output_dir / 'latest_phase2_regression_guard.json'}")
    print(f"Markdown: {args.output_dir / 'latest_phase2_regression_guard.md'}")


if __name__ == "__main__":
    main()