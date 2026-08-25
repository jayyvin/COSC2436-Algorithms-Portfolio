"""
Lab: Six Degrees -- Graph Modeling & Breadth-First Search
Chapter 6 concepts: representing a network as a graph (dict of lists),
and using a queue-based BFS to answer "is there a path?" and
"what's the shortest path?", plus a topological sort mini-exercise.

Fill in the TODO sections. Do not change the shape of the data
structures or the function signatures.
"""

import collections


# ---------------------------------------------------------------------------
# PART 1 DATA: a small professional/social network
# ---------------------------------------------------------------------------
network = {
    "you": ["alice", "bob", "claire"],
    "alice": ["peggy"],
    "bob": ["anuj", "peggy"],
    "claire": ["thom", "jonny"],
    "peggy": ["you", "maria"],
    "anuj": [],
    "thom": ["diego"],
    "jonny": ["sam"],
    "maria": ["lee"],
    "diego": [],
    "sam": [],
    "lee": [],
}


skills = {
    "you": ["project_management"],
    "alice": ["design"],
    "bob": ["sales"],
    "claire": ["marketing"],
    "peggy": ["finance"],
    "anuj": ["manufacturing"],
    "thom": ["design"],
    "jonny": ["sales"],
    "maria": ["manufacturing"],
    "diego": ["python"],
    "sam": ["python"],
    "lee": ["manufacturing"],
}


def person_has_skill(name, skill_to_find):
    """
    Return True if `name` has `skill_to_find` in the skills dict, else False.
    """
    persons_skills = skills.get(name, [])
    return skill_to_find in persons_skills


def search(start_name, skill_to_find):
    """
    Breadth-first search over `network` starting at start_name.
    Return True if someone reachable has the skill.
    """

    search_queue = collections.deque()
    search_queue.extend(network[start_name])

    searched = set()

    while search_queue:
        person = search_queue.popleft()

        if person not in searched:
            if person_has_skill(person, skill_to_find):
                return True
            else:
                search_queue.extend(network[person])
                searched.add(person)

    return False


# ---------------------------------------------------------------------------
# PART 2: shortest path
# ---------------------------------------------------------------------------

def search_shortest_path(start_name, skill_to_find):
    """
    Return the shortest number of hops to someone with the skill.
    Return -1 if no one has the skill.
    """

    search_queue = collections.deque(
        (neighbor, 1) for neighbor in network[start_name]
    )

    searched = set()

    while search_queue:
        person, distance = search_queue.popleft()

        if person not in searched:
            if person_has_skill(person, skill_to_find):
                return distance
            else:
                for neighbor in network[person]:
                    search_queue.append((neighbor, distance + 1))

                searched.add(person)

    return -1


def search_with_path(start_name, skill_to_find):
    """
    Return the shortest path to someone with the requested skill.
    Return [] if nobody is found.
    """

    search_queue = collections.deque(network[start_name])

    searched = set()

    came_from = {
        neighbor: start_name
        for neighbor in network[start_name]
    }

    while search_queue:
        person = search_queue.popleft()

        if person not in searched:
            if person_has_skill(person, skill_to_find):
                path = [person]

                while path[-1] != start_name:
                    path.append(came_from[path[-1]])

                path.reverse()
                return path

            else:
                for neighbor in network[person]:
                    if neighbor not in came_from:
                        came_from[neighbor] = person
                        search_queue.append(neighbor)

                searched.add(person)

    return []


# ---------------------------------------------------------------------------
# PART 3: topological sort mini-exercise
# ---------------------------------------------------------------------------

dependency_graph = {
    "create_repo_template": [],
    "write_starter_code": ["create_repo_template"],
    "write_tests": ["write_starter_code"],
    "create_classroom_assignment": [
        "write_starter_code",
        "write_tests"
    ],
    "invite_students": ["create_classroom_assignment"],
    "grade_submissions": ["invite_students"],
}


proposed_order = [
    "create_repo_template",
    "write_starter_code",
    "write_tests",
    "create_classroom_assignment",
    "invite_students",
    "grade_submissions",
]


def is_valid_order(order, dep_graph):
    """
    Return True if order is a valid topological ordering.
    """

    positions = {}

    for index, step in enumerate(order):
        positions[step] = index

    for step in dep_graph:
        for dependency in dep_graph[step]:
            if positions[dependency] > positions[step]:
                return False

    return True


def topological_sort(dep_graph):
    """
    Return a valid topological ordering.
    """

    order = []

    while len(order) < len(dep_graph):

        for step in dep_graph:

            if step not in order:

                ready = True

                for dependency in dep_graph[step]:
                    if dependency not in order:
                        ready = False
                        break

                if ready:
                    order.append(step)

    return order


if __name__ == "__main__":

    found_manufacturing = search("you", "manufacturing")
    print(found_manufacturing)

    found_python = search("you", "python")
    print(found_python)

    distance_manufacturing = search_shortest_path(
        "you",
        "manufacturing"
    )
    print(distance_manufacturing)

    path_to_python = search_with_path(
        "you",
        "python"
    )
    print(path_to_python)

    order_is_valid = is_valid_order(
        proposed_order,
        dependency_graph
    )
    print(order_is_valid)

    computed_order = topological_sort(dependency_graph)
    print(computed_order)
