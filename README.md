# 🌳 B+ Tree Visualizer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Algorithm-B%2B%20Tree-red.svg" alt="Algorithm">
  <img src="https://img.shields.io/badge/Domain-Data%20Structures-cyan.svg" alt="Domain">
  <img src="https://img.shields.io/badge/UI-PyQt6-orange.svg" alt="UI Framework">
  <img src="https://img.shields.io/badge/Feature-Visualization-brightgreen.svg" alt="Visualization">
  <img src="https://img.shields.io/badge/Operation-Rebalancing-yellow.svg" alt="Rebalancing">
  <img src="https://img.shields.io/badge/Linked%20List-Leaf%20Level-pink.svg" alt="Leaf Linked List">
</p>

<p align="center">
  Interactive visualization of the <strong>B+ Tree</strong> data structure with real-time insertion, deletion, searching, node splitting, merging, and leaf-level traversal.
</p>

---

## 📖 Overview

This project provides a complete implementation of a **B+ Tree** along with an interactive graphical visualizer built using **PyQt6**.

The application demonstrates how B+ Trees maintain balance during insertions and deletions while preserving logarithmic search performance. It visually represents internal nodes, leaf nodes, routing keys, parent-child relationships, and the linked list connecting leaf nodes.

This project is suitable for:

- Data Structures courses
- Database Systems courses
- Algorithm visualization
- Academic demonstrations
- Learning balanced search trees

---

## ✨ Features

### Core B+ Tree Operations

- ✅ Search
- ✅ Insert
- ✅ Delete
- ✅ Duplicate prevention
- ✅ Automatic leaf splitting
- ✅ Automatic internal node splitting
- ✅ Borrowing from siblings
- ✅ Node merging
- ✅ Tree height reduction

### Visualization

- 🎨 Modern Dark UI
- 🌳 Dynamic tree rendering
- 🔗 Leaf linked-list visualization
- 🔍 Search result highlighting
- 📊 Sorted leaf traversal display
- ⚙ Adjustable tree degree (order)
- 📜 Scrollable canvas for large trees

---

## 🏗 Architecture

```text
BPlusTreeVisualizer/
│
├── main.py
├── bplustree.py
├── gui_pyqt6.py
└── README.md
```

---

## 📂 File Descriptions

### `main.py`

Application entry point.

Responsibilities:

- Dependency checking
- Automatic PyQt6 installation
- Application startup
- Error handling

---

### `bplustree.py`

Core implementation of the B+ Tree.

Contains:

#### BPlusNode

Represents a single tree node.

Attributes:

- Keys
- Child pointers
- Parent pointer
- Leaf indicator
- Leaf linked-list pointer

#### BPlusTree

Implements:

- Search
- Insert
- Delete
- Split operations
- Merge operations
- Borrowing operations
- Tree traversal
- Visualization support

---

### `gui_pyqt6.py`

Graphical user interface.

Contains:

#### StyledButton

Custom reusable button widget.

#### TreeCanvas

Responsible for:

- Drawing nodes
- Drawing edges
- Drawing leaf links
- Highlighting search results
- Layout calculation

#### BPlusTreeApp

Main application window.

Provides:

- Degree selection
- Key insertion
- Search functionality
- Deletion functionality
- Tree reset
- Status updates
- Leaf sequence display

---

## 🌲 B+ Tree Properties

This implementation follows standard B+ Tree principles:

- All actual data resides in leaf nodes.
- Internal nodes store routing keys only.
- All leaves are located at the same depth.
- Leaf nodes are linked together.
- The tree remains balanced after updates.
- Supports efficient range queries.

---

## 🎯 Visualization Legend

| Color | Meaning |
|---------|---------|
| 🔵 Blue | Internal Node |
| 🟢 Green | Leaf Node |
| 🟡 Yellow | Search Result |
| 🩷 Pink Dashed Arrow | Leaf Linked List |

---

## ⚡ Time Complexity

| Operation | Complexity |
|------------|------------|
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |
| Range Traversal | O(k) |

Where:

- `n` = number of stored keys
- `k` = number of reported keys

---

## 🔄 Supported Rebalancing Operations

### During Insertion

- Leaf Split
- Internal Node Split
- Root Split

### During Deletion

