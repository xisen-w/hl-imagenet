#!/usr/bin/env python3
"""Download ImageNet subset using open sources.

Uses imagenette (a subset of 10 ImageNet classes) or fetches from open URLs.
"""

import sys
import tarfile
import urllib.request
import shutil
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "imagenet_10"

# Imagenette is a freely available subset of ImageNet with 10 easily classified classes
# We'll map the imagenette classes to our target names where they overlap
IMAGENETTE_URL = "https://s3.amazonaws.com/fast-ai-imageclas/imagenette2-160.tgz"
IMAGENETTE_DIR = Path(__file__).parent.parent / "data" / "_imagenette"

# Imagenette WNID -> our class name mapping
# imagenette classes: tench, English springer, cassette player, chain saw, church,
#                     French horn, garbage truck, gas pump, golf ball, parachute
# Only some overlap with our targets, so we also use imagewoof for dogs

# Actually let's use imagewang which has more variety, or just download both
# imagenette + imagewoof

# Better approach: use Caltech-256 or just web-scrape openly licensed images
# Simplest: use the tiny-imagenet dataset which has 200 classes including several of ours

TINY_IMAGENET_URL = "http://cs231n.stanford.edu/tiny-imagenet-200.zip"

# Tiny ImageNet WNID mapping for our classes
TINY_IMAGENET_WNIDS = {
    "goldfish": "n01443537",        # not in our set but useful for testing
    "banana": "n07753275",
    "school_bus": "n04146614",
    "teapot": "n04398044",
    "laptop": "n03642806",          # not in tiny-imagenet directly
}

# Let's just use a direct approach: download from URLs known to work
# We'll use the Stanford Dogs + other open datasets

def download_tiny_imagenet():
    """Download tiny-imagenet-200 which has some of our classes."""
    import zipfile

    zip_path = Path(__file__).parent.parent / "data" / "tiny-imagenet-200.zip"
    extract_dir = Path(__file__).parent.parent / "data" / "_tiny_imagenet"

    if extract_dir.exists() and (extract_dir / "tiny-imagenet-200").exists():
        print("Tiny ImageNet already downloaded")
    else:
        print(f"Downloading Tiny ImageNet (~237MB)...")
        extract_dir.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(TINY_IMAGENET_URL, zip_path)
        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)
        zip_path.unlink()
        print("Done")

    # Map tiny-imagenet classes to our classes
    # Tiny ImageNet WNIDs that match our classes:
    tiny_root = extract_dir / "tiny-imagenet-200"
    wnid_map = {
        "n02391049": "zebra",
        "n04146614": "school_bus",
        "n02099601": "golden_retriever",
        "n07734744": "mushroom",
        "n04398044": "teapot",
        "n07753275": "banana",
        "n02033041": "eagle",        # bald eagle (may not be in tiny)
        "n03642806": "laptop",       # may not be in tiny
        "n02835271": "bicycle",      # may not be in tiny
        "n03928116": "piano",        # may not be in tiny (grand piano)
    }

    # Check which classes are available
    train_dir = tiny_root / "train"
    available = {}
    if train_dir.exists():
        for wnid, class_name in wnid_map.items():
            wnid_dir = train_dir / wnid / "images"
            if wnid_dir.exists():
                images = list(wnid_dir.glob("*.JPEG"))
                if images:
                    available[class_name] = images
                    print(f"  Found {class_name}: {len(images)} images")

    # Also check val
    val_dir = tiny_root / "val"
    if val_dir.exists():
        # Tiny ImageNet val has annotations
        val_annotations = val_dir / "val_annotations.txt"
        if val_annotations.exists():
            val_map = {}
            with open(val_annotations) as f:
                for line in f:
                    parts = line.strip().split("\t")
                    fname, wnid = parts[0], parts[1]
                    if wnid in wnid_map:
                        class_name = wnid_map[wnid]
                        val_map.setdefault(class_name, []).append(val_dir / "images" / fname)
            for class_name, paths in val_map.items():
                if class_name in available:
                    available[class_name].extend(paths)
                else:
                    available[class_name] = paths

    # Copy to our data dir
    for class_name, image_paths in available.items():
        class_dir = DATA_DIR / class_name
        class_dir.mkdir(parents=True, exist_ok=True)
        existing = len(list(class_dir.glob("*.*")))
        if existing >= 50:
            continue
        for i, src in enumerate(image_paths[:50]):
            if src.exists():
                dst = class_dir / f"{class_name}_{i:04d}.JPEG"
                shutil.copy2(src, dst)
        count = len(list(class_dir.glob("*.*")))
        print(f"  Copied {class_name}: {count} images")

    return available


