"""Texture pattern features: striped, furry, smooth, periodic."""

from __future__ import annotations

import numpy as np

from hlinet.registry import register_feature
from hlinet.types import FeatureValue, Region, SceneGraph


@register_feature(name="striped_texture", tags=["texture", "animal", "pattern"], description="Alternating band patterns (zebra stripes, piano keys)")
class StripedTexture:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        texture_atoms = [a for a in graph.atoms if a.kind == "texture_patch"]
        if not texture_atoms:
            return FeatureValue.absent("no texture atoms")

        gabor_atoms = [a for a in texture_atoms if "dominant_orientation" in a.metadata]
        if len(gabor_atoms) < 4:
            return FeatureValue.absent("too few texture patches for stripe detection")

        orientations = [a.metadata["dominant_orientation"] for a in gabor_atoms]
        from collections import Counter
        orient_counts = Counter(orientations)
        most_common_orient, most_common_count = orient_counts.most_common(1)[0]
        consistency = most_common_count / len(orientations)

        high_energy_patches = [
            a for a in gabor_atoms
            if a.metadata.get("energy", 0) > 0.3
            and a.metadata["dominant_orientation"] == most_common_orient
        ]
        energy_ratio = len(high_energy_patches) / max(len(gabor_atoms), 1)

        # Real stripes need black+white color regions (alternating dark/light bands)
        bw_coverage = 0.0
        for atom in graph.atoms:
            if atom.kind == "color_region" and atom.metadata.get("color") in ("black", "white"):
                bw_coverage += atom.region.area_fraction

        bw_bonus = min(bw_coverage * 2, 1.0) * 0.2
        score = consistency * 0.5 + energy_ratio * 0.3 + bw_bonus
        if score > 0.55 and consistency > 0.6:
            return FeatureValue.detected(
                confidence=min(score, 1.0),
                evidence=[f"stripe: consistency={consistency:.2f}, energy={energy_ratio:.2f}, bw={bw_coverage:.2f}"],
            )
        return FeatureValue.absent(f"weak stripe: consistency={consistency:.2f}")


@register_feature(name="fur_texture", tags=["texture", "animal"], description="Fine-grained, high-entropy texture suggesting fur/hair")
class FurTexture:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        texture_atoms = [a for a in graph.atoms if a.kind == "texture_patch"]
        if not texture_atoms:
            return FeatureValue.absent("no texture atoms")

        fur_scores = []
        for atom in texture_atoms:
            entropy = atom.metadata.get("entropy", 0)
            energy = atom.metadata.get("energy", 0)
            # Fur: high entropy (complex), moderate energy (not smooth, not extreme)
            if 2.0 < entropy < 3.5 and 0.1 < energy < 0.5:
                fur_scores.append((entropy - 2.0) / 1.5)

        if fur_scores and len(fur_scores) > len(texture_atoms) * 0.3:
            score = np.mean(fur_scores)
            return FeatureValue.detected(
                confidence=min(score, 1.0),
                evidence=[f"fur-like texture in {len(fur_scores)}/{len(texture_atoms)} patches"],
            )
        return FeatureValue.absent("no fur texture pattern")


@register_feature(name="smooth_texture", tags=["texture"], description="Low-entropy, uniform texture (metal, plastic, sky)")
class SmoothTexture:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        texture_atoms = [a for a in graph.atoms if a.kind == "texture_patch"]
        if not texture_atoms:
            return FeatureValue.absent("no texture atoms")

        # At 64x64, use relative thresholds based on the patch distribution
        entropies = [a.metadata.get("entropy", 5) for a in texture_atoms]
        uniformities = [a.metadata.get("uniformity", 0) for a in texture_atoms]

        # Smooth: patches with below-median entropy or above-median uniformity
        med_entropy = np.median(entropies) if entropies else 3.0
        smooth_count = sum(1 for e, u in zip(entropies, uniformities)
                          if e < med_entropy * 0.85 or u > 0.25)

        ratio = smooth_count / len(texture_atoms)
        if ratio > 0.3:
            return FeatureValue.detected(
                confidence=min(ratio * 1.2, 1.0),
                evidence=[f"smooth texture in {smooth_count}/{len(texture_atoms)} patches"],
            )
        return FeatureValue.absent("texture too complex for smooth")


@register_feature(name="organic_texture", tags=["texture", "nature"], description="Irregular, natural texture (leaves, bark, mushroom cap)")
class OrganicTexture:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        texture_atoms = [a for a in graph.atoms if a.kind == "texture_patch"]
        if not texture_atoms:
            return FeatureValue.absent("no texture atoms")

        organic_scores = []
        for atom in texture_atoms:
            entropy = atom.metadata.get("entropy", 0)
            uniformity = atom.metadata.get("uniformity", 1)
            # Organic: moderate-high entropy, low uniformity, varied
            if entropy > 2.0 and uniformity < 0.4:
                organic_scores.append(entropy / 4.0)

        if organic_scores and len(organic_scores) > len(texture_atoms) * 0.2:
            return FeatureValue.detected(
                confidence=min(np.mean(organic_scores), 1.0),
                evidence=[f"organic texture in {len(organic_scores)} patches"],
            )
        return FeatureValue.absent("no organic texture pattern")


@register_feature(name="manufactured_smooth_surface", tags=["texture", "object"], description="Smooth manufactured surface (teapot glaze, ceramic, metal)")
class ManufacturedSmoothSurface:
    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        if graph.raw_image is None:
            return FeatureValue.absent("no raw image")
        import cv2
        gray = cv2.cvtColor(graph.raw_image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        mag = np.sqrt(gx**2 + gy**2)
        smooth_pct = float((mag < 10).sum()) / (h * w)
        if smooth_pct > 0.08:
            return FeatureValue.detected(
                confidence=min(smooth_pct * 5, 1.0),
                evidence=[f"smooth_surface={smooth_pct:.3f}"],
            )
        return FeatureValue.absent(f"smooth_pct={smooth_pct:.3f} < 0.08")
