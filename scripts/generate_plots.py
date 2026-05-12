#!/usr/bin/env python3
"""Generate publication-quality plots for the HL-ImageNet experiment."""

import json
import os
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.ticker import MultipleLocator

plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'font.family': 'sans-serif',
})

LOGS_DIR = Path(__file__).parent.parent / "logs"
PLOTS_DIR = Path(__file__).parent.parent / "docs" / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def load_all_evals():
    """Load all JSON eval logs, sorted chronologically."""
    results = []
    for f in sorted(LOGS_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            ts_str = f.stem.replace("eval_phase1_", "").replace("eval_baseline_", "").replace("eval_iter1_", "").replace("eval_iter2_", "").replace("eval_iter3_", "").replace("eval_iter4_", "").replace("eval_iter5_", "").replace("eval_iter6_", "")
            data["filename"] = f.name
            data["timestamp"] = f.stat().st_mtime
            results.append(data)
        except (json.JSONDecodeError, KeyError):
            continue
    results.sort(key=lambda x: x["timestamp"])
    return results


def plot_accuracy_trajectory(evals):
    """Plot 1: Main accuracy trajectory with annotated phase transitions."""
    fig, ax = plt.subplots(figsize=(14, 7))

    accuracies = [e["top1_accuracy"] * 100 for e in evals]
    iterations = list(range(1, len(accuracies) + 1))

    # Running max (envelope)
    running_max = []
    cur_max = 0
    for a in accuracies:
        cur_max = max(cur_max, a)
        running_max.append(cur_max)

    # Plot raw trajectory
    ax.plot(iterations, accuracies, color='#4A90D9', alpha=0.4, linewidth=0.8, label='Each eval run')
    ax.plot(iterations, running_max, color='#D94A4A', linewidth=2.2, label='Running best')

    # Phase transitions (annotated)
    phases = [
        (1, 12.7, "Baseline\n(random gates)"),
        (7, 24.5, "Color-first\nstrategy"),
        (28, 34.5, "Hierarchy +\nflat scorer"),
        (62, 43.5, "Compound features\n+ tiebreakers"),
        (92, 50.4, "50% barrier\nbroken"),
        (110, 63.9, "6 classes solved\n(eagle/banana)"),
        (135, 67.8, "Plateau\n(DCT fails)"),
        (155, 74.8, "Banana cap +\ncompound conds"),
        (170, 79.1, "Gradient/green\nconjunctions"),
        (190, 86.1, "Final: alt required\n+ guard tightening"),
    ]

    for idx, (iter_pos, acc, label) in enumerate(phases):
        iter_pos = min(iter_pos, len(iterations))
        ax.axvline(x=iter_pos, color='gray', alpha=0.3, linestyle='--', linewidth=0.7)
        y_offset = 5 if idx % 2 == 0 else -8
        ax.annotate(label, xy=(iter_pos, acc), xytext=(iter_pos + 2, acc + y_offset),
                    fontsize=7.5, ha='left', va='bottom',
                    arrowprops=dict(arrowstyle='->', color='#555', lw=0.8),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8, edgecolor='#ccc'))

    # Plateau zones
    ax.axhspan(42, 45, alpha=0.08, color='orange', label='Session 3 plateau (~43%)')
    ax.axhspan(66, 69, alpha=0.08, color='red', label='Session 7 plateau (~68%)')
    ax.axhspan(84, 87, alpha=0.08, color='purple', label='Final ceiling (~86%)')

    ax.set_xlabel("Evaluation Iteration (chronological)")
    ax.set_ylabel("Top-1 Accuracy (%)")
    ax.set_title("HL-ImageNet: Accuracy Trajectory Over 200+ Iterations\n12.7% → 86.1% through pure Heuristic Learning")
    ax.set_ylim(5, 95)
    ax.set_xlim(0, len(iterations) + 5)
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.legend(loc='lower right', framealpha=0.9)

    # 10% random baseline
    ax.axhline(y=10, color='black', linestyle=':', alpha=0.5, linewidth=1)
    ax.text(len(iterations) - 5, 11, "Random (10%)", fontsize=8, alpha=0.6)

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "01_accuracy_trajectory.png")
    plt.close()
    print(f"  Saved: 01_accuracy_trajectory.png")


