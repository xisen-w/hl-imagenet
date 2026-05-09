"""Shape analysis sensors: Hough circles/lines, convexity, elongation."""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.registry import register_sensor
from hlinet.types import Atom, Region


@register_sensor(name="hough_circles", output_kinds=["circle"])
class HoughCircleSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        gray = cv2.medianBlur(gray, 5)
        h, w = gray.shape
        total_area = h * w

        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1.2,
            minDist=int(min(h, w) * 0.1),
            param1=100, param2=40,
            minRadius=int(min(h, w) * 0.03),
            maxRadius=int(min(h, w) * 0.4),
        )

        atoms = []
        if circles is not None:
            for cx, cy, r in circles[0][:10]:
                cx, cy, r = int(cx), int(cy), int(r)
                x0 = max(cx - r, 0)
                y0 = max(cy - r, 0)
                bw = min(2 * r, w - x0)
                bh = min(2 * r, h - y0)

                region = Region(
                    bbox=(x0, y0, bw, bh),
                    area_fraction=(np.pi * r * r) / total_area,
                )
                descriptor = np.array([
                    r / min(h, w),
                    cx / w,
                    cy / h,
                    (np.pi * r * r) / total_area,
                ], dtype=np.float32)

                atoms.append(Atom(
                    kind="circle",
                    region=region,
                    descriptor=descriptor,
                    confidence=0.8,
                    metadata={"center": (cx, cy), "radius": r},
                ))

        return atoms


@register_sensor(name="hough_lines", output_kinds=["line"])
class HoughLineSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        edges = cv2.Canny(gray, 50, 150)
        h, w = gray.shape
        total_area = h * w

        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=10)

        atoms = []
        if lines is not None:
            for line in lines[:30]:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                angle = np.arctan2(y2 - y1, x2 - x1)

                x0 = min(x1, x2)
                y0_coord = min(y1, y2)
                bw = abs(x2 - x1) + 1
                bh = abs(y2 - y1) + 1

                region = Region(
                    bbox=(x0, y0_coord, bw, bh),
                    area_fraction=length / max(h, w),
                )
                descriptor = np.array([
                    length / max(h, w),
                    angle / np.pi,
                    (x1 + x2) / 2 / w,
                    (y1 + y2) / 2 / h,
                ], dtype=np.float32)

                atoms.append(Atom(
                    kind="line",
                    region=region,
                    descriptor=descriptor,
                    confidence=0.7,
                    metadata={"angle_deg": float(np.degrees(angle)), "length": length},
                ))

        return atoms
