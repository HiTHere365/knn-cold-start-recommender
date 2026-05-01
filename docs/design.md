# Cold-Start to Personalization: Pipeline Design

## Origin

This design came from observing recommendation behavior on content platforms and reasoning about
what a well-designed system would need to handle a brand-new user who has no interaction history.
The three-stage model below is my own framework, not a description of any company's internal system.

## The Core Problem

A new user has no clicks, no watch history, no saved content, no behavioral trail. The platform
has to recommend something immediately anyway. What does it use?

The answer is coarse proxy variables: things you can know at signup or infer immediately: region,
age band, device type, language, declared interests. These are not ideal, but they allow a reasonable
first guess by finding users who look similar on those attributes and recommending what worked for them.

This is the cold-start problem, and the solution is a cohort-based initialization strategy.

## Three-Stage Model

### Stage 1: Initialization

The system relies on broad cohort features.

Features: region, age band, device type, language, signup interests, time zone.

These form an initial profile. The recommendation engine finds similar users in the training set
and predicts preferences based on what that cohort responded to.

KNN is a natural fit here: it literally finds the nearest users in feature space and votes.

### Stage 2: Early Adaptation

The user has a few interactions. The system blends cohort priors with personal signals.

New features added: first few clicks, dwell time, content completions, skips.

The model begins weighting individual behavior alongside cohort assumptions.

### Stage 3: Personalization

Enough behavioral history exists that the individual profile drives the model.

The cohort assumptions fade in weight. The user's own interaction pattern becomes the primary signal.

## Formal Model

```
Score = α · cohort_profile + β · individual_behavior
```

| Stage | α | β |
|-------|---|---|
| Initialization | ~1.0 | ~0.0 |
| Early adaptation | ~0.5 | ~0.5 |
| Personalization | ~0.1 | ~0.9 |

α and β are not fixed constants; they are confidence weights that increase as behavioral history grows.
A simple version: β = min(1.0, interaction_count / threshold).

## Platform Variants

Each platform has a different behavioral feature set, but the same three-stage structure applies:

| Platform Type | Key Stage 2+ Signals |
|---------------|----------------------|
| Short-form video / social | dwell time, volume delta, regional engagement, replay |
| Long-form streaming | watch completion %, skip intro, watchlist add, rewatch |
| Music | time of day, audio energy/valence, skip position, playlist save |
| Gaming | session duration, genre hours, completion %, multiplayer ratio |

## Implementation Notes

- Normalize all features before computing distances (KNN is distance-sensitive to scale)
- Min-max normalization works for bounded features; consider z-score for open-ended ones
- K choice: start with K=5, validate with leave-one-out or k-fold cross-validation
- For Stage 2+, consider weighting behavioral features more heavily than cohort features in the distance function

## Relationship to Class Assignment

`class_version/knn_classifier.py` is a direct implementation of Stage 1 using a simplified
demographic dataset (age, height, weight, gender → video game genre). It demonstrates the core
KNN mechanics. The portfolio versions extend this into more realistic feature spaces and
eventually add the behavioral layer described in Stage 2 and Stage 3.