- Borrow from Left Sibling
- Borrow from Right Sibling
- Merge with Left Sibling
- Merge with Right Sibling
- Root Shrinking

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/BPlusTreeVisualizer.git
cd BPlusTreeVisualizer
```

### Install Dependencies

```bash
pip install PyQt6
```

---

## ▶ Running the Application

```bash
python main.py
```

---

## 🧪 Example Inputs

### Insert Multiple Keys

```text
10 - 20 - 5 - 30 - 15
```

### Search

```text
20
```

### Delete

```text
10
```

---

## 🧠 Educational Concepts Demonstrated

This project demonstrates:

- B+ Tree structure
- Database indexing concepts
- Balanced search trees
- Node splitting algorithms
- Node merging algorithms
- Underflow handling
- Overflow handling
- Leaf-level linked lists
- Breadth-first tree traversal

---

## 🔧 Technologies Used

- Python 3
- PyQt6
- Object-Oriented Programming (OOP)

---

## 📚 References

- Database System Concepts — Silberschatz
# 🔬 Implementation Details

This section describes the internal architecture and implementation of the project.

---

## Core Architecture

The application follows a layered architecture:

```text
┌─────────────────────────┐
│       User Actions      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      BPlusTreeApp       │
│   (GUI Controller)      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       BPlusTree         │
│  (Data Structure Layer) │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       BPlusNode         │
│    (Tree Storage)       │
└─────────────────────────┘
```

The GUI layer is completely separated from the data structure implementation, allowing the B+ Tree to be reused independently of the visualization system.

---

# 📦 Module Breakdown

## main.py

Application bootstrapper.

Responsibilities:

- Dependency checking
- Automatic PyQt6 installation
- Startup management
- Error handling

Execution starts from:

```python
main()
```

which eventually launches:

```python
run()
```

from the GUI module.

---

## bplustree.py

Contains the complete implementation of the B+ Tree.

---

### BPlusNode

Represents a single node inside the tree.

#### Attributes

| Attribute | Purpose |
|------------|------------|
| keys | Stores keys contained in the node |
| children | Child references for internal nodes |
| parent | Reference to parent node |
| is_leaf | Indicates leaf/internal node |
| next | Points to next leaf node |

---

### BPlusTree

Represents the entire B+ Tree.

#### Key Design Principles

- Data exists only in leaf nodes.
- Internal nodes contain routing keys.
- All leaves remain at the same depth.
- Leaf nodes form a linked list.
- Tree height remains balanced.

---

# 🔍 Search Algorithm

Search operation begins at the root and follows routing keys until a leaf node is reached.

```text
search(key)
    │
    ▼
_find_leaf(key)
    │
    ▼
Locate Target Leaf
    │
    ▼
Check Leaf Keys
```

### Complexity

```text
O(log n)
```

---

# ➕

# Insertion Algorithm

Insertion follows the standard B+ Tree procedure.

```text
insert(key)
    │
    ▼
_find_leaf()
    │
    ▼
_insert_into_leaf()
    │
    ▼
Overflow?
    │
 ┌──┴───┐
 │ Yes  │
 └──┬───┘
    ▼
_split_leaf()
    │
    ▼
_insert_into_parent()
    │
    ▼
_split_internal()
```

---

## Leaf Split

When a leaf node exceeds its maximum capacity:

1. A new leaf node is created.
2. Keys are divided into two halves.
3. Leaf linked-list pointers are updated.
4. The first key of the new leaf is promoted upward.

---

## Internal Node Split

When an internal node overflows:

1. The middle key is selected.
2. The middle key is promoted.
3. Two internal nodes are produced.
4. Child-parent references are updated.

---

# ➖ Deletion Algorithm

Deletion includes rebalancing operations.

```text
delete(key)
    │
    ▼
Remove Key
    │
    ▼
Underflow?
    │
 ┌──┴───┐
 │ Yes  │
 └──┬───┘
    ▼
Borrow?
    │
 ┌──┴───┐
 │ No   │
 └──┬───┘
    ▼
Merge
```

---

## Underflow Handling

The implementation attempts the following strategies:

### 1. Borrow from Right Sibling

```text
Current Node ← Right Sibling
```

---

### 2. Borrow from Left Sibling

```text
Current Node ← Left Sibling
```

---

### 3. Merge Nodes

If borrowing is impossible:

```text
Node A + Node B
        ↓
Merged Node
```

Parent keys are updated accordingly.

---

# 🌿 Leaf-Level Linked List

One of the most important properties of B+ Trees is that all leaf nodes are linked together.

The implementation maintains this through:

```python
node.next
```

references.

Visualization displays these connections using dashed pink arrows.

```text
[1, 5]
    ↓
[10, 15]
    ↓
[20, 25]
    ↓
[30, 35]
```

This structure enables efficient range queries and sequential traversal.

---

# 🎨 Visualization Engine

The graphical renderer is implemented inside:

```python
TreeCanvas
```

using:

```python
QPainter
```

---

## Rendering Pipeline

```text
Tree Layout
     │
     ▼
Compute Positions
     │
     ▼
Draw Edges
     │
     ▼
Draw Leaf Links
     │
     ▼
Draw Nodes
     │
     ▼
Apply Highlights
```

---

## Layout Strategy

The tree is positioned using a bottom-up approach.

### Step 1

Assign x-coordinates to leaf nodes.

### Step 2

Position internal nodes at the center of their children.

```text
      Parent
        │
   ┌────┴────┐
 Child    Child
```

This guarantees a visually balanced tree.

---

# 🔄 GUI–Tree Interaction Flow

Every user operation follows the same pattern:

```text
User Input
     │
     ▼
GUI Event
     │
     ▼
BPlusTree Operation
     │
     ▼
Generate Layout
     │
     ▼
Canvas Redraw
```

Example:

```text
Insert Button
      │
      ▼
tree.insert(key)
      │
      ▼
get_tree_layout()
      │
      ▼
update_tree()
      │
      ▼
paintEvent()
```

---

# 📊 Complexity Analysis

| Operation | Complexity |
|------------|------------|
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |
| Leaf Traversal | O(k) |
| Tree Rendering | O(n) |

Where:

- `n` = total number of stored keys
- `k` = number of traversed keys

---

# 🎯 Educational Goals

This implementation demonstrates:

- B+ Tree construction
- Balanced search trees
- Database indexing concepts
- Overflow handling
- Underflow handling
- Leaf linked-list organization
- Graphical algorithm visualization
- Object-Oriented Design principles
---

## 📄 License

This project is intended for educational and academic use.

---

## 👨‍💻 Author

Developed as a visualization and learning tool for understanding B+ Tree data structures and database indexing mechanisms.
