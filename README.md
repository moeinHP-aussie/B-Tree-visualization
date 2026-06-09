🌳 B+ Tree Visualizer
A high-performance B+ Tree implementation with an interactive PyQt6 visualization tool

https://img.shields.io/badge/python-3.10%252B-blue
https://img.shields.io/badge/GUI-PyQt6-41CD52
https://img.shields.io/badge/Algorithm-B%252B%2520Tree-FF6B6B
https://img.shields.io/badge/license-MIT-green

📌 Overview
This project implements a B+ Tree data structure with full insert, delete, and search operations, paired with a modern PyQt6-based graphical user interface. The B+ Tree is widely used in database indexing and file systems due to its balanced nature and efficient range queries. The visualizer allows users to see how keys propagate through internal nodes, how leaf nodes are linked for sequential access, and how the tree rebalances itself after splits and merges.

✨ Key Features
Complete B+ Tree Operations – Insert, delete, and search with automatic rebalancing (splits, merges, and borrowing).

Interactive Visualization – Real‑time rendering of the tree structure with distinct styling for leaf and internal nodes.

Leaf‑Level Linked List – Dashed arrows show the ordered sequence of leaf nodes, demonstrating efficient range scanning.

Search Highlighting – Found keys are highlighted in yellow for instant visual feedback.

Configurable Max Degree – Adjust the tree’s order (3–20) dynamically (clears the current tree).

Batch Insert – Insert multiple space‑separated keys at once (e.g., 10 - 20 - 5 - 30).

Leaf Sequence Display – The side panel shows all keys in sorted order as they appear in the leaf linked list.

Professional UI – Dark‑themed, responsive interface with hover effects, a scrollable canvas, and a status bar.

🛠 Technical Implementation
1️⃣ B+ Tree Node Design
Each node (internal or leaf) stores a sorted list of keys and maintains parent pointers to simplify splits and merges. Leaf nodes additionally hold a next pointer to form a singly linked list.

python
class BPlusNode:
    def __init__(self, is_leaf=False):
        self.keys = []          # sorted keys
        self.children = []      # child pointers (internal nodes only)
        self.is_leaf = is_leaf
        self.next = None        # next leaf node
        self.parent = None      # parent reference
2️⃣ Insertion & Split Logic
When a leaf exceeds max_keys, it splits into two leaves. The first key of the new right leaf is promoted up to the parent. For internal nodes, the middle key is pushed up (not copied), and the node is split into two. The propagation continues recursively up the tree.

python
def _split_leaf(self, leaf):
    mid = len(leaf.keys) // 2
    new_leaf = BPlusNode(is_leaf=True)
    new_leaf.keys = leaf.keys[mid:]   # right half
    leaf.keys = leaf.keys[:mid]       # left half
    # update linked list
    new_leaf.next = leaf.next
    leaf.next = new_leaf
    # promote first key of new leaf
    self._insert_into_parent(leaf, new_leaf.keys[0], new_leaf)
3️⃣ Deletion & Underflow Handling
After deleting a key from a leaf, the tree checks if the leaf falls below the minimum occupancy (ceil((max_degree-1)/2)). It first tries to borrow a key from a sibling; if that fails, it merges with a sibling. The same process is applied recursively to internal nodes. Routing keys in ancestors are updated using _update_internal_keys().

python
def _fix_leaf_underflow(self, leaf):
    # try borrowing from right sibling, then left sibling
    # if not possible, merge with right or left sibling
    # after merge, check parent underflow
4️⃣ Tree Layout & Drawing (PyQt6)
The get_tree_layout() method performs a BFS traversal and returns a level‑by‑level list of nodes with their keys and leaf status. The GUI canvas:

Computes positions – leaf nodes are placed left‑to‑right, internal nodes are centered above their children.

Draws edges – straight lines from internal nodes to children.

Draws leaf links – dashed arrows with arrowheads between consecutive leaf nodes.

Highlights searched keys – changes the background of the matching key slot.

Uses a scroll area – handles large trees gracefully.

python
def _compute_positions(self):
    # bottom‑up: position leaves, then parent centers
    for leaf in leaf_level:
        x += node_width + LEAF_GAP
    for internal in reverse_internal_levels:
        cx = (min(child_xs) + max(child_xs)) / 2
5️⃣ Leaf Sequence Display
The side panel displays all keys in sorted order by traversing the leaf linked list – a unique advantage of B+ Trees for range queries.

python
def get_all_leaves(self):
    node = self.root
    while not node.is_leaf:
        node = node.children[0]
    while node:
        result.extend(node.keys)
        node = node.next
📁 Project Structure
text
bplus-tree-visualizer/
├── bplustree.py          # Core B+ Tree implementation (node & tree classes)
├── gui_pyqt6.py          # PyQt6 GUI: canvas drawing, controls, event handlers
├── main.py               # Entry point (checks PyQt6, launches app)
└── README.md             # This documentation
⚡ Performance & Complexity
Operation	Average Case	Worst Case
Search	O(logₓ N)	O(logₓ N)
Insert	O(logₓ N)	O(logₓ N)
Delete	O(logₓ N)	O(logₓ N)
Range scan (k keys)	O(logₓ N + k)	O(logₓ N + k)
N = number of keys, x = max_degree (order)

The height of the tree is kept low (typically 3–4 for millions of keys).

Leaf nodes store up to max_degree - 1 keys, and the leaf linked list enables efficient sequential access without traversing the tree again.

🎯 Use Cases
Educational – Understand B+ Tree internals (splits, merges, borrowing, pointer updates).

Database Indexing – Prototype index behaviour for DBMS courses.

File System Simulation – Model how directory structures organise metadata.

Algorithm Visualization – Show how balanced trees remain balanced after many modifications.

🚀 Future Improvements
Node collapsing – Display very large trees by summarising subtrees.

Step‑by‑step animation – Allow users to see each insertion/deletion step.

Disk‑aware simulation – Simulate block reads/writes and page caching.

Export image – Save the current tree layout as PNG/SVG.

Custom key types – Support strings or other comparable types.

📦 Installation & Requirements
Prerequisites
Python 3.10 or higher

PyQt6

No other external dependencies (only Python standard library plus PyQt6)

Install from source
bash
git clone https://github.com/yourusername/bplus-tree-visualizer.git
cd bplus-tree-visualizer
pip install PyQt6
python main.py
The main.py script automatically checks for PyQt6 and prompts you to install it if missing.

Manual installation
bash
pip install PyQt6
python main.py
🖥️ How to Use
Set Max Degree – Use the spin box (3–20) and click Apply (clears the tree).

Insert Keys – Enter one or more integers separated by hyphens, e.g., 15 - 8 - 42 - 23, then click Insert.

Search – Enter a single key and click Search – the node slot turns yellow if found.

Delete – Enter a key and click Delete – the tree rebalances automatically.

Clear Tree – Removes all keys (keeps current max degree).

Leaf Sequence – The bottom panel shows all keys in sorted order (via the leaf linked list).

Note: The tree automatically expands in height when the root splits, and shrinks when the root becomes empty.

🧪 Example Walkthrough
Initial tree (empty) → Insert 10 → Insert 20 → Insert 5 → Insert 15 (root split) → Delete 10 (borrow from sibling) → Delete 5 (merge leaves). The GUI updates after every operation.

🤝 Contributing
Contributions are welcome! Areas you can help:

Bug reports – Open an issue with a clear description and screenshots.

Features – Propose new features (e.g., animation, file I/O, key ranges).

Code – Submit pull requests for bug fixes or enhancements.

Documentation – Improve this README or add tutorials.
