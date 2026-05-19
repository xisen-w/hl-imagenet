"""Rule-level credit assignment for verify conditions.

Ablates one verify pair-block at a time and measures marginal contribution
on inner_train, inner_dev, and val. This identifies which pair-blocks
generalize vs which are pure memorization.
"""

from __future__ import annotations

import json
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import cv2

from hlinet.classifier.predict import predict, set_verify_whitelist
from hlinet.eval.dataset import PHASE2_CLASSES, load_dataset
from hlinet.eval.splits import load_inner_split

LOGS_ROOT = Path(__file__).parent.parent.parent / "logs" / "generalization"


@dataclass
class RuleScore:
    rule_id: str
    stage: str
    pair: tuple[str, str]
    inner_train_helped: int = 0
    inner_train_hurt: int = 0
    inner_dev_helped: int = 0
    inner_dev_hurt: int = 0
    val_helped: int = 0
    val_hurt: int = 0
    support_train: int = 0
    support_dev: int = 0
    per_class_damage: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    @property
    def train_net(self) -> int:
        return self.inner_train_helped - self.inner_train_hurt

    @property
    def dev_net(self) -> int:
        return self.inner_dev_helped - self.inner_dev_hurt

    @property
    def val_net(self) -> int:
        return self.val_helped - self.val_hurt

    @property
    def transfer_ratio(self) -> float:
        if self.train_net <= 0:
            return 0.0
        return self.dev_net / self.train_net

    @property
    def passes_acceptance(self) -> bool:
        return (
            self.support_dev >= 3
            and self.dev_net > 0
            and all(v >= -2 for v in self.per_class_damage.values())
        )


def extract_verify_pairs() -> list[dict]:
    """Parse predict.py to extract all verify pair blocks with metadata."""
    predict_path = Path(__file__).parent.parent / "classifier" / "predict.py"
    source = predict_path.read_text()

    rules = []

    # _local_verify pairs (frozenset patterns)
    local_verify_start = source.find("def _local_verify(")
    rank3_start = source.find("def _rank3_verify(")
    local_section = source[local_verify_start:rank3_start]

    for m in re.finditer(r'pair == frozenset\(\["(\w+)", "(\w+)"\]\)', local_section):
        rules.append({
            "stage": "local_verify",
            "pair": tuple(sorted([m.group(1), m.group(2)])),
            "rule_id": f"lv_{m.group(1)}_{m.group(2)}",
        })

    # _rank3_verify pairs (key == (X, Y) patterns)
    rank4_start = source.find("def _rank4_verify(")
    rank3_section = source[rank3_start:rank4_start]

    for m in re.finditer(r'key == \("(\w+)", "(\w+)"\)', rank3_section):
        rules.append({
            "stage": "rank3_verify",
            "pair": tuple(sorted([m.group(1), m.group(2)])),
            "rule_id": f"r3_{m.group(1)}_{m.group(2)}",
        })

    # _rank4_verify pairs
    rank5_start = source.find("def _rank5_verify(")
    rank4_section = source[rank4_start:rank5_start]

    for m in re.finditer(r'key == \("(\w+)", "(\w+)"\)', rank4_section):
        rules.append({
            "stage": "rank4_verify",
            "pair": tuple(sorted([m.group(1), m.group(2)])),
            "rule_id": f"r4_{m.group(1)}_{m.group(2)}",
        })

    # _rank5_verify pairs
    rank5_end = source.find("\ndef ", rank5_start + 1)
    if rank5_end == -1:
        rank5_end = len(source)
    rank5_section = source[rank5_start:rank5_end]

    for m in re.finditer(r'key == \("(\w+)", "(\w+)"\)', rank5_section):
        rules.append({
            "stage": "rank5_verify",
            "pair": tuple(sorted([m.group(1), m.group(2)])),
            "rule_id": f"r5_{m.group(1)}_{m.group(2)}",
        })

    # Deduplicate by rule_id (some pairs appear in multiple elif blocks with same ordered key)
    seen = set()
    unique_rules = []
    for r in rules:
        if r["rule_id"] not in seen:
            seen.add(r["rule_id"])
            unique_rules.append(r)

    return unique_rules


