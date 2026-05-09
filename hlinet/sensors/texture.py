"""Texture analysis sensors: LBP, Gabor filter banks, periodicity detection."""

from __future__ import annotations

import cv2
import numpy as np
from skimage.feature import local_binary_pattern

from hlinet.registry import register_sensor
from hlinet.types import Atom, Region


@register_sensor(name="lbp_texture", output_kinds=["texture_patch"])
class LBPTextureSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        h, w = gray.shape
        total_area = h * w

        lbp = local_binary_pattern(gray, P=8, R=1, method="uniform")

        grid_h, grid_w = 4, 4
        cell_h, cell_w = h // grid_h, w // grid_w
        atoms = []

        for i in range(grid_h):
            for j in range(grid_w):
                y0, x0 = i * cell_h, j * cell_w
                cell = lbp[y0:y0 + cell_h, x0:x0 + cell_w]
                hist, _ = np.histogram(cell, bins=10, range=(0, 10), density=True)

                uniformity = hist.max()
                entropy = -np.sum(hist[hist > 0] * np.log2(hist[hist > 0]))

                region = Region(
                    bbox=(x0, y0, cell_w, cell_h),
                    area_fraction=(cell_w * cell_h) / total_area,
                )
                descriptor = np.concatenate([hist, [uniformity, entropy]]).astype(np.float32)

                atoms.append(Atom(
                    kind="texture_patch",
                    region=region,
                    descriptor=descriptor,
                    confidence=1.0,
                    metadata={"uniformity": uniformity, "entropy": entropy},
                ))

        return atoms


@register_sensor(name="gabor_texture", output_kinds=["texture_patch"])
class GaborTextureSensor:
    def extract(self, image: np.ndarray) -> list[Atom]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        gray = gray.astype(np.float32) / 255.0
        h, w = gray.shape
        total_area = h * w

        orientations = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
        frequencies = [0.05, 0.1, 0.2, 0.4]

        responses = []
        for theta in orientations:
            for freq in frequencies:
                kernel = cv2.getGaborKernel(
                    (21, 21), sigma=3.0, theta=theta,
                    lambd=1.0 / freq, gamma=0.5,
                )
                resp = cv2.filter2D(gray, cv2.CV_32F, kernel)
                responses.append(resp)

        response_stack = np.stack(responses, axis=-1)

        grid_h, grid_w = 3, 3
        cell_h, cell_w = h // grid_h, w // grid_w
        atoms = []

        for i in range(grid_h):
            for j in range(grid_w):
                y0, x0 = i * cell_h, j * cell_w
                cell = response_stack[y0:y0 + cell_h, x0:x0 + cell_w]
                descriptor = np.array([
                    cell[:, :, k].mean() for k in range(cell.shape[2])
                ] + [
                    cell[:, :, k].std() for k in range(cell.shape[2])
                ], dtype=np.float32)

                dominant_orientation = int(np.argmax([
                    np.abs(cell[:, :, o * 4:(o + 1) * 4]).mean()
                    for o in range(4)
                ]))

                region = Region(
                    bbox=(x0, y0, cell_w, cell_h),
                    area_fraction=(cell_w * cell_h) / total_area,
                )

                atoms.append(Atom(
                    kind="texture_patch",
                    region=region,
                    descriptor=descriptor,
                    confidence=1.0,
                    metadata={
                        "dominant_orientation": dominant_orientation,
                        "energy": float(np.abs(descriptor[:16]).mean()),
                    },
                ))

        return atoms
