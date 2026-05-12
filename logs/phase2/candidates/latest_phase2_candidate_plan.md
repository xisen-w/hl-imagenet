# HL-ImageNet Phase 2 Candidate Selection Plan

Generated: `2026-05-12T12:37:24`

## Summary

- Samples: `2000`
- Accuracy: `0.334`
- Top-3 accuracy: `0.686`
- Baseline-right / HL-wrong: `817`
- HL-right / all-baselines-wrong: `68`
- Outcome counts: `{'miss': 627, 'top3_rescue': 705, 'correct': 668}`

## Benchmark interpretation

- HL top-1: `0.334`
- HL top-3: `0.686`
- HL above: `['majority_class', 'random']`
- HL below/equal: `['handcrafted_stats_knn', 'image_stats_centroid', 'color_centroid']`
- Interpretation: HL beats random/majority but candidate changes must aim to close gaps against handcrafted baselines.

## Top baseline-right / HL-wrong candidates

| True | HL Pred | Collapse | Margin | Correct baselines | File |
|---|---|---|---:|---|---|
| brown_bear | banana | brown_bear->banana | 0.280 | image_stats_centroid, handcrafted_stats_knn | n02132136_390.JPEG |
| golden_retriever | banana | golden_retriever->banana | 0.266 | image_stats_centroid, handcrafted_stats_knn | n02099601_280.JPEG |
| banana | king_penguin | banana->king_penguin | 0.263 | majority_class | n07753592_338.JPEG |
| mushroom | king_penguin | mushroom->king_penguin | 0.259 | color_centroid, image_stats_centroid | n07734744_317.JPEG |
| banana | king_penguin | banana->king_penguin | 0.258 | majority_class, handcrafted_stats_knn | n07753592_397.JPEG |
| banana | king_penguin | banana->king_penguin | 0.255 | majority_class, handcrafted_stats_knn | n07753592_304.JPEG |
| brown_bear | banana | brown_bear->banana | 0.251 | image_stats_centroid | n02132136_293.JPEG |
| brown_bear | king_penguin | brown_bear->king_penguin | 0.247 | handcrafted_stats_knn | n02132136_421.JPEG |
| golden_retriever | banana | golden_retriever->banana | 0.246 | color_centroid, image_stats_centroid, handcrafted_stats_knn | n02099601_420.JPEG |
| golden_retriever | banana | golden_retriever->banana | 0.243 | image_stats_centroid | n02099601_32.JPEG |
| brown_bear | banana | brown_bear->banana | 0.240 | handcrafted_stats_knn | n02132136_398.JPEG |
| golden_retriever | banana | golden_retriever->banana | 0.239 | handcrafted_stats_knn | n02099601_312.JPEG |
| golden_retriever | king_penguin | golden_retriever->king_penguin | 0.238 | color_centroid | n02099601_422.JPEG |
| golden_retriever | banana | golden_retriever->banana | 0.237 | color_centroid, image_stats_centroid, handcrafted_stats_knn | n02099601_302.JPEG |
| brown_bear | banana | brown_bear->banana | 0.237 | image_stats_centroid | n02132136_424.JPEG |
| brown_bear | banana | brown_bear->banana | 0.236 | handcrafted_stats_knn | n02132136_41.JPEG |
| brown_bear | banana | brown_bear->banana | 0.236 | handcrafted_stats_knn | n02132136_290.JPEG |
| sports_car | king_penguin | sports_car->king_penguin | 0.234 | color_centroid, image_stats_centroid, handcrafted_stats_knn | n04285008_28.JPEG |
| teapot | king_penguin | teapot->king_penguin | 0.233 | random, handcrafted_stats_knn | n04398044_340.JPEG |
| sports_car | king_penguin | sports_car->king_penguin | 0.231 | handcrafted_stats_knn | n04285008_284.JPEG |
| jellyfish | king_penguin | jellyfish->king_penguin | 0.231 | color_centroid, image_stats_centroid | n01910747_450.JPEG |
| teapot | banana | teapot->banana | 0.228 | handcrafted_stats_knn | n04398044_429.JPEG |
| teapot | banana | teapot->banana | 0.226 | handcrafted_stats_knn | n04398044_423.JPEG |
| brown_bear | banana | brown_bear->banana | 0.224 | random, handcrafted_stats_knn | n02132136_289.JPEG |
| king_penguin | banana | king_penguin->banana | 0.220 | random | n02056570_320.JPEG |

## Top HL-right / all-baselines-wrong candidates

