# Copyright (C) 2026 William Rogers
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Shared KNN algorithm core.
Used by all pipeline versions (v4 gaming, v1-v3 future).
"""

import math
from collections import Counter


def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def normalize(dataset, feature_keys, query):
    """Min-max normalize features across dataset and query point."""
    mins = {k: min(row[k] for row in dataset) for k in feature_keys}
    maxs = {k: max(row[k] for row in dataset) for k in feature_keys}

    def scale(val, k):
        r = maxs[k] - mins[k]
        return (val - mins[k]) / r if r != 0 else 0.0

    normalized = [
        [scale(row[k], k) for k in feature_keys] + [row["label"]]
        for row in dataset
    ]
    norm_query = [scale(query[i], feature_keys[i]) for i in range(len(feature_keys))]
    return normalized, norm_query


def predict(dataset, feature_keys, query_values, k):
    """
    Find the k nearest neighbors and return the majority label.

    dataset     : list of dicts, each must have feature_keys + 'label'
    feature_keys: ordered list of feature names to use
    query_values: list of floats matching feature_keys order
    k           : number of neighbors

    Returns (predicted_label, ranked_vote_counts, top_k_neighbors)
    """
    normalized_data, norm_query = normalize(dataset, feature_keys, query_values)

    distances = []
    for row in normalized_data:
        features = row[:-1]
        label = row[-1]
        dist = euclidean_distance(norm_query, features)
        distances.append((dist, label))

    distances.sort(key=lambda x: x[0])
    top_k = distances[:k]
    vote = Counter(label for _, label in top_k)
    ranked = vote.most_common()

    return ranked[0][0], ranked, top_k
