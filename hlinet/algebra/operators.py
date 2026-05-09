"""Algebraic operators for composing features into complex predicates.

These operators take Features and return new Features, enabling compositional
construction of visual concepts from primitives.
"""

from __future__ import annotations

from hlinet.types import Feature, FeatureValue, Region, SceneGraph
from hlinet.registry import registry


class CompositeFeature:
    """Base for algebra-composed features."""
    version = "1.0"
    tags: list[str] = ["composite"]


class AND(CompositeFeature):
    def __init__(self, *feature_names: str, name: str = "", description: str = ""):
        self.feature_names = feature_names
        self.name = name or f"AND({', '.join(feature_names)})"
        self.description = description or f"All of: {', '.join(feature_names)}"

    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        sub_values = {}
        min_confidence = 1.0
        all_present = True
        evidence = []

        for fname in self.feature_names:
            feat = registry.get_feature(fname)
            val = feat.evaluate(graph, region)
            sub_values[fname] = val
            if not val.present:
                all_present = False
                evidence.append(f"missing: {fname}")
            else:
                min_confidence = min(min_confidence, val.confidence)
                evidence.append(f"{fname}: {val.confidence:.2f}")

        return FeatureValue(
            present=all_present,
            confidence=min_confidence if all_present else 0.0,
            evidence=evidence,
            sub_values=sub_values,
        )


class OR(CompositeFeature):
    def __init__(self, *feature_names: str, name: str = "", description: str = ""):
        self.feature_names = feature_names
        self.name = name or f"OR({', '.join(feature_names)})"
        self.description = description or f"Any of: {', '.join(feature_names)}"

    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        sub_values = {}
        max_confidence = 0.0
        any_present = False
        evidence = []

        for fname in self.feature_names:
            feat = registry.get_feature(fname)
            val = feat.evaluate(graph, region)
            sub_values[fname] = val
            if val.present:
                any_present = True
                max_confidence = max(max_confidence, val.confidence)
                evidence.append(f"{fname}: {val.confidence:.2f}")

        return FeatureValue(
            present=any_present,
            confidence=max_confidence,
            evidence=evidence,
            sub_values=sub_values,
        )


class NOT(CompositeFeature):
    def __init__(self, feature_name: str, name: str = "", description: str = ""):
        self.feature_name = feature_name
        self.name = name or f"NOT({feature_name})"
        self.description = description or f"Absence of: {feature_name}"
        self.feature_names = [feature_name]

    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        feat = registry.get_feature(self.feature_name)
        val = feat.evaluate(graph, region)
        return FeatureValue(
            present=not val.present,
            confidence=1.0 - val.confidence,
            evidence=[f"NOT {self.feature_name}: {'absent' if not val.present else 'present'}"],
            sub_values={self.feature_name: val},
        )


class EXISTS(CompositeFeature):
    """True if at least one region in the graph satisfies the feature."""
    def __init__(self, feature_name: str, name: str = "", description: str = ""):
        self.feature_name = feature_name
        self.name = name or f"EXISTS({feature_name})"
        self.description = description or f"Exists region with: {feature_name}"
        self.feature_names = [feature_name]

    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        feat = registry.get_feature(self.feature_name)
        best_val = FeatureValue.absent()

        for r in graph.regions:
            val = feat.evaluate(graph, r)
            if val.confidence > best_val.confidence:
                best_val = val

        return FeatureValue(
            present=best_val.present,
            confidence=best_val.confidence,
            region=best_val.region,
            evidence=[f"best region score for {self.feature_name}: {best_val.confidence:.2f}"],
            sub_values={self.feature_name: best_val},
        )


class COUNT_GE(CompositeFeature):
    """True if at least `k` regions satisfy the feature above threshold."""
    def __init__(self, feature_name: str, k: int, threshold: float = 0.5, name: str = "", description: str = ""):
        self.feature_name = feature_name
        self.k = k
        self.threshold = threshold
        self.name = name or f"COUNT_GE({feature_name}, {k})"
        self.description = description or f"At least {k} regions with {feature_name}"
        self.feature_names = [feature_name]

    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        feat = registry.get_feature(self.feature_name)
        count = 0

        for r in graph.regions:
            val = feat.evaluate(graph, r)
            if val.present and val.confidence >= self.threshold:
                count += 1

        satisfied = count >= self.k
        return FeatureValue(
            present=satisfied,
            confidence=min(count / self.k, 1.0) if self.k > 0 else 1.0,
            evidence=[f"found {count}/{self.k} regions with {self.feature_name}"],
        )


class THRESHOLD(CompositeFeature):
    """Gate a feature by a confidence threshold."""
    def __init__(self, feature_name: str, threshold: float, name: str = "", description: str = ""):
        self.feature_name = feature_name
        self.threshold = threshold
        self.name = name or f"THRESHOLD({feature_name}, {threshold})"
        self.description = description or f"{feature_name} above {threshold}"
        self.feature_names = [feature_name]

    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        feat = registry.get_feature(self.feature_name)
        val = feat.evaluate(graph, region)
        passes = val.confidence >= self.threshold
        return FeatureValue(
            present=passes,
            confidence=val.confidence if passes else 0.0,
            region=val.region,
            evidence=[f"{self.feature_name} = {val.confidence:.2f} {'>=' if passes else '<'} {self.threshold}"],
            sub_values={self.feature_name: val},
        )


class IF_THEN(CompositeFeature):
    """Conditional: only evaluate `then_feature` if `condition_feature` is present."""
    def __init__(self, condition: str, then_feature: str, name: str = "", description: str = ""):
        self.condition = condition
        self.then_feature = then_feature
        self.name = name or f"IF({condition})_THEN({then_feature})"
        self.description = description or f"If {condition}, then check {then_feature}"
        self.feature_names = [condition, then_feature]

    def evaluate(self, graph: SceneGraph, region: Region | None = None) -> FeatureValue:
        cond_feat = registry.get_feature(self.condition)
        cond_val = cond_feat.evaluate(graph, region)

        if not cond_val.present:
            return FeatureValue(
                present=False,
                confidence=0.0,
                evidence=[f"condition {self.condition} not met"],
                sub_values={self.condition: cond_val},
            )

        then_feat = registry.get_feature(self.then_feature)
        then_val = then_feat.evaluate(graph, region)

        return FeatureValue(
            present=then_val.present,
            confidence=cond_val.confidence * then_val.confidence,
            region=then_val.region,
            evidence=[f"condition {self.condition}: {cond_val.confidence:.2f}", f"then {self.then_feature}: {then_val.confidence:.2f}"],
            sub_values={self.condition: cond_val, self.then_feature: then_val},
        )
