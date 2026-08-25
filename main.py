
"""
Lab: "Out of Balance" -- Binary Search Trees and Why Shape Matters

Part 1: Build a working BST
Part 2: Watch a BST degenerate into a linked list on sorted input
Part 3: Rotate to fix it
"""


class BSTNode:
    """A single node in a binary search tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ---------------------------------------------------------------------------
# PART 1: Build a working BST
# ---------------------------------------------------------------------------

def insert(root, value):
    """Recursively insert value into the BST."""

    if root is None:
        return BSTNode(value)

    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)

    return root


def search(root, value):
    """
    Search for value and return (found, comparisons).

    This is similar to Chapter 1 binary search because each comparison
    eliminates one side of the remaining search space. Here we follow
    left/right child pointers instead of using array indexes.
    """

    comparisons = 0
    node = root

    while node is not None:
        comparisons += 1

        if node.value == value:
            return True, comparisons
        elif value < node.value:
            node = node.left
        else:
            node = node.right

    return False, comparisons


def height(root):
    """Return the height of the tree. An empty tree has height 0."""

    if root is None:
        return 0

    return 1 + max(height(root.left), height(root.right))


def in_order(root, result=None):
    """Return the values using recursive in-order traversal."""

    if result is None:
        result = []

    if root is None:
        return result

    in_order(root.left, result)
    result.append(root.value)
    in_order(root.right, result)

    return result


# ---------------------------------------------------------------------------
# PART 2: Watch it degenerate
# ---------------------------------------------------------------------------

def compare_bst_shapes():
    """
    Build two BSTs from the same values using different insertion orders.
    """

    mixed_order = [
        50, 30, 70, 20, 40, 60,
        80, 10, 25, 35, 45, 65
    ]

    sorted_order = sorted(mixed_order)
    largest_value = max(mixed_order)

    tree_a = None
    tree_b = None

    # Build Tree A using mixed insertion order.
    for value in mixed_order:
        tree_a = insert(tree_a, value)

    # Build Tree B using sorted insertion order.
    for value in sorted_order:
        tree_b = insert(tree_b, value)

    height_a = height(tree_a)
    height_b = height(tree_b)

    in_order_a = in_order(tree_a)
    in_order_b = in_order(tree_b)

    found_a, comparisons_a = search(tree_a, largest_value)
    found_b, comparisons_b = search(tree_b, largest_value)

    print("Tree A height:", height_a)
    print("Tree B height:", height_b)
    print("Tree A in-order:", in_order_a)
    print("Tree B in-order:", in_order_b)
    print(
        "Tree A search comparisons for largest value:",
        comparisons_a
    )
    print(
        "Tree B search comparisons for largest value:",
        comparisons_b
    )

    # Sorted input is the worst case for a plain BST because every new
    # value is greater than the values already inserted. The tree keeps
    # growing in one direction instead of branching, so it becomes
    # effectively a linked list.

    return tree_a, tree_b


# ---------------------------------------------------------------------------
# PART 3: Rotate to fix it
# ---------------------------------------------------------------------------

def balance_factor(node):
    """Return the left height minus the right height."""

    if node is None:
        return 0

    return height(node.left) - height(node.right)


def rotate_right(node):
    """
    Perform a single right rotation.

    Before:
        node
        /
      pivot
      /  \
     A    B

    After:
       pivot
       /  \
      A   node
           /
          B
    """

    pivot = node.left

    node.left = pivot.right
    pivot.right = node

    return pivot


def rotate_left(node):
    """
    Perform a single left rotation.

    Before:
      node
         \
         pivot
         /   \
        A     B

    After:
       pivot
       /   \
     node   B
       \
        A
    """

    pivot = node.right

    node.right = pivot.left
    pivot.left = node

    return pivot


def rotate_left_right(node):
    """Perform the double rotation for the LR case."""

    node.left = rotate_left(node.left)
    return rotate_right(node)


def rotate_right_left(node):
    """Perform the double rotation for the RL case."""

    node.right = rotate_right(node.right)
    return rotate_left(node)


def avl_insert(root, value):
    """Insert into the BST and rebalance it as an AVL tree."""

    if root is None:
        return BSTNode(value)

    if value < root.value:
        root.left = avl_insert(root.left, value)
    else:
        root.right = avl_insert(root.right, value)

    balance = balance_factor(root)

    # LL case
    if balance > 1 and value < root.left.value:
        return rotate_right(root)

    # RR case
    if balance < -1 and value >= root.right.value:
        return rotate_left(root)

    # LR case
    if balance > 1 and value >= root.left.value:
        return rotate_left_right(root)

    # RL case
    if balance < -1 and value < root.right.value:
        return rotate_right_left(root)

    return root


def avl_demo():
    """Build an AVL tree using the same sorted values."""

    sorted_order = sorted([
        50, 30, 70, 20, 40, 60,
        80, 10, 25, 35, 45, 65
    ])

    avl_root = None

    for value in sorted_order:
        avl_root = avl_insert(avl_root, value)

    print("AVL tree height after sorted insertion:", height(avl_root))
    print("AVL in-order:", in_order(avl_root))

    return avl_root


# ---------------------------------------------------------------------------
# REFLECTION
# ---------------------------------------------------------------------------

def print_reflection():
    """
    Print the Big-O comparison table for the three structures.
    """

    print("Structure              Search       Insert")
    print("Sorted array           O(log n)     O(n)")
    print("Linked list            O(n)         O(1)")
    print("Balanced BST           O(log n)     O(log n)")

    print()
    print(
        "A database uses a tree index because a balanced tree provides "
        "fast searching while also allowing efficient insertion."
    )


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print("=== PART 1: Basic BST operations ===")

    root = None

    starter_values = [50, 30, 70, 20, 40]

    for value in starter_values:
        root = insert(root, value)

    print("In-order:", in_order(root))
    print("Height:", height(root))

    found, comparisons = search(root, 40)

    print("Found 40:", found)
    print("Comparisons:", comparisons)

    print()
    print("=== PART 2: Same values, different insertion order ===")

    tree_a, tree_b = compare_bst_shapes()

    print()
    print("=== PART 3: AVL rotations fix the shape ===")

    avl_root = avl_demo()

    print()
    print("AVL height compared with ordinary BST:")
    print("Ordinary sorted BST height:", height(tree_b))
    print("AVL height:", height(avl_root))

    print()
    print("=== REFLECTION ===")

    print_reflection()


if __name__ == "__main__":
    main()


