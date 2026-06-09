<div align="center">
  <h1>🌳 B+ Tree Visualizer</h1>
  <p><b>A high-performance B+ Tree implementation with an interactive PyQt6 visualization tool</b></p>
</div>

<hr>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Algorithm-B%2B%20Tree-red.svg" alt="Algorithm">
  <img src="https://img.shields.io/badge/Domain-Data%20Structures-cyan.svg" alt="Domain">
  <img src="https://img.shields.io/badge/UI-PyQt6-orange.svg" alt="UI Framework">
  <img src="https://img.shields.io/badge/Feature-Visualization-green.svg" alt="Visualization">
  <img src="https://img.shields.io/badge/Operation-Insert%2FDelete%2FSearch-yellow.svg" alt="Operations">
</p>

<h2>📌 Overview</h2>
<p align="justify">
This project implements a <b>B+ Tree</b> data structure with full insert, delete, and search operations, paired with a modern <b>PyQt6-based graphical user interface</b>. The B+ Tree is widely used in database indexing and file systems due to its balanced nature and efficient range queries. The visualizer allows users to see how keys propagate through internal nodes, how leaf nodes are linked for sequential access, and how the tree rebalances itself after splits and merges.
</p>

<h2>✨ Key Features</h2>
<ul>
  <li><b>Complete B+ Tree Operations</b> – Insert, delete, and search with automatic rebalancing (splits, merges, and borrowing)</li>
  <li><b>Interactive Visualization</b> – Real‑time rendering of the tree structure with distinct styling for leaf and internal nodes</li>
  <li><b>Leaf‑Level Linked List</b> – Dashed arrows show the ordered sequence of leaf nodes, demonstrating efficient range scanning</li>
  <li><b>Search Highlighting</b> – Found keys are highlighted in yellow for instant visual feedback</li>
  <li><b>Configurable Max Degree</b> – Adjust the tree's order (3–20) dynamically (clears the current tree)</li>
  <li><b>Batch Insert</b> – Insert multiple space‑separated keys at once (e.g., <code>10 - 20 - 5 - 30</code>)</li>
  <li><b>Leaf Sequence Display</b> – The side panel shows all keys in sorted order as they appear in the leaf linked list</li>
  <li><b>Professional UI</b> – Dark‑themed, responsive interface with hover effects, a scrollable canvas, and a status bar</li>
</ul>

<h2>🛠 Technical Implementation</h2>

<h3>1️⃣ B+ Tree Node Design</h3>
<p>
Each node (internal or leaf) stores a sorted list of keys and maintains parent pointers to simplify splits and merges. Leaf nodes additionally hold a <code>next</code> pointer to form a singly linked list.
</p>

class BPlusNode:
    def __init__(self, is_leaf=False):
        self.keys = []          # sorted keys
        self.children = []      # child pointers (internal nodes only)
        self.is_leaf = is_leaf
        self.next = None        # next leaf node
        self.parent = None      # parent reference

<h3>2️⃣ Insertion & Split Logic</h3> <p> When a leaf exceeds <code>max_keys</code>, it splits into two leaves. The <b>first key</b> of the new right leaf is promoted up to the parent. For internal nodes, the <b>middle key</b> is pushed up (not copied), and the node is split into two. The propagation continues recursively up the tree. </p>
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
<h3>3️⃣ Deletion & Underflow Handling</h3> <p> After deleting a key from a leaf, the tree checks if the leaf falls below the minimum occupancy (<code>ceil((max_degree-1)/2)</code>). It first tries to <b>borrow</b> a key from a sibling; if that fails, it <b>merges</b> with a sibling. The same process is applied recursively to internal nodes. Routing keys in ancestors are updated using <code>_update_internal_keys()</code>. </p>
python
def _fix_leaf_underflow(self, leaf):
    # try borrowing from right sibling, then left sibling
    # if not possible, merge with right or left sibling
    # after merge, check parent underflow
<h3>4️⃣ Tree Layout & Drawing (PyQt6)</h3> <p> The <code>get_tree_layout()</code> method performs a BFS traversal and returns a level‑by‑level list of nodes with their keys and leaf status. The GUI canvas: </p> <ul> <li><b>Computes positions</b> – leaf nodes are placed left‑to‑right, internal nodes are centered above their children</li> <li><b>Draws edges</b> – straight lines from internal nodes to children</li> <li><b>Draws leaf links</b> – dashed arrows with arrowheads between consecutive leaf nodes</li> <li><b>Highlights searched keys</b> – changes the background of the matching key slot</li> <li><b>Uses a scroll area</b> – handles large trees gracefully</li> </ul>
python
def _compute_positions(self):
    # bottom‑up: position leaves, then parent centers
    for leaf in leaf_level:
        x += node_width + LEAF_GAP
    for internal in reverse_internal_levels:
        cx = (min(child_xs) + max(child_xs)) / 2
<h3>5️⃣ Leaf Sequence Display</h3> <p> The side panel displays all keys in sorted order by traversing the leaf linked list – a unique advantage of B+ Trees for range queries. </p>
python
def get_all_leaves(self):
    node = self.root
    while not node.is_leaf:
        node = node.children[0]
    while node:
        result.extend(node.keys)
        node = node.next
