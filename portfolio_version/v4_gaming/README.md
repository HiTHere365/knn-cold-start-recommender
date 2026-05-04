# V4: Game Recommendation

Stage 1 implementation using realistic gaming cold-start features. Extends the baseline demographic
approach into a richer feature space specific to the gaming platform context, and establishes the
scaffold for Stage 2 behavioral layer.

## Cold-Start Features (Stage 1)

| Feature | Type | Notes |
|---------|------|-------|
| age_band | categorical | more granular than the baseline dataset |
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
- [ ] Add behavioral layer as separate feature set

## Status

Scaffolded; location encoding and dataset design in progress.
