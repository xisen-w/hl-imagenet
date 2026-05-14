"""Segmentation sensors: superpixels, graph-based segmentation, object proposals."""

from __future__ import annotations

import cv2
import numpy as np
from skimage.segmentation import felzenszwalb, slic
from skimage.measure import regionprops

from hlinet.registry import register_sensor
from hlinet.types import Atom, Region


@register_sensor(name="superpixel_segments", output_kinds=["segment"])
class SuperpixelSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]
        total_area = h * w

        segments = slic(rgb, n_segments=30, compactness=10, start_label=0)
        props = regionprops(segments + 1, intensity_image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

        atoms = []
        for prop in props:
            if prop.area < total_area * 0.005:
                continue

            y0, x0, y1, x1 = prop.bbox
            bw, bh = x1 - x0, y1 - y0

            mean_color = cv2.mean(image[y0:y1, x0:x1])[:3]
            region = Region(
                bbox=(x0, y0, bw, bh),
                area_fraction=prop.area / total_area,
            )

            descriptor = np.array([
                prop.area / total_area,
                prop.eccentricity,
                prop.solidity,
                bw / max(bh, 1),
                prop.euler_number,
                mean_color[0] / 255,
                mean_color[1] / 255,
                mean_color[2] / 255,
            ], dtype=np.float32)

            atoms.append(Atom(
                kind="segment",
                region=region,
                descriptor=descriptor,
                confidence=1.0,
                metadata={
                    "eccentricity": prop.eccentricity,
                    "solidity": prop.solidity,
                    "label": prop.label,
                },
            ))

        return atoms


@register_sensor(name="felzenszwalb_segments", output_kinds=["segment"])
class FelzenszwalbSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]
        total_area = h * w

        segments = felzenszwalb(rgb, scale=200, sigma=0.5, min_size=50)
        unique_labels = np.unique(segments)

        atoms = []
        for label in unique_labels[:40]:
            mask = (segments == label).astype(np.uint8)
            area = mask.sum()
            if area < total_area * 0.01:
                continue

            ys, xs = np.where(mask > 0)
            x0, x1 = xs.min(), xs.max()
            y0, y1 = ys.min(), ys.max()
            bw, bh = x1 - x0, y1 - y0

            mean_color = cv2.mean(image, mask=mask * 255)[:3]
            region = Region(
                bbox=(int(x0), int(y0), int(bw), int(bh)),
                mask=mask,
                area_fraction=area / total_area,
            )

            compactness = area / max(bw * bh, 1)
            descriptor = np.array([
                area / total_area,
                compactness,
                bw / max(bh, 1),
                mean_color[0] / 255,
                mean_color[1] / 255,
                mean_color[2] / 255,
                (x0 + bw / 2) / w,
                (y0 + bh / 2) / h,
            ], dtype=np.float32)

            atoms.append(Atom(
                kind="segment",
                region=region,
                descriptor=descriptor,
                confidence=1.0,
                metadata={"compactness": compactness, "label": int(label)},
            ))

        return atoms
