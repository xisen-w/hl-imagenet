"""Mine zero-risk correction rules for the compiled forest.

For each train error: find feature thresholds that correctly identify it
WITHOUT matching any correctly-classified images with the same prediction.

This is analogous to Phase 2's verify conditions but for the forest."""

import sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from predict import predict, _extract_features, CLASSES
from build_forest import FEATURE_NAMES

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def main():
    # Collect all predictions + features
    print("Computing predictions and features...")
    data = []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = DATA_ROOT / cls
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            feats = _extract_features(img)
            pred = predict(img)
            pred_idx = CLASSES.index(pred)
            data.append({
                'true': cls_idx,
                'pred': pred_idx,
                'feats': feats,
                'correct': pred == cls,
                'path': str(p),
            })

    errors = [d for d in data if not d['correct']]
    correct = [d for d in data if d['correct']]
    print(f"Errors: {len(errors)}, Correct: {len(correct)}")

    # For each confusion pair, find zero-risk corrections
    # A correction rule: (predicted_class, feature_idx, direction, threshold) -> true_class
    # Zero-risk: no correctly-classified image with pred=predicted_class matches the threshold
    rules = []

    pair_groups = defaultdict(list)
    for e in errors:
        pair_groups[(e['pred'], e['true'])].append(e)

    for (pred_cls, true_cls), pair_errors in sorted(pair_groups.items(), key=lambda x: -len(x[1])):
        if len(pair_errors) < 3:
            continue

        # Get "risk pool": correctly classified images that were predicted as pred_cls
        risk_pool = [d for d in correct if d['pred'] == pred_cls]

        print(f"\n{CLASSES[true_cls]:15s} misclassified as {CLASSES[pred_cls]:15s}: {len(pair_errors)} errors, {len(risk_pool)} risk pool")

        # For each feature, find thresholds that separate errors from risk pool
        for f_idx in range(len(FEATURE_NAMES)):
            error_vals = np.array([e['feats'][f_idx] for e in pair_errors])
            risk_vals = np.array([d['feats'][f_idx] for d in risk_pool]) if risk_pool else np.array([])

            if len(risk_vals) == 0:
                # No risk — ANY threshold works
                # Use median of errors as threshold
                thresh = float(np.median(error_vals))
                n_fixed = int(np.sum(error_vals >= thresh))
                if n_fixed >= 2:
                    rules.append({
                        'pred': pred_cls, 'true': true_cls,
                        'feat': f_idx, 'dir': '>=', 'thresh': thresh,
                        'fixes': n_fixed, 'breaks': 0
                    })
                continue

            # Try direction: error_vals > threshold AND risk_vals <= threshold
            risk_max = float(np.max(risk_vals))
            errors_above_risk = error_vals > risk_max
            n_fixable = int(np.sum(errors_above_risk))
            if n_fixable >= 2:
                rules.append({
                    'pred': pred_cls, 'true': true_cls,
                    'feat': f_idx, 'dir': '>', 'thresh': risk_max,
                    'fixes': n_fixable, 'breaks': 0
                })

            # Try direction: error_vals < threshold AND risk_vals >= threshold
            risk_min = float(np.min(risk_vals))
            errors_below_risk = error_vals < risk_min
            n_fixable = int(np.sum(errors_below_risk))
            if n_fixable >= 2:
                rules.append({
                    'pred': pred_cls, 'true': true_cls,
                    'feat': f_idx, 'dir': '<', 'thresh': risk_min,
                    'fixes': n_fixable, 'breaks': 0
                })

    # Sort by fixes (most impactful first)
    rules.sort(key=lambda r: -r['fixes'])
    print(f"\n\nFound {len(rules)} zero-risk rules")
    print("\nTop 30 rules:")
    for r in rules[:30]:
        fname = FEATURE_NAMES[r['feat']] if r['feat'] < len(FEATURE_NAMES) else f"f[{r['feat']}]"
        print(f"  IF pred=={CLASSES[r['pred']]:15s} AND {fname:25s} {r['dir']} {r['thresh']:.4f} -> {CLASSES[r['true']]:15s} (fixes {r['fixes']})")

    # Now check how many of these rules fire on VAL (both helps and hurts)
    print("\n\nEvaluating top rules on val...")
    val_data = []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = VAL_ROOT / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            feats = _extract_features(img)
            pred = predict(img)
            pred_idx = CLASSES.index(pred)
            val_data.append({'true': cls_idx, 'pred': pred_idx, 'feats': feats})

    # Apply top N rules and count net effect
    for n_rules in [5, 10, 20, 30, 50]:
        selected = rules[:n_rules]
        helps = 0
        hurts = 0
        for d in val_data:
            final_pred = d['pred']
            for r in selected:
                if d['pred'] == r['pred']:
                    val = d['feats'][r['feat']]
                    if r['dir'] == '>' and val > r['thresh']:
                        final_pred = r['true']
                        break
                    elif r['dir'] == '<' and val < r['thresh']:
                        final_pred = r['true']
                        break
                    elif r['dir'] == '>=' and val >= r['thresh']:
                        final_pred = r['true']
                        break
            if final_pred == d['true'] and d['pred'] != d['true']:
                helps += 1
            elif final_pred != d['true'] and d['pred'] == d['true']:
                hurts += 1
        baseline = sum(1 for d in val_data if d['pred'] == d['true'])
        new_acc = baseline + helps - hurts
        print(f"  Top {n_rules:2d} rules: helps={helps:3d}, hurts={hurts:3d}, net={helps-hurts:+4d}, val={new_acc/len(val_data):.1%}")


if __name__ == "__main__":
    main()
