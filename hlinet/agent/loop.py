"""The agent loop: error analysis → feature proposal → test → accept/reject."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from hlinet.agent.analyzer import analyze_errors, format_analysis
from hlinet.agent.proposer import build_proposal_prompt, save_generated_feature, SYSTEM_PROMPT
from hlinet.agent.tester import test_feature
from hlinet.eval.dataset import load_dataset, PHASE1_CLASSES
from hlinet.eval.runner import run_evaluation

LOGS_DIR = Path(__file__).parent.parent.parent / "logs"


def run_agent_loop(
    max_iterations: int = 5,
    data_dir: Path | None = None,
    use_llm: bool = True,
    verbose: bool = True,
) -> dict:
    """Run the feature invention agent loop.

    1. Evaluate current system
    2. Analyze errors
    3. Propose new features (via LLM or manual)
    4. Test features
    5. Accept/reject
    6. Repeat
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_path = LOGS_DIR / f"agent_run_{timestamp}.md"

    log_lines = [f"# Agent Run: {timestamp}\n"]
    results_history = []

    for iteration in range(max_iterations):
        if verbose:
            print(f"\n{'='*60}")
            print(f"ITERATION {iteration + 1}/{max_iterations}")
            print(f"{'='*60}")

        # Step 1: Evaluate
        if verbose:
            print("\n[1/4] Evaluating current system...")
        eval_result = run_evaluation(data_dir=data_dir, max_per_class=15, verbose=False)
        results_history.append(eval_result.to_dict())

        log_lines.append(f"\n## Iteration {iteration + 1}")
        log_lines.append(f"- Top-1 accuracy: {eval_result.top1_accuracy:.3f}")
        log_lines.append(f"- Top-3 accuracy: {eval_result.top3_accuracy:.3f}")

        if verbose:
            print(f"  Accuracy: {eval_result.top1_accuracy:.3f} "
                  f"(top-3: {eval_result.top3_accuracy:.3f})")

        # Step 2: Analyze errors
        if verbose:
            print("\n[2/4] Analyzing errors...")
        samples = load_dataset(data_dir=data_dir, max_per_class=15)
        confusions = analyze_errors(samples)

        if not confusions:
            log_lines.append("- No confusions found. System may be perfect or data missing.")
            break

        log_lines.append(f"- Top confusion: {confusions[0].true_class} → {confusions[0].predicted_class} ({confusions[0].count}x)")
        if verbose:
            print(f"  Worst: {confusions[0].true_class} → {confusions[0].predicted_class} ({confusions[0].count}x)")

        # Step 3: Propose feature
        if verbose:
            print("\n[3/4] Proposing new feature...")
        target = confusions[0]
        prompt = build_proposal_prompt(target)

        if use_llm:
            try:
                code = _call_llm(prompt)
            except Exception as e:
                log_lines.append(f"- LLM call failed: {e}")
                if verbose:
                    print(f"  LLM failed: {e}")
                continue
        else:
            log_lines.append("- Manual mode: skipping LLM proposal")
            log_lines.append(f"  Prompt would be:\n```\n{prompt}\n```")
            if verbose:
                print(f"  [Manual mode] Prompt saved to log")
                print(f"  To fix: write a feature that distinguishes {target.true_class} from {target.predicted_class}")
            continue

        # Save proposed feature
        feature_name = f"gen_{target.true_class}_vs_{target.predicted_class}_{iteration}"
        feature_path = save_generated_feature(code, feature_name)
        log_lines.append(f"- Proposed feature: {feature_name}")

        # Step 4: Test feature
        if verbose:
            print("\n[4/4] Testing proposed feature...")
        positive = [s for s in samples if s.label == target.true_class]
        negative = [s for s in samples if s.label == target.predicted_class]

        report = test_feature(feature_path, positive, negative)
        log_lines.append(f"- Quality: gain={report.information_gain:.3f}, "
                        f"robust={report.robustness:.3f}, "
                        f"latency={report.mean_latency_ms:.0f}ms")
        log_lines.append(f"- Accepted: {report.passes}")

        if verbose:
            status = "ACCEPTED" if report.passes else "REJECTED"
            print(f"  {status}: gain={report.information_gain:.3f}, "
                  f"fires_pos={report.fires_positive:.2f}, fires_neg={report.fires_negative:.2f}")

        if not report.passes and report.errors:
            log_lines.append(f"- Errors: {report.errors}")
            # Remove failed feature
            feature_path.unlink(missing_ok=True)

    # Save log
    log_path.write_text("\n".join(log_lines))
    if verbose:
        print(f"\nAgent log saved to: {log_path}")

    return {
        "iterations": len(results_history),
        "history": results_history,
        "log_path": str(log_path),
    }


def _call_llm(prompt: str) -> str:
    """Call the LLM to generate feature code. Requires anthropic package."""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("Install 'anthropic' package: pip install anthropic")

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def main():
    """CLI entry point for the agent loop."""
    import argparse
    parser = argparse.ArgumentParser(description="Run the HL-Image-Net feature invention agent")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--data-dir", type=Path, default=None)
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM calls (manual mode)")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    run_agent_loop(
        max_iterations=args.iterations,
        data_dir=args.data_dir,
        use_llm=not args.no_llm,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
