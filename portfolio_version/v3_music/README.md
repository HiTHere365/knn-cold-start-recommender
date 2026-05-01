# V3: Mood-Aware Music Recommendation

Concept: music recommender that incorporates time-of-day and audio vibe signals to infer user mood
and suggest contextually appropriate music, going beyond genre to emotional/temporal context.

## Cold-Start Features (Stage 1)

| Feature | Type | Notes |
|---------|------|-------|
| age_band | categorical | |
| region | categorical | |
| signup_genres | list | genres / moods declared at signup |
| device_type | categorical | headphones, car, speaker, etc. |

## Behavioral Features (Stage 2+)

| Feature | Type | Notes |
|---------|------|-------|
| time_of_day | categorical | morning, commute, afternoon, evening, late night |
| day_of_week | categorical | weekday vs. weekend changes listening patterns |
| skipped_at_pct | float | where in the track the user skipped |
| replayed | bool | |
| volume_level | float | normalized; high volume correlates with energy preference |
| saved_to_library | bool | |
| added_to_playlist | bool | |
| audio_energy | float | track-level feature: low=calm, high=energetic |
| audio_valence | float | track-level feature: low=sad, high=happy |
| audio_tempo_bpm | float | track-level tempo |
| listening_streak_min | float | consecutive listening time in session |

## Mood Inference Model (Stage 3 concept)

Map (time_of_day, audio_energy, audio_valence) → inferred_mood:
- morning + high energy + high valence → "motivated / workout"
- late night + low energy + low valence → "reflective / wind-down"
- commute + medium energy → "commute / focus"

Use inferred mood as an additional feature for the recommendation model.

## Dataset Plan

- [ ] Define mood taxonomy (6-8 mood labels)
- [ ] Source audio features: Spotify Web API provides energy/valence/tempo per track
- [ ] Build synthetic listening log with time-of-day distribution
- [ ] Stage 1 first, add audio feature layer in v3.1

## Status

Scaffolded; mood taxonomy and audio feature sourcing in progress.
