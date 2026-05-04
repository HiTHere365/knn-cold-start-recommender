# Cold-Start to Personalization: KNN Recommender Pipeline

## Overview

A new user has no behavioral history. A platform has to recommend something immediately anyway. This project implements the first stage of a three-stage recommender lifecycle and outlines how subsequent stages work as behavioral data accumulates.

The pipeline design is an original concept developed by observing recommendation behavior across content platforms and reasoning about what a well-designed system would require. It is not a description of how any specific company operates internally.

## Repository Structure

```
legacy/                 ← baseline: KNN on simplified demographic features
  knn_classifier.py     ← accepts 4 floats, outputs predicted genre
  data/data.csv         ← original dataset

portfolio_version/      ← evolving recommender pipeline
  v4_gaming/            ← working: KNN on cold-start gaming features (500-row research-backed dataset)
  v1_content_feed/      ← design spec: short-form video / social feed concept
  v2_streaming/         ← design spec: long-form video / movie recommendation concept
  v3_music/             ← design spec: mood-aware music recommendation concept

docs/design.md          ← cold-start pipeline design doc
```

## Running the Baseline

```bash
pip install -r requirements.txt
python legacy/knn_classifier.py <age> <height_in> <weight_lbs> <gender>
# gender: 0=female, 1=male
```

Example:
```bash
python legacy/knn_classifier.py 22 68 160 1
# Predicted genre: RPG
```

## Demo

V4 Gaming cold-start prediction for an 18-24 male PC gamer in the US Northeast who signed up for Shooter:

```bash
python portfolio_version/v4_gaming/knn_gaming.py \
  --continent "North America" --country "USA" --region "Northeast" \
  --age-band "18-24" --gender 1 --platform "PC" \
  --session-pref "Long" --signup-genre "Shooter"
```

```
Cold-start profile:
  Location:     North America / USA / Northeast
  Age band:     18-24  |  Gender: Male
  Platform:     PC  |  Session: Long
  Signup genre: Shooter

Top recommendation:  Strategy

Full genre ranking:
  1. Strategy      (2 of 7 neighbors)
  2. Sports        (2 of 7 neighbors)
  3. RPG           (2 of 7 neighbors)
  4. Shooter       (1 of 7 neighbors)
```

## Cold-Start Pipeline Concept

The baseline implements **Stage 1** of a three-stage recommender lifecycle:

| Stage | Driver | Description |
|-------|--------|-------------|
| 1: Initialization | Cohort features | Use coarse attributes (age, demographics, signup signals) to bootstrap recommendations for users with no history |
| 2: Early adaptation | Blended signals | Mix cohort priors with first interaction signals |
| 3: Personalization | Individual behavior | User's own interaction history becomes the dominant ranking signal |

Formally:

```
Recommendation Score = α · (cohort profile) + β · (individual behavior)
```

At cold start, α ≈ 1, β ≈ 0. As behavioral history grows, β → 1 and α → 0.

## Environment

```bash
pip install -r requirements.txt
```

## License

GNU Affero General Public License v3.0 (AGPL v3)

For commercial licensing: fierier.heated9b@icloud.com
