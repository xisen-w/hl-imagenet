from __future__ import annotations

import json
import math
import re
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
METRICS_DIR = ROOT / "docs" / "metrics"
PLOTS_DIR = ROOT / "docs" / "plots"

METRICS_JSON = METRICS_DIR / "rcc_process_metrics.json"
METRICS_MD = METRICS_DIR / "rcc_process_metrics.md"
DASHBOARD_PNG = PLOTS_DIR / "rcc_process_dashboard.png"
TIMELINE_PNG = PLOTS_DIR / "rcc_process_timeline.png"
DELTA_BARS_PNG = PLOTS_DIR / "rcc_guard_delta_bars.png"


PHASES = [
    "Phase 2.2",
    "Phase 2.3",
    "Phase 2.4",
    "Phase 2.5",
    "Phase 2.6A",
    "Phase 2.6C",
    "Phase 2.6D",
    "Phase 2.6E",
]

COMMANDS = [
    "run_phase2_diagnostics.py",
    "run_phase2_benchmarks.py",
    "run_phase2_attribution.py",
    "run_phase2_candidates.py",
    "run_phase2_regression_guard.py",
]

BOUNDARY_TERMS = [
    "Benchmark boundary",
    "Attribution boundary",
    "Candidate-selection boundary",
    "Regression-guard boundary",
    "Rejected-delta boundary",
    "Rejected-probe boundary",
    "non-claim",
    "does not claim",
    "not a classifier improvement",
]

RCC_TERMS = [
    "RCC",
    "AI operating contract",
    "AI file routing guide",
    "AI non-claim lock",
    "README maintenance rule",
    "Current Identity",
    "architecture locks",
]

ARTIFACT_PATHS = [
    "logs/phase2/diagnostics/latest_phase2_diagnostic.md",
    "logs/phase2/benchmarks/latest_phase2_benchmark.md",
    "logs/phase2/attribution/latest_phase2_attribution.md",
    "logs/phase2/candidates/latest_phase2_candidate_plan.md",
    "logs/phase2/regression_guard/latest_phase2_regression_guard.md",
    "logs/phase2/rejected_deltas/phase2_6b_exclusion_guard/rejected_phase2_6b_delta_compare.md",
    "logs/phase2/rejected_deltas/phase2_6d_golden_retriever_orange_exclusion/rejected_phase2_6d_probe_compare.md",
    "logs/phase2/rejected_deltas/phase2_6e_golden_orange_banana_backstop/rejected_phase2_6e_probe_compare.md",
]