def download_imagenette_for_missing():
    """Use imagenette2 for classes we're still missing - it has 10 easy classes."""
    # imagenette doesn't have our exact classes, but let's check overlap
    # Actually imagenette has: tench, springer, cassette, chainsaw, church,
    # french horn, garbage truck, gas pump, golf ball, parachute
    # None of these are our target classes.
    #
    # Let's just create synthetic placeholder images for missing classes
    # so we can test the pipeline, then replace with real data later.
    pass


def create_synthetic_fallback():
    """For any class still missing, create synthetic test images so eval can run."""
    import numpy as np
    try:
        import cv2
    except ImportError:
        print("OpenCV not available for synthetic generation")
        return

    synthetic_recipes = {
        "zebra": lambda: _stripes_image(224, 224),
        "school_bus": lambda: _colored_rect_image(224, 224, (0, 200, 255)),  # yellow
        "golden_retriever": lambda: _noisy_colored_image(224, 224, (50, 160, 200)),
        "bicycle": lambda: _circles_image(224, 224),
        "mushroom": lambda: _organic_image(224, 224, (100, 130, 180)),
        "teapot": lambda: _blob_with_protrusion(224, 224),
        "piano": lambda: _keyboard_image(224, 224),
        "eagle": lambda: _symmetric_shape(224, 224),
        "laptop": lambda: _screen_rect_image(224, 224),
        "banana": lambda: _curved_yellow(224, 224),
    }

    for class_name, generator in synthetic_recipes.items():
        class_dir = DATA_DIR / class_name
        class_dir.mkdir(parents=True, exist_ok=True)
        existing = len(list(class_dir.glob("*.*")))
        if existing >= 10:
            continue
        # Only create a few synthetic as fallback
        for i in range(5):
            img = generator()
            # Add random noise for variety
            noise = np.random.randint(-20, 20, img.shape, dtype=np.int16)
            img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            dst = class_dir / f"{class_name}_synth_{i:04d}.JPEG"
            cv2.imwrite(str(dst), img)
        print(f"  Created 5 synthetic {class_name} images (fallback)")


def _stripes_image(h, w):
    import numpy as np
    img = np.zeros((h, w, 3), dtype=np.uint8)
    stripe_w = np.random.randint(10, 25)
    for i in range(0, w, stripe_w * 2):
        img[:, i:i+stripe_w] = 255
    return img

def _colored_rect_image(h, w, color):
    import numpy as np
    img = np.zeros((h, w, 3), dtype=np.uint8) + 128
    margin = 30
    img[margin:h-margin, margin:w-margin] = color
    return img

def _noisy_colored_image(h, w, color):
    import numpy as np
    img = np.full((h, w, 3), color, dtype=np.uint8)
    noise = np.random.randint(0, 40, (h, w, 3), dtype=np.uint8)
    return np.clip(img.astype(int) + noise, 0, 255).astype(np.uint8)

