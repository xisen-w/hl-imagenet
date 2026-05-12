# Phase 2 EDA: 10-Class Real Image Dataset

## Task

10-class classification on 64×64 Tiny ImageNet images. Given an image, predict one of 10 labels.

## Classes

| # | Class | wnid | Source |
|---|-------|------|--------|
| 1 | golden_retriever | n02099601 | Phase 1 (kept) |
| 2 | mushroom | n07734744 | Phase 1 (kept) |
| 3 | teapot | n04398044 | Phase 1 (kept) |
| 4 | school_bus | n04146614 | Phase 1 (kept) |
| 5 | banana | n07753592 | New (real images replacing synthetic) |
| 6 | orange | n07747607 | New |
| 7 | brown_bear | n02132136 | New |
| 8 | king_penguin | n02056570 | New |
| 9 | jellyfish | n01910747 | New |
| 10 | sports_car | n04285008 | New |

## Split

| Split | Per class | Total | Purpose |
|-------|:-:|:-:|---------|
| Train | 200 | 2,000 | HL loop tuning (images 0–199) |
| Val | 200 | 2,000 | Reported accuracy (images 200–399) |
| Test | 100 | 1,000 | Final held-out (images 400–499) |
| External | 50 | 500 | Official Tiny ImageNet val |

All images are real 64×64 JPEG from Tiny ImageNet 200.

## Color/Texture Statistics (train set, 200 images per class)

| Class | Hue (mean) | Sat (mean) | Val (mean) | Warm% | Green% | BW% | Edge% | Laplacian Var |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| banana | 35.9 | 143.7 | 149.2 | 60.2% | 6.9% | 14.4% | 0.206 | 4842 |
| orange | 32.3 | 170.8 | 162.1 | 71.3% | 6.5% | 11.0% | 0.192 | 3562 |
| golden_retriever | 36.9 | 90.5 | 141.7 | 57.9% | 7.7% | 21.2% | 0.268 | 5976 |
| brown_bear | 45.5 | 85.9 | 121.6 | 44.1% | 16.1% | 19.7% | 0.305 | 9530 |
| mushroom | 38.1 | 124.1 | 117.4 | 48.8% | 22.9% | 12.3% | 0.302 | 10878 |
| teapot | 45.4 | 88.8 | 131.0 | 48.5% | 7.1% | 29.5% | 0.205 | 5929 |
| school_bus | 52.4 | 105.9 | 132.9 | 44.2% | 8.6% | 21.6% | 0.268 | 12170 |
| sports_car | 64.0 | 90.5 | 121.6 | 35.0% | 9.5% | 30.9% | 0.248 | 11680 |
| king_penguin | 63.4 | 61.5 | 130.6 | 22.7% | 8.3% | 40.0% | 0.234 | 6973 |
| jellyfish | 92.1 | 165.1 | 144.3 | 15.7% | 8.0% | 8.7% | 0.146 | 3168 |

## Confusable Pairs (highest risk)

Ranked by histogram similarity (hue+saturation):

1. **brown_bear vs golden_retriever** — near-identical color profile (Δhue=8.6, Δsat=4.6). Both are warm furry blobs in outdoor settings. Hardest pair.
2. **golden_retriever vs teapot** — Phase 1's known hard pair. Brass/ceramic teapots share golden-brown hue.
3. **brown_bear vs teapot** — same problem (Δhue=0.1, Δsat=2.9).
4. **banana vs orange** — both warm, low texture, round-ish shapes. Differ mainly in saturation (144 vs 171) and shape (elongated vs round).
5. **school_bus vs sports_car** — both vehicles, similar edge density and texture complexity.
6. **mushroom vs brown_bear** — both have nature context (green), warm tones, high texture.

## Unique Visual Signatures (what might separate them)

| Class | Distinctive signal at 64×64 |
|-------|---------------------------|
| jellyfish | Blue/purple hue (92), highest saturation (165), lowest edges, translucent |
| king_penguin | Highest BW% (40%), low saturation (62), black/white with orange patch |
| orange | Highest warm% (71%), very high saturation (171), round, uniform |
| school_bus | Horizontal window pattern, yellow + sky above, rectangular |
| banana | Yellow + elongated shape, green context (often with other fruit) |
| sports_car | High edge density, metallic (high BW%), geometric, often red/blue |
| brown_bear | High green% (16%), high texture, warm but darker than dog |
| golden_retriever | Golden-brown (hue 37), moderate texture, often with human/outdoor |
| mushroom | Highest green% (23%), cap shape (top-heavy), high texture |
| teapot | Distinct background (30% BW), indoor, handle/spout shape |

## Baseline (Phase 1 classifier, unchanged, on 20 train images per class)

| Class | Accuracy | Most common prediction |
|-------|:---:|---|
| golden_retriever | 60% | golden_retriever |
| mushroom | 65% | mushroom |
| school_bus | 75% | school_bus |
| teapot | 60% | teapot |
| banana | 0% | teapot |
| orange | 0% | teapot |
| brown_bear | 0% | golden_retriever |
| king_penguin | 0% | teapot |
| jellyfish | 0% | teapot |
| sports_car | 0% | teapot |

**Overall: 26% (random = 10%)**

The 4 Phase 1 classes retain some accuracy (60–75%) since their rules still partially work on new data. The 6 new classes all go to 0% because no rules exist — teapot acts as the default "garbage collector" for anything warm/smooth.

## Predicted Difficulty Tiers

**Easy** (strong unique signals):
- jellyfish — blue/purple hue is unique, no other class is blue
- king_penguin — high BW% + low saturation is unique
- school_bus — window pattern feature already works

**Medium** (distinguishable but overlapping):
- orange — very high saturation + warm + round
- banana — yellow + elongated (but appears with other fruit/objects)
- sports_car — metallic + geometric + vehicles

**Hard** (heavily overlapping color/texture):
- golden_retriever vs brown_bear — nearly identical distributions
- mushroom vs golden_retriever — Phase 1's problem, still present
- teapot vs everything warm — catches anything with moderate warm tone

## Visual Samples

See `docs/phase2_eda_grid.png` for 5 random samples per class.
