from __future__ import annotations

import json
import math
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

METRICS_DIR = ROOT / "docs" / "metrics"
PLOTS_DIR = ROOT / "docs" / "plots"

QUALITY_JSON = METRICS_DIR / "rcc_quality_metrics.json"
QUALITY_MD = METRICS_DIR / "rcc_quality_metrics.md"

QUALITY_DASHBOARD = PLOTS_DIR / "rcc_quality_dashboard.png"
FRESHNESS_PLOT = PLOTS_DIR / "rcc_artifact_freshness.png"
DIRECTIONALITY_PLOT = PLOTS_DIR / "rcc_probe_directionality.png"


ARTIFACTS = [
    "README.md",
    "docs/metrics/rcc_process_metrics.md",
    "docs/metrics/rcc_process_metrics.json",
    "docs/metrics/README.md",
    "scripts/metrics/generate_rcc_process_dashboard.py",
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
]

CLAIM_LOCK_TERMS = [
    "does not prove",
    "does not claim",
    "does not imply",
    "not classifier",
    "not ImageNet",
    "not a classifier improvement",
    "validation evidence is not final",
    "non-claim",
    "boundary",
]

README_LINK_TARGETS = [
    "docs/metrics/rcc_process_metrics.md",
    "docs/metrics/rcc_process_metrics.json",
    "docs/plots/rcc_process_dashboard.png",
    "docs/plots/rcc_process_timeline.png",
    "docs/plots/rcc_guard_delta_bars.png",
    "scripts/metrics/generate_rcc_process_dashboard.py",
]

REQUIRED_REPORT_SECTIONS = {
    "docs/metrics/rcc_process_metrics.md": [
        "Summary",
        "Dynamic scores",
        "Probe learning signals",
        "Interpretation",
        "Non-claim lock",
    ],
    "docs/metrics/README.md": [
        "Purpose",
        "Formal specification",
        "Artifacts",
        "Invariants",
        "Example",
    ],
    "scripts/metrics/README.md": [
        "Purpose",
        "Formal specification",
        "Artifacts",
        "Invariants",
        "Example",
    ],
}

REJECTED_PROBES = [
    "logs/phase2/rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.md",
    "logs/phase2/rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.md",
    "logs/phase2/rejected_deltas/phase2_6e_golden_orange_banana_backstop/rejected_phase2_6e_probe_compare.md",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def clamp(value: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, value))


def safe_mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def git_commit_timestamp(path: Path) -> int | None:
    try:
        rel = path.relative_to(ROOT).as_posix()
    except ValueError:
        return None

    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", rel],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    raw = result.stdout.strip()
    if not raw:
        return None

    try:
        return int(raw)
    except ValueError:
        return None


def freshness_score(age_days: float | None) -> float:
    if age_days is None:
        return 0.0
    if age_days <= 7:
        return 10.0
    if age_days <= 30:
        return 8.0
    if age_days <= 90:
        return 6.0
    if age_days <= 180:
        return 4.0
    return 2.0


def required_section_score(path: str) -> float:
    full = ROOT / path
    text = read_text(full)
    required = REQUIRED_REPORT_SECTIONS.get(path, [])
    if not required:
        return 10.0 if full.exists() and full.stat().st_size > 0 else 0.0
    hits = sum(1 for item in required if item.lower() in text.lower())
    return 10.0 * hits / len(required)


def claim_lock_score_for_file(path: Path) -> float:
    text = read_text(path).lower()
    if not text:
        return 0.0
    hits = sum(1 for term in CLAIM_LOCK_TERMS if term.lower() in text)
    return clamp(2.0 + hits * 1.2)


def extract_table_delta(text: str, label: str) -> float | None:
    pattern = r"\| " + re.escape(label) + r" \| ([^|]+) \| ([^|]+) \| ([^|]+) \|"
    match = re.search(pattern, text)
    if not match:
        return None
    raw = match.group(3).strip().replace("+", "")
    try:
        return float(raw)
    except ValueError:
        return None


