"""Spatial relation inference between regions."""

from __future__ import annotations

from hlinet.types import Region


def infer_relations(regions: list[tuple[int, Region]]) -> list[tuple[int, int, str, float]]:
    """Infer spatial relations between pairs of regions.

    Returns: list of (source_id, target_id, relation_type, confidence)
    """
    relations = []

    for i, (id_a, reg_a) in enumerate(regions):
        for j, (id_b, reg_b) in enumerate(regions):
            if i >= j:
                continue

            ax, ay, aw, ah = reg_a.bbox
            bx, by, bw, bh = reg_b.bbox
            a_cx, a_cy = reg_a.center
            b_cx, b_cy = reg_b.center

            if aw == 0 or ah == 0 or bw == 0 or bh == 0:
                continue

            # Above/below
            if a_cy < b_cy - ah * 0.3:
                relations.append((id_a, id_b, "above", min(abs(a_cy - b_cy) / max(ah, bh, 1), 1.0)))
            elif a_cy > b_cy + bh * 0.3:
                relations.append((id_a, id_b, "below", min(abs(a_cy - b_cy) / max(ah, bh, 1), 1.0)))

            # Left/right
            if a_cx < b_cx - aw * 0.3:
                relations.append((id_a, id_b, "left_of", min(abs(a_cx - b_cx) / max(aw, bw, 1), 1.0)))
            elif a_cx > b_cx + bw * 0.3:
                relations.append((id_a, id_b, "right_of", min(abs(a_cx - b_cx) / max(aw, bw, 1), 1.0)))

            # Contains/inside
            if (ax <= bx and ay <= by and ax + aw >= bx + bw and ay + ah >= by + bh):
                relations.append((id_a, id_b, "contains", 0.9))
            elif (bx <= ax and by <= ay and bx + bw >= ax + aw and by + bh >= ay + ah):
                relations.append((id_a, id_b, "inside", 0.9))

            # Adjacent
            overlap = reg_a.overlaps(reg_b)
            if 0.01 < overlap < 0.3:
                relations.append((id_a, id_b, "adjacent", overlap))

            # Similar size
            size_a = aw * ah
            size_b = bw * bh
            size_ratio = min(size_a, size_b) / max(size_a, size_b, 1)
            if size_ratio > 0.7:
                relations.append((id_a, id_b, "similar_size", size_ratio))

    return relations
