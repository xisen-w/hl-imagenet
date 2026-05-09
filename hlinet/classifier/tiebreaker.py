"""Pairwise tiebreakers: when two classes are close, use direct discriminators."""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.types import SceneGraph


TIEBREAKER_RULES: dict[tuple[str, str], callable] = {}


def register_tiebreaker(class_a: str, class_b: str):
    def decorator(fn):
        TIEBREAKER_RULES[(class_a, class_b)] = fn
        TIEBREAKER_RULES[(class_b, class_a)] = lambda g: 1.0 - fn(g)
        return fn
    return decorator


def resolve_tie(class_a: str, class_b: str, graph: SceneGraph) -> float | None:
    key = (class_a, class_b)
    if key in TIEBREAKER_RULES:
        return TIEBREAKER_RULES[key](graph)
    return None


@register_tiebreaker("golden_retriever", "mushroom")
def dog_vs_mushroom(graph: SceneGraph) -> float:
    """Returns >0.5 if more like dog, <0.5 if more like mushroom.
    Uses bottom-third edge density (mushrooms have complex gills/stem)."""
    if graph.raw_image is None:
        return 0.5
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    edges = cv2.Canny(gray, 50, 150)
    bot_edges = float(edges[2 * h // 3:, :].sum() / 255) / (h // 3 * w)
    top_edges = float(edges[:h // 3, :].sum() / 255) / (h // 3 * w)

    # Mushrooms: more edge density in bottom (gills, stem detail)
    # Dogs: more uniform bottom (legs/ground)
    if bot_edges > 0.32 and bot_edges > top_edges:
        return 0.35  # lean mushroom
    return 0.55  # default: slight dog lean (since dog wins most head-to-heads)


@register_tiebreaker("golden_retriever", "teapot")
def dog_vs_teapot(graph: SceneGraph) -> float:
    """Returns >0.5 if more like dog, <0.5 if more like teapot.
    These classes overlap heavily at 64x64 — only flip on strong signal."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)

    # Only flip if very strong spout/handle shape detected
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, bw, bh = cv2.boundingRect(largest)
        aspect = bw / max(bh, 1)
        hull = cv2.convexHull(largest)
        hull_area = cv2.contourArea(hull)
        area = cv2.contourArea(largest)
        solidity = area / max(hull_area, 1)
        # Very wide + low solidity = likely teapot (spout extends)
        if aspect > 1.4 and solidity < 0.7:
            return 0.3
    return 0.5  # don't break tie (insufficient evidence)


@register_tiebreaker("school_bus", "zebra")
def bus_vs_zebra(graph: SceneGraph) -> float:
    """Returns >0.5 if more like bus, <0.5 if more like zebra."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]

    # Bus: yellow/orange mass, zebra: black+white with green
    yellow = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
              (hsv[:, :, 1] > 60) & (hsv[:, :, 2] > 60))
    yellow_ratio = float(yellow.sum()) / (h * w)

    # Black+white dominance (zebra)
    gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
    bw = float(((gray < 60) | (gray > 200)).sum()) / (h * w)

    # Clear bus signal: yellow body present
    if yellow_ratio > 0.15:
        return 0.8
    if bw > 0.5 and yellow_ratio < 0.05:
        return 0.2
    return 0.5


@register_tiebreaker("mushroom", "teapot")
def mushroom_vs_teapot(graph: SceneGraph) -> float:
    """Returns >0.5 if more like mushroom, <0.5 if more like teapot."""
    if graph.raw_image is None:
        return 0.5
    hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]

    # Mushroom: brown/red tones, multiple small objects, natural context
    # Teapot: ceramic (low saturation), single object, smooth-ish
    mean_sat = float(hsv[:, :, 1].mean())

    # Brown/earth tones (mushroom)
    brown = ((hsv[:, :, 0] >= 5) & (hsv[:, :, 0] <= 25) &
             (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 30))
    brown_ratio = float(brown.sum()) / (h * w)

    # Warm-red (mushroom cap)
    red = ((hsv[:, :, 0] <= 10) | (hsv[:, :, 0] >= 170)) & (hsv[:, :, 1] > 40)
    red_ratio = float(red.sum()) / (h * w)

    mush_signal = min(brown_ratio * 3, 1.0) * 0.4 + min(red_ratio * 5, 1.0) * 0.3 + min(mean_sat / 150, 1.0) * 0.3
    return min(max(mush_signal, 0.0), 1.0)