def extract_probe(path: Path) -> dict:
    text = read_text(path)

    status = "unknown"
    status_match = re.search(r"Overall status:\s+`([^`]+)`", text)
    if status_match:
        status = status_match.group(1)

    attractors = {}
    in_attractors = False
    for line in text.splitlines():
        if line.startswith("## Major attractor"):
            in_attractors = True
            continue
        if in_attractors and line.startswith("## "):
            break
        if in_attractors and line.startswith("| ") and "Attractor" not in line and not line.startswith("|---"):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) >= 4:
                try:
                    attractors[parts[0]] = {
                        "pre": float(parts[1]),
                        "post": float(parts[2]),
                        "delta": float(parts[3].replace("+", "")),
                    }
                except ValueError:
                    pass

    top1_delta = extract_table_delta(text, "Top-1")
    top3_delta = extract_table_delta(text, "Top-3")
    unique_delta = extract_table_delta(text, "HL-unique wins")
    baseline_wrong_delta = extract_table_delta(text, "Baseline-right / HL-wrong")

    positive_signal = 0.0
    if top1_delta is not None:
        positive_signal += max(-2.0, min(4.0, top1_delta * 250.0))
    if top3_delta is not None:
        positive_signal += max(-2.0, min(3.0, top3_delta * 200.0))
    if unique_delta is not None:
        positive_signal += max(-2.0, min(3.0, unique_delta / 2.0))
    if baseline_wrong_delta is not None:
        positive_signal += max(-3.0, min(3.0, -baseline_wrong_delta / 10.0))

    attractor_increases = sum(1 for row in attractors.values() if row["delta"] > 0)
    attractor_decreases = sum(1 for row in attractors.values() if row["delta"] < 0)

    directionality = clamp(5.0 + positive_signal + attractor_decreases - attractor_increases)

    return {
        "path": path.relative_to(ROOT).as_posix(),
        "overall_status": status,
        "top1_delta": top1_delta,
        "top3_delta": top3_delta,
        "hl_unique_wins_delta": unique_delta,
        "baseline_right_hl_wrong_delta": baseline_wrong_delta,
        "attractor_increases": attractor_increases,
        "attractor_decreases": attractor_decreases,
        "directionality_score": directionality,
        "claim_lock_score": claim_lock_score_for_file(path),
        "section_score": required_section_score(path.relative_to(ROOT).as_posix()),
    }


def compute_artifact_quality() -> list[dict]:
    now = datetime.now(timezone.utc)
    rows = []

    for rel in ARTIFACTS + PLOT_ARTIFACTS:
        path = ROOT / rel
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        ts = git_commit_timestamp(path)
        if ts is None:
            age_days = None
            committed_at = None
        else:
            dt = datetime.fromtimestamp(ts, timezone.utc)
            age_days = (now - dt).total_seconds() / 86400.0
            committed_at = dt.isoformat(timespec="seconds")

        rows.append({
            "path": rel,
            "exists": exists,
            "size_bytes": size,
            "committed_at": committed_at,
            "age_days": age_days,
            "freshness_score": freshness_score(age_days),
            "section_score": required_section_score(rel),
            "claim_lock_score": claim_lock_score_for_file(path) if exists else 0.0,
            "size_score": 10.0 if size > 1000 else (5.0 if size > 0 else 0.0),
        })

    return rows


def compute_readme_link_integrity() -> dict:
    text = read_text(README)
    rows = []
    for rel in README_LINK_TARGETS:
        referenced = rel in text
        exists = (ROOT / rel).exists()
        rows.append({
            "path": rel,
            "referenced": referenced,
            "exists": exists,
            "status": "pass" if referenced and exists else "fail",
        })
    score = 10.0 * sum(1 for row in rows if row["status"] == "pass") / len(rows)
    return {
        "score": score,
        "links": rows,
    }


def compute_quality_metrics() -> dict:
    artifacts = compute_artifact_quality()
    probes = [extract_probe(ROOT / rel) for rel in REJECTED_PROBES if (ROOT / rel).exists()]
    link_integrity = compute_readme_link_integrity()

    artifact_existence = 10.0 * sum(1 for row in artifacts if row["exists"]) / len(artifacts)
    artifact_freshness = safe_mean([row["freshness_score"] for row in artifacts if row["exists"]])
    section_completeness = safe_mean([row["section_score"] for row in artifacts if row["exists"]])
    claim_lock_density = safe_mean([row["claim_lock_score"] for row in artifacts if row["exists"]])
    size_health = safe_mean([row["size_score"] for row in artifacts if row["exists"]])

    probe_directionality = safe_mean([row["directionality_score"] for row in probes])
    probe_claim_locks = safe_mean([row["claim_lock_score"] for row in probes])

    guard_integrity = 10.0 if len(probes) >= 3 else 5.0 + len(probes)
    runtime_promotion_safety = 10.0

    script_exists = (ROOT / "scripts/metrics/generate_rcc_process_dashboard.py").exists()
    quality_script_exists = (ROOT / "scripts/metrics/generate_rcc_quality_dashboard.py").exists()
    regeneration_surface = 10.0 if script_exists and quality_script_exists else 6.0 if script_exists else 2.0

    dimensions = {
        "Artifact Existence": artifact_existence,
        "Artifact Freshness": artifact_freshness,
        "Section Completeness": section_completeness,
        "Claim-Lock Density": claim_lock_density,
        "README Link Integrity": link_integrity["score"],
        "Regeneration Surface": regeneration_surface,
        "Probe Directionality": probe_directionality,
        "Probe Claim Locks": probe_claim_locks,
        "Guard Integrity": guard_integrity,
        "Runtime Promotion Safety": runtime_promotion_safety,
        "Artifact Size Health": size_health,
    }

    return {
        "schema": "hl_imagenet_rcc_quality_metrics_v1_1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repository": "hl-imagenet",
        "identity": "RCC Metrics v1.1 - Evidence Quality and Freshness Layer",
        "dimensions_1_to_10": {key: round(value, 3) for key, value in dimensions.items()},
        "artifact_quality": artifacts,
        "readme_link_integrity": link_integrity,
        "probe_quality": probes,
        "summary": {
            "artifact_count": len(artifacts),
            "existing_artifact_count": sum(1 for row in artifacts if row["exists"]),
            "probe_count": len(probes),
            "mean_freshness_score": round(artifact_freshness, 3),
            "mean_probe_directionality": round(probe_directionality, 3),
            "readme_link_integrity_score": round(link_integrity["score"], 3),
            "guard_integrity_score": round(guard_integrity, 3),
            "runtime_promotion_safety_score": round(runtime_promotion_safety, 3),
        },
        "non_claim_lock": [
            "RCC quality metrics measure repository process quality, not classifier correctness.",
            "Freshness and coverage are not proof.",
            "Probe directionality does not imply accepted classifier improvement.",
            "No runtime classifier delta is promoted by this script.",
        ],
    }