def _circles_image(h, w):
    import numpy as np, cv2
    img = np.ones((h, w, 3), dtype=np.uint8) * 200
    cv2.circle(img, (w//3, 2*h//3), h//5, (0,0,0), 3)
    cv2.circle(img, (2*w//3, 2*h//3), h//5, (0,0,0), 3)
    cv2.line(img, (w//3, 2*h//3), (w//2, h//3), (0,0,0), 2)
    cv2.line(img, (2*w//3, 2*h//3), (w//2, h//3), (0,0,0), 2)
    return img

def _organic_image(h, w, color):
    import numpy as np, cv2
    img = np.full((h, w, 3), 60, dtype=np.uint8)
    cv2.ellipse(img, (w//2, h//2), (w//4, h//3), 0, 0, 360, color, -1)
    return img

def _blob_with_protrusion(h, w):
    import numpy as np, cv2
    img = np.ones((h, w, 3), dtype=np.uint8) * 220
    cv2.ellipse(img, (w//2, h//2), (w//4, h//4), 0, 0, 360, (140,140,180), -1)
    cv2.line(img, (3*w//4, h//2), (w-20, h//2-20), (140,140,180), 8)
    cv2.ellipse(img, (w//4, h//2), (15, 25), 0, 90, 270, (140,140,180), 5)
    return img

def _keyboard_image(h, w):
    import numpy as np, cv2
    img = np.ones((h, w, 3), dtype=np.uint8) * 40
    key_w = w // 14
    for i in range(14):
        x = i * key_w + 5
        cv2.rectangle(img, (x, h//3), (x+key_w-3, 2*h//3), (240,240,240), -1)
    # black keys
    for i in [1, 2, 4, 5, 6, 8, 9, 11, 12]:
        x = i * key_w + key_w//3
        cv2.rectangle(img, (x, h//3), (x+key_w//2, h//2+10), (20,20,20), -1)
    return img

def _symmetric_shape(h, w):
    import numpy as np, cv2
    img = np.ones((h, w, 3), dtype=np.uint8) * 180
    pts = np.array([[w//2, h//4], [w//5, 3*h//4], [4*w//5, 3*h//4]], np.int32)
    cv2.fillPoly(img, [pts], (80, 60, 40))
    return img

def _screen_rect_image(h, w):
    import numpy as np, cv2
    img = np.ones((h, w, 3), dtype=np.uint8) * 180
    cv2.rectangle(img, (30, 20), (w-30, h//2+30), (40, 40, 40), -1)
    cv2.rectangle(img, (35, 25), (w-35, h//2+25), (100, 120, 140), -1)
    # keyboard area below
    for i in range(10):
        x = 40 + i * 15
        cv2.rectangle(img, (x, h//2+50), (x+12, h//2+62), (60,60,60), -1)
    return img

def _curved_yellow(h, w):
    import numpy as np, cv2
    img = np.ones((h, w, 3), dtype=np.uint8) * 200
    cv2.ellipse(img, (w//2, h//2), (w//3, h//6), 20, 0, 360, (0, 220, 255), -1)
    return img


def print_status():
    print(f"\nDataset: {DATA_DIR}")
    print("-" * 40)
    total = 0
    for class_name in sorted(["zebra", "school_bus", "golden_retriever", "bicycle",
                               "mushroom", "teapot", "piano", "eagle", "laptop", "banana"]):
        class_dir = DATA_DIR / class_name
        if class_dir.exists():
            count = len(list(class_dir.glob("*.*")))
        else:
            count = 0
        total += count
        print(f"  {class_name:20s} {count:4d}")
    print(f"  {'TOTAL':20s} {total:4d}")


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: Trying Tiny ImageNet (has some of our classes)...")
    try:
        available = download_tiny_imagenet()
    except Exception as e:
        print(f"  Failed: {e}")
        available = {}

    print("\nStep 2: Creating synthetic fallback for missing classes...")
    create_synthetic_fallback()

    print_status()
    print("\nNote: For real evaluation, place actual ImageNet images in data/imagenet_10/<class>/")
    print("You can manually download from image-net.org or use kaggle datasets.")
