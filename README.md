# Cold-Start to Personalization: KNN Recommender Pipeline

## Overview

This project starts as a class assignment (KNN video game genre classifier) and evolves into a
multi-platform recommender pipeline prototype. The pipeline design is an original concept developed
by observing recommendation behavior across content platforms and reasoning about what a well-designed
system would require, not a description of how any specific company operates internally.

The core idea: a new user has no behavioral history, so a system must bootstrap recommendations from
coarse signals before it can personalize. This project implements that first stage and outlines how
subsequent stages would work as behavior data accumulates.

## Repository Structure

```
class_version/          ← CSC525 assignment submission
  knn_classifier.py     ← accepts 4 floats, outputs predicted genre
  data/data.csv         ← class-provided dataset

portfolio_version/      ← evolving recommender pipeline
  v4_gaming/            ← working: KNN on cold-start gaming features (500-row research-backed dataset)
  v1_content_feed/      ← design spec: short-form video / social feed concept
  v2_streaming/         ← design spec: long-form video / movie recommendation concept
  v3_music/             ← design spec: mood-aware music recommendation concept

docs/design.md          ← cold-start pipeline design doc
```

## Running the Class Assignment

```bash
conda activate MLFINALGRADCOURSE
python class_version/knn_classifier.py <age> <height_in> <weight_lbs> <gender>
# gender: 0=female, 1=male
```

Example:
```bash
python class_version/knn_classifier.py 22 68 160 1
# → Predicted genre: RPG
```

## Cold-Start Pipeline Concept

The class assignment implements **Stage 1** of a three-stage recommender lifecycle I designed:

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
conda activate MLFINALGRADCOURSE
pip install -r requirements.txt
```
