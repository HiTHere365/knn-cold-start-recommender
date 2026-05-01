# V1: Short-Form Content Feed (Social / Video)

Concept: short-form video / social post recommender modeled after how a content feed might behave.

## Cold-Start Features (Stage 1)

Coarse signals available at or shortly after signup:

| Feature | Type | Notes |
|---------|------|-------|
| age_band | categorical | e.g. 13-17, 18-24, 25-34, 35-44 |
| region | categorical | state, MGRS grid, or lat/long bucket |
| device_type | categorical | mobile, tablet, desktop |
| signup_interest | categorical | categories selected at signup |
| time_zone | categorical | inferred from location |

## Behavioral Features (Stage 2+)

Signals captured once a user starts interacting:

| Feature | Type | Notes |
|---------|------|-------|
| dwell_time_seconds | float | how long the user stayed on the content |
| volume_delta | float | did they turn volume up (+) or down (-) |
| scroll_past_speed | float | fast scroll = weak interest, slow = higher |
| replayed | bool | did they watch it more than once |
| shared | bool | share = strong positive signal |
| regional_engagement | float | % of users in same region who engaged |
| time_of_day | categorical | morning, afternoon, evening, night |

## Dataset Plan

- [ ] Define label schema (content category)
- [ ] Decide location encoding: MGRS vs lat/long bucket vs state
- [ ] Collect or synthesize initial dataset
- [ ] Version with Stage 1 features only, then expand to Stage 2

## Status

Scaffolded; dataset design in progress.