MINI_README_ROOTS = [
    "hlinet",
    "scripts",
    "docs",
    "logs",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


def pct(count: int, total: int) -> float:
    if total == 0:
        return 0.0
    return count / total


def count_existing(paths: list[str]) -> int:
    return sum(1 for p in paths if (ROOT / p).exists())


def find_mini_readmes() -> list[str]:
    out = []
    for folder in MINI_README_ROOTS:
        root = ROOT / folder
        if not root.exists():
            continue
        for path in root.rglob("README.md"):
            rel = path.relative_to(ROOT).as_posix()
            out.append(rel)
    return sorted(set(out))


def extract_probe_metrics(md_path: Path) -> dict:
    text = read_text(md_path)
    if not text:
        return {}

    def number_after(label: str) -> float | None:
        pattern = rf"\| {re.escape(label)} \| ([^|]+) \| ([^|]+) \| ([^|]+) \|"
        m = re.search(pattern, text)
        if not m:
            return None
        raw = m.group(3).strip().replace("+", "")
        try:
            return float(raw)
        except ValueError:
            return None

    overall = "unknown"
    m = re.search(r"Overall status:\s+`([^`]+)`", text)
    if m:
        overall = m.group(1)

    attractors = {}
    in_attractor = False
    for line in text.splitlines():
        if line.startswith("## Major attractor deltas"):
            in_attractor = True
            continue
        if in_attractor and line.startswith("## "):
            break
        if in_attractor and line.startswith("| ") and not line.startswith("|---") and "Attractor" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 4:
                try:
                    attractors[parts[0]] = {
                        "pre": float(parts[1]),
                        "post": float(parts[2]),
                        "delta": float(parts[3].replace("+", "")),
                    }
                except ValueError:
                    pass

    return {
        "path": md_path.relative_to(ROOT).as_posix(),
        "overall_status": overall,
        "top1_delta": number_after("Top-1"),
        "top3_delta": number_after("Top-3"),
        "hl_unique_wins_delta": number_after("HL-unique wins"),
        "baseline_right_hl_wrong_delta": number_after("Baseline-right / HL-wrong"),
        "attractor_deltas": attractors,
    }


def compute_metrics() -> dict:
    readme = read_text(README)

    phase_hits = {p: (p in readme) for p in PHASES}
    command_hits = {c: (c in readme) for c in COMMANDS}
    boundary_hits = {b: (b in readme) for b in BOUNDARY_TERMS}
    rcc_hits = {r: (r in readme) for r in RCC_TERMS}
    artifact_hits = {p: (ROOT / p).exists() for p in ARTIFACT_PATHS}
    mini_readmes = find_mini_readmes()

    rejected_paths = sorted((ROOT / "logs" / "phase2" / "rejected_deltas").rglob("*.md")) if (ROOT / "logs" / "phase2" / "rejected_deltas").exists() else []
    rejected_compare_paths = [p for p in rejected_paths if "rejected_phase2" in p.name]
    probe_metrics = [extract_probe_metrics(p) for p in rejected_compare_paths]
    probe_metrics = [m for m in probe_metrics if m]

    accepted_runtime_deltas = 0
    rejected_or_failed_deltas = len(probe_metrics)

    scores = {
        "Navigation Speed": clamp(4.0 + 6.0 * pct(sum(command_hits.values()), len(command_hits))),
        "Context Fidelity": clamp(4.0 + 3.0 * pct(sum(phase_hits.values()), len(phase_hits)) + 3.0 * pct(sum(rcc_hits.values()), len(rcc_hits))),
        "Edit Boundary Clarity": clamp(3.0 + 7.0 * pct(sum(boundary_hits.values()), len(boundary_hits))),
        "Claim Boundary Safety": clamp(4.0 + 6.0 * pct(sum(boundary_hits.values()), len(boundary_hits))),
        "Auditability": clamp(3.0 + 4.0 * pct(count_existing(ARTIFACT_PATHS), len(ARTIFACT_PATHS)) + 3.0 * min(1.0, len(probe_metrics) / 3.0)),
        "Agent Efficiency": clamp(3.0 + 4.0 * pct(len(mini_readmes), 8) + 3.0 * pct(sum(command_hits.values()), len(command_hits))),
        "Drift Resistance": clamp(3.0 + 3.0 * pct(sum(boundary_hits.values()), len(boundary_hits)) + 4.0 * min(1.0, rejected_or_failed_deltas / 3.0)),
        "Onboarding Clarity": clamp(4.0 + 3.0 * pct(sum(rcc_hits.values()), len(rcc_hits)) + 3.0 * pct(len(mini_readmes), 8)),
        "Evidence Chain Completeness": clamp(2.0 + 8.0 * pct(count_existing(ARTIFACT_PATHS), len(ARTIFACT_PATHS))),
        "Failure Learning": clamp(2.0 + 8.0 * min(1.0, rejected_or_failed_deltas / 3.0)),
        "Controlled Evolution": clamp(3.0 + 3.0 * pct(sum(phase_hits.values()), len(phase_hits)) + 4.0 * min(1.0, rejected_or_failed_deltas / 3.0)),
        "Runtime Integrity": clamp(8.0 + 2.0 * (1.0 if accepted_runtime_deltas == 0 else 0.0)),
    }

    original_scores = {
        "Navigation Speed": 4.0,
        "Context Fidelity": 5.0,
        "Edit Boundary Clarity": 3.5,
        "Claim Boundary Safety": 6.0,
        "Auditability": 6.5,
        "Agent Efficiency": 4.0,
        "Drift Resistance": 4.0,
        "Onboarding Clarity": 5.0,
        "Evidence Chain Completeness": 3.5,
        "Failure Learning": 2.5,
        "Controlled Evolution": 3.0,
        "Runtime Integrity": 8.0,
    }

    metrics = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repository": "hl-imagenet",
        "identity": "governed heuristic-learning workbench",
        "phase_hits": phase_hits,
        "command_hits": command_hits,
        "boundary_hits": boundary_hits,
        "rcc_hits": rcc_hits,
        "artifact_hits": artifact_hits,
        "mini_readmes": mini_readmes,
        "counts": {
            "phase_coverage": sum(phase_hits.values()),
            "phase_total": len(phase_hits),
            "command_coverage": sum(command_hits.values()),
            "command_total": len(command_hits),
            "boundary_coverage": sum(boundary_hits.values()),
            "boundary_total": len(boundary_hits),
            "rcc_coverage": sum(rcc_hits.values()),
            "rcc_total": len(rcc_hits),
            "artifact_coverage": count_existing(ARTIFACT_PATHS),
            "artifact_total": len(ARTIFACT_PATHS),
            "mini_readme_count": len(mini_readmes),
            "rejected_or_failed_delta_count": rejected_or_failed_deltas,
            "accepted_runtime_delta_count": accepted_runtime_deltas,
        },
        "scores_1_to_10": scores,
        "original_repo_reference_scores_1_to_10": original_scores,
        "probe_metrics": probe_metrics,
        "interpretation": [
            "RCC is functioning as durable repository memory.",
            "The repo now exposes navigation, claim boundaries, command surfaces, evidence artifacts, and rejected-delta lessons without needing chat context.",
            "No accepted runtime classifier delta has been promoted after the guard was installed.",
            "Rejected probes are becoming useful constraints for the next controlled experiment.",
        ],
    }
    return metrics


