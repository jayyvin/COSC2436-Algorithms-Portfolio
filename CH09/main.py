"""
Lab: "Cheapest Route" -- Weighted Graphs and Dijkstra's Algorithm

Part 1: Implement Dijkstra's algorithm (dict-of-dicts weighted graph).
Part 2: Compare BFS "fewest hops" vs Dijkstra "lowest cost".
Part 3: Break Dijkstra's algorithm on purpose with a negative-weight edge.
"""

from collections import deque

INFINITY = float("inf")


# ---------------------------------------------------------------------------
# PART 1: Weighted graphs and Dijkstra's algorithm
# ---------------------------------------------------------------------------

def find_lowest_cost_node(costs, processed):
    """
    Return the cheapest unprocessed node.
    """
    lowest_cost = INFINITY
    lowest_cost_node = None

    for node, cost in costs.items():
        if node not in processed and cost < lowest_cost:
            lowest_cost = cost
            lowest_cost_node = node

    return lowest_cost_node


def dijkstra(graph, start, finish):
    """
    Run Dijkstra's algorithm on a weighted graph.

    Returns:
        costs, parents
    """
    costs = {}
    parents = {}

    # Initialize every node as unreachable.
    for node in graph:
        costs[node] = INFINITY
        parents[node] = None

    # Set the costs of start's direct neighbors.
    for neighbor, weight in graph[start].items():
        costs[neighbor] = weight
        parents[neighbor] = start

    processed = []

    node = find_lowest_cost_node(costs, processed)

    while node is not None:
        cost = costs[node]
        neighbors = graph[node]

        for neighbor, weight in neighbors.items():
            new_cost = cost + weight

            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parents[neighbor] = node

        # The processed list is necessary because Dijkstra assumes that
        # once a node is finalized, its current cost is the cheapest possible.
        # Without processed, the same node could be selected again and again,
        # causing unnecessary repeated work and preventing the algorithm from
        # making clean progress through the graph.
        processed.append(node)

        node = find_lowest_cost_node(costs, processed)

    return costs, parents


def build_path(parents, start, finish):
    """
    Reconstruct the path by walking backward from finish to start.
    """
    path = []
    node = finish

    while node is not None:
        path.append(node)
        node = parents.get(node)

    path.reverse()
    return path


# Book's warm-up graph

book_graph = {
    "start": {"a": 6, "b": 2},
    "a": {"finish": 1},
    "b": {"a": 3, "finish": 5},
    "finish": {}
}


# ---------------------------------------------------------------------------
# PART 2: Fewest hops vs. lowest cost
# ---------------------------------------------------------------------------

def bfs_shortest_path(graph, start, finish):
    """
    Breadth-first search finds the path with the FEWEST EDGES.
    """
    queue = deque([start])
    visited = {start}
    parents = {start: None}

    while queue:
        node = queue.popleft()

        if node == finish:
            break

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = node
                queue.append(neighbor)

    path = []
    node = finish

    while node is not None:
        path.append(node)
        node = parents.get(node)

    path.reverse()
    return path


# Unweighted version

sf_unweighted = {
    "twin_peaks": ["a", "c"],
    "a": ["b"],
    "b": ["golden_gate"],
    "c": ["d"],
    "d": ["e"],
    "e": ["golden_gate"],
    "golden_gate": [],
}


# Weighted version

sf_weighted = {
    "twin_peaks": {"a": 10, "c": 3},
    "a": {"b": 10},
    "b": {"golden_gate": 10},
    "c": {"d": 3},
    "d": {"e": 3},
    "e": {"golden_gate": 3},
    "golden_gate": {},
}


# ---------------------------------------------------------------------------
# PART 3: Negative-weight edge
# ---------------------------------------------------------------------------

negative_graph = {
    "start": {"b": 1, "a": 2},
    "a": {"b": -10, "finish": 100},
    "b": {"finish": 5},
    "finish": {},
}


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():

    print("=== Part 1: Book's Start/A/B/Finish graph ===")

    costs, parents = dijkstra(
        book_graph,
        "start",
        "finish"
    )

    print("Costs:", costs)
    print("Parents:", parents)

    path = build_path(
        parents,
        "start",
        "finish"
    )

    print("Path:", path)

    print()

    # -----------------------------------------------------------------------
    # PART 2
    # -----------------------------------------------------------------------

    print("=== Part 2: Twin Peaks -> Golden Gate Bridge ===")

    bfs_path = bfs_shortest_path(
        sf_unweighted,
        "twin_peaks",
        "golden_gate"
    )

    print("BFS path (fewest hops):")
    print(bfs_path)

    print("BFS hop count:")
    print(len(bfs_path) - 1)

    sf_costs, sf_parents = dijkstra(
        sf_weighted,
        "twin_peaks",
        "golden_gate"
    )

    dijkstra_path = build_path(
        sf_parents,
        "twin_peaks",
        "golden_gate"
    )

    print("Dijkstra path (lowest cost):")
    print(dijkstra_path)

    print("Dijkstra total cost:")
    print(sf_costs["golden_gate"])

    # BFS considers "shortest" to mean the fewest number of edges or hops.
    # Dijkstra considers "shortest" to mean the lowest total edge weight.
    # Therefore, Dijkstra can choose a route with more hops if those hops
    # have a lower total cost.

    print()

    # -----------------------------------------------------------------------
    # PART 3
    # -----------------------------------------------------------------------

    print("=== Part 3: Negative-weight edge breaks Dijkstra ===")

    neg_costs, neg_parents = dijkstra(
        negative_graph,
        "start",
        "finish"
    )

    print("Costs:", neg_costs)
    print("Parents:", neg_parents)

    neg_path = build_path(
        neg_parents,
        "start",
        "finish"
    )

    print("Path:", neg_path)

    print("Reported cost:", neg_costs["finish"])
    print("True cheapest cost: -3")

    # Node "b" gets processed too early at cost 1 because the direct
    # start -> b edge looks cheaper than start -> a.
    # Later, the negative a -> b edge creates a cheaper route to b,
    # but Dijkstra assumes that a processed node will never become cheaper.
    # Negative weights break this assumption. Bellman-Ford can correctly
    # handle graphs containing negative-weight edges.

    # Reflection:
    # In real routing software, an edge's cost could represent travel time,
    # tolls, fuel usage, elevation, distance, data-transfer latency, or another
    # measurement. Changing what the edge weights represent changes which
    # route is considered "best," even though the Dijkstra algorithm itself
    # does not change.


if __name__ == "__main__":
    main()
