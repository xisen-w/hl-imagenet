"""Global registry for sensors and features with autodiscovery."""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Any

from hlinet.types import Feature, Sensor


class Registry:
    def __init__(self):
        self._sensors: dict[str, Sensor] = {}
        self._features: dict[str, Feature] = {}

    def register_sensor(self, sensor: Sensor) -> None:
        self._sensors[sensor.name] = sensor

    def register_feature(self, feature: Feature) -> None:
        self._features[feature.name] = feature

    def get_sensor(self, name: str) -> Sensor:
        return self._sensors[name]

    def get_feature(self, name: str) -> Feature:
        return self._features[name]

    @property
    def sensors(self) -> list[Sensor]:
        return list(self._sensors.values())

    @property
    def features(self) -> list[Feature]:
        return list(self._features.values())

    def features_by_tag(self, tag: str) -> list[Feature]:
        return [f for f in self._features.values() if tag in f.tags]

    def discover_package(self, package_path: str) -> None:
        """Import all modules in a package to trigger registration."""
        try:
            pkg = importlib.import_module(package_path)
        except ImportError:
            return
        if not hasattr(pkg, "__path__"):
            return
        for _, module_name, is_pkg in pkgutil.walk_packages(pkg.__path__, prefix=package_path + "."):
            if module_name.endswith("__init__"):
                continue
            try:
                importlib.import_module(module_name)
            except Exception:
                pass

    def discover_directory(self, directory: Path) -> None:
        """Import all .py files in a directory to trigger registration."""
        if not directory.exists():
            return
        for py_file in directory.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue
            module_path = py_file.with_suffix("")
            parts = module_path.parts
            try:
                hlinet_idx = parts.index("hlinet")
                module_name = ".".join(parts[hlinet_idx:])
                importlib.import_module(module_name)
            except (ValueError, ImportError):
                pass

    def summary(self) -> str:
        lines = [
            f"Registry: {len(self._sensors)} sensors, {len(self._features)} features",
            "",
            "Sensors:",
        ]
        for s in self._sensors.values():
            lines.append(f"  {s.name} → {s.output_kinds}")
        lines.append("")
        lines.append("Features:")
        for f in self._features.values():
            lines.append(f"  {f.name} v{f.version} [{', '.join(f.tags)}]")
        return "\n".join(lines)


registry = Registry()


def register_feature(
    name: str,
    tags: list[str] | None = None,
    description: str = "",
    version: str = "1.0",
):
    """Decorator to register a feature class with the global registry."""
    def decorator(cls: type) -> type:
        cls.name = name
        cls.tags = tags or []
        cls.description = description
        cls.version = version
        instance = cls()
        registry.register_feature(instance)
        return cls
    return decorator


def get_feature(name: str):
    """Get a registered feature instance by name, or None if not found."""
    try:
        return registry.get_feature(name)
    except KeyError:
        return None


def register_sensor(name: str, output_kinds: list[str] | None = None):
    """Decorator to register a sensor class with the global registry."""
    def decorator(cls: type) -> type:
        cls.name = name
        cls.output_kinds = output_kinds or []
        instance = cls()
        registry.register_sensor(instance)
        return cls
    return decorator