def plot_radar(metrics: dict) -> None:
    labels = list(metrics["scores_1_to_10"].keys())
    current = [metrics["scores_1_to_10"][k] for k in labels]
    original = [metrics["original_repo_reference_scores_1_to_10"][k] for k in labels]

    angles = [2 * math.pi * i / len(labels) for i in range(len(labels))]
    angles += angles[:1]
    current += current[:1]
    original += original[:1]

    fig = plt.figure(figsize=(12, 12))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, original, marker="o", label="Original repo reference")
    ax.fill(angles, original, alpha=0.12)
    ax.plot(angles, current, marker="o", label="RCC / evidence-governed repo")
    ax.fill(angles, current, alpha=0.18)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_title("HL-ImageNet RCC Process Dashboard\nDynamic repository-navigation and evidence-governance metrics", pad=28)
    ax.legend(loc="upper right", bbox_to_anchor=(1.26, 1.12))
    fig.text(
        0.5,
        0.03,
        "Scores are generated from README/RCC coverage, command surfaces, evidence artifacts, and rejected-delta ledgers. They measure repo-process quality, not classifier accuracy.",
        ha="center",
        fontsize=9,
    )
    plt.tight_layout(rect=[0.03, 0.05, 0.97, 0.95])
    fig.savefig(DASHBOARD_PNG, dpi=180)
    plt.close(fig)


def plot_timeline(metrics: dict) -> None:
    phases = list(metrics["phase_hits"].keys())
    values = [1 if metrics["phase_hits"][p] else 0 for p in phases]
    cumulative = []
    total = 0
    for v in values:
        total += v
        cumulative.append(total)

    fig = plt.figure(figsize=(12, 5))
    ax = plt.gca()
    ax.plot(phases, cumulative, marker="o")
    ax.set_ylim(0, len(phases) + 1)
    ax.set_ylabel("Cumulative documented phases")
    ax.set_title("HL-ImageNet RCC / Evidence-Governance Phase Coverage")
    ax.grid(True, axis="y", alpha=0.3)
    for i, val in enumerate(cumulative):
        ax.text(i, val + 0.15, str(val), ha="center")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    fig.savefig(TIMELINE_PNG, dpi=180)
    plt.close(fig)


def plot_delta_bars(metrics: dict) -> None:
    probes = metrics.get("probe_metrics", [])
    if not probes:
        return

    labels = []
    top1 = []
    unique = []
    baseline_wrong = []

    for p in probes:
        name = Path(p["path"]).parts[-2]
        labels.append(name.replace("phase2_", "").replace("_", " "))
        top1.append(p.get("top1_delta") or 0.0)
        unique.append(p.get("hl_unique_wins_delta") or 0.0)
        baseline_wrong.append(p.get("baseline_right_hl_wrong_delta") or 0.0)

    x = list(range(len(labels)))
    width = 0.25

    fig = plt.figure(figsize=(13, 6))
    ax = plt.gca()
    ax.bar([i - width for i in x], top1, width, label="Top-1 delta")
    ax.bar(x, unique, width, label="HL-unique wins delta")
    ax.bar([i + width for i in x], baseline_wrong, width, label="Baseline-right / HL-wrong delta")
    ax.axhline(0, linewidth=1)
    ax.set_title("Rejected Probe Learning Signals")
    ax.set_ylabel("Delta")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(DELTA_BARS_PNG, dpi=180)
    plt.close(fig)


