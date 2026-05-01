#!/usr/bin/env python3
"""
KNN Classifier — Video Game Genre Prediction
CSC525 Assignment: Option 2

Usage:
    python knn_classifier.py <age> <height> <weight> <gender>
    gender: 0 = female, 1 = male

Example:
    python knn_classifier.py 22 68.0 160.0 1
"""

import sys
import csv
import math
import os
from collections import Counter

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "data.csv")
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
                "genre":  row["genre"].strip(),
            })
    return dataset


def euclidean_distance(a, b):
    return math.sqrt(
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2 +
        (a[2] - b[2]) ** 2 +
        (a[3] - b[3]) ** 2
    )


def normalize(dataset, query):
    """Min-max normalize all features including the query point."""
    keys = ["age", "height", "weight", "gender"]
    mins = {k: min(row[k] for row in dataset) for k in keys}
    maxs = {k: max(row[k] for row in dataset) for k in keys}

    def scale(val, k):
        r = maxs[k] - mins[k]
        return (val - mins[k]) / r if r != 0 else 0.0

    normalized = [
        [scale(row[k], k) for k in keys] + [row["genre"]]
        for row in dataset
    ]
    norm_query = [scale(query[i], keys[i]) for i in range(len(keys))]
    return normalized, norm_query


def predict(dataset, query_features, k):
    normalized_data, norm_query = normalize(dataset, query_features)

    distances = []
    for row in normalized_data:
        features = row[:4]
        label = row[4]
        dist = euclidean_distance(norm_query, features)
        distances.append((dist, label))

    distances.sort(key=lambda x: x[0])

    top_k = distances[:k]
    top_k_labels = [label for _, label in top_k]

    vote = Counter(top_k_labels)
    predicted_genre = vote.most_common(1)[0][0]
    return predicted_genre, top_k


def main():
    if len(sys.argv) != 5:
        print("Usage: python knn_classifier.py <age> <height_in> <weight_lbs> <gender>")
        print("  gender: 0 = female, 1 = male")
        sys.exit(1)

    try:
        query = [float(sys.argv[1]), float(sys.argv[2]),
                 float(sys.argv[3]), float(sys.argv[4])]
    except ValueError:
        print("Error: all four inputs must be numbers.")
        sys.exit(1)

    if not os.path.exists(DATA_FILE):
        print(f"Dataset not found at: {DATA_FILE}")
        print("Place data.csv in the class_version/data/ directory.")
        sys.exit(1)

    dataset = load_data(DATA_FILE)
    genre, neighbors = predict(dataset, query, K)

    print(f"\nInput: age={query[0]}, height={query[1]}, weight={query[2]}, gender={int(query[3])}")
    print(f"Predicted genre: {genre}")
    print(f"\nTop {K} nearest neighbors:")
    for i, (dist, label) in enumerate(neighbors, 1):
        print(f"  {i}. genre={label}  (distance={dist:.4f})")


if __name__ == "__main__":
    main()
