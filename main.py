"""
Lab: "You Are Your Neighbors" -- Classification, Regression, and KNN

This lab builds a hand-rolled K-Nearest-Neighbors pipeline in three parts:

  Part 1: Turn real things into numbers (features) and measure the
          straight-line distance between them.
  Part 2: Watch KNN break in two different ways -- a badly chosen k,
          and features measured on wildly different scales.
  Part 3: Reuse the exact same k_nearest() neighbors for two different
          endings -- classify() (majority vote) and predict_rating()
          (average) -- to see that classification and regression are
          one algorithm with two different endings.

Scope: no scikit-learn, no train/test split, no accuracy metrics.
Everything below is hardcoded and deterministic -- no randomness, no
file I/O -- so results can be checked exactly.
"""

import math


# ---------------------------------------------------------------------------
# PART 1: Features and distance
# ---------------------------------------------------------------------------

# The book's oranges-vs-grapefruit dataset.
# size = diameter in cm, redness = rating from 1 (very orange) to 10 (very red)
FRUITS = [
    {"size": 5, "redness": 2, "label": "orange"},
    {"size": 6, "redness": 3, "label": "orange"},
    {"size": 5, "redness": 1, "label": "orange"},
    {"size": 6, "redness": 4, "label": "orange"},
    {"size": 7, "redness": 3, "label": "orange"},
    {"size": 6, "redness": 2, "label": "orange"},
    {"size": 9, "redness": 6, "label": "grapefruit"},
    {"size": 10, "redness": 7, "label": "grapefruit"},
    {"size": 9, "redness": 8, "label": "grapefruit"},
    {"size": 11, "redness": 6, "label": "grapefruit"},
    {"size": 10, "redness": 9, "label": "grapefruit"},
    {"size": 9, "redness": 7, "label": "grapefruit"},
]

# A fruit of unknown type -- this is what we want to classify.
NEW_FRUIT = {"size": 7, "redness": 5}


def extract_features(item):
    """
    Turn a fruit dict like {"size": 5, "redness": 2, "label": "orange"}
    into a plain list of numbers: [size, redness].

    This is the whole point of the chapter: a fruit becomes a point on
    a graph the moment you pull its numbers out.

    TODO:
      1. Read item["size"] and item["redness"].
      2. Return them as a list: [size, redness].
    """
    size = item["size"]
    redness = item["redness"]
    return [size, redness]


def euclidean_distance(a, b):
    """
    Compute the straight-line distance between two feature lists a and b.
    Write this out yourself with a loop -- do not import a distance
    function. It is just the Pythagorean theorem generalized to more
    than two dimensions.

    TODO:
      1. For each pair of matching values (a[i], b[i]), compute the
         squared difference (a[i] - b[i]) ** 2.
      2. Add up all the squared differences.
      3. Return the square root of that sum (math.sqrt).
    """
    total = 0

    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2

    return math.sqrt(total)


def k_nearest(training_set, new_item, k):
    """
    Return the k training items closest to new_item, sorted from
    nearest to farthest.

    training_set: a list of dicts, each with a "features" key
                   (a list of numbers) and a "label" or "value" key.
    new_item:      a dict with a "features" key (the point we are
                   asking about).
    k:             how many neighbors to return.

    TODO:
      1. Sort training_set by distance to new_item["features"]. Use
         sorted(training_set, key=...) -- a callback to the Chapter 2
         selection sort lab. In a comment, explain what your key
         function computes for each item.
      2. Return only the first k items of that sorted list.
    """
    # The key function calculates the distance from each training item
    # to the new item, so sorted() puts the closest items first.
    sorted_items = sorted(
        training_set,
        key=lambda item: euclidean_distance(
            item["features"], new_item["features"]
        )
    )

    return sorted_items[:k]


# ---------------------------------------------------------------------------
# Core KNN endings, used in Parts 1, 2, and 3
# ---------------------------------------------------------------------------

def classify(neighbors):
    """
    Majority vote: given a list of neighbor dicts (each with a "label"
    key), return the most common label.

    TODO:
      1. Count how many times each label appears among neighbors.
      2. Return the label with the highest count.
    """
    counts = {}

    for neighbor in neighbors:
        label = neighbor["label"]
        counts[label] = counts.get(label, 0) + 1

    best_label = None
    best_count = -1

    for label, count in counts.items():
        if count > best_count:
            best_count = count
            best_label = label

    return best_label


