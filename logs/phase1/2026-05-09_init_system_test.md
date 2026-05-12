# System Initialization Test — 2026-05-09

## Status: PASS

The full pipeline runs end-to-end on synthetic images.

## Registered Components

- **Sensors**: 10 (canny_edges, contour_shapes, color_regions, color_histogram, lbp_texture, gabor_texture, superpixel_segments, felzenszwalb_segments, hough_circles, hough_lines)
- **Features**: 21 (4 color primitives, 4 shape primitives, 4 texture patterns, 5 structural parts, 4 high-level concepts)

## Pipeline Test

Tested on 4 synthetic images (colored rectangles/circles, not real photos).
- Pipeline executes without errors
- All sensors produce atoms
- Scene graphs are built correctly
- Features evaluate and return structured FeatureValues
- Hierarchical routing activates correct branches
- Proofs are generated with evidence chains

## Observations

1. Synthetic images trigger features in non-obvious ways (e.g., stripes on a striped rectangle register as both "zebra stripes" and "keyboard pattern") — this is expected since features need real visual complexity to discriminate
2. Feature confidence calibration will need tuning on real images
3. The `handle_spout` feature fires too easily (false positives on any adjacent segments)
4. `bilateral_symmetry` fires very strongly on simple geometric shapes

## Next Steps

1. Download real ImageNet subset (10 classes, ~100 images each)
2. Run evaluation on real images to get baseline accuracy
3. Calibrate feature thresholds
4. Run agent loop to identify and fix worst confusions