| True | HL Pred | Margin | File | Top features |
|---|---|---:|---|---|
| king_penguin | king_penguin | 0.243 | n02056570_364.JPEG | bilateral_symmetry, phase2_king_penguin_signature, black_white_dominant, phase2_sports_car_signature |
| jellyfish | jellyfish | 0.164 | n01910747_327.JPEG | bilateral_symmetry, phase2_jellyfish_signature, quadruped_like, phase2_sports_car_signature |
| king_penguin | king_penguin | 0.144 | n02056570_367.JPEG | bilateral_symmetry, phase2_king_penguin_signature, phase2_brown_bear_signature, phase2_sports_car_signature |
| king_penguin | king_penguin | 0.138 | n02056570_431.JPEG | black_white_dominant, bilateral_symmetry, quadruped_like, phase2_teapot_signature |
| king_penguin | king_penguin | 0.133 | n02056570_345.JPEG | black_white_dominant, rectangular_shape, bilateral_symmetry, phase2_king_penguin_signature |
| school_bus | school_bus | 0.133 | n04146614_34.JPEG | golden_fur_in_nature, yellow_body_with_sky, golden_brown_color, horizontal_window_pattern |
| golden_retriever | golden_retriever | 0.122 | n02099601_434.JPEG | golden_fur_in_nature, golden_brown_color, bilateral_symmetry, phase2_golden_retriever_signature |
| king_penguin | king_penguin | 0.121 | n02056570_340.JPEG | distinct_background, bilateral_symmetry, phase2_king_penguin_signature, phase2_mushroom_signature |
| king_penguin | king_penguin | 0.120 | n02056570_34.JPEG | blob_textured_interior, bilateral_symmetry, black_white_dominant, phase2_king_penguin_signature |
| king_penguin | king_penguin | 0.120 | n02056570_300.JPEG | bilateral_symmetry, phase2_king_penguin_signature, phase2_teapot_signature, quadruped_like |
| school_bus | school_bus | 0.119 | n04146614_311.JPEG | golden_fur_in_nature, yellow_dominant, horizontal_window_pattern, golden_brown_color |
| jellyfish | jellyfish | 0.116 | n01910747_306.JPEG | green_context, black_white_dominant, bilateral_symmetry, phase2_jellyfish_signature |
| school_bus | school_bus | 0.103 | n04146614_392.JPEG | golden_fur_in_nature, yellow_dominant, blob_textured_interior, yellow_body_with_sky |
| mushroom | mushroom | 0.100 | n07734744_405.JPEG | golden_fur_in_nature, bilateral_symmetry, phase2_mushroom_signature, blob_textured_interior |
| golden_retriever | golden_retriever | 0.090 | n02099601_438.JPEG | golden_brown_color, bilateral_symmetry, golden_fur_in_nature, quadruped_like |
| king_penguin | king_penguin | 0.088 | n02056570_36.JPEG | bilateral_symmetry, golden_fur_in_nature, quadruped_like, phase2_teapot_signature |
| golden_retriever | golden_retriever | 0.085 | n02099601_360.JPEG | golden_fur_in_nature, yellow_dominant, yellow_body_with_sky, golden_brown_color |
| golden_retriever | golden_retriever | 0.083 | n02099601_322.JPEG | golden_fur_in_nature, bilateral_symmetry, phase2_mushroom_signature, quadruped_like |
| king_penguin | king_penguin | 0.080 | n02056570_417.JPEG | black_white_dominant, bilateral_symmetry, phase2_sports_car_signature, phase2_teapot_signature |
| king_penguin | king_penguin | 0.080 | n02056570_329.JPEG | bilateral_symmetry, golden_fur_in_nature, phase2_king_penguin_signature, phase2_mushroom_signature |
| golden_retriever | golden_retriever | 0.078 | n02099601_354.JPEG | golden_fur_in_nature, distinct_background, yellow_body_with_sky, bilateral_symmetry |
| king_penguin | king_penguin | 0.077 | n02056570_392.JPEG | golden_fur_in_nature, bilateral_symmetry, blob_textured_interior, phase2_king_penguin_signature |
| golden_retriever | golden_retriever | 0.074 | n02099601_333.JPEG | golden_fur_in_nature, yellow_dominant, golden_brown_color, bilateral_symmetry |
| school_bus | school_bus | 0.071 | n04146614_319.JPEG | golden_fur_in_nature, blob_textured_interior, horizontal_window_pattern, bilateral_symmetry |
| golden_retriever | golden_retriever | 0.070 | n02099601_317.JPEG | yellow_body_with_sky, golden_fur_in_nature, distinct_background, bilateral_symmetry |

## Feature overactivation warnings

| Feature | Count | Rate | Top true classes |
|---|---:|---:|---|
| bilateral_symmetry | 2000 | 1.000 | golden_retriever:200, mushroom:200, teapot:200, school_bus:200, banana:200 |
| quadruped_like | 1966 | 0.983 | golden_retriever:200, brown_bear:199, sports_car:199, mushroom:198, king_penguin:198 |
| phase2_golden_retriever_signature | 1780 | 0.890 | orange:195, banana:191, jellyfish:191, teapot:189, golden_retriever:186 |
| phase2_teapot_signature | 1495 | 0.748 | jellyfish:185, orange:182, king_penguin:178, teapot:174, banana:167 |
| phase2_mushroom_signature | 1490 | 0.745 | mushroom:189, brown_bear:185, sports_car:180, school_bus:167, golden_retriever:164 |
| phase2_banana_signature | 1489 | 0.745 | orange:191, banana:188, mushroom:175, golden_retriever:172, teapot:162 |
| phase2_school_bus_signature | 1463 | 0.732 | school_bus:191, sports_car:188, brown_bear:166, mushroom:160, king_penguin:160 |
| phase2_brown_bear_signature | 1438 | 0.719 | brown_bear:192, king_penguin:188, sports_car:172, golden_retriever:170, mushroom:164 |
| golden_fur_in_nature | 1385 | 0.693 | orange:191, banana:189, school_bus:186, golden_retriever:178, mushroom:163 |
| phase2_king_penguin_signature | 1075 | 0.537 | king_penguin:181, sports_car:168, jellyfish:165, teapot:134, brown_bear:113 |
| phase2_sports_car_signature | 1051 | 0.525 | jellyfish:181, sports_car:169, king_penguin:150, teapot:114, school_bus:96 |
| phase2_orange_signature | 1024 | 0.512 | orange:185, jellyfish:171, banana:147, mushroom:105, golden_retriever:102 |
| golden_brown_color | 1003 | 0.501 | orange:176, banana:159, golden_retriever:149, brown_bear:127, teapot:102 |

