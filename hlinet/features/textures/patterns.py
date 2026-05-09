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

        # Stripes require: strong orientation consistency across multiple patches
        # AND alternating light/dark pattern (not just generic texture)
        gabor_atoms = [a for a in texture_atoms if "dominant_orientation" in a.metadata]
        if len(gabor_atoms) < 4:
            return FeatureValue.absent("too few texture patches for stripe detection")

        # Check orientation consistency: stripes have ONE dominant orientation
        orientations = [a.metadata["dominant_orientation"] for a in gabor_atoms]
        from collections import Counter
        orient_counts = Counter(orientations)
        most_common_orient, most_common_count = orient_counts.most_common(1)[0]
        consistency = most_common_count / len(orientations)

        # Also need high contrast / energy in that orientation
        high_energy_patches = [
            a for a in gabor_atoms
            if a.metadata.get("energy", 0) > 0.3
            and a.metadata["dominant_orientation"] == most_common_orient
        ]
        energy_ratio = len(high_energy_patches) / max(len(gabor_atoms), 1)

        # Strong stripes: >70% patches share orientation AND have high energy
        score = consistency * 0.6 + energy_ratio * 0.4
        if score > 0.55 and consistency > 0.6:
            return FeatureValue.detected(
                confidence=min(score, 1.0),
                evidence=[f"stripe: orient_consistency={consistency:.2f}, energy_ratio={energy_ratio:.2f}"],
            )
        return FeatureValue.absent(f"weak stripe signal: consistency={consistency:.2f}")


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

        smooth_count = 0
        for atom in texture_atoms:
            entropy = atom.metadata.get("entropy", 5)
            uniformity = atom.metadata.get("uniformity", 0)
            if entropy < 2.0 or uniformity > 0.5:
                smooth_count += 1

        ratio = smooth_count / len(texture_atoms)
        if ratio > 0.4:
            return FeatureValue.detected(
                confidence=min(ratio, 1.0),
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
