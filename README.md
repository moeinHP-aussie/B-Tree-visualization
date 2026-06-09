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

## 🖼 Screenshots

### Main Window

```text
Add your screenshots here
```

```markdown
![Main Window](screenshots/main_window.png)
```

### Example Tree

```markdown
![Tree Example](screenshots/tree_example.png)
```

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
- Introduction to Algorithms (CLRS)
- Database Management Systems — Raghu Ramakrishnan

---

## 📄 License

This project is intended for educational and academic use.

---

## 👨‍💻 Author

Developed as a visualization and learning tool for understanding B+ Tree data structures and database indexing mechanisms.
