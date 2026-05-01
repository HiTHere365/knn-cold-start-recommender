# V4 — Game Recommendation (Full Circle)

Concept: full-circle evolution of the class assignment. Starts with the same demographic cold-start
features, then layers in behavioral signals specific to gaming. This version closes the loop between
the CSC525 assignment and the complete pipeline vision.

## Cold-Start Features (Stage 1 — mirrors class assignment)

| Feature | Type | Notes |
|---------|------|-------|
| age_band | categorical | more granular than the class dataset |
| region | categorical | MGRS / lat-long bucket |
| device_type | categorical | PC, console, mobile, handheld |
| signup_genres | list | genres selected at account creation |
| platform | categorical | Steam, PlayStation, Xbox, Switch, mobile store |

## Behavioral Features (Stage 2+)

| Feature | Type | Notes |
|---------|------|-------|
| session_duration_min | float | total play time per session |
| days_since_last_play | float | engagement frequency |
| completion_pct | float | how far into the game the user got |
| achievement_rate | float | achievements earned / total available |
| multiplayer_ratio | float | % of sessions in multiplayer vs. solo |
| genre_hours | dict | time spent per genre across all titles |
| refunded | bool | strong negative signal |
| wishlisted | bool | intent signal for future recommendations |
| in_game_purchase | bool | engagement depth signal |
| review_score | float | if user left a review |

## Location Encoding Decision (TBD)

Options being evaluated:
- MGRS grid zone (concise, military-standard, region-preserving)
- Lat/long bucketed to ~50km cells
- State / country (coarser but simpler to work with for v1)

## Dataset Plan

- [ ] Finalize location encoding approach
- [ ] Build or source dataset with session-level behavioral features
- [ ] Port class_version/knn_classifier.py as the Stage 1 baseline
- [ ] Add behavioral layer as separate feature set

## Connection to Class Assignment

The class version (`class_version/knn_classifier.py`) is Stage 1 of this model.
In the final form, age/height/weight/gender → age_band/region/device/signup_genre,
and session hours, completion rate, and genre time replace the physical attributes entirely.

## Status

Scaffolded — location encoding and dataset design in progress.
