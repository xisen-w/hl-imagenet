"""Phase 2 attribution-guided candidate selection for HL-ImageNet.

Reads Phase 2 diagnostics, benchmark, and attribution artifacts and emits a
candidate plan for future controlled classifier changes.

This module does not change classifier behavior.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_ATTRIBUTION = REPO_ROOT / "logs" / "phase2" / "attribution" / "latest_phase2_attribution.json"
DEFAULT_BENCHMARK = REPO_ROOT / "logs" / "phase2" / "benchmarks" / "latest_phase2_benchmark.json"
DEFAULT_DIAGNOSTIC = REPO_ROOT / "logs" / "phase2" / "diagnostics" / "latest_phase2_diagnostic.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "logs" / "phase2" / "candidates"


def _load_json(path: Path, required: bool = True) -> dict[str, Any]:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Required file not found: {path}")
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _score_candidate_row(row: dict[str, Any]) -> float:
    """Rank rows by confidence margin and specificity of collapse."""
    margin = float(row.get("margin") or 0.0)
    has_proof = 1.0 if row.get("proof") else 0.0
    feature_count = len(row.get("activated_features") or [])
    return margin + 0.02 * min(feature_count, 12) + 0.05 * has_proof


def _compact_row(row: dict[str, Any]) -> dict[str, Any]:
    baseline = row.get("baseline_agreement") or {}
    correct_baselines = [
        name for name, payload in baseline.items()
        if payload.get("correct")
    ]

    return {
        "file": row.get("file"),
        "path": row.get("path"),
        "true_label": row.get("true_label"),
        "predicted_label": row.get("predicted_label"),
        "top3": row.get("top3"),
        "margin": row.get("margin"),
        "outcome": row.get("outcome"),
        "collapse_path": row.get("collapse_path"),
        "correct_baselines": correct_baselines,
        "top_features": [
            {
                "name": f.get("name"),
                "confidence": f.get("confidence"),
            }
            for f in (row.get("activated_features") or [])[:8]
        ],
        "proof_head": (row.get("proof") or [])[:5],
    }


def _top_rows(records: list[dict[str, Any]], predicate, limit: int) -> list[dict[str, Any]]:
    rows = [r for r in records if predicate(r)]
    rows.sort(key=_score_candidate_row, reverse=True)
    return [_compact_row(r) for r in rows[:limit]]


def _feature_overactivation(records: list[dict[str, Any]], threshold: float) -> list[dict[str, Any]]:
    n = max(len(records), 1)
    counts = Counter()

    by_feature_class = defaultdict(Counter)

    for row in records:
        true_label = row.get("true_label")
        for feat in row.get("activated_features") or []:
            name = feat.get("name")
            if not name:
                continue
            counts[name] += 1
            by_feature_class[name][true_label] += 1

    results = []
    for name, count in counts.most_common():
        rate = count / n
        if rate >= threshold:
            top_classes = by_feature_class[name].most_common(5)
            results.append({
                "feature": name,
                "sample_count": count,
                "activation_rate": rate,
                "top_true_classes": top_classes,
                "risk": "global_overactivation",
            })

    return results


def _collapse_targets(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pred_counts = Counter()
    path_counts = Counter()

    for row in records:
        if row.get("outcome") == "correct":
            continue
        pred = row.get("predicted_label")
        true = row.get("true_label")
        path = row.get("collapse_path")
        if pred and pred != true:
            pred_counts[pred] += 1
        if path:
            path_counts[path] += 1

    targets = []
    for label, count in pred_counts.most_common(10):
        top_paths = [
            {"collapse_path": path, "count": c}
            for path, c in path_counts.most_common(30)
            if path.endswith("->" + label)
        ][:8]
        targets.append({
            "attractor_label": label,
            "false_positive_count": count,
            "top_collapse_paths": top_paths,
            "candidate_action": "inspect suppressive conditions or tighten broad signatures before changing scoring",
        })

    return targets


def _victim_targets(summary: dict[str, Any]) -> list[dict[str, Any]]:
    per_class = summary.get("per_class") or {}
    rows = []

    for cls, payload in per_class.items():
        recall = float(payload.get("recall") or 0.0)
        top3_recall = float(payload.get("top3_recall") or 0.0)
        rescue_gap = max(0.0, top3_recall - recall)
        miss_count = int(payload.get("miss_count") or 0)

        rows.append({
            "class": cls,
            "recall": recall,
            "top3_recall": top3_recall,
            "rescue_gap": rescue_gap,
            "miss_count": miss_count,
            "top_wrong_predictions": payload.get("top_wrong_predictions") or [],
            "candidate_action": "prioritize if low recall and high top3 rescue gap",
        })

    rows.sort(key=lambda r: (r["miss_count"], r["rescue_gap"]), reverse=True)
    return rows


def _benchmark_interpretation(benchmark: dict[str, Any]) -> dict[str, Any]:
    models = benchmark.get("models") or {}
    hl = models.get("hl_symbolic_classifier") or {}
    leaderboard = benchmark.get("leaderboard") or []

    above = []
    below = []

    hl_top1 = float(hl.get("top1_accuracy") or 0.0)

    for row in leaderboard:
        name = row.get("name")
        if name == "hl_symbolic_classifier":
            continue
        top1 = float(row.get("top1_accuracy") or 0.0)
        if hl_top1 > top1:
            above.append(name)
        else:
            below.append(name)

    return {
        "hl_top1": hl_top1,
        "hl_top3": float(hl.get("top3_accuracy") or 0.0),
        "hl_above": above,
        "hl_below_or_equal": below,
        "interpretation": "HL beats random/majority but candidate changes must aim to close gaps against handcrafted baselines.",
    }


def build_candidate_plan(
    attribution_path: Path,
    benchmark_path: Path,
    diagnostic_path: Path,
    output_dir: Path,
    limit: int,
    overactivation_threshold: float,
) -> dict[str, Any]:
    attribution = _load_json(attribution_path, required=True)
    benchmark = _load_json(benchmark_path, required=False)
    diagnostic = _load_json(diagnostic_path, required=False)

    records = attribution.get("records") or []
    summary = attribution.get("summary") or {}

    baseline_right_hl_wrong = _top_rows(
        records,
        lambda r: bool(r.get("baseline_right_hl_wrong")),
        limit,
    )

    hl_right_all_baselines_wrong = _top_rows(
        records,
        lambda r: bool(r.get("hl_right_all_baselines_wrong")),
        limit,
    )

    feature_warnings = _feature_overactivation(records, overactivation_threshold)
    attractor_targets = _collapse_targets(records)
    victim_targets = _victim_targets(summary)

    plan = {
        "schema": "hl_imagenet_phase2_candidate_selection_v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_files": {
            "attribution": str(attribution_path),
            "benchmark": str(benchmark_path) if benchmark else None,
            "diagnostic": str(diagnostic_path) if diagnostic else None,
        },
        "summary": {
            "n_samples": summary.get("n_samples"),
            "accuracy": summary.get("accuracy"),
            "top3_accuracy": summary.get("top3_accuracy"),
            "baseline_right_hl_wrong_count": summary.get("baseline_right_hl_wrong"),
            "hl_right_all_baselines_wrong_count": summary.get("hl_right_all_baselines_wrong"),
            "outcome_counts": summary.get("outcome_counts"),
        },
        "benchmark_interpretation": _benchmark_interpretation(benchmark) if benchmark else {},
        "candidate_sets": {
            "baseline_right_hl_wrong_top": baseline_right_hl_wrong,
            "hl_right_all_baselines_wrong_top": hl_right_all_baselines_wrong,
            "feature_overactivation_warnings": feature_warnings,
            "victim_rescue_targets": victim_targets,
            "attractor_suppression_targets": attractor_targets,
        },
        "phase2_6_recommendation": {
            "recommended_first_move": "do not modify classifier yet; inspect baseline-right/HL-wrong rows for the top collapse paths and compare them against HL-right/all-baselines-wrong rows",
            "likely_first_code_target": "tighten globally overactive Phase 2 signatures or add regression guards before attractor suppression",
            "must_rerun_after_any_classifier_change": [
                "python scripts/run_phase2_diagnostics.py --input <new_phase2_eval_json>",
                "python scripts/run_phase2_benchmarks.py --data-root \".\\data\\phase2\" --split val",
                "python scripts/run_phase2_attribution.py --data-root \".\\data\\phase2\" --split val",
                "python scripts/run_phase2_candidates.py",
            ],
        },
        "non_claim_lock": [
            "This candidate plan does not change classifier behavior.",
            "This candidate plan does not claim accuracy improvement.",
            "This candidate plan does not prove classifier correctness.",
            "Validation candidate selection is not final test evidence.",
            "Any future classifier change must rerun diagnostics, benchmarks, attribution, and candidate selection.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "latest_phase2_candidate_plan.json"
    md_path = output_dir / "latest_phase2_candidate_plan.md"

    json_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    _write_markdown(plan, md_path)

    return plan


def _write_markdown(plan: dict[str, Any], path: Path) -> None:
    summary = plan["summary"]
    candidate_sets = plan["candidate_sets"]

    lines = []
    lines.append("# HL-ImageNet Phase 2 Candidate Selection Plan")
    lines.append("")
    lines.append(f"Generated: `{plan['generated_at']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Samples: `{summary.get('n_samples')}`")
    lines.append(f"- Accuracy: `{float(summary.get('accuracy') or 0.0):.3f}`")
    lines.append(f"- Top-3 accuracy: `{float(summary.get('top3_accuracy') or 0.0):.3f}`")
    lines.append(f"- Baseline-right / HL-wrong: `{summary.get('baseline_right_hl_wrong_count')}`")
    lines.append(f"- HL-right / all-baselines-wrong: `{summary.get('hl_right_all_baselines_wrong_count')}`")
    lines.append(f"- Outcome counts: `{summary.get('outcome_counts')}`")
    lines.append("")
    lines.append("## Benchmark interpretation")
    lines.append("")
    bench = plan.get("benchmark_interpretation") or {}
    if bench:
        lines.append(f"- HL top-1: `{bench.get('hl_top1'):.3f}`")
        lines.append(f"- HL top-3: `{bench.get('hl_top3'):.3f}`")
        lines.append(f"- HL above: `{bench.get('hl_above')}`")
        lines.append(f"- HL below/equal: `{bench.get('hl_below_or_equal')}`")
        lines.append(f"- Interpretation: {bench.get('interpretation')}")
    else:
        lines.append("- Benchmark artifact not found.")
    lines.append("")
    lines.append("## Top baseline-right / HL-wrong candidates")
    lines.append("")
    lines.append("| True | HL Pred | Collapse | Margin | Correct baselines | File |")
    lines.append("|---|---|---|---:|---|---|")
    for row in candidate_sets["baseline_right_hl_wrong_top"][:25]:
        lines.append(
            f"| {row.get('true_label')} | {row.get('predicted_label')} | {row.get('collapse_path')} | "
            f"{float(row.get('margin') or 0.0):.3f} | {', '.join(row.get('correct_baselines') or [])} | {row.get('file')} |"
        )
    lines.append("")
    lines.append("## Top HL-right / all-baselines-wrong candidates")
    lines.append("")
    lines.append("| True | HL Pred | Margin | File | Top features |")
    lines.append("|---|---|---:|---|---|")
    for row in candidate_sets["hl_right_all_baselines_wrong_top"][:25]:
        feats = ", ".join(f.get("name") for f in (row.get("top_features") or [])[:4] if f.get("name"))
        lines.append(
            f"| {row.get('true_label')} | {row.get('predicted_label')} | "
            f"{float(row.get('margin') or 0.0):.3f} | {row.get('file')} | {feats} |"
        )
    lines.append("")
    lines.append("## Feature overactivation warnings")
    lines.append("")
    lines.append("| Feature | Count | Rate | Top true classes |")
    lines.append("|---|---:|---:|---|")
    for row in candidate_sets["feature_overactivation_warnings"][:25]:
        cls = ", ".join(f"{name}:{count}" for name, count in row.get("top_true_classes") or [])
        lines.append(
            f"| {row.get('feature')} | {row.get('sample_count')} | "
            f"{float(row.get('activation_rate') or 0.0):.3f} | {cls} |"
        )
    lines.append("")
    lines.append("## Victim rescue targets")
    lines.append("")
    lines.append("| Class | Recall | Top-3 recall | Rescue gap | Misses | Top wrong predictions |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for row in candidate_sets["victim_rescue_targets"][:10]:
        wrong = ", ".join(f"{label}:{count}" for label, count in row.get("top_wrong_predictions") or [])
        lines.append(
            f"| {row.get('class')} | {row.get('recall'):.3f} | {row.get('top3_recall'):.3f} | "
            f"{row.get('rescue_gap'):.3f} | {row.get('miss_count')} | {wrong} |"
        )
    lines.append("")
    lines.append("## Attractor suppression targets")
    lines.append("")
    lines.append("| Attractor | False-positive count | Top collapse paths |")
    lines.append("|---|---:|---|")
    for row in candidate_sets["attractor_suppression_targets"][:10]:
        paths = ", ".join(f"{p['collapse_path']}:{p['count']}" for p in row.get("top_collapse_paths") or [])
        lines.append(f"| {row.get('attractor_label')} | {row.get('false_positive_count')} | {paths} |")
    lines.append("")
    lines.append("## Phase 2.6 recommendation")
    lines.append("")
    rec = plan["phase2_6_recommendation"]
    lines.append(f"- Recommended first move: {rec['recommended_first_move']}")
    lines.append(f"- Likely first code target: {rec['likely_first_code_target']}")
    lines.append("")
    lines.append("Required reruns after any classifier change:")
    lines.append("")
    for cmd in rec["must_rerun_after_any_classifier_change"]:
        lines.append(f"    {cmd}")
    lines.append("")
    lines.append("## Non-claim lock")
    lines.append("")
    for lock in plan["non_claim_lock"]:
        lines.append(f"- {lock}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase 2 candidate selection.")
    parser.add_argument("--attribution", type=Path, default=DEFAULT_ATTRIBUTION)
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--diagnostic", type=Path, default=DEFAULT_DIAGNOSTIC)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--overactivation-threshold", type=float, default=0.50)
    args = parser.parse_args()

    plan = build_candidate_plan(
        attribution_path=args.attribution,
        benchmark_path=args.benchmark,
        diagnostic_path=args.diagnostic,
        output_dir=args.output_dir,
        limit=args.limit,
        overactivation_threshold=args.overactivation_threshold,
    )

    print("Phase 2 candidate selection complete.")
    print(f"Samples: {plan['summary']['n_samples']}")
    print(f"Baseline-right / HL-wrong: {plan['summary']['baseline_right_hl_wrong_count']}")
    print(f"HL-right / all-baselines-wrong: {plan['summary']['hl_right_all_baselines_wrong_count']}")
    print(f"JSON: {args.output_dir / 'latest_phase2_candidate_plan.json'}")
    print(f"Markdown: {args.output_dir / 'latest_phase2_candidate_plan.md'}")


if __name__ == "__main__":
    main()