"""Layout predicates: spatial arrangements that distinguish confusable classes."""

from __future__ import annotations

import cv2
import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(name="horizontal_window_pattern", tags=["spatial", "vehicle"], description="Repeated dark horizontal elements on colored body (bus windows)")
class HorizontalWindowPattern:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Compute horizontal projection (row means)
        row_means = gray.mean(axis=1)

        # Look for alternating bright/dark pattern in the middle rows
        mid_rows = row_means[h // 4:3 * h // 4]
        if len(mid_rows) < 8:
            return FeatureValue.absent("image too small")

        # Count zero-crossings of deviation from mean (indicates banding)
        mean_val = mid_rows.mean()
        deviations = mid_rows - mean_val
        crossings = np.sum(np.diff(np.sign(deviations)) != 0)

        # Also check amplitude of variation
        amplitude = float(mid_rows.max() - mid_rows.min())

        if crossings >= 4 and amplitude > 40:
            score = min(crossings / 10 * amplitude / 80, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"horizontal bands: {crossings} crossings, amplitude={amplitude:.0f}"],
            )
        return FeatureValue.absent(f"weak horizontal pattern: crossings={crossings}, amp={amplitude:.0f}")


@register_feature(name="curved_elongated_yellow", tags=["spatial", "food"], description="Yellow curved elongated shape (banana-specific)")
class CurvedElongatedYellow:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        # Yellow mask: H20-45 high saturation
        yellow_mask = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 45) &
                       (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 80)).astype(np.uint8) * 255

        coverage = float(yellow_mask.sum()) / 255 / (h * w)
        if coverage < 0.05:
            return FeatureValue.absent("not enough yellow for banana")

        # Check if yellow region is elongated (fit ellipse)
        contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return FeatureValue.absent("no yellow contours")

        largest = max(contours, key=cv2.contourArea)
        if len(largest) < 5:
            return FeatureValue.absent("yellow region too small for ellipse fit")

        ellipse = cv2.fitEllipse(largest)
        (cx, cy), (ma, MA), angle = ellipse
        aspect = MA / max(ma, 1)

        # Banana: elongated (aspect > 2) + tilted (not perfectly horizontal/vertical)
        if aspect > 2.0 and coverage > 0.08:
            score = min((aspect - 1.5) / 3 * coverage * 5, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"curved yellow: aspect={aspect:.1f}, coverage={coverage:.2f}, angle={angle:.0f}"],
            )
        return FeatureValue.absent(f"yellow not elongated enough: aspect={aspect:.1f}")


@register_feature(name="large_dark_rectangle_center", tags=["spatial", "electronics"], description="Large dark rectangular region in center (screen/monitor)")
class LargeDarkRectangleCenter:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Dark region mask
        dark_mask = (gray < 80).astype(np.uint8) * 255
        dark_coverage = float(dark_mask.sum()) / 255 / (h * w)

        if dark_coverage < 0.08 or dark_coverage > 0.7:
            return FeatureValue.absent(f"dark coverage not right: {dark_coverage:.2f}")

        # Check if dark region is rectangular and centered
        contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return FeatureValue.absent("no dark contours")

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        rect = cv2.minAreaRect(largest)
        rect_area = rect[1][0] * rect[1][1]
        rectangularity = area / max(rect_area, 1)

        # Check center position
        M = cv2.moments(largest)
        if M["m00"] == 0:
            return FeatureValue.absent("zero moment")
        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]
        centered = (0.25 < cx / w < 0.75) and (0.2 < cy / h < 0.7)

        if rectangularity > 0.7 and centered and area > h * w * 0.1:
            score = rectangularity * (area / (h * w))
            return FeatureValue.detected(
                confidence=min(score * 3, 1.0),
                evidence=[f"dark rect: rectangularity={rectangularity:.2f}, area_frac={area/(h*w):.2f}"],
            )
        return FeatureValue.absent("no centered dark rectangle")


@register_feature(name="repeated_vertical_lines", tags=["spatial", "instrument"], description="Repeated thin vertical lines (piano keys, fence)")
class RepeatedVerticalLines:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Compute column projection (vertical line detection)
        col_means = gray.mean(axis=0)

        # Look for periodic pattern in columns
        mean_val = col_means.mean()
        deviations = col_means - mean_val
        crossings = np.sum(np.diff(np.sign(deviations)) != 0)
        amplitude = float(col_means.max() - col_means.min())

        # Piano keys: many regular vertical transitions
        if crossings >= 8 and amplitude > 30:
            score = min(crossings / 15 * amplitude / 60, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"vertical lines: {crossings} crossings, amplitude={amplitude:.0f}"],
            )
        return FeatureValue.absent(f"weak vertical pattern: crossings={crossings}")


@register_feature(name="pure_vertical_stripes", tags=["spatial", "pattern"], description="Purely vertical stripe pattern with no horizontal variation (zebra body)")
class PureVerticalStripes:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        col_var = float(gray.mean(axis=0).std())
        row_var = float(gray.mean(axis=1).std())

        # Pure vertical: very high col variance, very low row variance
        if col_var > 50 and row_var < 20:
            ratio = col_var / max(row_var, 0.1)
            score = min(ratio / 100, 1.0)
            return FeatureValue.detected(
                confidence=score,
                evidence=[f"pure vertical: col_var={col_var:.1f}, row_var={row_var:.1f}"],
            )
        return FeatureValue.absent(f"not pure vertical: col_var={col_var:.1f}, row_var={row_var:.1f}")


@register_feature(name="sky_above_object", tags=["spatial", "context"], description="Blue/bright uniform region in top rows (outdoor sky)")
class SkyAboveObject:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")

        hsv = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2HSV)
        h, w = hsv.shape[:2]

        # Top quarter of image
        top_quarter = hsv[:h // 4, :, :]

        # Sky: blue hue (H90-130) OR very bright low-saturation (overcast)
        blue_mask = ((top_quarter[:, :, 0] >= 90) & (top_quarter[:, :, 0] <= 130) &
                     (top_quarter[:, :, 1] > 30))
        bright_mask = (top_quarter[:, :, 2] > 180) & (top_quarter[:, :, 1] < 50)

        sky_pixels = float((blue_mask | bright_mask).sum())
        top_area = h // 4 * w
        sky_ratio = sky_pixels / top_area

        if sky_ratio > 0.3:
            return FeatureValue.detected(
                confidence=min(sky_ratio, 1.0),
                evidence=[f"sky detected in top: ratio={sky_ratio:.2f}"],
            )
        return FeatureValue.absent(f"no sky in top: ratio={sky_ratio:.2f}")
