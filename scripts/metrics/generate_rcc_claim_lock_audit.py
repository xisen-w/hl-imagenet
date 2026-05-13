from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
METRICS_DIR = ROOT / "docs" / "metrics"
PLOTS_DIR = ROOT / "docs" / "plots"

AUDIT_JSON = METRICS_DIR / "rcc_claim_lock_audit.json"
AUDIT_MD = METRICS_DIR / "rcc_claim_lock_audit.md"
AUDIT_PNG = PLOTS_DIR / "rcc_claim_lock_density.png"


TEXT_ARTIFACTS = [
    "README.md",
    "docs/metrics/README.md",
    "scripts/metrics/README.md",
    "docs/plots/README.md",
    "docs/metrics/rcc_process_metrics.md",
    "docs/metrics/rcc_quality_metrics.md",
    "logs/phase2/diagnostics/latest_phase2_diagnostic.md",
    "logs/phase2/benchmarks/latest_phase2_benchmark.md",
    "logs/phase2/attribution/latest_phase2_attribution.md",
    "logs/phase2/candidates/latest_phase2_candidate_plan.md",
    "logs/phase2/regression_guard/latest_phase2_regression_guard.md",
    "logs/phase2/rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.md",
    "logs/phase2/rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.md",
    "logs/phase2/rejected_deltas/phase2_6e_golden_orange_banana_backstop/rejected_phase2_6e_probe_compare.md",
]

PLOT_ARTIFACTS = [
    "docs/plots/rcc_process_dashboard.png",
    "docs/plots/rcc_process_timeline.png",
    "docs/plots/rcc_guard_delta_bars.png",
    "docs/plots/rcc_quality_dashboard.png",
    "docs/plots/rcc_artifact_freshness.png",
    "docs/plots/rcc_probe_directionality.png",
]

REQUIRED_LOCKS = [
    "does not prove classifier correctness",
    "does not claim ImageNet performance",
    "does not imply RCC changed classifier runtime behavior",
    "does not promote classifier behavior",
    "not a classifier improvement",
    "validation evidence is not final test evidence",
    "repository-process",
    "non-claim",
]

