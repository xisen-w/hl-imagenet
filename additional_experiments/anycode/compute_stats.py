"""Compute per-class feature statistics from training data.
Outputs means/stds in a format ready to paste into predict.py."""

import sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from predict import _extract_features, CLASSES

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"


def main():
    features_by_class = defaultdict(list)

    for cls in CLASSES:
        cls_dir = DATA_ROOT / cls
        if not cls_dir.exists():
            print(f"MISSING: {cls_dir}")
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            feats = _extract_features(img)
            features_by_class[cls].append(feats)

    print(f"# {len(features_by_class[CLASSES[0]][0])} features total\n")

    print("CLASS_MEANS = {")
    for cls in CLASSES:
        arr = np.array(features_by_class[cls])
        means = np.mean(arr, axis=0)
        vals = ", ".join(f"{v:.4f}" if abs(v) < 100 else f"{v:.1f}" for v in means)
        print(f'    "{cls}": [{vals}],')
    print("}\n")

    print("CLASS_STDS = {")
    for cls in CLASSES:
        arr = np.array(features_by_class[cls])
        stds = np.std(arr, axis=0)
        vals = ", ".join(f"{v:.4f}" if abs(v) < 100 else f"{v:.1f}" for v in stds)
        print(f'    "{cls}": [{vals}],')
    print("}\n")

    # Also print std floors (per-feature minimum std across all classes)
    all_stds = []
    for cls in CLASSES:
        arr = np.array(features_by_class[cls])
        all_stds.append(np.std(arr, axis=0))
    all_stds = np.array(all_stds)
    min_stds = np.min(all_stds, axis=0)
    print("STD_FLOOR = [")
    for i in range(0, len(min_stds), 10):
        chunk = min_stds[i:i+10]
        vals = ", ".join(f"{v:.4f}" if abs(v) < 100 else f"{v:.1f}" for v in chunk)
        print(f"    {vals},")
    print("]\n")

    # Print feature discriminability (F-ratio: between-class var / within-class var)
    print("# Feature discriminability (F-ratio):")
    all_means = np.array([np.mean(np.array(features_by_class[cls]), axis=0) for cls in CLASSES])
    grand_mean = np.mean(all_means, axis=0)
    between_var = np.mean((all_means - grand_mean)**2, axis=0)
    within_var = np.mean([np.mean(np.var(np.array(features_by_class[cls]), axis=0)) for cls in CLASSES])
    for i in range(len(grand_mean)):
        wv = np.mean([np.var(np.array(features_by_class[cls])[:, i]) for cls in CLASSES])
        f_ratio = between_var[i] / max(wv, 1e-10)
        print(f"#   {i:2d}: F={f_ratio:.3f}")


if __name__ == "__main__":
    main()
