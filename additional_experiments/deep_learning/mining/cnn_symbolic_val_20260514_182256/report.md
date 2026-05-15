# CNN vs Symbolic Gap Mining

Split: `val`
Samples: 2000

## Outcome Counts

- both_correct: 893
- cnn_correct_symbolic_wrong: 543
- symbolic_correct_cnn_wrong: 107
- both_wrong: 457

## Top CNN-Correct / Symbolic-Wrong Groups

### orange -> symbolic banana (3 cases)

- CNN true prob avg: 0.9803
- Symbolic confidence avg: 0.657
- Top occlusion regions: [('bottom_center', 4), ('middle_left', 2), ('center', 2), ('bottom_left', 1)]
- Mean top-patch stats: `{'blue_frac': 0.0, 'edge_density': 0.211, 'green_frac': 0.0, 'mean_hue': 18.619, 'mean_sat': 0.898, 'mean_val': 0.939, 'texture_lap_var': 3253.722, 'warm_frac': 0.997, 'yellow_frac': 0.991}`
- Feature hint: For true orange misread as banana, the CNN often relies on edge-dense, warm-color, yellow evidence in bottom_center, middle_left, center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against banana.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/orange_as_banana_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/orange_as_banana_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/orange_as_banana_3.jpg`

### sports_car -> symbolic school_bus (3 cases)

- CNN true prob avg: 0.9595
- Symbolic confidence avg: 0.7014
- Top occlusion regions: [('middle_left', 2), ('center', 2), ('top_center', 2), ('bottom_right', 1), ('bottom_left', 1), ('bottom_center', 1)]
- Mean top-patch stats: `{'blue_frac': 0.049, 'edge_density': 0.289, 'green_frac': 0.025, 'mean_hue': 66.079, 'mean_sat': 0.221, 'mean_val': 0.381, 'texture_lap_var': 15780.233, 'warm_frac': 0.156, 'yellow_frac': 0.113}`
- Feature hint: For true sports_car misread as school_bus, the CNN often relies on edge-dense, high-texture evidence in middle_left, center, top_center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against school_bus.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/sports_car_as_school_bus_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/sports_car_as_school_bus_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/sports_car_as_school_bus_3.jpg`

### brown_bear -> symbolic mushroom (3 cases)

- CNN true prob avg: 0.9432
- Symbolic confidence avg: 0.5277
- Top occlusion regions: [('middle_right', 4), ('middle_left', 2), ('center', 2), ('bottom_center', 1)]
- Mean top-patch stats: `{'blue_frac': 0.01, 'edge_density': 0.331, 'green_frac': 0.0, 'mean_hue': 29.6, 'mean_sat': 0.439, 'mean_val': 0.452, 'texture_lap_var': 7670.233, 'warm_frac': 0.672, 'yellow_frac': 0.179}`
- Feature hint: For true brown_bear misread as mushroom, the CNN often relies on edge-dense, warm-color, yellow, high-texture evidence in middle_right, middle_left, center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against mushroom.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_mushroom_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_mushroom_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_mushroom_3.jpg`

### golden_retriever -> symbolic banana (3 cases)

- CNN true prob avg: 0.9341
- Symbolic confidence avg: 0.6001
- Top occlusion regions: [('center', 4), ('middle_left', 2), ('top_left', 1), ('middle_right', 1), ('top_center', 1)]
- Mean top-patch stats: `{'blue_frac': 0.001, 'edge_density': 0.317, 'green_frac': 0.0, 'mean_hue': 17.287, 'mean_sat': 0.523, 'mean_val': 0.493, 'texture_lap_var': 1155.944, 'warm_frac': 0.892, 'yellow_frac': 0.356}`
- Feature hint: For true golden_retriever misread as banana, the CNN often relies on edge-dense, warm-color, yellow evidence in center, middle_left, top_left. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against banana.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/golden_retriever_as_banana_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/golden_retriever_as_banana_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/golden_retriever_as_banana_3.jpg`

### brown_bear -> symbolic golden_retriever (3 cases)

- CNN true prob avg: 0.898
- Symbolic confidence avg: 0.5801
- Top occlusion regions: [('middle_left', 4), ('center', 4), ('bottom_left', 1)]
- Mean top-patch stats: `{'blue_frac': 0.0, 'edge_density': 0.274, 'green_frac': 0.0, 'mean_hue': 22.843, 'mean_sat': 0.559, 'mean_val': 0.272, 'texture_lap_var': 3524.378, 'warm_frac': 0.444, 'yellow_frac': 0.137}`
- Feature hint: For true brown_bear misread as golden_retriever, the CNN often relies on edge-dense, warm-color evidence in middle_left, center, bottom_left. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against golden_retriever.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_golden_retriever_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_golden_retriever_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_golden_retriever_3.jpg`

### mushroom -> symbolic brown_bear (3 cases)

- CNN true prob avg: 0.8114
- Symbolic confidence avg: 0.5684
- Top occlusion regions: [('bottom_center', 4), ('bottom_left', 2), ('bottom_right', 1), ('middle_right', 1), ('middle_left', 1)]
- Mean top-patch stats: `{'blue_frac': 0.01, 'edge_density': 0.361, 'green_frac': 0.087, 'mean_hue': 49.98, 'mean_sat': 0.404, 'mean_val': 0.266, 'texture_lap_var': 16821.9, 'warm_frac': 0.219, 'yellow_frac': 0.071}`
- Feature hint: For true mushroom misread as brown_bear, the CNN often relies on edge-dense, high-texture evidence in bottom_center, bottom_left, bottom_right. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against brown_bear.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/mushroom_as_brown_bear_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/mushroom_as_brown_bear_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/mushroom_as_brown_bear_3.jpg`

