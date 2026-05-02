# Copyright (C) 2026 William Rogers
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Synthetic dataset generator for v4 Gaming Cold-Start Recommender.

Distributions are research-backed. Sources:
  - ESA Essential Facts 2024 (North America)
    https://www.theesa.com/wp-content/uploads/2024/05/Essential-Facts-2024-FINAL.pdf
  - RetroStyle Games Genre Popularity Case Study
    https://retrostylegames.com/blog/video-game-genre-popularity-case-study/
  - Niko Partners East Asia Games Market 2025
    https://nikopartners.com/east-asia-games-market-in-2025-navigating-the-changes/
  - KPMG Africa Games Industry Report 2025
    https://assets.kpmg.com/content/dam/kpmg/ng/pdf/2025/02/2025%20Africa%20Games%20Industry%20Report.pdf
  - InvestGame Genre and Great Games Report 2023
    https://investgame.net/wp-content/uploads/2023/08/Genre-and-Great-Games-Report.pdf
  - Rakuten Insight Online Gaming in Asia
    https://insight.rakuten.com/online-gaming-in-asia/
  - Atlantic Council: Africa's Game Revolution
    https://www.atlanticcouncil.org/blogs/africasource/africas-game-revolution-is-loading/
  - PlayIO Genre Popularity by Region
    https://blog.playio.co/most-popular-mobile-game-genres-by-region

