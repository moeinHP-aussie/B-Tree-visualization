<div align="center">
  <h1>🌳 B+ Tree Visualizer</h1>
  <p><b>An interactive B+ Tree implementation with real-time visualization and full CRUD operations</b></p>
</div>

<hr>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Algorithm-B%2B%20Tree-red.svg" alt="Algorithm">
  <img src="https://img.shields.io/badge/Domain-Data%20Structures-cyan.svg" alt="Domain">
  <img src="https://img.shields.io/badge/UI-PyQt6-orange.svg" alt="UI Framework">
  <img src="https://img.shields.io/badge/Feature-Visualization-brightgreen.svg" alt="Visualization">
  <img src="https://img.shields.io/badge/Operation-Rebalancing-yellow.svg" alt="Rebalancing">
  <img src="https://img.shields.io/badge/Linked%20List-Leaf%20Level-pink.svg" alt="Leaf Linked List">
</p>

<h2>📌 Overview</h2>
<p align="justify">
This project implements a <b>B+ Tree</b> data structure with a complete set of operations (insert, delete, search) and an interactive <b>PyQt6-based visualization tool</b>. B+ Trees are fundamental to database indexing and file systems due to their self-balancing nature, efficient range queries, and disk-friendly design. Unlike traditional visualization tools that only show static trees, this application provides real-time visual feedback showing how the tree reorganizes itself during splits, merges, and key redistribution operations.
</p>

<h2>✨ Key Features</h2>
<ul>
  <li><b>Complete CRUD Operations:</b> Full insert, delete, and search functionality with automatic rebalancing</li>
  <li><b>Real-time Visualization:</b> Live tree rendering showing node splits, merges, and key redistribution as they happen</li>
  <li><b>Leaf-level Linked List:</b> Visual representation of the leaf node chain enabling O(log n + k) range queries</li>
  <li><b>Search Highlighting:</b> Found keys are visually highlighted in yellow across the tree structure</li>
  <li><b>Configurable Tree Order:</b> Adjustable max degree (3–20) to demonstrate different branching factors</li>
  <li><b>Batch Operations:</b> Insert multiple keys at once using hyphen-separated syntax (e.g., <code>15 - 8 - 42 - 23</code>)</li>
  <li><b>Parent Pointer Support:</b> Each node maintains parent references, simplifying upward traversal during splits and merges</li>
  <li><b>Dark-themed Professional UI:</b> Modern interface with scrollable canvas, color-coded nodes, and responsive layout</li>
</ul>

<h2>🛠 Technical Implementation</h2>

<h3>1️⃣ Node Architecture with Parent Pointers</h3>
<p>
Unlike many B+ Tree implementations that traverse from root for every operation, this implementation stores <b>parent pointers</b> in every node. This optimization simplifies the split and merge propagation logic, eliminating the need to search for parent nodes during rebalancing operations.
</p>

python
class BPlusNode:
    def __init__(self, is_leaf=False):
        self.keys = []          # Sorted keys in the node
        self.children = []      # Child pointers (internal nodes only)
        self.is_leaf = is_leaf  # Node type flag
        self.next = None        # Next leaf pointer (leaf-level linked list)
        self.parent = None      # Parent reference for upward traversal
<h3>2️⃣ Intelligent Leaf Split with Key Promotion</h3> <p> When a leaf node exceeds <code>max_keys</code>, it splits into two nodes. The <b>first key</b> of the right leaf is promoted upward to become a routing key in the parent. This design ensures that internal nodes never store duplicate keys (unlike some implementations that push the middle key up). </p>
python
def _split_leaf(self, leaf):
    mid = len(leaf.keys) // 2
    new_leaf = BPlusNode(is_leaf=True)
    new_leaf.keys = leaf.keys[mid:]   # Right half moves to new leaf
    leaf.keys = leaf.keys[:mid]       # Left half stays
    
    # Update leaf linked list
    new_leaf.next = leaf.next
    leaf.next = new_leaf
    
    # Promote the first key of new leaf to parent
    self._insert_into_parent(leaf, new_leaf.keys[0], new_leaf)
<h3>3️⃣ Internal Node Split (Key Pushing)</h3> <p> Internal nodes follow a different splitting strategy: the <b>middle key is pushed up</b> to the parent (not copied), while the remaining keys are distributed between the two new internal nodes. This preserves the invariant that internal nodes contain only routing keys. </p>
python
def _split_internal(self, node):
    mid = len(node.keys) // 2
    push_up_key = node.keys[mid]
    
    new_node = BPlusNode(is_leaf=False)
    new_node.keys = node.keys[mid + 1:]
    new_node.children = node.children[mid + 1:]
    
    node.keys = node.keys[:mid]
    node.children = node.children[:mid + 1]
    
    self._insert_into_parent(node, push_up_key, new_node)