### sports_car -> symbolic king_penguin (3 cases)

- CNN true prob avg: 0.9712
- Symbolic confidence avg: 0.5905
- Top occlusion regions: [('middle_left', 3), ('center', 2), ('top_right', 1), ('top_center', 1), ('bottom_right', 1), ('bottom_center', 1)]
- Mean top-patch stats: `{'blue_frac': 0.07, 'edge_density': 0.257, 'green_frac': 0.003, 'mean_hue': 84.692, 'mean_sat': 0.317, 'mean_val': 0.391, 'texture_lap_var': 15357.011, 'warm_frac': 0.021, 'yellow_frac': 0.009}`
- Feature hint: For true sports_car misread as king_penguin, the CNN often relies on edge-dense, high-texture evidence in middle_left, center, top_right. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against king_penguin.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/sports_car_as_king_penguin_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/sports_car_as_king_penguin_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/sports_car_as_king_penguin_3.jpg`

### banana -> symbolic school_bus (3 cases)

- CNN true prob avg: 0.9223
- Symbolic confidence avg: 0.4863
- Top occlusion regions: [('top_center', 2), ('middle_right', 2), ('bottom_center', 2), ('middle_left', 1), ('center', 1), ('bottom_right', 1)]
- Mean top-patch stats: `{'blue_frac': 0.002, 'edge_density': 0.268, 'green_frac': 0.291, 'mean_hue': 31.053, 'mean_sat': 0.657, 'mean_val': 0.776, 'texture_lap_var': 9634.889, 'warm_frac': 0.867, 'yellow_frac': 0.805}`
- Feature hint: For true banana misread as school_bus, the CNN often relies on edge-dense, warm-color, yellow, green-context, high-texture evidence in top_center, middle_right, bottom_center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against school_bus.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/banana_as_school_bus_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/banana_as_school_bus_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/banana_as_school_bus_3.jpg`

### brown_bear -> symbolic king_penguin (3 cases)

- CNN true prob avg: 0.7431
- Symbolic confidence avg: 0.4635
- Top occlusion regions: [('center', 7), ('middle_left', 1), ('bottom_center', 1)]
- Mean top-patch stats: `{'blue_frac': 0.188, 'edge_density': 0.303, 'green_frac': 0.11, 'mean_hue': 73.766, 'mean_sat': 0.22, 'mean_val': 0.305, 'texture_lap_var': 5843.5, 'warm_frac': 0.01, 'yellow_frac': 0.0}`
- Feature hint: For true brown_bear misread as king_penguin, the CNN often relies on edge-dense, blue/purple, high-texture evidence in center, middle_left, bottom_center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against king_penguin.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_king_penguin_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_king_penguin_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/brown_bear_as_king_penguin_3.jpg`

### mushroom -> symbolic banana (3 cases)

- CNN true prob avg: 0.8239
- Symbolic confidence avg: 0.577
- Top occlusion regions: [('center', 3), ('bottom_center', 2), ('bottom_left', 2), ('top_center', 1), ('top_left', 1)]
- Mean top-patch stats: `{'blue_frac': 0.0, 'edge_density': 0.289, 'green_frac': 0.398, 'mean_hue': 27.797, 'mean_sat': 0.561, 'mean_val': 0.5, 'texture_lap_var': 9064.389, 'warm_frac': 0.83, 'yellow_frac': 0.378}`
- Feature hint: For true mushroom misread as banana, the CNN often relies on edge-dense, warm-color, yellow, green-context, high-texture evidence in center, bottom_center, bottom_left. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against banana.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/mushroom_as_banana_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/mushroom_as_banana_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/mushroom_as_banana_3.jpg`

### teapot -> symbolic banana (3 cases)

- CNN true prob avg: 0.6614
- Symbolic confidence avg: 0.6705
- Top occlusion regions: [('bottom_center', 3), ('top_center', 2), ('center', 2), ('top_right', 1), ('bottom_left', 1)]
- Mean top-patch stats: `{'blue_frac': 0.0, 'edge_density': 0.179, 'green_frac': 0.0, 'mean_hue': 18.93, 'mean_sat': 0.564, 'mean_val': 0.49, 'texture_lap_var': 2782.567, 'warm_frac': 0.849, 'yellow_frac': 0.543}`
- Feature hint: For true teapot misread as banana, the CNN often relies on warm-color, yellow evidence in bottom_center, top_center, center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against banana.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/teapot_as_banana_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/teapot_as_banana_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/teapot_as_banana_3.jpg`

### king_penguin -> symbolic sports_car (3 cases)

- CNN true prob avg: 0.9716
- Symbolic confidence avg: 0.5057
- Top occlusion regions: [('middle_left', 3), ('bottom_right', 2), ('center', 2), ('bottom_left', 2)]
- Mean top-patch stats: `{'blue_frac': 0.106, 'edge_density': 0.194, 'green_frac': 0.173, 'mean_hue': 79.158, 'mean_sat': 0.19, 'mean_val': 0.605, 'texture_lap_var': 8125.067, 'warm_frac': 0.101, 'yellow_frac': 0.053}`
- Feature hint: For true king_penguin misread as sports_car, the CNN often relies on green-context, high-texture evidence in middle_left, bottom_right, center. Candidate symbolic direction: add a local patch/grid detector for this evidence and gate it against sports_car.
- Example visuals:
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/king_penguin_as_sports_car_1.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/king_penguin_as_sports_car_2.jpg`
  - `additional_experiments/deep_learning/mining/cnn_symbolic_val_20260514_182256/visuals/king_penguin_as_sports_car_3.jpg`