Random seed fixed at 42 for reproducibility.
Run: python generate_dataset.py
Output: data/gaming_cold_start.csv
"""

import random
import csv
import os
from collections import Counter

random.seed(42)

GENRES = ["Action", "RPG", "Strategy", "Sports", "Platformer", "Puzzle", "Shooter"]

LOCATION = {
    "North America": {
        "USA":      ["Northeast", "Southeast", "Midwest", "West", "Southwest"],
        "Canada":   ["East", "West", "Central"],
        "Mexico":   ["North", "Central", "South"],
    },
    "South America": {
        "Brazil":    ["North", "Northeast", "South", "Southeast"],
        "Argentina": ["North", "Central", "South"],
        "Colombia":  ["North", "Central", "South"],
    },
    "Europe": {
        "UK":      ["England", "Scotland", "Wales"],
        "Germany": ["North", "South", "East", "West"],
        "France":  ["North", "South", "East", "West"],
        "Sweden":  ["North", "Central", "South"],
        "Spain":   ["North", "Central", "South"],
    },
    "East Asia": {
        "Japan":       ["North", "Central", "South"],
        "South Korea": ["North", "Central", "South"],
        "China":       ["North", "Central", "South", "East", "West"],
    },
    "South Asia": {
        "India": ["North", "Central", "South", "East", "West"],
    },
    "Africa": {
        "South Africa": ["North", "Central", "South"],
        "Nigeria":      ["North", "Central", "South"],
    },
    "Oceania": {
        "Australia": ["East", "West", "Central"],
    },
}

# Approximate global gamer population share per continent
CONTINENT_WEIGHTS = {
    "East Asia":     35,
    "Europe":        20,
    "North America": 15,
    "South Asia":    12,
    "South America":  8,
    "Africa":         7,
    "Oceania":        3,
}

# Genre distribution by continent (Action, RPG, Strategy, Sports, Platformer, Puzzle, Shooter)
GENRE_DIST = {
    "North America": [15, 20, 10, 25, 10,  5, 15],
    "South America": [20, 15,  7, 35, 10,  3, 10],
    "Europe":        [10, 28, 30, 15,  7,  2,  8],
    "East Asia":     [10, 35, 30,  3,  7, 10,  5],
    "South Asia":    [18, 15,  7, 20,  3, 30,  7],
    "Africa":        [20,  8,  5, 25,  2, 32,  8],
    "Oceania":       [18, 20, 15, 25,  7,  3, 12],
}

PLATFORM_DIST = {
    "North America": {"Mobile": 20, "PC": 35, "Console": 35, "Handheld": 10},
    "South America": {"Mobile": 45, "PC": 25, "Console": 25, "Handheld":  5},
    "Europe":        {"Mobile": 20, "PC": 40, "Console": 30, "Handheld": 10},
    "East Asia":     {"Mobile": 30, "PC": 30, "Console": 20, "Handheld": 20},
    "South Asia":    {"Mobile": 60, "PC": 25, "Console": 10, "Handheld":  5},
    "Africa":        {"Mobile": 80, "PC": 14, "Console":  5, "Handheld":  1},
    "Oceania":       {"Mobile": 25, "PC": 30, "Console": 35, "Handheld": 10},
}

SESSION_DIST = {
    "Mobile":   {"Short": 65, "Medium": 30, "Long":  5},
    "PC":       {"Short": 10, "Medium": 35, "Long": 55},
    "Console":  {"Short": 15, "Medium": 45, "Long": 40},
    "Handheld": {"Short": 50, "Medium": 40, "Long": 10},
}

AGE_BANDS   = ["8-12", "13-17", "18-24", "25-34", "35+"]
AGE_WEIGHTS = [10, 20, 30, 25, 15]

GENDER_MALE_PROB = {
    "8-12":  0.55,
    "13-17": 0.65,
    "18-24": 0.55,
    "25-34": 0.50,
    "35+":   0.45,
}

AGE_GENRE_LEAN = {
    "8-12":  ["Platformer", "Puzzle", "Platformer"],
    "13-17": ["Action", "Sports", "Shooter", "Action"],
    "18-24": ["Action", "RPG", "Sports", "Shooter"],
    "25-34": ["RPG", "Strategy", "RPG"],
    "35+":   ["Strategy", "Puzzle", "Strategy"],
}

ADJACENT = {
    "Action":    ["RPG",      "Shooter"],
    "RPG":       ["Strategy", "Action"],
    "Strategy":  ["RPG",      "Puzzle"],
    "Sports":    ["Action",   "Shooter"],
    "Platformer":["Action",   "Puzzle"],
    "Puzzle":    ["Strategy", "Platformer"],
    "Shooter":   ["Action",   "Sports"],
}


def weighted_choice(options, weights):
    total = sum(weights)
    r = random.uniform(0, total)
    upto = 0
    for option, weight in zip(options, weights):
        upto += weight
        if r <= upto:
            return option
    return options[-1]


def pick_from_dict(d):
    return weighted_choice(list(d.keys()), list(d.values()))


def generate_row():
    continent = weighted_choice(list(CONTINENT_WEIGHTS.keys()),
                                list(CONTINENT_WEIGHTS.values()))
    country   = random.choice(list(LOCATION[continent].keys()))
    region    = random.choice(LOCATION[continent][country])
    platform  = pick_from_dict(PLATFORM_DIST[continent])
    session   = pick_from_dict(SESSION_DIST[platform])
    age_band  = weighted_choice(AGE_BANDS, AGE_WEIGHTS)
    gender    = 1 if random.random() < GENDER_MALE_PROB[age_band] else 0

    # 70% regional bias drives actual genre, 30% age/gender lean overrides
    if random.random() < 0.70:
        label = weighted_choice(GENRES, GENRE_DIST[continent])
    else:
        label = random.choice(AGE_GENRE_LEAN[age_band])

    # Cold-start signup guess: correct 70% of the time, adjacent mismatch 30%
    signup_genre = label if random.random() < 0.70 else random.choice(ADJACENT[label])

    return {
        "continent":    continent,
        "country":      country,
        "region":       region,
        "age_band":     age_band,
        "gender":       gender,
        "platform":     platform,
        "session_pref": session,
        "signup_genre": signup_genre,
        "label":        label,
    }


def main():
    out_path = os.path.join(os.path.dirname(__file__), "data", "gaming_cold_start.csv")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    rows = [generate_row() for _ in range(500)]

    fields = ["continent", "country", "region", "age_band", "gender",
              "platform", "session_pref", "signup_genre", "label"]

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows -> {out_path}\n")

    print("Label distribution:")
    for genre, count in sorted(Counter(r["label"] for r in rows).items(), key=lambda x: -x[1]):
        print(f"  {genre:<12} {count:>4}  ({count / len(rows) * 100:.1f}%)")

    mismatches = sum(1 for r in rows if r["signup_genre"] != r["label"])
    print(f"\nCold-start mismatch rate: {mismatches / len(rows) * 100:.1f}%")

    print("\nContinent distribution:")
    for continent, count in sorted(Counter(r["continent"] for r in rows).items(), key=lambda x: -x[1]):
        print(f"  {continent:<15} {count:>4}  ({count / len(rows) * 100:.1f}%)")


if __name__ == "__main__":
    main()
