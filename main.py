"""
Lab: "Write It Down Once" -- Dynamic Programming

Part 1: Measure the waste (naive recursive knapsack + call counter)
Part 2: Fill the grid instead (bottom-up DP knapsack)
Part 3: Point the same technique somewhere else (longest common
        substring vs longest common subsequence)

All data below is hardcoded -- no randomness, no file I/O.
The naive recursion is capped at 18 items so it finishes well inside
the autograder's time budget (2**18 is roughly half a million calls).
"""


# ---------------------------------------------------------------------------
# Part 1: Measure the waste
# ---------------------------------------------------------------------------

def naive_knapsack(items, capacity, index, counter):
    """
    Naive recursive 0/1 knapsack: at each item, either take it or don't,
    and return the best value achievable from items[index:] given the
    remaining capacity.

    items: list of (weight, value) tuples
    capacity: remaining capacity (int)
    index: index of the current item being considered
    counter: a one-element list, e.g. [0], used to count every call
             made to this function (increment counter[0] each call)

    Returns: best value achievable (int)
    """
    # Record that this call happened.
    counter[0] += 1

    # Base case: no items left to consider, or capacity has run out.
    if index >= len(items) or capacity <= 0:
        return 0

    weight, value = items[index]

    # Option 1: skip this item.
    without_item = naive_knapsack(items, capacity, index + 1, counter)

    # Option 2: take this item, if it fits.
    if weight <= capacity:
        with_item = value + naive_knapsack(
            items, capacity - weight, index + 1, counter
        )
        return max(without_item, with_item)

    return without_item


# ---------------------------------------------------------------------------
# Part 2: Fill the grid instead
# ---------------------------------------------------------------------------

def dp_knapsack(items, capacity):
    """
    Bottom-up dynamic programming knapsack.

    Build a grid with one row per item (plus a row 0 for "no items yet")
    and one column per capacity value from 0 to capacity.

    grid[i][j] is the most value that can fit in capacity j using the
    first i items.

    Returns: (grid, best_value) where grid is a list of lists and
             best_value is the value in the bottom-right cell.
    """
    rows = len(items) + 1
    cols = capacity + 1

    # Build the grid as a list of lists, rows x cols, initialized to 0.
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Fill the grid row by row using the knapsack recurrence.
    for i in range(1, rows):
        weight, value = items[i - 1]

        for j in range(cols):
            without_item = grid[i - 1][j]

            if weight <= j:
                with_item = value + grid[i - 1][j - weight]
                grid[i][j] = max(without_item, with_item)
            else:
                grid[i][j] = without_item

    best_value = grid[rows - 1][cols - 1]

    return grid, best_value


def print_grid(grid):
    """
    Print the grid in a readable, row-by-row format so students can
    actually look at the values that were computed.
    """
    for row_index, row in enumerate(grid):
        print("row {}: {}".format(row_index, row))


# ---------------------------------------------------------------------------
# Part 3: Point the same technique somewhere else
# ---------------------------------------------------------------------------

def longest_common_substring(a, b):
    """
    Return the longest common SUBSTRING of a and b (letters must be
    consecutive in both strings).

    Build a grid where grid[i][j] is 0 on a mismatch between a[i-1] and
    b[j-1], and grid[i-1][j-1] + 1 on a match. Track the largest value
    seen anywhere in the grid and the substring that produced it.
    """
    # Build the grid.
    rows = len(a) + 1
    cols = len(b) + 1

    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    max_len = 0
    end_index = 0

    # Fill the grid using the substring recurrence.
    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                grid[i][j] = grid[i - 1][j - 1] + 1

                if grid[i][j] > max_len:
                    max_len = grid[i][j]
                    end_index = i
            else:
                grid[i][j] = 0

    # Slice out the longest common substring.
    return a[end_index - max_len:end_index]


def longest_common_subsequence(a, b):
    """
    Return the longest common SUBSEQUENCE of a and b (letters do NOT need
    to be consecutive, just in the same relative order).

    Same grid shape as longest_common_substring, but a different rule:
    on a match, grid[i][j] = grid[i-1][j-1] + 1; on a mismatch,
    grid[i][j] = max(grid[i-1][j], grid[i][j-1]).
    """
    # Build the grid.
    rows = len(a) + 1
    cols = len(b) + 1

    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Fill the grid using the subsequence recurrence.
    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                grid[i][j] = grid[i - 1][j - 1] + 1
            else:
                grid[i][j] = max(grid[i - 1][j], grid[i][j - 1])

    # Walk backward through the grid to reconstruct the subsequence.
    i = rows - 1
    j = cols - 1
    result = []

    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif grid[i - 1][j] >= grid[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()

    return "".join(result)


# ---------------------------------------------------------------------------
# Entry point -- hardcoded, deterministic scaffolding
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 20 hardcoded (weight, value) items. Naive recursion is capped at the
    # first 18 of these to stay inside the autograder's time budget.
    items = [
        (2, 3), (3, 4), (4, 5), (5, 6), (9, 10),
        (1, 1), (6, 7), (7, 8), (8, 9), (10, 11),
        (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
        (7, 7), (8, 8), (9, 9), (10, 10), (1, 2),
    ]
    capacity = 50

    print("Part 1: Measure the waste")

    # Run the naive recursion on growing subsets of items: 3, 10, 18.
    # (Not 20 -- 18 keeps 2**n calls around half a million, well inside
    # the 15-second test budget; 20+ would risk blowing it.)
    for n in [3, 10, 18]:
        subset = items[:n]
        counter = [0]
        naive_knapsack(subset, capacity, 0, counter)
        print(n)
        print(counter[0])

    # The call count grows very quickly because each new item creates
    # another take-or-skip branch, so the number of calls roughly doubles.
    print("The call count roughly doubles as more items are added.")

    print("Part 2: Fill the grid instead")

    # Use the same 18-item slice for a fair naive-vs-DP comparison.
    comparison_items = items[:18]
    comparison_counter = [0]
    naive_knapsack(comparison_items, capacity, 0, comparison_counter)

    grid, best_value = dp_knapsack(comparison_items, capacity)
    print_grid(grid)
    print(best_value)

    num_cells = (len(comparison_items) + 1) * (capacity + 1)
    print(comparison_counter[0])
    print(num_cells)

    print("Part 3: Point the same technique somewhere else")

    # The book's example pair, plus one more to show the substring vs
    # subsequence disagreement.
    word_a = "hish"
    word_b = "fish"
    word_c = "vista"

    substring_ab = longest_common_substring(word_a, word_b)
    subsequence_ab = longest_common_subsequence(word_a, word_b)
    print(substring_ab)
    print(subsequence_ab)

    substring_ac = longest_common_substring(word_a, word_c)
    subsequence_ac = longest_common_subsequence(word_a, word_c)
    print(substring_ac)
    print(subsequence_ac)

    # Substrings require matching letters to be consecutive, while
    # subsequences only require them to stay in the same relative order.
    print("Substring requires consecutive matching letters, while")
    print("subsequence allows gaps between matching letters.")

    # -----------------------------------------------------------------
    # Reflection:
    #
    # A DP grid works when a problem can be broken into smaller
    # subproblems whose answers can be reused to solve larger problems.
    # A real-world example is git diff because it compares pieces of
    # two files and reuses those smaller comparison results.
    # -----------------------------------------------------------------