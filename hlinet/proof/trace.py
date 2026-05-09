"""Proof trace rendering — human-readable and structured formats."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime

from hlinet.types import Prediction


def render_proof(prediction: Prediction) -> str:
    """Render a prediction as a human-readable proof."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"CLASSIFICATION: {prediction.label}")
    lines.append(f"CONFIDENCE:     {prediction.confidence:.3f}")
    lines.append("=" * 60)

    if prediction.route:
        lines.append(f"Route: {' → '.join(prediction.route)}")
        lines.append("")

    lines.append("PROOF:")
    for line in prediction.proof:
        lines.append(f"  {line}")

    if prediction.alternatives:
        lines.append("")
        lines.append("ALTERNATIVES:")
        for label, score in prediction.alternatives:
            lines.append(f"  {label}: {score:.3f}")

    lines.append("=" * 60)
    return "\n".join(lines)


def proof_to_dict(prediction: Prediction) -> dict:
    """Convert a prediction to a serializable dict."""
    return {
        "label": prediction.label,
        "confidence": prediction.confidence,
        "alternatives": [{"label": l, "score": s} for l, s in prediction.alternatives],
        "proof": prediction.proof,
        "route": prediction.route,
        "features": {
            name: {
                "present": val.present,
                "confidence": val.confidence,
                "evidence": val.evidence,
            }
            for name, val in prediction.feature_activations.items()
        },
        "timestamp": datetime.now().isoformat(),
    }


def proof_to_json(prediction: Prediction) -> str:
    """Serialize a prediction proof as JSON."""
    return json.dumps(proof_to_dict(prediction), indent=2)
