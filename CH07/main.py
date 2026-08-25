"""
Lab: Rooted & Compressed - Tree Traversal and Huffman Coding
COSC 2436 - Chapter 7

This starter code scaffolds three parts:
Part 1: BFS vs DFS directory traversal
Part 2: DFS vs BFS shortest-path counterexample (mango-seller style)
Part 3: Mini Huffman coding (build tree, encode, decode)
"""

from collections import deque
import heapq

# ---------------------------------------------------------------------------
# PART 1: File directory traversal (BFS vs DFS)
# ---------------------------------------------------------------------------


class DirNode:
    """A simple directory/file node used to build a tree."""

    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children is not None else []


def build_sample_directory():
    """Build a small, hardcoded nested directory tree."""

    file1 = DirNode("notes.txt")
    file2 = DirNode("todo.txt")
    file3 = DirNode("photo.png")
    file4 = DirNode("song.mp3")
    file5 = DirNode("draft.docx")
    file6 = DirNode("index.html")
    file7 = DirNode("style.css")

    docs = DirNode("docs", [file1, file2, file5])
    media = DirNode("media", [file3, file4])
    web = DirNode("web", [file6, file7])

    root = DirNode("root", [docs, media, web])
    return root


def print_names_bfs(start_dir):
    """
    Print every node name using breadth-first traversal.
    """
    queue = deque([start_dir])

    # Trees have no cycles, so each node can only be reached through
    # one parent path from the root. Therefore, no searched set is needed.
    while queue:
        current = queue.popleft()
        print(current.name)

        for child in current.children:
            queue.append(child)


def print_names_dfs(start_dir):
    """
    Print every node name using recursive depth-first traversal.
    """
    print(start_dir.name)

    for child in start_dir.children:
        print_names_dfs(child)


# ---------------------------------------------------------------------------
# PART 2: DFS fails at shortest path - counterexample
# ---------------------------------------------------------------------------


class TreeNode:
    """A binary tree node used for the mango-seller counterexample."""

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def build_mango_tree():
    """
    Build a binary tree where DFS finds a farther target before
    BFS finds the closer target.
    """

    # Left branch: root -> left -> left -> left = target
    left_leaf = TreeNode("target")
    left_level2 = TreeNode("L2", left=left_leaf)
    left_level1 = TreeNode("L1", left=left_level2)

    # Right branch: root -> right = target
    right_leaf = TreeNode("target")

    root = TreeNode("root", left=left_level1, right=right_leaf)
    return root


def dfs_search(root, target):
    """
    Recursively search the tree using DFS.
    Search the left branch completely before the right branch.
    """
    if root is None:
        return None

    if root.value == target:
        return root

    left_result = dfs_search(root.left, target)

    if left_result is not None:
        return left_result

    return dfs_search(root.right, target)


def bfs_search(root, target):
    """
    Search the tree using BFS and return the shallowest matching node.
    """
    queue = deque([root]) if root is not None else deque()

    while queue:
        current = queue.popleft()

        if current.value == target:
            return current

        if current.left is not None:
            queue.append(current.left)

        if current.right is not None:
            queue.append(current.right)

    return None


# ---------------------------------------------------------------------------
# PART 3: Mini Huffman coding
# ---------------------------------------------------------------------------


class HuffmanNode:
    """A node in the Huffman tree."""

    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def count_frequencies(text):
    """
    Count how many times each character appears in text.
    """
    freq_dict = {}

    for char in text:
        freq_dict[char] = freq_dict.get(char, 0) + 1

    return freq_dict


def build_huffman_tree(freq_dict):
    """
    Build a Huffman tree using a heap-based greedy algorithm.
    """
    heap = []

    # Add every character as a leaf node.
    for char, freq in freq_dict.items():
        node = HuffmanNode(freq, char)
        heapq.heappush(heap, node)

    # Empty input.
    if not heap:
        return None

    # Special case: only one unique character.
    # Wrap it in an internal node so the tree still has a branch.
    if len(heap) == 1:
        only = heapq.heappop(heap)
        return HuffmanNode(only.freq, left=only)

    # Repeatedly combine the two least-frequent nodes.
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = HuffmanNode(
            left.freq + right.freq,
            left=left,
            right=right
        )

        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(root):
    """
    Walk the Huffman tree and create a character-to-bitstring dictionary.
    Left = 0, right = 1.
    """
    codes = {}

    def helper(node, path):
        if node is None:
            return

        # A node with a character is a leaf.
        if node.char is not None:
            # If there is only one character, give it code "0".
            codes[node.char] = path if path else "0"
            return

        helper(node.left, path + "0")
        helper(node.right, path + "1")

    helper(root, "")
    return codes


def huffman_encode(text, codes):
    """
    Encode text into one bitstring using the Huffman code table.
    """
    encoded = ""

    for char in text:
        encoded += codes[char]

    return encoded


def huffman_decode(encoded, root):
    """
    Decode a Huffman bitstring by walking the tree.
    """
    if root is None:
        return ""

    # Special case for a tree containing only one character.
    if root.left is not None and root.right is None:
        return root.left.char * len(encoded)

    decoded = []
    current = root

    for bit in encoded:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.char is not None:
            decoded.append(current.char)
            current = root

    return "".join(decoded)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":

    # ---- Part 1 ----
    print("Part 1: Directory traversal")
    sample_root = build_sample_directory()

    print("BFS order:")
    print_names_bfs(sample_root)

    print("DFS order:")
    print_names_dfs(sample_root)

    # BFS and DFS visit the same nodes but in different orders because
    # BFS explores one level at a time while DFS completely explores one
    # branch before moving to the next. No searched set is needed because
    # this is a tree with no cycles.

    # ---- Part 2 ----
    print("\nPart 2: DFS vs BFS shortest path counterexample")
    mango_root = build_mango_tree()

    dfs_result = dfs_search(mango_root, "target")
    bfs_result = bfs_search(mango_root, "target")

    print("DFS found target node:")
    print(dfs_result.value if dfs_result else None)

    print("BFS found target node:")
    print(bfs_result.value if bfs_result else None)

    # DFS finds the target on the deeper left branch first.
    # BFS finds the target at the shallower right branch first.

    # ---- Part 3 ----
    print("\nPart 3: Mini Huffman coding")
    sample_text = "huffman coding builds trees from frequencies"

    freqs = count_frequencies(sample_text)
    print("Character frequencies:")
    print(freqs)

    huffman_root = build_huffman_tree(freqs)
    codes = generate_codes(huffman_root)

    print("Code table:")
    print(codes)

    encoded_text = huffman_encode(sample_text, codes)
    print("Encoded bitstring:")
    print(encoded_text)

    decoded_text = huffman_decode(encoded_text, huffman_root)
    print("Decoded text:")
    print(decoded_text)

    print("Round trip matches original:")
    print(decoded_text == sample_text)

    # Frequent characters receive shorter Huffman codes because the greedy
    # algorithm repeatedly combines the two least-frequent nodes. This
    # places common characters closer to the root, reducing the total
    # number of bits needed to represent the entire message.

    fixed_width_bits = 8 * len(sample_text)
    compressed_bits = len(encoded_text)

    print("Fixed-width bit count (8 times length of string):")
    print(fixed_width_bits)

    print("Compressed bit count:")
    print(compressed_bits)