<h3>4️⃣ Deletion and Underflow Resolution</h3> <p> The deletion algorithm maintains B+ Tree invariants through a three-stage process: </p> <ol> <li><b>Key Removal:</b> Locate and remove the target key from the leaf node</li> <li><b>Borrow Attempt:</b> Try to borrow a key from left or right sibling if underflow occurs</li> <li><b>Merge Operation:</b> If borrowing fails, merge with a sibling and recursively fix parent underflow</li> </ol>
python
def _fix_leaf_underflow(self, leaf):
    # Try borrowing from right sibling
    if right_sibling and len(right_sibling.keys) > min_keys:
        leaf.keys.append(right_sibling.keys.pop(0))
        parent.keys[idx] = right_sibling.keys[0]
        return
    
    # Try borrowing from left sibling
    if left_sibling and len(left_sibling.keys) > min_keys:
        leaf.keys.insert(0, left_sibling.keys.pop())
        parent.keys[idx - 1] = leaf.keys[0]
        return
    
    # Merge with sibling
    leaf.keys.extend(right_sibling.keys)
    leaf.next = right_sibling.next
    parent.keys.pop(idx)
    parent.children.pop(idx + 1)
<h3>5️⃣ Hierarchical Tree Layout Algorithm</h3> <p> The visualization uses a <b>bottom-up positioning algorithm</b> that first places leaf nodes horizontally (with proper spacing), then recursively centers each internal node above its children. This produces aesthetically pleasing, balanced tree drawings even for skewed distributions. </p>
python
def _compute_positions(self):
    # Position leaf nodes left-to-right
    x = CANVAS_PAD_X
    for leaf in leaf_level:
        width = self._node_width(leaf)
        self._positions[id(leaf)] = (x + width / 2, leaf_y)
        x += width + LEAF_GAP
    
    # Center internal nodes over their children
    for level in reversed(internal_levels):
        for node in level:
            child_xs = [self._positions[id(c)][0] for c in node.children]
            cx = (min(child_xs) + max(child_xs)) / 2
            self._positions[id(node)] = (cx, internal_y)
