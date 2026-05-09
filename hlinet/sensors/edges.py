"""Edge detection sensors: Canny, Sobel, contour extraction."""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.registry import register_sensor
from hlinet.types import Atom, Region


@register_sensor(name="canny_edges", output_kinds=["edge"])
class CannyEdgeSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        h, w = gray.shape
        total_area = h * w
        atoms = []

        for contour in contours:
            if cv2.arcLength(contour, False) < 20:
                continue
            x, y, cw, ch = cv2.boundingRect(contour)
            region = Region(
                bbox=(x, y, cw, ch),
                area_fraction=(cw * ch) / total_area,
            )
            descriptor = np.array([
                cv2.arcLength(contour, True),
                cv2.contourArea(contour),
                cw / max(ch, 1),  # aspect ratio
                len(contour),     # point count
            ], dtype=np.float32)

            atoms.append(Atom(
                kind="edge",
                region=region,
                descriptor=descriptor,
                confidence=1.0,
                metadata={"contour": contour},
            ))

        return atoms


@register_sensor(name="contour_shapes", output_kinds=["contour"])
class ContourShapeSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        h, w = gray.shape
        total_area = h * w
        atoms = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < total_area * 0.005:
                continue

            x, y, cw, ch = cv2.boundingRect(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = (4 * np.pi * area) / max(perimeter ** 2, 1)
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            solidity = area / max(hull_area, 1)

            moments = cv2.moments(contour)
            hu = cv2.HuMoments(moments).flatten()

            region = Region(bbox=(x, y, cw, ch), area_fraction=area / total_area)
            descriptor = np.concatenate([
                [circularity, solidity, cw / max(ch, 1), area / total_area],
                hu[:4],
            ]).astype(np.float32)

            atoms.append(Atom(
                kind="contour",
                region=region,
                descriptor=descriptor,
                confidence=1.0,
                metadata={
                    "circularity": circularity,
                    "solidity": solidity,
                    "contour": contour,
                },
            ))

        return atoms