def _get_all_verify_classes() -> set[str]:
    """Get all classes that appear in any verify rule."""
    rules = extract_verify_pairs()
    classes = set()
    for r in rules:
        classes.update(r["pair"])
    return classes


def run_rule_credit(verbose: bool = True, include_train: bool = False) -> list[RuleScore]:
    """Ablate each pair-block and measure marginal contribution.

    Method: For each pair-block, run with whitelist = ALL_CLASSES minus
    the pair's classes. Compare against full-verify predictions to measure
    what that pair contributed.
    """
    all_classes = set(PHASE2_CLASSES)
    rules = extract_verify_pairs()

    # Deduplicate by sorted pair (many rule_ids map to same pair across stages)
    pair_to_stages: dict[tuple[str, str], list[str]] = defaultdict(list)
    for r in rules:
        pair_to_stages[r["pair"]].append(r["stage"])

    unique_pairs = sorted(pair_to_stages.keys())

    if verbose:
        print(f"Found {len(rules)} rule blocks across {len(unique_pairs)} unique pairs")
        print(f"Stages: {set(r['stage'] for r in rules)}")
        print()

    splits = {
        "inner_train": load_inner_split("inner_train"),
        "inner_dev": load_inner_split("inner_dev"),
        "val": load_dataset(split="val"),
    }

    # For speed, allow skipping inner_train (large and not the decision criterion)
    if not include_train:
        splits.pop("inner_train", None)

    # Get full-verify and base_rerank predictions to identify verify-affected images
    if verbose:
        print("Computing baseline predictions (full + base_rerank)...")
    set_verify_whitelist(None)
    full_preds: dict[str, dict[str, str]] = {}
    base_preds: dict[str, dict[str, str]] = {}
    affected_images: dict[str, list[tuple[Path, str]]] = {}  # split -> [(path, label)]

    for split_name, samples in splits.items():
        full_preds[split_name] = {}
        base_preds[split_name] = {}
        affected_images[split_name] = []
        for sample in samples:
            image = cv2.imread(str(sample.path))
            if image is None:
                continue
            pred_full = predict(image, mode="full")
            pred_base = predict(image, mode="base_rerank")
            full_preds[split_name][str(sample.path)] = pred_full.label
            base_preds[split_name][str(sample.path)] = pred_base.label
            if pred_full.label != pred_base.label:
                affected_images[split_name].append((sample.path, sample.label))

    total_affected = sum(len(v) for v in affected_images.values())
    if verbose:
        for sn, imgs in affected_images.items():
            print(f"  {sn}: {len(imgs)} verify-affected images")
        print(f"  Total affected: {total_affected}")
        print(f"  Ablation cost: {total_affected} × {len(unique_pairs)} pairs = "
              f"{total_affected * len(unique_pairs)} predictions")
        print()

    # For each unique pair, ablate it — only re-predict affected images
    results: list[RuleScore] = []

    for pair in unique_pairs:
        cls_a, cls_b = pair
        stages = pair_to_stages[pair]

        # Whitelist = everything EXCEPT this pair's classes
        ablation_whitelist = all_classes - {cls_a, cls_b}
        set_verify_whitelist(ablation_whitelist)

        score = RuleScore(
            rule_id=f"{cls_a}_{cls_b}",
            stage="/".join(sorted(set(stages))),
            pair=pair,
        )

        for split_name in splits:
            for img_path, true_label in affected_images[split_name]:
                path_str = str(img_path)
                full_label = full_preds[split_name][path_str]

                image = cv2.imread(path_str)
                if image is None:
                    continue
                ablated_pred = predict(image, mode="full")
                ablated_label = ablated_pred.label

                if full_label != ablated_label:
                    if split_name == "inner_train":
                        score.support_train += 1
                    elif split_name == "inner_dev":
                        score.support_dev += 1

                    full_correct = full_label == true_label
                    ablated_correct = ablated_label == true_label

                    if full_correct and not ablated_correct:
                        if split_name == "inner_train":
                            score.inner_train_helped += 1
                        elif split_name == "inner_dev":
                            score.inner_dev_helped += 1
                        else:
                            score.val_helped += 1
                    elif ablated_correct and not full_correct:
                        if split_name == "inner_train":
                            score.inner_train_hurt += 1
                        elif split_name == "inner_dev":
                            score.inner_dev_hurt += 1
                        else:
                            score.val_hurt += 1
                            score.per_class_damage[true_label] -= 1

        results.append(score)

        if verbose:
            print(f"  {score.rule_id:35s} stages={score.stage:30s} "
                  f"train={score.train_net:+3d} dev={score.dev_net:+3d} "
                  f"val={score.val_net:+3d} support_dev={score.support_dev:2d} "
                  f"{'PASS' if score.passes_acceptance else 'FAIL'}")

    set_verify_whitelist(None)

    if verbose:
        _print_summary(results)

    _save_report(results)
    return results