def predict_rating(neighbors):
    """
    Average: given a list of neighbor dicts (each with a "value" key),
    return the average of their values.

    TODO:
      1. Add up the "value" field of every neighbor.
      2. Divide by the number of neighbors and return that average.
    """
    total = 0

    for neighbor in neighbors:
        total += neighbor["value"]

    return total / len(neighbors)


# ---------------------------------------------------------------------------
# PART 2: The two ways KNN goes wrong
# ---------------------------------------------------------------------------

# --- Failure A: the wrong k ------------------------------------------------
# 7 real "cat" points cluster near (1-3, 1-3). 7 real "dog" points cluster
# near (8-10, 8-10). One mislabeled "dog" outlier sits right next to the
# test point, inside the cat cluster.
TRAINING_SET_A = [
    {"features": [1, 1], "label": "cat"},
    {"features": [1, 2], "label": "cat"},
    {"features": [2, 1], "label": "cat"},
    {"features": [1, 3], "label": "cat"},
    {"features": [3, 1], "label": "cat"},
    {"features": [2, 3], "label": "cat"},
    {"features": [3, 2], "label": "cat"},
    {"features": [2, 2], "label": "dog"},  # mislabeled outlier, right next to the test point!
    {"features": [8, 8], "label": "dog"},
    {"features": [9, 9], "label": "dog"},
    {"features": [8, 9], "label": "dog"},
    {"features": [9, 8], "label": "dog"},
    {"features": [10, 10], "label": "dog"},
    {"features": [8, 10], "label": "dog"},
    {"features": [10, 8], "label": "dog"},
]

TEST_POINT_A = {"features": [2, 2]}

# --- Failure B: unscaled features ------------------------------------------
# feature 0 = weight in grams (hundreds), feature 1 = quality rating (1-5).
# The gram-scale feature can drown out the quality feature entirely unless
# both are rescaled to the same 0-1 range.
RAW_DATASET_B = [
    {"features": [500, 5], "label": "premium"},
    {"features": [520, 4], "label": "premium"},
    {"features": [480, 5], "label": "premium"},
    {"features": [510, 4], "label": "premium"},
    {"features": [495, 5], "label": "premium"},
    {"features": [505, 4], "label": "premium"},
    {"features": [150, 1], "label": "standard"},
    {"features": [160, 2], "label": "standard"},
    {"features": [140, 1], "label": "standard"},
    {"features": [155, 2], "label": "standard"},
    {"features": [145, 1], "label": "standard"},
    {"features": [165, 2], "label": "standard"},
]

TEST_POINT_B = {"features": [300, 5]}


def normalize(dataset):
    """
    Rescale every feature in dataset to the 0-1 range (min-max scaling),
    so that no single feature can dominate the distance calculation just
    because of the units it happens to be measured in.

    dataset: a list of dicts, each with a "features" key (a list of
             numbers, all the same length).

    Return a NEW list of dicts in the same shape, with rescaled
    "features" (and the same "label"/"value"/other keys copied over).

    TODO:
      1. For each feature position (column), find its min and max
         across the whole dataset.
      2. For each item and each feature value, rescale it with
         (value - min) / (max - min).
      3. Build and return a new list of dicts with the rescaled
         "features" lists (keep every other key the same).
    """
    num_features = len(dataset[0]["features"])

    mins = []
    maxs = []

    # Find the minimum and maximum for each feature column.
    for i in range(num_features):
        values = [item["features"][i] for item in dataset]
        mins.append(min(values))
        maxs.append(max(values))

    normalized = []

    for item in dataset:
        new_features = []

        for i in range(num_features):
            value = item["features"][i]

            if maxs[i] == mins[i]:
                scaled = 0.0
            else:
                scaled = (value - mins[i]) / (maxs[i] - mins[i])

            new_features.append(scaled)

        new_item = dict(item)
        new_item["features"] = new_features
        normalized.append(new_item)

    return normalized


# ---------------------------------------------------------------------------
# PART 3: Same neighbors, different question -- regression
# ---------------------------------------------------------------------------

