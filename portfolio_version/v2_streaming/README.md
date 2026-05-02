# V2: Long-Form Streaming (Movie / Series Recommendation)

> **Status:** Design phase only. Implementation planned after v4 gaming is complete.

Concept: movie and series recommender for a streaming platform.

## Cold-Start Features (Stage 1)

| Feature | Type | Notes |
|---------|------|-------|
| age_band | categorical | |
| region | categorical | |
| signup_genres | list | genres selected during onboarding |
| device_type | categorical | TV, mobile, desktop |
| subscription_tier | categorical | signals content budget / preferences |

## Behavioral Features (Stage 2+)

| Feature | Type | Notes |
|---------|------|-------|
| watch_completion_pct | float | % of title completed |
| paused_count | int | frequent pausing may signal disengagement |
| skipped_intro | bool | |
| rated | bool | explicit feedback |
| added_to_watchlist | bool | intent signal |
| rewatch | bool | strong positive |
| time_since_last_session | float | engagement frequency |
| avg_session_length_min | float | |

## Dataset Plan

- [ ] Define title label taxonomy (genre, subgenre)
- [ ] Decide on synthetic vs. public dataset (MovieLens is a strong public option)
- [ ] Stage 1 dataset first, add behavioral columns in v2.1

## Status

Scaffolded; dataset selection in progress.
