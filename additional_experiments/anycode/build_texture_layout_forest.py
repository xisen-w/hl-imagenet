"""Forest with texture-layout features inspired by CNN gap mining.

CNN mining shows the CNN uses LOCAL texture (Laplacian variance in specific patches)
to discriminate pairs like sports_car/school_bus and bear/mushroom.

Key insight: rather than spatial COLOR (which overfits to position), spatial TEXTURE
may generalize better because:
1. Texture is more invariant to color shifts across train/val
2. Texture layout captures "where the detail is" not "where the color is"
3. Animals/vehicles have DISTRIBUTED texture; fruits/simple objects have LOCALIZED texture

Design: Original 90 features + 10 texture-layout features (replace 10 weakest).
But to avoid dilution, let's try these as a standalone forest first."""

import sys
from pathlib import Path
from collections import Counter
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from build_forest import extract_features, CLASSES, gini, Node, find_best_split, build_tree, count_nodes, predict_tree

DATA_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "train"
VAL_ROOT = Path(__file__).parent.parent.parent / "data" / "phase2" / "val"


def extract_texture_layout_features(image):
    """Original 90 features + texture layout features added to replace worst 10."""
    # Get original features
    orig = extract_features(image)

    # Compute texture maps
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    lap = cv2.Laplacian(gray, cv2.CV_32F)
    lap_abs = np.abs(lap)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Texture layout features (10)
    texture_feats = []

    # 1. Center texture concentration: center lap_var / total lap_var
    center_tex = float(np.var(lap[16:48, 16:48]))
    total_tex = float(np.var(lap))
    texture_feats.append(center_tex / max(total_tex, 1.0))

    # 2. Texture uniformity: std of per-quadrant textures (low = uniform like bus)
    q_textures = []
    for r0, c0 in [(0, 0), (0, 32), (32, 0), (32, 32)]:
        q_textures.append(float(np.var(lap[r0:r0+32, c0:c0+32])))
    texture_feats.append(float(np.std(q_textures)) / max(np.mean(q_textures), 1.0))

    # 3. Max patch texture (16x16 patches) — captures "textured spots"
    max_patch_tex = 0.0
    for row in range(4):
        for col in range(4):
            r0, c0 = row*16, col*16
            pt = float(np.var(lap[r0:r0+16, c0:c0+16]))
            max_patch_tex = max(max_patch_tex, pt)
    texture_feats.append(max_patch_tex / max(total_tex, 1.0))

    # 4. Texture in warm regions vs cool regions
    warm_mask = (h < 30) & (s > 30)
    cool_mask = (h > 90) & (s > 30)
    warm_tex = float(np.mean(lap_abs[warm_mask])) if np.sum(warm_mask) > 50 else 0.0
    cool_tex = float(np.mean(lap_abs[cool_mask])) if np.sum(cool_mask) > 50 else 0.0
    texture_feats.append(warm_tex / max(warm_tex + cool_tex, 1.0))

    # 5. Edge density in top half vs bottom half (relative)
    top_edge_dens = float(np.mean(lap_abs[:32, :]))
    bot_edge_dens = float(np.mean(lap_abs[32:, :]))
    texture_feats.append((top_edge_dens - bot_edge_dens) / max(top_edge_dens + bot_edge_dens, 1.0))

    # 6. Fraction of image area with "high texture" (lap > P75)
    p75 = np.percentile(lap_abs, 75)
    texture_feats.append(float(np.mean(lap_abs > p75 * 1.5)))

    # 7. Texture spreading: distance of high-texture pixels from center
    high_tex = lap_abs > np.percentile(lap_abs, 80)
    yy, xx = np.where(high_tex)
    if len(yy) > 20:
        mean_dist = float(np.mean(np.sqrt((yy - 32)**2 + (xx - 32)**2)))
        texture_feats.append(mean_dist / 32.0)
    else:
        texture_feats.append(1.0)

    # 8. Texture in saturated vs achromatic regions
    sat_mask = s > 80
    achrom_mask = s < 40
    sat_tex = float(np.mean(lap_abs[sat_mask])) if np.sum(sat_mask) > 50 else 0.0
    achrom_tex = float(np.mean(lap_abs[achrom_mask])) if np.sum(achrom_mask) > 50 else 0.0
    texture_feats.append(sat_tex / max(sat_tex + achrom_tex, 1.0))

    # 9. Number of "texture blobs" (connected high-texture regions)
    high_tex_binary = (lap_abs > np.percentile(lap_abs, 70)).astype(np.uint8)
    n_labels, _ = cv2.connectedComponents(high_tex_binary)
    texture_feats.append(min(float(n_labels - 1), 20.0) / 20.0)

    # 10. Ratio of horizontal to vertical texture
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    h_tex = float(np.mean(np.abs(gy)))
    v_tex = float(np.mean(np.abs(gx)))
    texture_feats.append(h_tex / max(h_tex + v_tex, 1.0))

    # Replace worst 10 features (indices: 87, 39, 21, 9, 62, 48, 52, 41, 28, 37)
    REMOVE = {87, 39, 21, 9, 62, 48, 52, 41, 28, 37}
    kept = [orig[i] for i in range(90) if i not in REMOVE]  # 80 features
    return kept + texture_feats  # 90 features total