def plot_per_class_evolution(evals):
    """Plot 2: Per-class accuracy evolution at key milestones."""
    milestones = {
        "Baseline": None,
        "Session 2": None,
        "Session 3": None,
        "Session 4": None,
        "Session 5": None,
        "Session 6": None,
        "Session 8": None,
        "Session 10": None,
        "Final": None,
    }

    # Map milestones to approximate accuracy levels
    targets = [12.7, 34.5, 43.5, 50.4, 63.9, 67.8, 74.8, 79.1, 86.1]
    milestone_data = []

    for target in targets:
        best_match = None
        for e in evals:
            acc = e["top1_accuracy"] * 100
            if best_match is None or abs(acc - target) < abs(best_match["top1_accuracy"] * 100 - target):
                best_match = e
        milestone_data.append(best_match)

    classes = ['golden_retriever', 'mushroom', 'teapot', 'school_bus', 'banana', 'bicycle', 'eagle', 'laptop', 'piano', 'zebra']
    class_labels = ['Dog', 'Mushroom', 'Teapot', 'Bus', 'Banana', 'Bicycle', 'Eagle', 'Laptop', 'Piano', 'Zebra']
    milestone_labels = ['12.7%\n(Base)', '34.5%\n(S2)', '43.5%\n(S3)', '50.4%\n(S4)', '63.9%\n(S5-6)', '67.8%\n(S7)', '74.8%\n(S8)', '79.1%\n(S9)', '86.1%\n(Final)']

    fig, ax = plt.subplots(figsize=(14, 7))

    colors = plt.cm.tab10(np.linspace(0, 1, 10))
    x = np.arange(len(milestone_labels))
    bar_width = 0.085

    for i, (cls, label) in enumerate(zip(classes, class_labels)):
        values = []
        for md in milestone_data:
            pc = md.get("per_class_accuracy", {})
            values.append(pc.get(cls, 0) * 100)
        offset = (i - 4.5) * bar_width
        bars = ax.bar(x + offset, values, bar_width, label=label, color=colors[i], alpha=0.85, edgecolor='white', linewidth=0.3)

    ax.set_xlabel("System State (overall accuracy)")
    ax.set_ylabel("Per-Class Accuracy (%)")
    ax.set_title("Per-Class Accuracy Evolution Across Development Milestones")
    ax.set_xticks(x)
    ax.set_xticklabels(milestone_labels)
    ax.set_ylim(0, 110)
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.legend(loc='upper left', ncol=5, framealpha=0.9)
    ax.grid(True, axis='y', alpha=0.3, linewidth=0.5)

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "02_per_class_evolution.png")
    plt.close()
    print(f"  Saved: 02_per_class_evolution.png")


