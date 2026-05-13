"""Download and prepare Phase 3 data: 128×128 images from ImageNet-1k (256 resized).

Source: evanarlian/imagenet_1k_resized_256 on HuggingFace (publicly accessible)
Target: data/phase3/{train,val,test}/<class_name>/*.JPEG

Split: 200 train, 200 val, 100 test per class (same as Phase 2)
Uses .filter() to skip irrelevant classes before iterating.
"""

import os
import sys
from pathlib import Path

import cv2
import numpy as np
from datasets import load_dataset

TARGET_SIZE = 128

CLASS_INDICES = {
    "banana": 954,
    "brown_bear": 294,
    "golden_retriever": 207,
    "jellyfish": 107,
    "king_penguin": 145,
    "mushroom": 947,
    "orange": 950,
    "school_bus": 779,
    "sports_car": 817,
    "teapot": 849,
}

SPLIT_SIZES = {"train": 200, "val": 200, "test": 100}
TARGET_INDICES = set(CLASS_INDICES.values())


def save_image(img_pil, cls_name, split_name, idx, base_dir):
    img = np.array(img_pil)
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (TARGET_SIZE, TARGET_SIZE), interpolation=cv2.INTER_AREA)
    fname = f"{cls_name}_{idx:04d}.JPEG"
    path = base_dir / split_name / cls_name / fname
    cv2.imwrite(str(path), img)


def main():
    base_dir = Path("data/phase3")

    idx_to_name = {v: k for k, v in CLASS_INDICES.items()}

    for split_name in SPLIT_SIZES:
        for cls_name in CLASS_INDICES:
            (base_dir / split_name / cls_name).mkdir(parents=True, exist_ok=True)

    # Check what's already downloaded
    already = {}
    for split_name in ["train", "val"]:
        for cls_name in CLASS_INDICES:
            count = len(list((base_dir / split_name / cls_name).glob("*.JPEG")))
            already[(split_name, cls_name)] = count

    # Determine what we still need from train split
    need_from_train = {}
    for cls_name in CLASS_INDICES:
        train_have = already.get(("train", cls_name), 0)
        val_have = already.get(("val", cls_name), 0)
        need_train = max(0, 200 - train_have)
        need_val = max(0, 200 - val_have)
        if need_train > 0 or need_val > 0:
            need_from_train[cls_name] = {"train": need_train, "val": need_val,
                                         "train_have": train_have, "val_have": val_have}

    if need_from_train:
        remaining_indices = set(CLASS_INDICES[n] for n in need_from_train)
        print(f"Need from train split: {need_from_train}")
        print(f"Loading train split (streaming, filtered to {len(remaining_indices)} classes)...")

        ds = load_dataset("evanarlian/imagenet_1k_resized_256", split="train", streaming=True)

        counts = {n: dict(d) for n, d in need_from_train.items()}

        for sample in ds:
            label = sample["label"]
            if label not in remaining_indices:
                continue

            cls_name = idx_to_name[label]
            if cls_name not in counts:
                continue

            c = counts[cls_name]
            if c["train"] > 0:
                idx = c["train_have"] + (200 - c["train_have"] - c["train"])
                save_image(sample["image"], cls_name, "train", idx, base_dir)
                c["train"] -= 1
                total_remaining = sum(cc["train"] + cc["val"] for cc in counts.values())
                if total_remaining % 50 == 0:
                    print(f"  {total_remaining} images remaining...")
            elif c["val"] > 0:
                idx = c["val_have"] + (200 - c["val_have"] - c["val"])
                save_image(sample["image"], cls_name, "val", idx, base_dir)
                c["val"] -= 1
                total_remaining = sum(cc["train"] + cc["val"] for cc in counts.values())
                if total_remaining % 50 == 0:
                    print(f"  {total_remaining} images remaining...")
            else:
                continue

            all_done = all(cc["train"] == 0 and cc["val"] == 0 for cc in counts.values())
            if all_done:
                print("  All train/val images collected!")
                break

    # Test split from val
    test_need = {}
    for cls_name in CLASS_INDICES:
        have = len(list((base_dir / "test" / cls_name).glob("*.JPEG")))
        need = max(0, 100 - have)
        if need > 0:
            test_need[cls_name] = {"need": need, "have": have}

    if test_need:
        remaining_indices = set(CLASS_INDICES[n] for n in test_need)
        print(f"\nLoading val split for test images (filtered to {len(remaining_indices)} classes)...")

        ds_val = load_dataset("evanarlian/imagenet_1k_resized_256", split="val", streaming=True)

        for sample in ds_val:
            label = sample["label"]
            if label not in remaining_indices:
                continue

            cls_name = idx_to_name[label]
            if cls_name not in test_need:
                continue

            c = test_need[cls_name]
            if c["need"] > 0:
                idx = c["have"] + (100 - c["have"] - c["need"])
                save_image(sample["image"], cls_name, "test", idx, base_dir)
                c["need"] -= 1
            else:
                continue

            all_done = all(cc["need"] == 0 for cc in test_need.values())
            if all_done:
                print("  All test images collected!")
                break

    # Summary
    print("\nFinal summary:")
    for split_name in ["train", "val", "test"]:
        for cls_name in sorted(CLASS_INDICES):
            count = len(list((base_dir / split_name / cls_name).glob("*.JPEG")))
            target = SPLIT_SIZES[split_name]
            status = "OK" if count >= target else f"MISSING {target - count}"
            print(f"  {split_name}/{cls_name}: {count}/{target} {status}")


if __name__ == "__main__":
    main()