<h2>📁 Project Structure</h2><pre> bplus-tree-visualizer/ ├── bplustree.py # Core B+ Tree implementation (node & tree classes) │ ├── BPlusNode # Node class with parent pointers │ └── BPlusTree # Tree class with insert/delete/search ├── gui_pyqt6.py # PyQt6 GUI application │ ├── TreeCanvas # Custom drawing widget │ └── BPlusTreeApp # Main window with controls ├── main.py # Entry point (dependency checker & launcher) └── README.md # This documentation </pre><h2>🎨 Visual Design Features</h2> <ul> <li><b>Color-coded Nodes:</b> Green for leaf nodes, blue for internal nodes</li> <li><b>Search Highlighting:</b> Yellow background for matching keys</li> <li><b>Leaf Links:</b> Dashed pink arrows showing the leaf-level linked list</li> <li><b>Drop Shadows:</b> Subtle shadows for visual depth</li> <li><b>Scrollable Canvas:</b> Handles trees of any size</li> <li><b>Status Bar:</b> Real-time feedback on operations</li> <li><b>Leaf Sequence Display:</b> Shows all keys in sorted order</li> </ul><h2>⚡ Algorithmic Highlights</h2><h3>Parent Pointer Optimization:</h3> <p> Unlike traditional recursive implementations that pass parent information down the call stack, storing parent pointers in each node enables <b>iterative upward traversal</b> during splits and merges. This reduces code complexity and improves cache locality. </p><h3>Efficient Range Query Support:</h3> <p> The leaf-level linked list allows O(log n + k) range queries, where k is the number of keys returned. After finding the starting leaf (O(log n)), subsequent keys are retrieved by following <code>next</code> pointers without additional tree traversal. </p><h3>Memory Layout:</h3> <ul> <li>Keys stored in sorted Python lists for efficient binary search</li> <li>Children stored as parallel lists to maintain index alignment</li> <li>Parent references stored as weak references to prevent circular dependency issues</li> </ul><h2>🎯 Educational Use Cases</h2><h3>Ideal Applications:</h3> <ul> <li><b>Database Indexing Course:</b> Demonstrate how B+ Trees maintain balance under insertions and deletions</li> <li><b>File System Design:</b> Show how directory structures organize metadata</li> <li><b>Algorithm Visualization:</b> Visualize the split, merge, and redistribution process in real-time</li> <li><b>Performance Analysis:</b> Experiment with different branching factors to observe tree height changes</li> </ul><h3>Learning Objectives:</h3> <ol> <li>Understanding the difference between leaf and internal node storage</li> <li>Visualizing how keys propagate upward during splits</li> <li>Observing how deletions trigger borrowing and merging</li> <li>Seeing the leaf-level linked list in action for range queries</li> <li>Experimenting with different order parameters to see height/width tradeoffs</li> </ol><h2>🔬 Technical Deep Dive</h2><h3>Split Strategy Comparison:</h3> <p> This implementation uses <b>asymmetric split strategies</b>: leaves promote the first key of the right node, while internal nodes push up the middle key. This design choice ensures that: </p> <ul> <li>Leaf nodes maintain their linked list integrity</li> <li>Internal nodes never contain keys that don't exist in the subtree</li> <li>Search operations can use simple binary comparison without special cases</li> </ul><h3>Minimum Occupancy Invariant:</h3> <p> After any operation, every non-root node maintains at least <code>⌈(max_degree-1)/2⌉</code> keys. This ensures: </p> <ul> <li>At least 50% storage utilization (except root)</li> <li>Bound on tree height: <code>log_{ceil(degree/2)} N</code></li> <li>Predictable performance guarantees</li> </ul><h3>GUI Rendering Pipeline:</h3> <ol> <li>Tree operations modify the internal data structure</li> <li><code>get_tree_layout()</code> performs BFS to collect node data</li> <li><code>_compute_positions()</code> calculates canvas coordinates</li> <li><code>paintEvent()</code> draws edges, links, and nodes</li> <li>Scroll area adjusts to fit the entire drawing</li> </ol><h2>🚀 Future Improvements</h2><h3>Planned Features:</h3> <ul> <li><b>Step-by-step Animation:</b> Animate each split, merge, and key movement operation</li> <li><b>String/Generic Key Support:</b> Extend beyond integer keys to support any comparable type</li> <li><b>Persistent Storage:</b> Save and load trees from disk (JSON or SQLite)</li> <li><b>Export Visualization:</b> Save tree diagrams as PNG, SVG, or PDF</li> <li><b>Performance Metrics Display:</b> Show tree height, node counts, and utilization percentages</li> <li><b>Batch Operations from File:</b> Load sequences of operations from text files</li> </ul><h3>Research Directions:</h3> <ul> <li>Bulk loading optimization for initial tree construction</li> <li>Concurrent B+ Tree simulation for multi-user scenarios</li> <li>Cache-aware node layout for better memory performance</li> </ul><h2>🤝 Contributing</h2> <p>Contributions are welcome! Here's how you can help:</p> <ol> <li><b>Report Bugs:</b> Open an issue with detailed description and screenshots</li> <li><b>Suggest Features:</b> Propose new features or improvements</li> <li><b>Submit Code:</b> Create pull requests with well-documented changes</li> <li><b>Improve Documentation:</b> Enhance this README or add usage tutorials</li> <li><b>Test Edge Cases:</b> Help test unusual scenarios and boundary conditions</li> </ol><h2>📦 Installation & Requirements</h2><pre><code>pip install PyQt6</code></pre><h3>Dependencies:</h3> <ul> <li><b>Python 3.10+</b>: Required for modern Python features (type hints, dataclasses)</li> <li><b>PyQt6</b>: For the graphical user interface</li> <li><b>No other external dependencies</b> – Pure Python implementation</li> </ul><h3>Install from source:</h3><pre><code>git clone https://github.com/yourusername/bplus-tree-visualizer.git cd bplus-tree-visualizer pip install PyQt6 python main.py</code></pre><p> The <code>main.py</code> script automatically detects missing PyQt6 and prompts for installation. </p><h2>🖥️ User Interface Guide</h2><h3>Control Panel Elements:</h3> <ol> <li><b>Max Degree Spin Box:</b> Set the tree order (3–20)</li> <li><b>Apply Button:</b> Reset tree with new degree (clears existing data)</li> <li><b>Key Input Field:</b> Enter keys separated by hyphens (e.g., <code>10 - 20 - 5</code>)</li> <li><b>Insert Button:</b> Add keys to the tree</li> <li><b>Search Button:</b> Find and highlight a key</li> <li><b>Delete Button:</b> Remove a key and rebalance</li> <li><b>Clear Button:</b> Reset tree to empty state</li> <li><b>Status Area:</b> Shows operation results and errors</li> <li><b>Leaf Sequence Display:</b> Shows all keys in sorted order</li> <li><b>Legend:</b> Color guide for node types</li> </ol><h3>Keyboard Shortcuts:</h3> <ul> <li><kbd>Enter</kbd>: Trigger insert operation</li> <li><kbd>Ctrl+S</kbd>: Focus search input</li> <li><kbd>Ctrl+D</kbd>: Focus delete input</li> </ul><h2>🧪 Example Walkthrough</h2><p><b>Step 1: Initial State</b><br> Empty tree with a single leaf node (root).</p><p><b>Step 2: Insert Keys 10, 20, 5</b><br> Keys inserted into the leaf node in sorted order: [5, 10, 20]</p><p><b>Step 3: Insert Key 15 (Triggers Split)</b><br> Leaf overflows → splits into [5, 10] and [15, 20]<br> Key 15 promoted to new root internal node → tree height becomes 2</p><p><b>Step 4: Search for Key 10</b><br> Traverse root (compare with 15 → go left) → found in left leaf, highlighted yellow</p><p><b>Step 5: Delete Key 10</b><br> Left leaf has [5] (below minimum) → borrows 15 from right leaf<br> Parent routing key updated from 15 to 20</p><p><b>Step 6: Delete Key 5 (Triggers Merge)</b><br> Left leaf empty → merges with right leaf → tree height returns to 1</p><h2>📄 License</h2><p> <b>MIT License</b> – Free for personal, educational, and commercial use. </p><hr><p align="center"> Built with ❤️ using Python, PyQt6, and a deep appreciation for balanced trees. </p> ```