def plot_plateau_analysis(evals):
    """Plot 3: Plateau analysis showing diminishing returns and phase boundaries."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    accuracies = [e["top1_accuracy"] * 100 for e in evals]

    # Left: Marginal gain per iteration (smoothed)
    gains = [accuracies[i] - accuracies[i-1] for i in range(1, len(accuracies))]
    window = 10
    smoothed_gains = np.convolve(gains, np.ones(window)/window, mode='valid')

    ax1.bar(range(len(gains)), gains, color='#4A90D9', alpha=0.3, width=1.0, label='Raw gain per iteration')
    ax1.plot(range(window//2, window//2 + len(smoothed_gains)), smoothed_gains,
             color='#D94A4A', linewidth=2, label=f'Smoothed ({window}-iter moving avg)')
    ax1.axhline(y=0, color='black', linewidth=0.5)
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Accuracy Gain (%)")
    ax1.set_title("Marginal Gain Per Iteration")
    ax1.legend(loc='upper right')
    ax1.set_ylim(-10, 10)
    ax1.grid(True, alpha=0.3)

    # Annotate plateau zones
    ax1.axvspan(55, 70, alpha=0.1, color='orange', label='Plateau 1')
    ax1.axvspan(125, 145, alpha=0.1, color='red', label='Plateau 2')
    ax1.axvspan(180, 200, alpha=0.1, color='purple', label='Final ceiling')

    # Right: Cumulative accuracy vs log(iterations) — showing diminishing returns
    running_max = []
    cur_max = 0
    for a in accuracies:
        cur_max = max(cur_max, a)
        running_max.append(cur_max)

    ax2.plot(range(1, len(running_max)+1), running_max, color='#D94A4A', linewidth=2)
    ax2.set_xlabel("Iterations (log scale)")
    ax2.set_ylabel("Best Accuracy Achieved (%)")
    ax2.set_title("Diminishing Returns: Accuracy vs Effort")
    ax2.set_xscale('log')
    ax2.set_ylim(10, 90)
    ax2.grid(True, alpha=0.3)

    # Annotate effort per 10% gain
    milestones_effort = [
        (20, "10→20%: 1 iter"),
        (30, "20→30%: 19 iters"),
        (40, "30→40%: 27 iters"),
        (50, "40→50%: 45 iters"),
        (60, "50→60%: 40 iters"),
        (70, "60→70%: 44 iters"),
        (80, "70→80%: 36 iters"),
        (86, "80→86%: 34 iters"),
    ]

    for acc, label in milestones_effort:
        ax2.axhline(y=acc, color='gray', alpha=0.2, linestyle='--', linewidth=0.5)
        ax2.text(195, acc + 0.5, label, fontsize=7.5, va='bottom', ha='right', alpha=0.7)

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "03_plateau_analysis.png")
    plt.close()
    print(f"  Saved: 03_plateau_analysis.png")


def plot_confusion_heatmap(evals):
    """Plot 4: Final confusion matrix heatmap."""
    final = evals[-1]
    classes = ['golden_retriever', 'mushroom', 'teapot', 'school_bus', 'banana', 'bicycle', 'eagle', 'laptop', 'piano', 'zebra']
    class_labels = ['Dog', 'Mushroom', 'Teapot', 'Bus', 'Banana', 'Bicycle', 'Eagle', 'Laptop', 'Piano', 'Zebra']

    n = len(classes)
    matrix = np.zeros((n, n))

    confusion = final.get("confusion_matrix", {})
    for key, count in confusion.items():
        parts = key.split("->")
        if len(parts) == 2:
            true_cls, pred_cls = parts
            if true_cls in classes and pred_cls in classes:
                i = classes.index(true_cls)
                j = classes.index(pred_cls)
                matrix[i, j] = count

    # Normalize by row (true class)
    row_sums = matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    matrix_norm = matrix / row_sums * 100

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(matrix_norm, cmap='YlOrRd', vmin=0, vmax=100, aspect='auto')

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(class_labels, rotation=45, ha='right')
    ax.set_yticklabels(class_labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title("Final Confusion Matrix (% of true class)\n86.1% overall accuracy")

    # Add text annotations
    for i in range(n):
        for j in range(n):
            val = matrix_norm[i, j]
            if val > 0.5:
                color = 'white' if val > 50 else 'black'
                ax.text(j, i, f'{val:.0f}', ha='center', va='center', fontsize=9, color=color, fontweight='bold' if i == j else 'normal')

    plt.colorbar(im, ax=ax, shrink=0.8, label='% of predictions')
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "04_confusion_matrix.png")
    plt.close()
    print(f"  Saved: 04_confusion_matrix.png")


def plot_session_timeline(evals):
    """Plot 5: Session timeline showing wall-clock progression."""
    fig, ax = plt.subplots(figsize=(14, 5))

    timestamps = [e["timestamp"] for e in evals]
    accuracies = [e["top1_accuracy"] * 100 for e in evals]

    # Convert to hours from start
    t0 = timestamps[0]
    hours = [(t - t0) / 3600 for t in timestamps]

    ax.scatter(hours, accuracies, c=accuracies, cmap='RdYlGn', s=20, alpha=0.7, edgecolors='none')
    ax.plot(hours, accuracies, color='#4A90D9', alpha=0.3, linewidth=0.8)

    # Session boundaries (approximate, from timestamps)
    session_breaks = [
        (0, "S1: Build\nbaseline"),
        (0.5, "S2: Hierarchy"),
        (1.3, "S3: Features"),
        (9.2, "S4: Tiebreakers"),
        (10.5, "S5: Spatial"),
        (11.5, "S6: Eagle/Banana"),
        (11.8, "S7: DCT plateau"),
        (16.5, "S8: Banana cap"),
        (18.0, "S9: Grad/green"),
        (19.0, "S10-11: Guards"),
    ]

    for h, label in session_breaks:
        ax.axvline(x=h, color='gray', alpha=0.4, linestyle='--', linewidth=0.7)
        ax.text(h + 0.1, 90, label, fontsize=7, rotation=0, va='top', ha='left',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='#ddd'))

    ax.set_xlabel("Wall-clock Time (hours from start)")
    ax.set_ylabel("Top-1 Accuracy (%)")
    ax.set_title("Development Timeline: ~20 Hours from 12.7% to 86.1%")
    ax.set_ylim(5, 95)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "05_session_timeline.png")
    plt.close()
    print(f"  Saved: 05_session_timeline.png")


def plot_hard_class_focus():
    """Plot 6: Focus on the 4 hard classes progression."""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Data extracted from milestones
    sessions = ['Base', 'S2', 'S3', 'S4', 'S5-6', 'S7', 'S8', 'S9', 'Final']
    dog =       [0,  80, 70, 72, 68, 68, 70, 72, 82]
    mushroom =  [15, 20, 18, 26, 44, 52, 70, 76, 88]
    teapot =    [10, 30, 26, 30, 50, 60, 64, 74, 82]
    bus =       [0,  0,  56, 74, 72, 72, 80, 82, 84]

    x = np.arange(len(sessions))

    ax.plot(x, dog, 'o-', color='#E8A838', linewidth=2.5, markersize=8, label='Golden Retriever')
    ax.plot(x, mushroom, 's-', color='#8B4513', linewidth=2.5, markersize=8, label='Mushroom')
    ax.plot(x, teapot, '^-', color='#4A90D9', linewidth=2.5, markersize=8, label='Teapot')
    ax.plot(x, bus, 'D-', color='#FFD700', linewidth=2.5, markersize=8, label='School Bus')

    # The "triangle of confusion" region
    ax.axhspan(60, 90, alpha=0.05, color='green')
    ax.text(7.5, 63, "Convergence zone", fontsize=8, alpha=0.5, ha='center')

    ax.set_xticks(x)
    ax.set_xticklabels(sessions)
    ax.set_xlabel("Development Session")
    ax.set_ylabel("Per-Class Accuracy (%)")
    ax.set_title("The Hard Classes: Dog/Mushroom/Teapot/Bus Progression\n(All share warm colors and organic textures at 64x64)")
    ax.set_ylim(-5, 105)
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.legend(loc='lower right', framealpha=0.9)
    ax.grid(True, alpha=0.3)

    # Key insight annotations
    ax.annotate("Bus solved by\nwindow pattern", xy=(3, 74), xytext=(3.5, 50),
                fontsize=8, arrowprops=dict(arrowstyle='->', color='#555'),
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    ax.annotate("Mushroom breakthrough:\ngrad+green conjunctions", xy=(7, 76), xytext=(5.5, 40),
                fontsize=8, arrowprops=dict(arrowstyle='->', color='#555'),
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "06_hard_classes.png")
    plt.close()
    print(f"  Saved: 06_hard_classes.png")


def plot_feature_growth(evals):
    """Plot 7: Feature library growth vs accuracy."""
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Count features at various milestones (from the feature_reuse dict)
    feature_counts = []
    accs = []
    for e in evals:
        fr = e.get("feature_reuse", {})
        if fr:
            feature_counts.append(len(fr))
            accs.append(e["top1_accuracy"] * 100)

    if not feature_counts:
        plt.close()
        return

    ax1.scatter(range(len(accs)), accs, c='#D94A4A', s=15, alpha=0.6, label='Accuracy')
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Top-1 Accuracy (%)", color='#D94A4A')
    ax1.tick_params(axis='y', labelcolor='#D94A4A')

    ax2 = ax1.twinx()
    ax2.scatter(range(len(feature_counts)), feature_counts, c='#4A90D9', s=15, alpha=0.6, label='Feature count')
    ax2.set_ylabel("Number of Registered Features", color='#4A90D9')
    ax2.tick_params(axis='y', labelcolor='#4A90D9')

    ax1.set_title("Feature Library Growth vs Accuracy\n(More features enable higher accuracy, but with diminishing returns)")
    ax1.grid(True, alpha=0.2)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right')

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "07_feature_growth.png")
    plt.close()
    print(f"  Saved: 07_feature_growth.png")


def plot_summary_infographic():
    """Plot 8: Summary infographic with key stats."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Panel 1: Final accuracy donut
    ax = axes[0, 0]
    correct = 86.1
    wrong = 13.9
    wedges, texts = ax.pie([correct, wrong], colors=['#4CAF50', '#FF5252'],
                           startangle=90, wedgeprops=dict(width=0.4))
    ax.text(0, 0, f'{correct:.1f}%', ha='center', va='center', fontsize=24, fontweight='bold')
    ax.set_title("Final Top-1 Accuracy")

    # Panel 2: Iterations count
    ax = axes[0, 1]
    ax.text(0.5, 0.5, "248", ha='center', va='center', fontsize=48, fontweight='bold', color='#4A90D9',
            transform=ax.transAxes)
    ax.text(0.5, 0.25, "evaluation iterations", ha='center', va='center', fontsize=14,
            transform=ax.transAxes, color='#666')
    ax.text(0.5, 0.15, "in ~20 hours", ha='center', va='center', fontsize=12,
            transform=ax.transAxes, color='#999')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title("Total Iterations")

    # Panel 3: System complexity
    ax = axes[0, 2]
    metrics = ['Lines of Code', 'Features', 'Tiebreakers', 'Thresholds', 'Classes Solved']
    values = [5000, 40, 22, 50, 10]
    bars = ax.barh(metrics, values, color=['#4A90D9', '#4CAF50', '#FF9800', '#9C27B0', '#F44336'])
    ax.set_xlabel("Count")
    ax.set_title("System Complexity")
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2, str(val),
                va='center', fontsize=10, fontweight='bold')

    # Panel 4: Accuracy gains per phase type
    ax = axes[1, 0]
    phase_types = ['Architecture\n(scorer, hierarchy)', 'New Features\n(sensors, detectors)',
                   'Tiebreakers\n(pairwise logic)', 'Guard Tightening\n(thresholds, caps)']
    gains = [22, 20, 25, 19]
    colors_phase = ['#4A90D9', '#4CAF50', '#FF9800', '#9C27B0']
    wedges, texts, autotexts = ax.pie(gains, labels=phase_types, colors=colors_phase,
                                       autopct='%1.0f%%', startangle=90)
    ax.set_title("Accuracy Gains by Strategy Type")

    # Panel 5: Error budget breakdown
    ax = axes[1, 1]
    error_cats = ['Dog→Other', 'Other→Dog', 'Mush/Tea\nconfusion', 'Bus errors', 'Other']
    error_counts = [9, 12, 3, 8, 0]
    ax.bar(error_cats, error_counts, color='#FF5252', alpha=0.8)
    ax.set_ylabel("Remaining Errors (out of 230)")
    ax.set_title(f"Error Budget: {sum(error_counts)} errors remain")
    ax.set_ylim(0, 15)

    # Panel 6: Key insight text
    ax = axes[1, 2]
    ax.text(0.5, 0.7, "Representation\nSaturation", ha='center', va='center',
            fontsize=20, fontweight='bold', color='#D94A4A', transform=ax.transAxes)
    ax.text(0.5, 0.35, "At 64x64, dog/mushroom/teapot\nare indistinguishable warm blobs.\nNo pixel-level feature can\nseparate them further.",
            ha='center', va='center', fontsize=11, color='#555', transform=ax.transAxes,
            style='italic')
    ax.text(0.5, 0.1, "Next: 128x128 resolution", ha='center', va='center',
            fontsize=10, color='#999', transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title("The Final Ceiling")

    fig.suptitle("HL-ImageNet Experiment Summary", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(PLOTS_DIR / "08_summary_infographic.png")
    plt.close()
    print(f"  Saved: 08_summary_infographic.png")


if __name__ == "__main__":
    print("Loading evaluation logs...")
    evals = load_all_evals()
    print(f"  Found {len(evals)} evaluation runs")

    print("\nGenerating plots...")
    plot_accuracy_trajectory(evals)
    plot_per_class_evolution(evals)
    plot_plateau_analysis(evals)
    plot_confusion_heatmap(evals)
    plot_session_timeline(evals)
    plot_hard_class_focus()
    plot_feature_growth(evals)
    plot_summary_infographic()

    print(f"\nAll plots saved to: {PLOTS_DIR}")
    print("Files:")
    for f in sorted(PLOTS_DIR.glob("*.png")):
        print(f"  {f.name}")