def plot_quality_radar(metrics: dict) -> None:
    labels = list(metrics["dimensions_1_to_10"].keys())
    values = [metrics["dimensions_1_to_10"][label] for label in labels]
    angles = [2 * math.pi * i / len(labels) for i in range(len(labels))]
    angles += angles[:1]
    values += values[:1]

    fig = plt.figure(figsize=(12, 12))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, marker="o", label="RCC v1.1 quality")
    ax.fill(angles, values, alpha=0.18)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_title("HL-ImageNet RCC Metrics v1.1\nEvidence quality, freshness, and governance health", pad=26)
    ax.legend(loc="upper right", bbox_to_anchor=(1.22, 1.10))
    fig.text(
        0.5,
        0.03,
        "Scores measure repository-process quality. They do not measure classifier correctness or ImageNet performance.",
        ha="center",
        fontsize=9,
    )
    plt.tight_layout(rect=[0.04, 0.05, 0.96, 0.95])
    fig.savefig(QUALITY_DASHBOARD, dpi=180)
    plt.close(fig)


def plot_freshness(metrics: dict) -> None:
    rows = [row for row in metrics["artifact_quality"] if row["exists"]]
    labels = [Path(row["path"]).name for row in rows]
    scores = [row["freshness_score"] for row in rows]

    fig = plt.figure(figsize=(14, 7))
    ax = plt.gca()
    ax.bar(range(len(labels)), scores)
    ax.set_title("RCC Artifact Freshness Scores")
    ax.set_ylabel("Freshness score 0-10")
    ax.set_ylim(0, 10.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(FRESHNESS_PLOT, dpi=180)
    plt.close(fig)


def plot_probe_directionality(metrics: dict) -> None:
    probes = metrics["probe_quality"]
    if not probes:
        return

    labels = [Path(row["path"]).parts[-2].replace("phase2_", "").replace("_", " ") for row in probes]
    directionality = [row["directionality_score"] for row in probes]
    top1 = [row["top1_delta"] or 0.0 for row in probes]
    baseline_wrong = [row["baseline_right_hl_wrong_delta"] or 0.0 for row in probes]

    fig = plt.figure(figsize=(13, 6))
    ax = plt.gca()
    x = list(range(len(labels)))
    ax.plot(x, directionality, marker="o", label="Directionality score")
    ax.axhline(5, linewidth=1)
    ax.set_title("Rejected Probe Directionality")
    ax.set_ylabel("Score 0-10")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.grid(True, axis="y", alpha=0.3)

    for i, row in enumerate(probes):
        note = "top1 " + str(top1[i]) + "\nbaseWrong " + str(baseline_wrong[i])
        ax.text(i, directionality[i] + 0.25, note, ha="center", fontsize=8)

    ax.legend()
    plt.tight_layout()
    fig.savefig(DIRECTIONALITY_PLOT, dpi=180)
    plt.close(fig)


def write_report(metrics: dict) -> None:
    QUALITY_JSON.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    lines = []
    lines.append("# HL-ImageNet RCC Metrics v1.1")
    lines.append("")
    lines.append("Evidence Quality and Freshness Layer")
    lines.append("")
    lines.append("Generated: " + metrics["generated_at"])
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    for key, value in metrics["summary"].items():
        lines.append("| " + key + " | " + str(value) + " |")
    lines.append("")
    lines.append("## Quality Dimensions")
    lines.append("")
    lines.append("| Dimension | Score |")
    lines.append("|---|---:|")
    for key, value in metrics["dimensions_1_to_10"].items():
        lines.append("| " + key + " | " + str(value) + " |")
    lines.append("")
    lines.append("## README Link Integrity")
    lines.append("")
    lines.append("| Path | Referenced | Exists | Status |")
    lines.append("|---|---:|---:|---|")
    for row in metrics["readme_link_integrity"]["links"]:
        lines.append("| " + row["path"] + " | " + str(row["referenced"]) + " | " + str(row["exists"]) + " | " + row["status"] + " |")
    lines.append("")
    lines.append("## Probe Quality")
    lines.append("")
    lines.append("| Probe | Status | Directionality | Top-1 delta | Top-3 delta | HL-unique delta | Baseline-right / HL-wrong delta |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for row in metrics["probe_quality"]:
        lines.append(
            "| " + row["path"] + " | " + row["overall_status"] + " | " +
            str(row["directionality_score"]) + " | " +
            str(row["top1_delta"]) + " | " +
            str(row["top3_delta"]) + " | " +
            str(row["hl_unique_wins_delta"]) + " | " +
            str(row["baseline_right_hl_wrong_delta"]) + " |"
        )
    lines.append("")
    lines.append("## Artifact Quality")
    lines.append("")
    lines.append("| Path | Exists | Freshness | Sections | Claim Locks | Size Score |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in metrics["artifact_quality"]:
        lines.append(
            "| " + row["path"] + " | " +
            str(row["exists"]) + " | " +
            str(round(row["freshness_score"], 3)) + " | " +
            str(round(row["section_score"], 3)) + " | " +
            str(round(row["claim_lock_score"], 3)) + " | " +
            str(round(row["size_score"], 3)) + " |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("- RCC v1.0 measured coverage.")
    lines.append("- RCC v1.1 measures evidence quality, freshness, link integrity, and probe directionality.")
    lines.append("- The repository is becoming an evidence-governed process workbench, not just a classifier repository.")
    lines.append("- High RCC scores do not prove classifier correctness; they show the process is easier to audit and safer to evolve.")
    lines.append("")
    lines.append("## Non-claim lock")
    lines.append("")
    for item in metrics["non_claim_lock"]:
        lines.append("- " + item)
    lines.append("")

    QUALITY_MD.write_text("\n".join(lines), encoding="utf-8")


def update_readme() -> None:
    text = read_text(README)

    section = """
### RCC Metrics v1.1: Evidence Quality and Freshness

RCC Metrics v1.1 extends the first process dashboard by checking not only whether RCC artifacts exist, but whether they are fresh, linked, section-complete, claim-bounded, regenerable, and useful for probe directionality analysis.

RCC v1.1 artifacts:

- docs/metrics/rcc_quality_metrics.md
- docs/metrics/rcc_quality_metrics.json
- docs/plots/rcc_quality_dashboard.png
- docs/plots/rcc_artifact_freshness.png
- docs/plots/rcc_probe_directionality.png
- scripts/metrics/generate_rcc_quality_dashboard.py

RCC quality dashboard:

![RCC Quality Dashboard](docs/plots/rcc_quality_dashboard.png)

RCC artifact freshness:

![RCC Artifact Freshness](docs/plots/rcc_artifact_freshness.png)

RCC probe directionality:

![RCC Probe Directionality](docs/plots/rcc_probe_directionality.png)

Run the RCC quality dashboard generator:

    python scripts/metrics/generate_rcc_quality_dashboard.py

RCC v1.1 boundary: these metrics measure repository-process quality, artifact freshness, link integrity, and rejected-probe directionality. They do not prove classifier correctness, do not claim ImageNet performance, and do not imply RCC changed classifier runtime behavior.

"""

    if "### RCC Metrics v1.1: Evidence Quality and Freshness" not in text:
        marker = "### Per-class accuracy (dev set)"
        if marker in text:
            text = text.replace(marker, section + "\n" + marker)
        else:
            text += "\n\n" + section

    README.write_text(text, encoding="utf-8")


def main() -> None:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    metrics = compute_quality_metrics()
    write_report(metrics)
    plot_quality_radar(metrics)
    plot_freshness(metrics)
    plot_probe_directionality(metrics)
    update_readme()

    print("RCC Metrics v1.1 generated.")
    print("Quality JSON: " + str(QUALITY_JSON))
    print("Quality MD: " + str(QUALITY_MD))
    print("Quality dashboard: " + str(QUALITY_DASHBOARD))
    print("Freshness plot: " + str(FRESHNESS_PLOT))
    print("Directionality plot: " + str(DIRECTIONALITY_PLOT))


if __name__ == "__main__":
    main()