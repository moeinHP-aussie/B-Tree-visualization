<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B+ Tree Visualizer - مستندات پروژه</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #e2e8f0;
            line-height: 1.6;
            padding: 40px 20px;
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
            background: rgba(30, 30, 46, 0.95);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }

        /* Header Section */
        .header {
            background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
            padding: 50px 60px;
            border-bottom: 1px solid #383850;
            text-align: center;
        }

        .header h1 {
            font-size: 3rem;
            background: linear-gradient(135deg, #60a5fa, #4ade80);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 15px;
        }

        .header p {
            font-size: 1.2rem;
            color: #94a3b8;
            max-width: 800px;
            margin: 0 auto;
        }

        .badges {
            margin-top: 25px;
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .badge {
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            background: rgba(129, 140, 248, 0.15);
            border: 1px solid rgba(129, 140, 248, 0.3);
            color: #a5b4fc;
        }

        /* Content */
        .content {
            padding: 50px 60px;
        }

        h2 {
            font-size: 1.8rem;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #4ade80;
            display: inline-block;
            color: #e2e8f0;
        }

        h3 {
            font-size: 1.4rem;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #60a5fa;
        }

        h4 {
            font-size: 1.2rem;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #cbd5e1;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .feature-card {
            background: rgba(42, 42, 62, 0.6);
            border: 1px solid #383850;
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            border-color: #60a5fa;
        }

        .feature-card h4 {
            margin-top: 0;
            color: #4ade80;
        }

        pre {
            background: #0f0f1a;
            border: 1px solid #2d2d44;
            border-radius: 12px;
            padding: 20px;
            overflow-x: auto;
            margin: 20px 0;
            font-family: 'Courier New', 'Fira Code', monospace;
            font-size: 0.9rem;
            line-height: 1.4;
        }

        code {
            background: #1e1e2e;
            padding: 2px 6px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            color: #fbbf24;
        }

        pre code {
            background: none;
            padding: 0;
            color: #e2e8f0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(42, 42, 62, 0.4);
            border-radius: 12px;
            overflow: hidden;
        }

        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #383850;
        }

        th {
            background: #2a2a3e;
            color: #4ade80;
            font-weight: 600;
        }

        tr:hover {
            background: rgba(74, 222, 128, 0.05);
        }

        .tech-stack {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 20px 0;
        }

        .tech-tag {
            background: linear-gradient(135deg, #60a5fa, #4ade80);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            color: #1e1e2e;
        }

        .note {
            background: rgba(79, 70, 229, 0.2);
            border-left: 4px solid #818cf8;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
        }

        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #4ade80, #60a5fa, transparent);
            margin: 40px 0;
        }

        @media (max-width: 768px) {
            .header {
                padding: 30px 20px;
            }
            .content {
                padding: 30px 20px;
            }
            h2 {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌳 B+ Tree Visualizer</h1>
            <p><strong>A high-performance B+ Tree implementation with an interactive PyQt6 visualization tool</strong></p>
            <div class="badges">
                <span class="badge">🐍 Python 3.10+</span>
                <span class="badge">🎨 PyQt6</span>
                <span class="badge">🌲 B+ Tree Algorithm</span>
                <span class="badge">📊 Data Structures</span>
                <span class="badge">💡 Educational</span>
            </div>
        </div>

        <div class="content">
            <h2>📌 Overview</h2>
            <p>This project implements a <strong>B+ Tree</strong> data structure with full insert, delete, and search operations, paired with a modern <strong>PyQt6-based graphical user interface</strong>. The B+ Tree is widely used in database indexing and file systems due to its balanced nature and efficient range queries. The visualizer allows users to see how keys propagate through internal nodes, how leaf nodes are linked for sequential access, and how the tree rebalances itself after splits and merges.</p>

            <hr>

            <h2>✨ Key Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🔧 Complete B+ Tree Operations</h4>
                    <p>Insert, delete, and search with automatic rebalancing (splits, merges, and borrowing).</p>
                </div>
                <div class="feature-card">
                    <h4>🎨 Interactive Visualization</h4>
                    <p>Real‑time rendering with distinct styling for leaf and internal nodes.</p>
                </div>
                <div class="feature-card">
                    <h4>🔗 Leaf‑Level Linked List</h4>
                    <p>Dashed arrows show ordered leaf sequence for efficient range scanning.</p>
                </div>
                <div class="feature-card">
                    <h4>🔍 Search Highlighting</h4>
                    <p>Found keys are highlighted in yellow for instant visual feedback.</p>
                </div>
                <div class="feature-card">
                    <h4>⚙️ Configurable Max Degree</h4>
                    <p>Adjust the tree’s order (3–20) dynamically.</p>
                </div>
                <div class="feature-card">
                    <h4>📦 Batch Insert</h4>
                    <p>Insert multiple space‑separated keys at once (e.g., <code>10 - 20 - 5 - 30</code>).</p>
                </div>
                <div class="feature-card">
                    <h4>📋 Leaf Sequence Display</h4>
                    <p>Side panel shows all keys in sorted order as they appear in the leaf linked list.</p>
                </div>
                <div class="feature-card">
                    <h4>💎 Professional UI</h4>
                    <p>Dark‑themed, responsive interface with hover effects and scrollable canvas.</p>
                </div>
            </div>

            <hr>

            <h2>🛠 Technical Implementation</h2>

            <h3>1️⃣ B+ Tree Node Design</h3>
            <p>Each node (internal or leaf) stores a sorted list of keys and maintains parent pointers to simplify splits and merges. Leaf nodes additionally hold a <code>next</code> pointer to form a singly linked list.</p>
            <pre><code>class BPlusNode:
    def __init__(self, is_leaf=False):
        self.keys = []          # sorted keys
        self.children = []      # child pointers (internal nodes only)
        self.is_leaf = is_leaf
        self.next = None        # next leaf node
        self.parent = None      # parent reference</code></pre>

            <h3>2️⃣ Insertion & Split Logic</h3>
            <p>When a leaf exceeds <code>max_keys</code>, it splits into two leaves. The <em>first key</em> of the new right leaf is promoted up to the parent. For internal nodes, the <em>middle key</em> is pushed up (not copied), and the node is split into two. The propagation continues recursively up the tree.</p>
            <pre><code>def _split_leaf(self, leaf):
    mid = len(leaf.keys) // 2
    new_leaf = BPlusNode(is_leaf=True)
    new_leaf.keys = leaf.keys[mid:]   # right half
    leaf.keys = leaf.keys[:mid]       # left half
    # update linked list
    new_leaf.next = leaf.next
    leaf.next = new_leaf
    # promote first key of new leaf
    self._insert_into_parent(leaf, new_leaf.keys[0], new_leaf)</code></pre>

            <h3>3️⃣ Deletion & Underflow Handling</h3>
            <p>After deleting a key from a leaf, the tree checks if the leaf falls below the minimum occupancy. It first tries to <strong>borrow</strong> a key from a sibling; if that fails, it <strong>merges</strong> with a sibling. The same process is applied recursively to internal nodes.</p>
            <pre><code>def _fix_leaf_underflow(self, leaf):
    # try borrowing from right sibling, then left sibling
    # if not possible, merge with right or left sibling
    # after merge, check parent underflow</code></pre>

            <h3>4️⃣ Tree Layout & Drawing (PyQt6)</h3>
            <p>The <code>get_tree_layout()</code> method performs a BFS traversal and returns a level‑by‑level list of nodes. The GUI canvas computes positions, draws edges, leaf links, and highlights searched keys.</p>
            <pre><code>def _compute_positions(self):
    # bottom‑up: position leaves, then parent centers
    for leaf in leaf_level:
        x += node_width + LEAF_GAP
    for internal in reverse_internal_levels:
        cx = (min(child_xs) + max(child_xs)) / 2</code></pre>

            <h3>5️⃣ Leaf Sequence Display</h3>
            <p>The side panel displays all keys in sorted order by traversing the leaf linked list – a unique advantage of B+ Trees for range queries.</p>
            <pre><code>def get_all_leaves(self):
    node = self.root
    while not node.is_leaf:
        node = node.children[0]
    while node:
        result.extend(node.keys)
        node = node.next</code></pre>

            <hr>

            <h2>📁 Project Structure</h2>
            <pre><code>bplus-tree-visualizer/
├── bplustree.py          # Core B+ Tree implementation (node & tree classes)
├── gui_pyqt6.py          # PyQt6 GUI: canvas drawing, controls, event handlers
├── main.py               # Entry point (checks PyQt6, launches app)
└── README.md             # This documentation</code></pre>

            <hr>

            <h2>⚡ Performance & Complexity</h2>
            <table>
                <thead>
                    <tr><th>Operation</th><th>Average Case</th><th>Worst Case</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>Search</strong></td><td>O(logₓ N)</td><td>O(logₓ N)</td></tr>
                    <tr><td><strong>Insert</strong></td><td>O(logₓ N)</td><td>O(logₓ N)</td></tr>
                    <tr><td><strong>Delete</strong></td><td>O(logₓ N)</td><td>O(logₓ N)</td></tr>
                    <tr><td><strong>Range scan (k keys)</strong></td><td>O(logₓ N + k)</td><td>O(logₓ N + k)</td></tr>
                </tbody>
            </table>
            <div class="note">
                <strong>📌 Note:</strong> N = number of keys, x = max_degree (order). The height of the tree is kept low (typically 3–4 for millions of keys).
            </div>

            <hr>

            <h2>🎯 Use Cases</h2>
            <div class="feature-grid">
                <div class="feature-card"><h4>🎓 Educational</h4><p>Understand B+ Tree internals (splits, merges, borrowing, pointer updates).</p></div>
                <div class="feature-card"><h4>🗄️ Database Indexing</h4><p>Prototype index behaviour for DBMS courses.</p></div>
                <div class="feature-card"><h4>💾 File System Simulation</h4><p>Model how directory structures organise metadata.</p></div>
                <div class="feature-card"><h4>📊 Algorithm Visualization</h4><p>Show how balanced trees remain balanced after many modifications.</p></div>
            </div>

            <hr>

            <h2>🚀 Future Improvements</h2>
            <ul style="margin-left: 30px; margin-top: 10px;">
                <li><strong>Node collapsing</strong> – Display very large trees by summarising subtrees.</li>
                <li><strong>Step‑by‑step animation</strong> – Allow users to see each insertion/deletion step.</li>
                <li><strong>Disk‑aware simulation</strong> – Simulate block reads/writes and page caching.</li>
                <li><strong>Export image</strong> – Save the current tree layout as PNG/SVG.</li>
                <li><strong>Custom key types</strong> – Support strings or other comparable types.</li>
            </ul>

            <hr>

            <h2>📦 Installation & Requirements</h2>
            <h3>Prerequisites</h3>
            <ul style="margin-left: 30px;">
                <li>Python 3.10 or higher</li>
                <li>PyQt6</li>
                <li>No other external dependencies (only Python standard library plus PyQt6)</li>
            </ul>

            <h3>Install from source</h3>
            <pre><code>git clone https://github.com/yourusername/bplus-tree-visualizer.git
cd bplus-tree-visualizer
pip install PyQt6
python main.py</code></pre>

            <p>The <code>main.py</code> script automatically checks for PyQt6 and prompts you to install it if missing.</p>

            <hr>

            <h2>🖥️ How to Use</h2>
            <ol style="margin-left: 30px; margin-bottom: 20px;">
                <li><strong>Set Max Degree</strong> – Use the spin box (3–20) and click <strong>Apply</strong> (clears the tree).</li>
                <li><strong>Insert Keys</strong> – Enter one or more integers separated by hyphens, e.g., <code>15 - 8 - 42 - 23</code>, then click <strong>Insert</strong>.</li>
                <li><strong>Search</strong> – Enter a single key and click <strong>Search</strong> – the node slot turns yellow if found.</li>
                <li><strong>Delete</strong> – Enter a key and click <strong>Delete</strong> – the tree rebalances automatically.</li>
                <li><strong>Clear Tree</strong> – Removes all keys (keeps current max degree).</li>
                <li><strong>Leaf Sequence</strong> – The bottom panel shows all keys in sorted order (via the leaf linked list).</li>
            </ol>
            <div class="note">
                <strong>💡 Tip:</strong> The tree automatically expands in height when the root splits, and shrinks when the root becomes empty.
            </div>

            <hr>

            <h2>🧪 Example Walkthrough</h2>
            <p><strong>Initial tree (empty)</strong> → Insert <code>10</code> → Insert <code>20</code> → Insert <code>5</code> → Insert <code>15</code> (root split) → Delete <code>10</code> (borrow from sibling) → Delete <code>5</code> (merge leaves). The GUI updates after every operation.</p>

            <hr>

            <h2>🤝 Contributing</h2>
            <p>Contributions are welcome! Areas you can help:</p>
            <ul style="margin-left: 30px;">
                <li><strong>Bug reports</strong> – Open an issue with a clear description and screenshots.</li>
                <li><strong>Features</strong> – Propose new features (e.g., animation, file I/O, key ranges).</li>
                <li><strong>Code</strong> – Submit pull requests for bug fixes or enhancements.</li>
                <li><strong>Documentation</strong> – Improve this README or add tutorials.</li>
            </ul>

            <hr>

            <h2>📄 License</h2>
            <p><strong>MIT License</strong> – free for personal and commercial use.</p>

            <hr>

            <div style="text-align: center; margin-top: 40px; padding: 20px; color: #64748b;">
                Built with ❤️ using Python, PyQt6, and a passion for data structures.
            </div>
        </div>
    </div>
</body>
</html>