# Each user rated 3 movies everyone has seen ("features"), plus the movie
# we want to predict ("value" = star rating 1-5). "label" is just a
# derived like/dislike bucket from that same rating, so the SAME neighbor
# list can be used for both classify() and predict_rating().
USERS = [
    {"name": "Alice", "features": [5, 2, 1], "value": 5, "label": "likes"},
    {"name": "Bob", "features": [4, 3, 2], "value": 4, "label": "likes"},
    {"name": "Carol", "features": [5, 1, 1], "value": 5, "label": "likes"},
    {"name": "Dave", "features": [2, 4, 5], "value": 2, "label": "dislikes"},
    {"name": "Eve", "features": [1, 5, 4], "value": 1, "label": "dislikes"},
    {"name": "Frank", "features": [3, 3, 3], "value": 3, "label": "dislikes"},
    {"name": "Grace", "features": [5, 2, 2], "value": 4, "label": "likes"},
    {"name": "Heidi", "features": [2, 5, 5], "value": 2, "label": "dislikes"},
    {"name": "Ivan", "features": [4, 2, 1], "value": 5, "label": "likes"},
    {"name": "Judy", "features": [1, 4, 5], "value": 1, "label": "dislikes"},
]

# Sam has rated the same 3 movies but has NOT seen the target movie yet.
TARGET_USER = {"name": "Sam", "features": [5, 2, 1]}


def recommend(user, users, k):
    """
    Predict how `user` would rate the target movie, using the k users
    in `users` whose ratings on the shared movies are most similar.

    TODO:
      1. Find the k nearest users to `user` with k_nearest().
      2. Use predict_rating() on those neighbors to get the predicted
         rating.
      3. Return that predicted rating.
    """
    neighbors = k_nearest(users, user, k)
    return predict_rating(neighbors)


# ---------------------------------------------------------------------------
# Main program -- runs all three parts with hardcoded, deterministic data
# ---------------------------------------------------------------------------

def main():
    # ----- Part 1: features and distance -----
    fruits_data = [
        {"features": extract_features(fruit), "label": fruit["label"]}
        for fruit in FRUITS
    ]
    new_fruit_item = {"features": extract_features(NEW_FRUIT)}

    fruit_neighbors = k_nearest(fruits_data, new_fruit_item, 3)
    print(fruit_neighbors)

    fruit_prediction = classify(fruit_neighbors)
    print(fruit_prediction)

    # ----- Part 2, Failure A: the wrong k -----
    for k in [1, 3, 15]:
        neighbors_a = k_nearest(TRAINING_SET_A, TEST_POINT_A, k)
        prediction_a = classify(neighbors_a)
        print(prediction_a)

        # With k=1, the mislabeled dog right next to the test point
        # controls the prediction. With k=15, every point is included,
        # so the local neighborhood no longer matters and the overall
        # majority class wins.

    # ----- Part 2, Failure B: unscaled features -----
    raw_neighbors_b = k_nearest(RAW_DATASET_B, TEST_POINT_B, 3)
    raw_prediction_b = classify(raw_neighbors_b)
    print(raw_prediction_b)

    # Normalize the training set together with the test point so both
    # are rescaled using the same min/max.
    combined_b = RAW_DATASET_B + [{"features": TEST_POINT_B["features"], "label": None}]
    normalized_combined_b = normalize(combined_b)
    normalized_dataset_b = normalized_combined_b[:-1]
    normalized_test_point_b = {"features": normalized_combined_b[-1]["features"]}

    normalized_neighbors_b = k_nearest(normalized_dataset_b, normalized_test_point_b, 3)
    normalized_prediction_b = classify(normalized_neighbors_b)
    print(normalized_prediction_b)

    # The weight feature is measured in hundreds of grams while quality
    # is only measured from 1-5, so the weight feature has a much bigger
    # effect on raw distance. Normalizing puts both features on the same
    # 0-1 scale so they can contribute more fairly.

    # ----- Part 3: same neighbors, different question -----
    shared_neighbors = k_nearest(USERS, TARGET_USER, 3)

    # Same neighbor list, two different endings:
    predicted_label = classify(shared_neighbors)
    predicted_rating = predict_rating(shared_neighbors)
    print(predicted_label)
    print(predicted_rating)

    # The neighbor-finding step is the same for both. Only the ending
    # changes: classify() takes a majority vote, while predict_rating()
    # takes an average.

    recommended_rating = recommend(TARGET_USER, USERS, 3)
    print(recommended_rating)


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# REFLECTION (answer in comments below, no code needed):
#
# 1. If you were building a KNN recommender for restaurants, what
#    features would you extract from each restaurant?I would use stuff like price, how far it is, and rating to recomend resturants. 
# 2. What would go wrong if one of those features had the exact same
#    value for every restaurant in your dataset?   It would be haard for them to trell it apart but stuff like
#
# ---------------------------------------------------------------------------