## Victim rescue targets

| Class | Recall | Top-3 recall | Rescue gap | Misses | Top wrong predictions |
|---|---:|---:|---:|---:|---|
| teapot | 0.050 | 0.450 | 0.400 | 190 | king_penguin:72, golden_retriever:50, banana:43, mushroom:6, jellyfish:6 |
| brown_bear | 0.060 | 0.550 | 0.490 | 188 | banana:70, king_penguin:58, golden_retriever:32, mushroom:14, school_bus:5 |
| sports_car | 0.115 | 0.615 | 0.500 | 177 | king_penguin:113, school_bus:22, golden_retriever:21, banana:9, mushroom:7 |
| orange | 0.165 | 0.720 | 0.555 | 167 | banana:83, golden_retriever:61, teapot:9, king_penguin:6, school_bus:5 |
| mushroom | 0.220 | 0.550 | 0.330 | 156 | banana:67, king_penguin:35, golden_retriever:25, school_bus:11, teapot:8 |
| golden_retriever | 0.275 | 0.765 | 0.490 | 145 | banana:82, king_penguin:34, mushroom:9, school_bus:8, teapot:4 |
| school_bus | 0.575 | 0.850 | 0.275 | 85 | king_penguin:27, banana:22, mushroom:15, golden_retriever:13, sports_car:6 |
| banana | 0.580 | 0.795 | 0.215 | 84 | golden_retriever:27, teapot:18, king_penguin:12, school_bus:11, mushroom:7 |
| king_penguin | 0.645 | 0.800 | 0.155 | 71 | banana:30, jellyfish:16, teapot:8, golden_retriever:6, mushroom:5 |
| jellyfish | 0.655 | 0.770 | 0.115 | 69 | king_penguin:32, golden_retriever:10, banana:10, teapot:7, orange:5 |

## Attractor suppression targets

| Attractor | False-positive count | Top collapse paths |
|---|---:|---|
| banana | 416 | orange->banana:83, golden_retriever->banana:82, brown_bear->banana:70, mushroom->banana:67, teapot->banana:43, king_penguin->banana:30, school_bus->banana:22 |
| king_penguin | 389 | sports_car->king_penguin:113, teapot->king_penguin:72, brown_bear->king_penguin:58, mushroom->king_penguin:35, golden_retriever->king_penguin:34, jellyfish->king_penguin:32, school_bus->king_penguin:27, banana->king_penguin:12 |
| golden_retriever | 245 | orange->golden_retriever:61, teapot->golden_retriever:50, brown_bear->golden_retriever:32, banana->golden_retriever:27, mushroom->golden_retriever:25, sports_car->golden_retriever:21, school_bus->golden_retriever:13, jellyfish->golden_retriever:10 |
| school_bus | 72 | sports_car->school_bus:22, mushroom->school_bus:11, banana->school_bus:11 |
| mushroom | 66 | school_bus->mushroom:15, brown_bear->mushroom:14 |
| teapot | 57 | banana->teapot:18 |
| jellyfish | 32 | king_penguin->jellyfish:16 |
| sports_car | 27 |  |
| brown_bear | 16 |  |
| orange | 12 |  |

## Phase 2.6 recommendation

- Recommended first move: do not modify classifier yet; inspect baseline-right/HL-wrong rows for the top collapse paths and compare them against HL-right/all-baselines-wrong rows
- Likely first code target: tighten globally overactive Phase 2 signatures or add regression guards before attractor suppression

Required reruns after any classifier change:

    python scripts/run_phase2_diagnostics.py --input <new_phase2_eval_json>
    python scripts/run_phase2_benchmarks.py --data-root ".\data\phase2" --split val
    python scripts/run_phase2_attribution.py --data-root ".\data\phase2" --split val
    python scripts/run_phase2_candidates.py

## Non-claim lock

- This candidate plan does not change classifier behavior.
- This candidate plan does not claim accuracy improvement.
- This candidate plan does not prove classifier correctness.
- Validation candidate selection is not final test evidence.
- Any future classifier change must rerun diagnostics, benchmarks, attribution, and candidate selection.
