# Copyright (C) 2026 William Rogers
# SPDX-License-Identifier: GPL-3.0-or-later
"""
V4 Gaming Cold-Start Recommender
Stage 1: KNN on cold-start cohort features (no behavioral history required)

Usage:
    python knn_gaming.py --continent "North America" --country "USA" \
        --region "Northeast" --age-band "18-24" --gender 1 \
        --platform "PC" --session-pref "Long" --signup-genre "Shooter"

gender: 0 = female, 1 = male
"""

import sys
import csv
import os
import argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from knn_core import predict

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "gaming_cold_start.csv")
K = 7

AGE_BAND_ENC = {"8-12": 0, "13-17": 1, "18-24": 2, "25-34": 3, "35+": 4}
SESSION_ENC  = {"Short": 0, "Medium": 1, "Long": 2}

FEATURE_KEYS = [
    "continent_enc", "country_enc", "region_enc",
    "age_band_enc", "gender",
    "platform_enc", "session_enc", "signup_genre_enc",
]


def build_encodings(dataset):
    def enc_map(key):
        return {v: i for i, v in enumerate(sorted(set(row[key] for row in dataset)))}
    return {
        "continent":    enc_map("continent"),
        "country":      enc_map("country"),
        "region":       enc_map("region"),
        "platform":     enc_map("platform"),
        "signup_genre": enc_map("signup_genre"),
    }


def load_data(filepath):
    raw = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw.append(row)

    encodings = build_encodings(raw)

    dataset = []
    for row in raw:
        dataset.append({
            "continent_enc":    encodings["continent"][row["continent"]],
            "country_enc":      encodings["country"][row["country"]],
            "region_enc":       encodings["region"][row["region"]],
            "age_band_enc":     AGE_BAND_ENC[row["age_band"]],
            "gender":           float(row["gender"]),
            "platform_enc":     encodings["platform"][row["platform"]],
            "session_enc":      SESSION_ENC[row["session_pref"]],
            "signup_genre_enc": encodings["signup_genre"][row["signup_genre"]],
            "label":            row["label"],
        })

    return dataset, encodings


def encode_query(args, encodings):
    errors = []

    def check(key, value, mapping):
        if value not in mapping:
            errors.append(f"  '{value}' is not a valid {key}. Options: {sorted(mapping.keys())}")
            return 0
        return mapping[value]

    continent_enc    = check("continent",    args.continent,    encodings["continent"])
    country_enc      = check("country",      args.country,      encodings["country"])
    region_enc       = check("region",       args.region,       encodings["region"])
    platform_enc     = check("platform",     args.platform,     encodings["platform"])
    signup_genre_enc = check("signup_genre", args.signup_genre, encodings["signup_genre"])

    if args.age_band not in AGE_BAND_ENC:
        errors.append(f"  '{args.age_band}' is not a valid age-band. Options: {list(AGE_BAND_ENC.keys())}")
    if args.session_pref not in SESSION_ENC:
        errors.append(f"  '{args.session_pref}' is not a valid session-pref. Options: {list(SESSION_ENC.keys())}")

    if errors:
        print("Input errors:")
        for e in errors:
            print(e)
        sys.exit(1)

    return [
        continent_enc, country_enc, region_enc,
        AGE_BAND_ENC[args.age_band],
        float(args.gender),
        platform_enc,
        SESSION_ENC[args.session_pref],
        signup_genre_enc,
    ]


def main():
    parser = argparse.ArgumentParser(description="V4 Gaming Cold-Start KNN Recommender")
    parser.add_argument("--continent",    required=True)
    parser.add_argument("--country",      required=True)
    parser.add_argument("--region",       required=True)
    parser.add_argument("--age-band",     required=True, dest="age_band")
    parser.add_argument("--gender",       required=True, type=int, choices=[0, 1])
    parser.add_argument("--platform",     required=True)
    parser.add_argument("--session-pref", required=True, dest="session_pref")
    parser.add_argument("--signup-genre", required=True, dest="signup_genre")
    args = parser.parse_args()

    if not os.path.exists(DATA_FILE):
        print(f"Dataset not found: {DATA_FILE}")
        print("Run generate_dataset.py first.")
        sys.exit(1)

    dataset, encodings = load_data(DATA_FILE)
    query = encode_query(args, encodings)
    genre, ranked, neighbors = predict(dataset, FEATURE_KEYS, query, K)

    print(f"\nCold-start profile:")
    print(f"  Location:     {args.continent} / {args.country} / {args.region}")
    print(f"  Age band:     {args.age_band}  |  Gender: {'Male' if args.gender == 1 else 'Female'}")
    print(f"  Platform:     {args.platform}  |  Session: {args.session_pref}")
    print(f"  Signup genre: {args.signup_genre}")

    print(f"\nTop recommendation:  {genre}")

    print(f"\nFull genre ranking:")
    for rank, (label, count) in enumerate(ranked, 1):
        print(f"  {rank}. {label:<12}  ({count} of {K} neighbors)")

    print(f"\nNearest neighbors:")
    for i, (dist, label) in enumerate(neighbors, 1):
        print(f"  {i}. {label:<12}  distance={dist:.4f}")


if __name__ == "__main__":
    main()
