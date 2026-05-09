#!/usr/bin/env python3
"""Quick demo: create a synthetic test image and run the full pipeline."""

import sys
import numpy as np
import cv2

# Add parent to path for direct execution
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

from hlinet.classifier.predict import predict
from hlinet.proof.trace import render_proof
from hlinet.registry import registry


def create_test_images() -> dict[str, np.ndarray]:
    """Create simple synthetic images for testing the pipeline."""
    images = {}

    # Zebra-like: black and white stripes
    zebra = np.zeros((224, 224, 3), dtype=np.uint8)
    for i in range(0, 224, 20):
        zebra[i:i+10, :] = 255
    images["zebra_synthetic"] = zebra

    # School bus-like: large yellow rectangle
    bus = np.zeros((224, 224, 3), dtype=np.uint8)
    bus[40:180, 20:200] = (0, 200, 255)  # yellow in BGR
    cv2.circle(bus, (60, 180), 20, (50, 50, 50), -1)
    cv2.circle(bus, (160, 180), 20, (50, 50, 50), -1)
    images["school_bus_synthetic"] = bus

    # Banana-like: yellow elongated curve
    banana = np.zeros((224, 224, 3), dtype=np.uint8) + 100
    cv2.ellipse(banana, (112, 112), (80, 30), 30, 0, 360, (0, 220, 255), -1)
    images["banana_synthetic"] = banana

    # Bicycle-like: two circles with connecting frame
    bike = np.ones((224, 224, 3), dtype=np.uint8) * 200
    cv2.circle(bike, (70, 150), 40, (0, 0, 0), 3)
    cv2.circle(bike, (154, 150), 40, (0, 0, 0), 3)
    cv2.line(bike, (70, 150), (112, 80), (0, 0, 0), 3)
    cv2.line(bike, (154, 150), (112, 80), (0, 0, 0), 3)
    images["bicycle_synthetic"] = bike

    return images


def main():
    print("=" * 60)
    print("HL-Image-Net Demo: Symbolic Visual Algebra")
    print("=" * 60)
    print()
    print(f"Registered sensors: {len(registry.sensors)}")
    print(f"Registered features: {len(registry.features)}")
    print()

    images = create_test_images()

    for name, image in images.items():
        print(f"\n{'─' * 60}")
        print(f"Image: {name} ({image.shape})")
        print(f"{'─' * 60}")

        result = predict(image)
        print(render_proof(result))
        print()


if __name__ == "__main__":
    main()