def _print_summary(results: list[RuleScore]) -> None:
    print("\n" + "=" * 80)
    print("RULE CREDIT ASSIGNMENT SUMMARY")
    print("=" * 80)

    passing = [r for r in results if r.passes_acceptance]
    failing = [r for r in results if not r.passes_acceptance]

    print(f"\nPassing rules ({len(passing)}/{len(results)}):")
    print(f"{'Rule':<35} {'Stage':<20} {'dev_net':>8} {'val_net':>8} {'support':>8} {'transfer':>9}")
    print("-" * 80)
    for r in sorted(passing, key=lambda x: -x.dev_net):
        print(f"{r.rule_id:<35} {r.stage:<20} {r.dev_net:>+7d} {r.val_net:>+7d} "
              f"{r.support_dev:>7d} {r.transfer_ratio:>8.2f}")

    print(f"\nFailing rules ({len(failing)}/{len(results)}):")
    for r in sorted(failing, key=lambda x: x.val_net):
        reason = []
        if r.support_dev < 3:
            reason.append(f"low_support({r.support_dev})")
        if r.dev_net <= 0:
            reason.append(f"dev_negative({r.dev_net})")
        worst_class = min(r.per_class_damage.items(), key=lambda x: x[1]) if r.per_class_damage else ("", 0)
        if worst_class[1] < -2:
            reason.append(f"class_collapse({worst_class[0]}:{worst_class[1]})")
        print(f"  {r.rule_id:<33} val={r.val_net:+3d} dev={r.dev_net:+3d} "
              f"{'|'.join(reason)}")

    print(f"\nTotal passing rules' val contribution: "
          f"{sum(r.val_net for r in passing):+d}")
    print(f"Total failing rules' val contribution: "
          f"{sum(r.val_net for r in failing):+d}")


def _save_report(results: list[RuleScore]) -> None:
    LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = LOGS_ROOT / f"rule_credit_{timestamp}.json"

    data = []
    for r in results:
        data.append({
            "rule_id": r.rule_id,
            "stage": r.stage,
            "pair": list(r.pair),
            "inner_train_helped": r.inner_train_helped,
            "inner_train_hurt": r.inner_train_hurt,
            "inner_dev_helped": r.inner_dev_helped,
            "inner_dev_hurt": r.inner_dev_hurt,
            "val_helped": r.val_helped,
            "val_hurt": r.val_hurt,
            "support_train": r.support_train,
            "support_dev": r.support_dev,
            "train_net": r.train_net,
            "dev_net": r.dev_net,
            "val_net": r.val_net,
            "transfer_ratio": r.transfer_ratio,
            "passes_acceptance": r.passes_acceptance,
            "per_class_damage": dict(r.per_class_damage),
        })

    with open(path, "w") as f:
        json.dump({"timestamp": timestamp, "rules": data}, f, indent=2)
    print(f"\nReport saved: {path}")


if __name__ == "__main__":
    print("Running rule-level credit assignment...")
    print("This ablates each pair-block and measures marginal contribution.\n")
    run_rule_credit()
