# CNN vs Symbolic Gap Mining

Split: `val`
Samples: 20

## Outcome Counts

- both_correct: 12
- cnn_correct_symbolic_wrong: 5
- symbolic_correct_cnn_wrong: 0
- both_wrong: 3

## Top CNN-Correct / Symbolic-Wrong Groups

### golden_retriever -> symbolic mushroom (1 cases)

- CNN true prob avg: 0.3775
- Symbolic confidence avg: 0.6308
- Top occlusion regions: [('center', 2), ('middle_left', 1)]
- Mean top-patch stats: `{'blue_frac': 0.0, 'edge_density': 0.341, 'green_frac': 0.0, 'mean_hue': 16.797, 'mean_sat': 0.515, 'mean_val': 0.642, 'texture_lap_var': 7549.733, 'warm_frac': 0.943, 'yellow_frac': 0.806}`
- Feature hint: For true golden_retriever misread as mushroom, the CNN often relies on edge-dense, warm-color, yellow, high-texture evidence in center, middle_left. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against mushroom.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_181551/visuals/golden_retriever_as_mushroom_1.jpg`

### mushroom -> symbolic golden_retriever (1 cases)

- CNN true prob avg: 0.3394
- Symbolic confidence avg: 0.5871
- Top occlusion regions: [('bottom_center', 3)]
- Mean top-patch stats: `{'blue_frac': 0.0, 'edge_density': 0.28, 'green_frac': 0.0, 'mean_hue': 25.433, 'mean_sat': 0.624, 'mean_val': 0.194, 'texture_lap_var': 2542.533, 'warm_frac': 0.444, 'yellow_frac': 0.038}`
- Feature hint: For true mushroom misread as golden_retriever, the CNN often relies on edge-dense, warm-color evidence in bottom_center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against golden_retriever.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_181551/visuals/mushroom_as_golden_retriever_1.jpg`

### teapot -> symbolic banana (1 cases)

- CNN true prob avg: 0.3782
- Symbolic confidence avg: 0.6162
- Top occlusion regions: [('top_center', 3)]
- Mean top-patch stats: `{'blue_frac': 0.0, 'edge_density': 0.229, 'green_frac': 0.0, 'mean_hue': 15.253, 'mean_sat': 0.352, 'mean_val': 0.403, 'texture_lap_var': 1773.867, 'warm_frac': 0.775, 'yellow_frac': 0.638}`
- Feature hint: For true teapot misread as banana, the CNN often relies on edge-dense, warm-color, yellow evidence in top_center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against banana.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_181551/visuals/teapot_as_banana_1.jpg`