PLOT_LOCKS = [
    "plots are process-observability artifacts",
    "plots are not benchmark results",
    "plots do not prove classifier correctness",
    "plots do not claim ImageNet performance",
    "plots do not imply runtime classifier changes",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def count_hits(text: str, terms: list[str]) -> dict[str, bool]:
    lower = text.lower()
    return {term: term.lower() in lower for term in terms}


def score_hits(hits: dict[str, bool]) -> float:
    if not hits:
        return 0.0
    return round(10.0 * sum(1 for value in hits.values() if value) / len(hits), 3)


def audit_text_artifact(rel: str) -> dict:
    path = ROOT / rel
    text = read_text(path)
    hits = count_hits(text, REQUIRED_LOCKS)
    return {
        "path": rel,
        "exists": path.exists(),
        "type": "text",
        "lock_hits": hits,
        "lock_score": score_hits(hits),
        "word_count": len(re.findall(r"\w+", text)),
    }


def audit_plot_artifact(rel: str, plot_readme_text: str) -> dict:
    path = ROOT / rel
    hits = count_hits(plot_readme_text, PLOT_LOCKS)
    return {
        "path": rel,
        "exists": path.exists(),
        "type": "plot",
        "governed_by": "docs/plots/README.md",
        "lock_hits": hits,
        "lock_score": score_hits(hits),
        "size_bytes": path.stat().st_size if path.exists() else 0,
    }


def main() -> None:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    plot_readme_text = read_text(ROOT / "docs" / "plots" / "README.md")

    text_rows = [audit_text_artifact(rel) for rel in TEXT_ARTIFACTS]
    plot_rows = [audit_plot_artifact(rel, plot_readme_text) for rel in PLOT_ARTIFACTS]

    all_rows = text_rows + plot_rows
    existing_rows = [row for row in all_rows if row["exists"]]

    mean_all = round(sum(row["lock_score"] for row in existing_rows) / len(existing_rows), 3) if existing_rows else 0.0
    mean_text = round(sum(row["lock_score"] for row in text_rows if row["exists"]) / max(1, sum(1 for row in text_rows if row["exists"])), 3)
    mean_plots = round(sum(row["lock_score"] for row in plot_rows if row["exists"]) / max(1, sum(1 for row in plot_rows if row["exists"])), 3)

    audit = {
        "schema": "hl_imagenet_rcc_claim_lock_audit_v1_2",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repository": "hl-imagenet",
        "identity": "RCC Metrics v1.2 - Claim-Lock Density Repair",
        "summary": {
            "artifact_count": len(all_rows),
            "existing_artifact_count": len(existing_rows),
            "mean_claim_lock_score_all_existing": mean_all,
            "mean_claim_lock_score_text": mean_text,
            "mean_claim_lock_score_plots": mean_plots,
            "required_lock_count": len(REQUIRED_LOCKS),
            "plot_lock_count": len(PLOT_LOCKS),
        },
        "required_locks": REQUIRED_LOCKS,
        "plot_locks": PLOT_LOCKS,
        "artifact_audit": all_rows,
        "non_claim_lock": [
            "Claim-lock audit measures explicit boundary language, not classifier correctness.",
            "High claim-lock density does not prove the source is correct.",
            "High claim-lock density does not claim ImageNet performance.",
            "High claim-lock density does not imply RCC changed classifier runtime behavior.",
            "Plot claim-locks are governed through docs/plots/README.md because PNG files are binary artifacts.",
        ],
    }

    AUDIT_JSON.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    write_markdown(audit)
    plot_claim_lock_density(audit)

    print("RCC claim-lock audit generated.")
    print("Audit JSON: " + str(AUDIT_JSON))
    print("Audit MD: " + str(AUDIT_MD))
    print("Audit plot: " + str(AUDIT_PNG))


def write_markdown(audit: dict) -> None:
    lines = []
    lines.append("# HL-ImageNet RCC Metrics v1.2")
    lines.append("")
    lines.append("Claim-Lock Density Repair")
    lines.append("")
    lines.append("Generated: " + audit["generated_at"])
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    for key, value in audit["summary"].items():
        lines.append("| " + key + " | " + str(value) + " |")
    lines.append("")
    lines.append("## Required claim-lock terms")
    lines.append("")
    for item in audit["required_locks"]:
        lines.append("- " + item)
    lines.append("")
    lines.append("## Plot-governance claim-lock terms")
    lines.append("")
    for item in audit["plot_locks"]:
        lines.append("- " + item)
    lines.append("")
    lines.append("## Artifact audit")
    lines.append("")
    lines.append("| Path | Type | Exists | Claim-lock score |")
    lines.append("|---|---|---:|---:|")
    for row in audit["artifact_audit"]:
        lines.append("| " + row["path"] + " | " + row["type"] + " | " + str(row["exists"]) + " | " + str(row["lock_score"]) + " |")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- RCC v1.2 repairs the weakest v1.1 metric by auditing explicit boundary language.")
    lines.append("- Text artifacts are scored by direct claim-lock term coverage.")
    lines.append("- Plot artifacts are governed through docs/plots/README.md because PNG files cannot carry reliable text-boundary metadata.")
    lines.append("- The audit improves process trust without changing classifier runtime behavior.")
    lines.append("")
    lines.append("## Non-claim lock")
    lines.append("")
    for item in audit["non_claim_lock"]:
        lines.append("- " + item)
    lines.append("")
    AUDIT_MD.write_text("\n".join(lines), encoding="utf-8")


def plot_claim_lock_density(audit: dict) -> None:
    rows = [row for row in audit["artifact_audit"] if row["exists"]]
    labels = [Path(row["path"]).name for row in rows]
    scores = [row["lock_score"] for row in rows]

    fig = plt.figure(figsize=(15, 7))
    ax = plt.gca()
    ax.bar(range(len(labels)), scores)
    ax.set_title("RCC Metrics v1.2 Claim-Lock Density")
    ax.set_ylabel("Claim-lock score 0-10")
    ax.set_ylim(0, 10.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.axhline(7.5, linewidth=1)
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(AUDIT_PNG, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()