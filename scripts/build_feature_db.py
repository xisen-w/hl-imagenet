"""Extract feature vectors for all training images and save as NPZ."""
import sys
sys.path.insert(0, "/Users/wangxiang/Desktop/my_workspace/hl-image-net")

import cv2
import numpy as np
from pathlib import Path
from hlinet.features.compounds.phase2_signatures import _stats
from hlinet.scene.builder import SceneGraphBuilder

DATA_DIR = Path("/Users/wangxiang/Desktop/my_workspace/hl-image-net/data/phase2/train")
OUT_PATH = Path("/Users/wangxiang/Desktop/my_workspace/hl-image-net/hlinet/classifier/feature_db.npz")

CLASSES = sorted([d.name for d in DATA_DIR.iterdir() if d.is_dir()])
builder = SceneGraphBuilder()

FEATURE_KEYS = None
all_vectors = []
all_labels = []
all_paths = []

for cls_idx, cls_name in enumerate(CLASSES):
    cls_dir = DATA_DIR / cls_name
    images = sorted(cls_dir.glob("*.JPEG"))
    for img_path in images:
        image = cv2.imread(str(img_path))
        if image is None:
            continue
        graph = builder.build(image)
        s = _stats(graph)

        if FEATURE_KEYS is None:
            FEATURE_KEYS = sorted([k for k in s.keys() if not k.startswith("hist_") or k.startswith("hist_") and "_minus_" not in k])
            FEATURE_KEYS = sorted(s.keys())
            print(f"Feature count: {len(FEATURE_KEYS)}")

        vec = np.array([s.get(k, 0.0) for k in FEATURE_KEYS], dtype=np.float32)
        all_vectors.append(vec)
        all_labels.append(cls_idx)
        all_paths.append(str(img_path))

    print(f"  {cls_name}: {len(images)} images processed")

vectors = np.array(all_vectors, dtype=np.float32)
labels = np.array(all_labels, dtype=np.int32)

np.savez(str(OUT_PATH),
         vectors=vectors,
         labels=labels,
         classes=np.array(CLASSES),
         feature_keys=np.array(FEATURE_KEYS),
         paths=np.array(all_paths))

print(f"\nSaved {len(vectors)} vectors x {vectors.shape[1]} features to {OUT_PATH}")
print(f"Classes: {CLASSES}")