<h2>📁 Project Structure</h2><pre> bplus-tree-visualizer/ ├── bplustree.py # Core B+ Tree implementation (node & tree classes) ├── gui_pyqt6.py # PyQt6 GUI: canvas drawing, controls, event handlers ├── main.py # Entry point (checks PyQt6, launches app) └── README.md # This documentation </pre><h2>⚡ Performance & Complexity</h2>
Operation	Average Case	Worst Case
Search	O(logₓ N)	O(logₓ N)
Insert	O(logₓ N)	O(logₓ N)
Delete	O(logₓ N)	O(logₓ N)
Range scan (k keys)	O(logₓ N + k)	O(logₓ N + k)
<p align="justify"> <b>N</b> = number of keys, <b>x</b> = max_degree (order). The height of the tree is kept low (typically 3–4 for millions of keys). Leaf nodes store up to <code>max_degree - 1</code> keys, and the leaf linked list enables efficient sequential access without traversing the tree again. </p><h2>🎯 Use Cases</h2><h3>Ideal Applications:</h3> <ul> <li><b>Educational Tool:</b> Understand B+ Tree internals (splits, merges, borrowing, pointer updates)</li> <li><b>Database Indexing:</b> Prototype index behaviour for DBMS courses</li> <li><b>File System Simulation:</b> Model how directory structures organise metadata</li> <li><b>Algorithm Visualization:</b> Show how balanced trees remain balanced after many modifications</li> </ul><h2>⚠️ Limitations & Considerations</h2><h3>Current Limitations:</h3> <ul> <li>Only supports integer keys (not strings or other types)</li> <li>No persistent storage (in-memory only)</li> <li>No undo/redo functionality</li> <li>Limited to trees that fit on screen</li> </ul><h3>Best Practices:</h3> <ol> <li>Start with degree 4 for small demonstrations (fewer than 50 keys)</li> <li>Use degree 5–7 for medium trees (50–500 keys)</li> <li>Degree 8+ creates wider, shorter trees (better for large datasets)</li> <li>Clear the tree before changing degree to avoid inconsistencies</li> </ol><h2>🔄 Comparison with Other Tree Structures</h2><table> <tr> <th>Structure</th> <th>Advantages</th> <th>Disadvantages</th> </tr> <tr> <td><b>Binary Search Tree</b></td> <td>Simple, O(log n) average</td> <td>Can become skewed (O(n) worst case)</td> </tr> <tr> <td><b>AVL / Red-Black Tree</b></td> <td>Always balanced, O(log n) guaranteed</td> <td>Complex rotations, not disk-friendly</td> </tr> <tr> <td><b>B+ Tree (This Project)</b></td> <td>Disk-friendly, efficient range queries, high branching factor</td> <td>More complex implementation</td> </tr> </table><h2>🚀 Future Improvements</h2><h3>Planned Features:</h3> <ul> <li>Node collapsing – Display very large trees by summarising subtrees</li> <li>Step‑by‑step animation – Allow users to see each insertion/deletion step</li> <li>Disk‑aware simulation – Simulate block reads/writes and page caching</li> <li>Export image – Save the current tree layout as PNG/SVG</li> <li>Custom key types – Support strings or other comparable types</li> <li>Undo/Redo functionality for operations</li> </ul><h2>🤝 Contributing</h2> <p>Contributions are welcome! Here's how you can help:</p> <ol> <li><b>Report Bugs:</b> Open an issue with detailed bug reports and screenshots</li> <li><b>Suggest Features:</b> Propose new features or improvements</li> <li><b>Submit Code:</b> Create pull requests with well-documented changes</li> <li><b>Improve Documentation:</b> Help enhance this README or add tutorials</li> </ol><h2>📦 Installation & Requirements</h2><pre><code>pip install PyQt6</code></pre><h3>Dependencies:</h3> <ul> <li><b>Python 3.10+</b>: Required for modern Python features</li> <li><b>PyQt6</b>: For the graphical user interface</li> <li><b>No other external dependencies</b> – only Python standard library plus PyQt6</li> </ul><h3>Install from source:</h3><pre><code>git clone https://github.com/yourusername/bplus-tree-visualizer.git cd bplus-tree-visualizer pip install PyQt6 python main.py</code></pre><p> The <code>main.py</code> script automatically checks for PyQt6 and prompts you to install it if missing. </p><h2>🖥️ How to Use</h2><ol> <li><b>Set Max Degree</b> – Use the spin box (3–20) and click <b>Apply</b> (clears the tree)</li> <li><b>Insert Keys</b> – Enter one or more integers separated by hyphens, e.g., <code>15 - 8 - 42 - 23</code>, then click <b>Insert</b></li> <li><b>Search</b> – Enter a single key and click <b>Search</b> – the node slot turns yellow if found</li> <li><b>Delete</b> – Enter a key and click <b>Delete</b> – the tree rebalances automatically</li> <li><b>Clear Tree</b> – Removes all keys (keeps current max degree)</li> <li><b>Leaf Sequence</b> – The bottom panel shows all keys in sorted order (via the leaf linked list)</li> </ol><blockquote> <p><b>💡 Note:</b> The tree automatically expands in height when the root splits, and shrinks when the root becomes empty.</p> </blockquote><h2>🧪 Example Walkthrough</h2><p> <b>Initial tree (empty)</b> → Insert <code>10</code> → Insert <code>20</code> → Insert <code>5</code> → Insert <code>15</code> (root split) → Delete <code>10</code> (borrow from sibling) → Delete <code>5</code> (merge leaves). The GUI updates after every operation. </p><h2>📄 License</h2><p> <b>MIT License</b> – free for personal and commercial use. </p><hr><p align="center"> Built with ❤️ using Python, PyQt6, and a passion for data structures. </p> ```
