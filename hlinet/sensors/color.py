"""Color analysis sensors: histograms, dominant colors, spatial color distribution."""

from __future__ import annotations

import cv2
import numpy as np
from scipy import ndimage

from hlinet.registry import register_sensor
from hlinet.types import Atom, Region


@register_sensor(name="color_regions", output_kinds=["color_region"])
class ColorRegionSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, w = image.shape[:2]
        total_area = h * w
        atoms = []

        color_ranges = {
            "red": [(0, 100, 100), (10, 255, 255)],
            "orange": [(10, 100, 100), (25, 255, 255)],
            "yellow": [(25, 100, 100), (35, 255, 255)],
            "green": [(35, 100, 100), (85, 255, 255)],
            "blue": [(85, 100, 100), (130, 255, 255)],
            "purple": [(130, 100, 100), (170, 255, 255)],
            "white": [(0, 0, 200), (180, 30, 255)],
            "black": [(0, 0, 0), (180, 255, 50)],
            "brown": [(10, 100, 50), (20, 255, 200)],
            "golden": [(10, 30, 80), (25, 255, 255)],
        }

        for color_name, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            coverage = mask.sum() / 255 / total_area

            if coverage < 0.01:
                continue

            labeled, n_components = ndimage.label(mask)
            for i in range(1, min(n_components + 1, 6)):
                component = (labeled == i).astype(np.uint8) * 255
                comp_area = component.sum() / 255
                if comp_area < total_area * 0.005:
                    continue

                ys, xs = np.where(component > 0)
                x_min, x_max = xs.min(), xs.max()
                y_min, y_max = ys.min(), ys.max()
                bw, bh = x_max - x_min, y_max - y_min

                region = Region(
                    bbox=(int(x_min), int(y_min), int(bw), int(bh)),
                    area_fraction=comp_area / total_area,
                )

                mean_hsv = cv2.mean(hsv, mask=component)[:3]
                descriptor = np.array([
                    coverage,
                    comp_area / total_area,
                    mean_hsv[0] / 180,
                    mean_hsv[1] / 255,
                    mean_hsv[2] / 255,
                    bw / max(bh, 1),
                ], dtype=np.float32)

                atoms.append(Atom(
                    kind="color_region",
                    region=region,
                    descriptor=descriptor,
                    confidence=min(coverage * 5, 1.0),
                    metadata={"color": color_name, "coverage": coverage},
                ))

        return atoms


@register_sensor(name="color_histogram", output_kinds=["color_hist"])
class ColorHistogramSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, w = image.shape[:2]

        hist_h = cv2.calcHist([hsv], [0], None, [18], [0, 180]).flatten()
        hist_s = cv2.calcHist([hsv], [1], None, [8], [0, 256]).flatten()
        hist_v = cv2.calcHist([hsv], [2], None, [8], [0, 256]).flatten()

        hist_h = hist_h / max(hist_h.sum(), 1)
        hist_s = hist_s / max(hist_s.sum(), 1)
        hist_v = hist_v / max(hist_v.sum(), 1)

        descriptor = np.concatenate([hist_h, hist_s, hist_v]).astype(np.float32)
        region = Region(bbox=(0, 0, w, h), area_fraction=1.0)

        return [Atom(
            kind="color_hist",
            region=region,
            descriptor=descriptor,
            confidence=1.0,
            metadata={
                "dominant_hue_bin": int(np.argmax(hist_h)),
                "saturation_mean": float(hist_s @ np.arange(8) / 8),
                "brightness_mean": float(hist_v @ np.arange(8) / 8),
            },
        )]