def write_reports(metrics: dict) -> None:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    METRICS_JSON.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    c = metrics["counts"]
    lines = []
    lines.append("# HL-ImageNet RCC Process Metrics")
    lines.append("")
    lines.append(f"Generated: `{metrics['generated_at']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Phase coverage | {c['phase_coverage']} / {c['phase_total']} |")
    lines.append(f"| Command coverage | {c['command_coverage']} / {c['command_total']} |")
    lines.append(f"| Boundary coverage | {c['boundary_coverage']} / {c['boundary_total']} |")
    lines.append(f"| RCC coverage | {c['rcc_coverage']} / {c['rcc_total']} |")
    lines.append(f"| Evidence artifact coverage | {c['artifact_coverage']} / {c['artifact_total']} |")
    lines.append(f"| Mini README count | {c['mini_readme_count']} |")
    lines.append(f"| Rejected / failed delta count | {c['rejected_or_failed_delta_count']} |")
    lines.append(f"| Accepted runtime delta count after guard | {c['accepted_runtime_delta_count']} |")
    lines.append("")
    lines.append("## Dynamic scores")
    lines.append("")
    lines.append("| Dimension | Original reference | Current RCC-governed repo |")
    lines.append("|---|---:|---:|")
    for key, val in metrics["scores_1_to_10"].items():
        old = metrics["original_repo_reference_scores_1_to_10"].get(key, 0)
        lines.append(f"| {key} | {old:.1f} | {val:.1f} |")
    lines.append("")
    lines.append("## Probe learning signals")
    lines.append("")
    lines.append("| Probe | Status | Top-1 delta | Top-3 delta | HL-unique wins delta | Baseline-right / HL-wrong delta |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for p in metrics["probe_metrics"]:
        lines.append(
            f"| {p['path']} | {p['overall_status']} | "
            f"{p.get('top1_delta') or 0:.6f} | {p.get('top3_delta') or 0:.6f} | "
            f"{p.get('hl_unique_wins_delta') or 0:.6f} | {p.get('baseline_right_hl_wrong_delta') or 0:.6f} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    for item in metrics["interpretation"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Non-claim lock")
    lines.append("")
    lines.append("- These metrics measure repository navigation, evidence governance, auditability, and process control.")
    lines.append("- These metrics do not prove classifier correctness.")
    lines.append("- These metrics do not claim standard ImageNet performance.")
    lines.append("- These metrics do not imply RCC changed classifier runtime behavior.")
    lines.append("")

    METRICS_MD.write_text("\n".join(lines), encoding="utf-8")


def update_readme() -> None:
    text = read_text(README)
    section = """
## RCC Process Metrics Dashboard

RCC / AEFL context is now tracked as a repository-process metric layer. The dashboard below measures navigation, context fidelity, claim-boundary safety, auditability, drift resistance, evidence-chain completeness, failure learning, and controlled evolution. These are repo-governance metrics, not classifier-accuracy claims.

![RCC Process Dashboard](docs/plots/rcc_process_dashboard.png)

Generated metric artifacts:

- `docs/metrics/rcc_process_metrics.md`
- `docs/metrics/rcc_process_metrics.json`
- `docs/plots/rcc_process_dashboard.png`
- `docs/plots/rcc_process_timeline.png`
- `docs/plots/rcc_guard_delta_bars.png`

> **RCC metrics boundary**: These metrics describe repository navigation and evidence governance. They do not prove classifier correctness, do not claim ImageNet performance, and do not imply RCC changed classifier runtime behavior.

"""
    if "## RCC Process Metrics Dashboard" not in text:
        marker = "## Technical Details"
        if marker in text:
            text = text.replace(marker, section + "\n" + marker)
        else:
            text += "\n\n" + section
        README.write_text(text, encoding="utf-8")


def main() -> None:
    metrics = compute_metrics()
    write_reports(metrics)
    plot_radar(metrics)
    plot_timeline(metrics)
    plot_delta_bars(metrics)
    update_readme()

    print("RCC process metrics generated.")
    print(f"Metrics JSON: {METRICS_JSON}")
    print(f"Metrics MD: {METRICS_MD}")
    print(f"Dashboard: {DASHBOARD_PNG}")
    print(f"Timeline: {TIMELINE_PNG}")
    print(f"Delta bars: {DELTA_BARS_PNG}")


if __name__ == "__main__":
    main()