def load_data(data_root):
    X, y = [], []
    for cls_idx, cls in enumerate(CLASSES):
        cls_dir = data_root / cls
        if not cls_dir.exists():
            continue
        images = sorted(cls_dir.glob("*.JPEG")) + sorted(cls_dir.glob("*.jpg"))
        for p in images:
            img = cv2.imread(str(p))
            if img is None:
                continue
            feats = extract_texture_layout_features(img)
            X.append(feats)
            y.append(cls_idx)
    return np.array(X), np.array(y)


def eval_forest_fn(trees, X, y):
    correct = 0
    for i in range(len(y)):
        votes = Counter()
        for t in trees:
            votes[predict_tree(t, X[i])] += 1
        if votes.most_common(1)[0][0] == y[i]:
            correct += 1
    return correct / len(y)


def main():
    print("Loading texture-layout features...")
    X_train, y_train = load_data(DATA_ROOT)
    X_val, y_val = load_data(VAL_ROOT)
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Features: {X_train.shape[1]}")

    n_feat_sample = int(np.sqrt(X_train.shape[1]) * 2)
    print(f"Config: 101 trees, depth 14, min_samples 16, n_feat={n_feat_sample}")

    trees = []
    for i in range(101):
        rng = np.random.RandomState(i * 7 + 42)
        idx = rng.choice(len(X_train), len(X_train), replace=True)
        tree = build_tree(X_train[idx], y_train[idx], max_depth=14, min_samples=16,
                         n_feat_sample=n_feat_sample, rng=rng)
        trees.append(tree)
        if i % 25 == 0:
            print(f"  Tree {i}: {count_nodes(tree)} nodes")

    train_acc = eval_forest_fn(trees, X_train, y_train)
    val_acc = eval_forest_fn(trees, X_val, y_val)
    print(f"\nTexture-Layout Forest: Train={train_acc:.1%}, Val={val_acc:.1%}, Gap={100*(train_acc-val_acc):.1f}pp")
    print(f"Baseline: Train=90.2%, Val=64.4%")

    # Per-class val breakdown
    from collections import defaultdict
    per_class = defaultdict(lambda: [0, 0])
    for i in range(len(y_val)):
        votes = Counter([predict_tree(t, X_val[i]) for t in trees])
        pred = votes.most_common(1)[0][0]
        cls = CLASSES[y_val[i]]
        per_class[cls][1] += 1
        if pred == y_val[i]:
            per_class[cls][0] += 1
    for cls in CLASSES:
        cc, ct = per_class[cls]
        print(f"  {cls:20s} {cc/ct:.1%} ({cc}/{ct})")


if __name__ == "__main__":
    main()
