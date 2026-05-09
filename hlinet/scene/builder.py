"""Orchestrates sensors → atoms → scene graph."""

from __future__ import annotations

import cv2
import networkx as nx
import numpy as np

from hlinet.registry import registry
from hlinet.scene.relations import infer_relations
from hlinet.types import Atom, Region, SceneGraph


class SceneGraphBuilder:
    def __init__(self, max_atoms_per_sensor: int = 50):
        self.max_atoms_per_sensor = max_atoms_per_sensor

    def build(self, image: np.ndarray) -> SceneGraph:
        all_atoms = self._extract_atoms(image)
        graph = self._build_graph(all_atoms, image.shape)
        return SceneGraph(graph=graph, image_shape=image.shape, atoms=all_atoms)

    def _extract_atoms(self, image: np.ndarray) -> list[Atom]:
        all_atoms = []
        for sensor in registry.sensors:
            try:
                atoms = sensor.extract(image)
                all_atoms.extend(atoms[:self.max_atoms_per_sensor])
            except Exception:
                continue
        return all_atoms

    def _build_graph(self, atoms: list[Atom], image_shape: tuple) -> nx.DiGraph:
        G = nx.DiGraph()

        for i, atom in enumerate(atoms):
            G.add_node(i, **{
                "kind": atom.kind,
                "region": atom.region,
                "descriptor": atom.descriptor,
                "confidence": atom.confidence,
                "metadata": atom.metadata,
            })

        regions = [(i, atom.region) for i, atom in enumerate(atoms)
                   if atom.region.area_fraction > 0.01]

        relations = infer_relations(regions)
        for src, tgt, rel_type, conf in relations:
            G.add_edge(src, tgt, type=rel_type, confidence=conf)

        return G
