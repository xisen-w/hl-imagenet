"""Relational compound features: combine WHERE + WHAT + HOW signals."""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(name="yellow_body_with_sky", tags=["compound", "vehicle"], description="Large yellow mass below blue sky (school bus signature)")
class YellowBodyWithSky:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        # Sky in top quarter
        top = hsv[:h // 4, :, :]
        blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
        bright_sky = (top[:, :, 2] > 180) & (top[:, :, 1] < 50)
        sky_ratio = float((blue_sky | bright_sky).sum()) / (h // 4 * w)

        # Yellow in middle-bottom (the bus body)
        body = hsv[h // 4:, :, :]
        yellow_body = ((body[:, :, 0] >= 15) & (body[:, :, 0] <= 45) &
                       (body[:, :, 1] > 80) & (body[:, :, 2] > 80))
        yellow_ratio = float(yellow_body.sum()) / (3 * h // 4 * w)

        if sky_ratio > 0.12 and yellow_ratio > 0.06:
            score = min((sky_ratio * yellow_ratio) * 25, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"yellow_body+sky: sky={sky_ratio:.2f}, yellow_body={yellow_ratio:.2f}"],
            )
        return FeatureValue.absent(f"no yellow-body-with-sky: sky={sky_ratio:.2f}, yellow={yellow_ratio:.2f}")


@register_feature(name="stripes_with_nature", tags=["compound", "animal"], description="Striped texture in green/outdoor context (zebra in field)")
class StripesWithNature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        # Green presence (grass/trees around zebra)
        green_mask = ((hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 85) &
                      (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 40))
        green_ratio = float(green_mask.sum()) / (h * w)

        # B&W stripes: check for high-contrast vertical/horizontal pattern in center
        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        center = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
        col_means = center.mean(axis=0)
        crossings = np.sum(np.diff(np.sign(col_means - col_means.mean())) != 0)
        amplitude = float(col_means.max() - col_means.min())

        has_stripes = crossings >= 4 and amplitude > 40
        has_green = green_ratio > 0.05

        if has_stripes and has_green:
            score = min((crossings / 8) * (green_ratio * 5) * (amplitude / 60), 1.0)
            return FeatureValue.detected(
                confidence=max(0.3, score),
                evidence=[f"stripes+nature: crossings={crossings}, green={green_ratio:.2f}"],
            )
        # Stripes alone (indoor zebra) — still partial signal
        if has_stripes and amplitude > 60:
            return FeatureValue.detected(
                confidence=0.2,
                evidence=[f"stripes only (no green): crossings={crossings}, amp={amplitude:.0f}"],
            )
        return FeatureValue.absent("no stripes-with-nature")


@register_feature(name="golden_fur_in_nature", tags=["compound", "animal"], description="Golden/brown textured mass in green/outdoor setting (retriever)")
class GoldenFurInNature:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        # Golden/brown: H10-35, moderate S, moderate V
        golden_mask = ((hsv[:, :, 0] >= 10) & (hsv[:, :, 0] <= 35) &
                       (hsv[:, :, 1] > 50) & (hsv[:, :, 2] > 60))
        golden_ratio = float(golden_mask.sum()) / (h * w)

        # Green context
        green_mask = ((hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 85) &
                      (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 40))
        green_ratio = float(green_mask.sum()) / (h * w)

        # Texture complexity in golden region (fur has high local variance)
        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        local_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        textured = local_var > 200

        if golden_ratio > 0.1 and (green_ratio > 0.03 or textured):
            score = min(golden_ratio * 3 * (1 + green_ratio * 3), 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"golden_fur_nature: golden={golden_ratio:.2f}, green={green_ratio:.2f}, var={local_var:.0f}"],
            )
        return FeatureValue.absent(f"no golden-fur-nature: golden={golden_ratio:.2f}")


@register_feature(name="round_object_on_surface", tags=["compound", "food", "container"], description="Rounded object on uniform/flat surface (mushroom, teapot)")
class RoundObjectOnSurface:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Bottom third should be uniform (table/surface)
        bottom = gray[2 * h // 3:, :]
        bottom_std = float(bottom.std())
        uniform_surface = bottom_std < 35

        # Object in center should have edges (non-uniform)
        center = gray[h // 6:2 * h // 3, w // 4:3 * w // 4]
        edges = cv2.Canny(center, 50, 150)
        edge_density = float(edges.sum()) / 255 / (center.shape[0] * center.shape[1])

        # Check for roundness via contours
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        roundness = 0.0
        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            perimeter = cv2.arcLength(largest, True)
            if perimeter > 0:
                roundness = 4 * np.pi * area / (perimeter ** 2)

        if uniform_surface and edge_density > 0.05 and roundness > 0.3:
            score = min(roundness * (1 - bottom_std / 50) * edge_density * 10, 1.0)
            return FeatureValue.detected(
                confidence=max(0.3, score),
                evidence=[f"round_on_surface: roundness={roundness:.2f}, surface_std={bottom_std:.0f}"],
            )
        return FeatureValue.absent(f"no round-on-surface: std={bottom_std:.0f}, edges={edge_density:.2f}")


@register_feature(name="bw_keys_indoor", tags=["compound", "instrument"], description="B&W vertical pattern in indoor/dark setting (piano)")
class BWKeysIndoor:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        # Low saturation (B&W scene)
        mean_sat = float(hsv[:, :, 1].mean())
        low_sat = mean_sat < 60

        # No sky (indoor)
        top = hsv[:h // 4, :, :]
        blue_sky = ((top[:, :, 0] >= 90) & (top[:, :, 0] <= 130) & (top[:, :, 1] > 30))
        sky_ratio = float(blue_sky.sum()) / (h // 4 * w)
        no_sky = sky_ratio < 0.1

        # Vertical line pattern
        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        col_means = gray.mean(axis=0)
        crossings = np.sum(np.diff(np.sign(col_means - col_means.mean())) != 0)
        amplitude = float(col_means.max() - col_means.min())

        if low_sat and no_sky and crossings >= 6 and amplitude > 30:
            score = min(crossings / 12 * (1 - mean_sat / 100), 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"bw_keys_indoor: sat={mean_sat:.0f}, crossings={crossings}, no_sky"],
            )
        return FeatureValue.absent(f"no bw-keys-indoor: sat={mean_sat:.0f}, crossings={crossings}")


@register_feature(name="spout_handle_shape", tags=["compound", "container"], description="Lateral protrusions on compact body (teapot spout+handle)")
class SpoutHandleShape:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Threshold to find main object
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return FeatureValue.absent("no contours")

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area < h * w * 0.05:
            return FeatureValue.absent("main object too small")

        # Check for lateral extent: object wider than tall with protrusions
        x, y, bw, bh = cv2.boundingRect(largest)
        aspect = bw / max(bh, 1)

        # Convex hull vs actual area (protrusions = convexity defects)
        hull = cv2.convexHull(largest)
        hull_area = cv2.contourArea(hull)
        solidity = area / max(hull_area, 1)

        # Teapot: wider than tall (spout extends), has concavities (handle hole)
        if aspect > 1.1 and solidity < 0.85 and area > h * w * 0.08:
            score = min((aspect - 1.0) * (1 - solidity) * 10, 1.0)
            return FeatureValue.detected(
                confidence=max(0.3, score),
                evidence=[f"spout_handle: aspect={aspect:.2f}, solidity={solidity:.2f}"],
            )
        return FeatureValue.absent(f"no spout-handle: aspect={aspect:.2f}, solidity={solidity:.2f}")


@register_feature(name="warm_color_dominated", tags=["compound", "color"], description="Image dominated by warm tones (R>B) — dogs, not teapots/mushrooms")
class WarmColorDominated:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        b, g, r = cv2.split(graph.raw_image)
        h, w = r.shape

        # Fraction of pixels where red channel > blue by significant margin
        warm_pixels = float((r.astype(int) - b.astype(int) > 30).sum()) / (h * w)

        if warm_pixels > 0.45:
            score = min((warm_pixels - 0.3) * 2, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"warm_dominated: {warm_pixels:.2f} warm pixels"],
            )
        return FeatureValue.absent(f"not warm dominated: {warm_pixels:.2f}")


@register_feature(name="outdoor_animal_scene", tags=["compound", "animal"], description="Animal-like mass in outdoor/green setting (not bus, not indoor)")
class OutdoorAnimalScene:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        # Green/brown (nature colors) in periphery
        green_mask = ((hsv[:, :, 0] >= 35) & (hsv[:, :, 0] <= 85) &
                      (hsv[:, :, 1] > 30) & (hsv[:, :, 2] > 30))
        brown_mask = ((hsv[:, :, 0] >= 5) & (hsv[:, :, 0] <= 25) &
                      (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 40))
        nature_ratio = float((green_mask | brown_mask).sum()) / (h * w)

        # NOT dominated by yellow (bus) — yellow should be <30%
        yellow_mask = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
                       (hsv[:, :, 1] > 100) & (hsv[:, :, 2] > 100))
        yellow_ratio = float(yellow_mask.sum()) / (h * w)

        # Texture complexity in center (animal body, not flat surface)
        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        center = gray[h // 4:3 * h // 4, w // 4:3 * w // 4]
        local_var = float(cv2.Laplacian(center, cv2.CV_64F).var())

        if nature_ratio > 0.1 and yellow_ratio < 0.25 and local_var > 150:
            score = min(nature_ratio * 2 * (local_var / 500), 1.0)
            return FeatureValue.detected(
                confidence=max(0.25, score),
                evidence=[f"outdoor_animal: nature={nature_ratio:.2f}, var={local_var:.0f}"],
            )
        return FeatureValue.absent(f"no outdoor-animal: nature={nature_ratio:.2f}, yellow={yellow_ratio:.2f}")
