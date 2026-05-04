#!/usr/bin/env python3
# Copyright (C) 2026 William Rogers
# SPDX-License-Identifier: GPL-3.0-or-later
"""
KNN Classifier: Video Game Genre Prediction

Usage:
    python knn_classifier.py <age> <height> <weight> <gender>
    gender: 0 = female, 1 = male

Example:
    python knn_classifier.py 22 68.0 160.0 1
"""

import sys
import csv
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from knn_core import predict

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "data.csv")
FEATURE_KEYS = ["age", "height", "weight", "gender"]
K = 5


def load_data(filepath):
    dataset = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append({
                "age":    float(row["age"]),
                "height": float(row["height"]),
                "weight": float(row["weight"]),
                "gender": float(row["gender"]),
                "label":  row["genre"].strip(),
            })
    return dataset


def main():
    if len(sys.argv) != 5:
        print("Usage: python knn_classifier.py <age> <height_in> <weight_lbs> <gender>")
        print("  gender: 0 = female, 1 = male")
        sys.exit(1)

    try:
        query = [float(x) for x in sys.argv[1:]]
    except ValueError:
        print("Error: all four inputs must be numbers.")
        sys.exit(1)

    if not os.path.exists(DATA_FILE):
        print(f"Dataset not found at: {DATA_FILE}")
        print("Place data.csv in the legacy/data/ directory.")
        sys.exit(1)

    dataset = load_data(DATA_FILE)
    genre, ranked, neighbors = predict(dataset, FEATURE_KEYS, query, K)

    print(f"\nInput: age={query[0]}, height={query[1]}, weight={query[2]}, gender={int(query[3])}")
    print(f"Predicted genre: {genre}")
    print(f"\nTop {K} nearest neighbors:")
    for i, (dist, label) in enumerate(neighbors, 1):
        print(f"  {i}. genre={label}  (distance={dist:.4f})")
    print(f"\nVote breakdown:")
    for label, count in ranked:
        print(f"  {label}: {count} vote(s)")


if __name__ == "__main__":
    main()
