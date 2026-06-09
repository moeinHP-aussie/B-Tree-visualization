"""
gui.py
------
Graphical User Interface for the B+ Tree application.
Built with PyQt6 for a modern, polished look.
Handles all drawing, input, and user interaction.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QScrollArea,
    QMessageBox, QSizePolicy, QSpinBox
)
from PyQt6.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont, QPainterPath,
    QLinearGradient, QPolygonF
)
from PyQt6.QtCore import Qt, QRectF, QPointF, QSizeF

from bplustree import BPlusTree


# ─────────────────────────────────────────────────────────────
# Color Palette
# ─────────────────────────────────────────────────────────────
C_BG          = QColor("#1e1e2e")   # Main background
C_PANEL       = QColor("#2a2a3e")   # Left panel background
C_PANEL_BORDER= QColor("#383850")   # Panel border
C_CANVAS_BG   = QColor("#181825")   # Canvas background

C_NODE_LEAF   = QColor("#4ade80")   # Leaf node fill
C_NODE_INT    = QColor("#60a5fa")   # Internal node fill
C_NODE_HIT    = QColor("#fbbf24")   # Search-hit highlight
C_NODE_SHADOW = QColor(0, 0, 0, 60) # Drop shadow

C_EDGE        = QColor("#64748b")   # Tree edges
C_LEAF_LINK   = QColor("#f472b6")   # Linked-list arrows (pink)

C_TEXT_NODE   = QColor("#1e1e2e")   # Text inside nodes
C_TEXT_LIGHT  = QColor("#e2e8f0")   # Text on dark bg
C_TEXT_DIM    = QColor("#64748b")   # Dimmed text

C_ACCENT      = QColor("#818cf8")   # Accent / highlight

C_BTN_INS     = QColor("#22c55e")
C_BTN_INS_H   = QColor("#16a34a")
C_BTN_DEL     = QColor("#ef4444")
C_BTN_DEL_H   = QColor("#dc2626")
C_BTN_SRC     = QColor("#3b82f6")
C_BTN_SRC_H   = QColor("#2563eb")
C_BTN_CLR     = QColor("#8b5cf6")
C_BTN_CLR_H   = QColor("#7c3aed")
C_BTN_APL     = QColor("#818cf8")
C_BTN_APL_H   = QColor("#6366f1")

# ─────────────────────────────────────────────────────────────
# Drawing constants
# ─────────────────────────────────────────────────────────────
NODE_H        = 38      # Node rectangle height (px)
KEY_W         = 38      # Width per key slot inside a node
NODE_PAD      = 10      # Horizontal padding inside node
NODE_RADIUS   = 6       # Corner radius of node rect
LEVEL_GAP     = 90      # Vertical gap between levels
LEAF_GAP      = 24      # Horizontal gap between sibling leaves
CANVAS_PAD_X  = 60
CANVAS_PAD_Y  = 50
LINK_OFFSET   = 22      # Vertical offset for leaf linked-list arrows


# ═════════════════════════════════════════════════════════════
# Styled Button
# ═════════════════════════════════════════════════════════════
class StyledButton(QPushButton):
    """
    A flat, rounded push-button with hover color support.
    """

    def __init__(self, text, normal_color: QColor, hover_color: QColor, parent=None):
        super().__init__(text, parent)
        self._normal = normal_color.name()
        self._hover  = hover_color.name()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.setFixedHeight(36)
        self._apply_style(self._normal)

    def _apply_style(self, bg):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: #1e1e2e;
                border: none;
                border-radius: 7px;
                padding: 0 14px;
                font-weight: bold;
            }}
        """)

    def enterEvent(self, event):
        self._apply_style(self._hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style(self._normal)
        super().leaveEvent(event)


# ═════════════════════════════════════════════════════════════
# Tree Canvas
# ═════════════════════════════════════════════════════════════
class TreeCanvas(QWidget):
    """
    Custom widget that draws the B+ Tree using QPainter.
    Placed inside a QScrollArea to support large trees.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_data   = []    # Tree level layout from BPlusTree.get_tree_layout()
        self.highlighted   = None  # Key to highlight (after search)
        self._positions    = {}    # node -> (cx, cy)
        self.setMinimumSize(800, 400)

    def update_tree(self, layout_data, highlighted_key=None):
        """Receive new layout data and trigger a repaint."""
        self.layout_data = layout_data
        self.highlighted = highlighted_key
        self._positions  = {}
        self._compute_positions()
        # Resize widget to fit content
        if self._positions:
            max_x = max(x for x, y in self._positions.values()) + 100
            max_y = max(y for x, y in self._positions.values()) + 80
            self.setMinimumSize(int(max_x), int(max_y))
        else:
            self.setMinimumSize(800, 400)
        self.update()

    # ------------------------------------------------------------------
    # Position calculation
    # ------------------------------------------------------------------

    def _node_width(self, node_info):
        """Return the pixel width of a node based on its key count."""
        return max(len(node_info['keys']), 1) * KEY_W + NODE_PAD * 2

    def _compute_positions(self):
        """BFS bottom-up: assign (cx, cy) to every node."""
        if not self.layout_data:
            return

        num_levels = len(self.layout_data)
        leaf_level = self.layout_data[-1]

        # ── Assign leaf x positions ──────────────────────────────
        x = float(CANVAS_PAD_X)
        for node_info in leaf_level:
            nw = self._node_width(node_info)
            cy = CANVAS_PAD_Y + (num_levels - 1) * LEVEL_GAP
            self._positions[id(node_info['node'])] = (x + nw / 2, cy)
            x += nw + LEAF_GAP

        # ── Center internal nodes over their children ─────────────
        for level_idx in range(num_levels - 2, -1, -1):
            for node_info in self.layout_data[level_idx]:
                node = node_info['node']
                if node.is_leaf:
                    continue
                child_xs = [
                    self._positions[id(c)][0]
                    for c in node.children
                    if id(c) in self._positions
                ]
                if child_xs:
                    cx = (min(child_xs) + max(child_xs)) / 2
                    cy = CANVAS_PAD_Y + level_idx * LEVEL_GAP
                    self._positions[id(node)] = (cx, cy)

    # ------------------------------------------------------------------
    # paintEvent — called by Qt whenever the widget needs to be drawn
    # ------------------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.fillRect(self.rect(), C_CANVAS_BG)

        if not self.layout_data:
            self._draw_empty(painter)
            return

        # Check if tree is truly empty (single leaf with no keys)
        if (len(self.layout_data) == 1 and
                self.layout_data[0] and
                not self.layout_data[0][0]['keys']):
            self._draw_empty(painter)
            return

        self._draw_edges(painter)
        self._draw_leaf_links(painter)
        self._draw_nodes(painter)

        painter.end()

    def _draw_empty(self, painter):
        """Show a placeholder message when the tree is empty."""
        painter.setPen(QPen(C_TEXT_DIM))
        painter.setFont(QFont("Segoe UI", 16))
        painter.drawText(
            self.rect(), Qt.AlignmentFlag.AlignCenter,
            "Tree is empty.\nInsert some keys to get started!"
        )

    def _draw_edges(self, painter):
        """Draw straight lines from each internal node to its children."""
        pen = QPen(C_EDGE, 1.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        for level in self.layout_data:
            for node_info in level:
                node = node_info['node']
                if node.is_leaf or id(node) not in self._positions:
                    continue
                px, py = self._positions[id(node)]
                for child in node.children:
                    if id(child) not in self._positions:
                        continue
                    cx, cy = self._positions[id(child)]
                    painter.drawLine(
                        QPointF(px, py + NODE_H / 2),
                        QPointF(cx, cy - NODE_H / 2)
                    )

    def _draw_leaf_links(self, painter):
        """Draw dashed arrows connecting consecutive leaf nodes (linked list)."""
        if not self.layout_data:
            return
        leaf_level = self.layout_data[-1]

        pen = QPen(C_LEAF_LINK, 1.6, Qt.PenStyle.DashLine)
        pen.setDashPattern([5, 3])
        painter.setPen(pen)

        for i in range(len(leaf_level) - 1):
            n1 = leaf_level[i]['node']
            n2 = leaf_level[i + 1]['node']
            if id(n1) not in self._positions or id(n2) not in self._positions:
                continue

            x1, y1 = self._positions[id(n1)]
            x2, y2 = self._positions[id(n2)]
            nw1 = self._node_width(leaf_level[i])
            nw2 = self._node_width(leaf_level[i + 1])

            start = QPointF(x1 + nw1 / 2, y1 + LINK_OFFSET)
            end   = QPointF(x2 - nw2 / 2, y2 + LINK_OFFSET)

            painter.drawLine(start, end)

            # Draw arrowhead
            painter.setPen(QPen(C_LEAF_LINK, 1.6))
            painter.setBrush(QBrush(C_LEAF_LINK))
            self._draw_arrowhead(painter, start, end, size=7)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            pen2 = QPen(C_LEAF_LINK, 1.6, Qt.PenStyle.DashLine)
            pen2.setDashPattern([5, 3])
            painter.setPen(pen2)

    def _draw_arrowhead(self, painter, p1: QPointF, p2: QPointF, size=8):
        """Draw a filled triangle arrowhead at the end (p2) of a line."""
        import math
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        angle = math.atan2(dy, dx)

        tip = p2
        left = QPointF(
            tip.x() - size * math.cos(angle - math.pi / 7),
            tip.y() - size * math.sin(angle - math.pi / 7)
        )
        right = QPointF(
            tip.x() - size * math.cos(angle + math.pi / 7),
            tip.y() - size * math.sin(angle + math.pi / 7)
        )
        poly = QPolygonF([tip, left, right])
        painter.drawPolygon(poly)

    def _draw_nodes(self, painter):
        """Draw all nodes in the tree layout."""
        for level in self.layout_data:
            for node_info in level:
                node = node_info['node']
                if id(node) not in self._positions:
                    continue
                cx, cy = self._positions[id(node)]
                self._draw_single_node(painter, node_info, cx, cy)

    def _draw_single_node(self, painter, node_info, cx, cy):
        """
        Draw one node: a rounded rectangle divided into key slots.
        Highlighted key slot gets a yellow background.
        """
        keys   = node_info['keys']
        is_leaf= node_info['is_leaf']
        num_k  = max(len(keys), 1)
        nw     = num_k * KEY_W + NODE_PAD * 2
        nh     = NODE_H

        x0 = cx - nw / 2
        y0 = cy - nh / 2

        base_color = C_NODE_LEAF if is_leaf else C_NODE_INT

        # ── Drop shadow ────────────────────────────────────────
        shadow_rect = QRectF(x0 + 3, y0 + 3, nw, nh)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(C_NODE_SHADOW))
        painter.drawRoundedRect(shadow_rect, NODE_RADIUS, NODE_RADIUS)

        # ── Node body ──────────────────────────────────────────
        node_rect = QRectF(x0, y0, nw, nh)
        painter.setBrush(QBrush(base_color))
        painter.setPen(QPen(QColor("#1e1e2e"), 1.2))
        painter.drawRoundedRect(node_rect, NODE_RADIUS, NODE_RADIUS)

        # ── Key slots ──────────────────────────────────────────
        for i, key in enumerate(keys):
            kx0 = x0 + NODE_PAD + i * KEY_W
            kx1 = kx0 + KEY_W
            slot_rect = QRectF(kx0, y0, KEY_W, nh)

            # Highlight slot if key matches search result
            if self.highlighted is not None and key == self.highlighted:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(C_NODE_HIT))
                # Clip to node corners on first/last slot
                painter.drawRect(slot_rect)

            # Vertical divider between keys
            if i > 0:
                painter.setPen(QPen(C_TEXT_NODE, 0.8))
                painter.drawLine(
                    QPointF(kx0, y0 + 5),
                    QPointF(kx0, y0 + nh - 5)
                )

            # Key text
            painter.setPen(QPen(C_TEXT_NODE))
            painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            painter.drawText(slot_rect, Qt.AlignmentFlag.AlignCenter, str(key))


# ═════════════════════════════════════════════════════════════
# Main Application Window
# ═════════════════════════════════════════════════════════════
class BPlusTreeApp(QMainWindow):
    """
    Main window of the B+ Tree Visualizer.
    Left panel: controls. Right area: scrollable tree canvas.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("B+ Tree Visualizer")
        self.resize(1280, 740)
        self.setMinimumSize(900, 580)

        self.tree = None
        self.highlighted_key = None

        self._build_ui()
        self._init_tree(4)   # Default max degree = 4

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        """Set up the two-column layout: control panel + canvas."""

        # Root central widget
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Left Panel ────────────────────────────────────────────
        panel = QFrame()
        panel.setFixedWidth(270)
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {C_PANEL.name()};
                border-right: 1px solid {C_PANEL_BORDER.name()};
            }}
        """)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(18, 24, 18, 18)
        panel_layout.setSpacing(0)

        # Title
        title = QLabel("B+ Tree")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C_ACCENT.name()}; background: transparent; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(title)

        sub = QLabel("Visualizer")
        sub.setFont(QFont("Segoe UI", 11))
        sub.setStyleSheet("color: #94a3b8; background: transparent; border: none;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(sub)
        panel_layout.addSpacing(16)

        panel_layout.addWidget(self._separator())
        panel_layout.addSpacing(14)

        # ── Degree control ─────────────────────────────────────
        deg_label = QLabel("Max Degree (order):")
        deg_label.setFont(QFont("Segoe UI", 10))
        deg_label.setStyleSheet("color: #cbd5e1; background: transparent; border: none;")
        panel_layout.addWidget(deg_label)
        panel_layout.addSpacing(4)

        deg_row = QHBoxLayout()
        deg_row.setSpacing(8)

        self.degree_spin = QSpinBox()
        self.degree_spin.setRange(3, 20)
        self.degree_spin.setValue(4)
        self.degree_spin.setFixedHeight(34)
        self.degree_spin.setFont(QFont("Segoe UI", 11))
        self.degree_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3b3b52;
                color: #e2e8f0;
                border: none;
                border-radius: 6px;
                padding: 2px 6px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: #4a4a65;
                border-radius: 3px;
                width: 18px;
            }
        """)
        deg_row.addWidget(self.degree_spin)

        apply_btn = StyledButton("Apply", C_BTN_APL, C_BTN_APL_H)
        apply_btn.clicked.connect(self._apply_degree)
        deg_row.addWidget(apply_btn)
        panel_layout.addLayout(deg_row)

        panel_layout.addSpacing(14)
        panel_layout.addWidget(self._separator())
        panel_layout.addSpacing(14)

        # ── Key Input ──────────────────────────────────────────
        key_label = QLabel('Key(s) — separate with  " - " :')
        key_label.setFont(QFont("Segoe UI", 10))
        key_label.setStyleSheet("color: #cbd5e1; background: transparent; border: none;")
        panel_layout.addWidget(key_label)
        panel_layout.addSpacing(4)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("e.g.  10 - 20 - 5 - 30")
        self.key_input.setFont(QFont("Segoe UI", 12))
        self.key_input.setFixedHeight(38)
        self.key_input.setStyleSheet("""
            QLineEdit {
                background-color: #3b3b52;
                color: #e2e8f0;
                border: none;
                border-radius: 7px;
                padding: 0 10px;
            }
            QLineEdit:focus {
                border: 1.5px solid #818cf8;
            }
        """)
        self.key_input.returnPressed.connect(self._insert)
        panel_layout.addWidget(self.key_input)
        panel_layout.addSpacing(10)

        # ── Operation buttons ──────────────────────────────────
        ins_btn = StyledButton("⬆   Insert",  C_BTN_INS, C_BTN_INS_H)
        src_btn = StyledButton("🔍   Search",  C_BTN_SRC, C_BTN_SRC_H)
        del_btn = StyledButton("✕   Delete",  C_BTN_DEL, C_BTN_DEL_H)

        ins_btn.clicked.connect(self._insert)
        src_btn.clicked.connect(self._search)
        del_btn.clicked.connect(self._delete)

        for btn in (ins_btn, src_btn, del_btn):
            panel_layout.addWidget(btn)
            panel_layout.addSpacing(4)

        panel_layout.addSpacing(4)
        panel_layout.addWidget(self._separator())
        panel_layout.addSpacing(8)

        clr_btn = StyledButton("🗑   Clear Tree", C_BTN_CLR, C_BTN_CLR_H)
        clr_btn.clicked.connect(self._clear_tree)
        panel_layout.addWidget(clr_btn)

        panel_layout.addSpacing(14)
        panel_layout.addWidget(self._separator())
        panel_layout.addSpacing(10)

        # ── Status label ───────────────────────────────────────
        self.status_label = QLabel("Ready.")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #64748b; background: transparent; border: none;")
        self.status_label.setWordWrap(True)
        panel_layout.addWidget(self.status_label)

        panel_layout.addSpacing(10)
        panel_layout.addWidget(self._separator())
        panel_layout.addSpacing(10)

        # ── Leaf sequence display ──────────────────────────────
        leaf_title = QLabel("Leaf sequence (sorted):")
        leaf_title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        leaf_title.setStyleSheet(f"color: {C_ACCENT.name()}; background: transparent; border: none;")
        panel_layout.addWidget(leaf_title)

        self.leaf_seq_label = QLabel("—")
        self.leaf_seq_label.setFont(QFont("Courier New", 9))
        self.leaf_seq_label.setStyleSheet("color: #e2e8f0; background: transparent; border: none;")
        self.leaf_seq_label.setWordWrap(True)
        panel_layout.addWidget(self.leaf_seq_label)

        panel_layout.addStretch()

        # ── Legend ────────────────────────────────────────────
        panel_layout.addWidget(self._separator())
        panel_layout.addSpacing(8)
        panel_layout.addWidget(self._legend())

        root_layout.addWidget(panel)

        # ── Right: scrollable canvas area ─────────────────────
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {C_CANVAS_BG.name()};
            }}
            QScrollBar:horizontal, QScrollBar:vertical {{
                background: #2a2a3e;
                width: 10px; height: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal, QScrollBar::handle:vertical {{
                background: #4a4a65;
                border-radius: 5px;
            }}
        """)

        self.canvas = TreeCanvas()
        self.scroll_area.setWidget(self.canvas)
        root_layout.addWidget(self.scroll_area)

        # Window background
        self.setStyleSheet(f"QMainWindow {{ background-color: {C_BG.name()}; }}")

    def _separator(self):
        """Create a horizontal separator line."""
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #383850; border: none; max-height: 1px;")
        return sep

    def _legend(self):
        """Small color legend at the bottom of the panel."""
        frame = QFrame()
        frame.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        def legend_row(color: QColor, text: str):
            row = QWidget()
            row.setStyleSheet("background: transparent;")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(8)
            swatch = QLabel()
            swatch.setFixedSize(14, 14)
            swatch.setStyleSheet(f"background-color: {color.name()}; border-radius: 3px;")
            lbl = QLabel(text)
            lbl.setFont(QFont("Segoe UI", 8))
            lbl.setStyleSheet("color: #94a3b8;")
            rl.addWidget(swatch)
            rl.addWidget(lbl)
            rl.addStretch()
            return row

        layout.addWidget(legend_row(C_NODE_LEAF, "Leaf node"))
        layout.addWidget(legend_row(C_NODE_INT,  "Internal node"))
        layout.addWidget(legend_row(C_NODE_HIT,  "Search result"))
        layout.addWidget(legend_row(C_LEAF_LINK, "Leaf linked list"))
        return frame

    # ------------------------------------------------------------------
    # Tree Initialization
    # ------------------------------------------------------------------

    def _init_tree(self, degree: int):
        """Create a fresh B+ Tree with the given max degree."""
        self.tree = BPlusTree(max_degree=degree)
        self.highlighted_key = None
        self._redraw()
        self._set_status(f"New B+ Tree created  •  Max degree: {degree}")

    def _apply_degree(self):
        """Apply the chosen degree, after confirming tree reset."""
        d = self.degree_spin.value()
        reply = QMessageBox.question(
            self, "Confirm Reset",
            f"Changing the degree will clear the current tree.\n\nProceed with max degree {d}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._init_tree(d)

    # ------------------------------------------------------------------
    # Key Parsing
    # ------------------------------------------------------------------

    def _parse_keys(self):
        """
        Read and parse key(s) from the input field.
        Keys are separated by '-'.
        Returns a list of ints, or None on error.
        """
        raw = self.key_input.text().strip()
        if not raw:
            self._set_status("⚠  Please enter a key.")
            return None

        parts = [p.strip() for p in raw.split("-") if p.strip()]
        keys = []
        for p in parts:
            try:
                keys.append(int(p))
            except ValueError:
                QMessageBox.critical(self, "Invalid Input", f"'{p}' is not a valid integer.")
                return None

        if not keys:
            self._set_status("⚠  No valid key entered.")
            return None
        return keys

    # ------------------------------------------------------------------
    # Operations
    # ------------------------------------------------------------------

    def _insert(self):
        """Insert one or more keys into the tree."""
        keys = self._parse_keys()
        if keys is None:
            return

        inserted, skipped = [], []
        for k in keys:
            (inserted if self.tree.insert(k) else skipped).append(k)

        self.highlighted_key = None
        self._redraw()
        self.key_input.clear()

        msg = ""
        if inserted:
            msg += f"✓  Inserted: {inserted}.  "
        if skipped:
            msg += f"⚠  Already existed (skipped): {skipped}."
        self._set_status(msg)

    def _search(self):
        """Search for the first key and highlight it if found."""
        keys = self._parse_keys()
        if keys is None:
            return

        key = keys[0]
        found = self.tree.search(key)
        self.highlighted_key = key if found else None
        self._redraw()

        if found:
            self._set_status(f"🔍  Key {key} FOUND  (highlighted in yellow).")
        else:
            self._set_status(f"🔍  Key {key} NOT found in the tree.")

    def _delete(self):
        """Delete the first key from the tree."""
        keys = self._parse_keys()
        if keys is None:
            return

        key = keys[0]
        deleted = self.tree.delete(key)
        self.highlighted_key = None
        self._redraw()
        self.key_input.clear()

        if deleted:
            self._set_status(f"✓  Key {key} deleted successfully.")
        else:
            self._set_status(f"⚠  Key {key} was NOT found — nothing deleted.")

    def _clear_tree(self):
        """Reset the tree, keeping the current max degree."""
        degree = self.tree.max_degree
        self._init_tree(degree)
        self.key_input.clear()

    def _set_status(self, msg: str):
        self.status_label.setText(msg)

    # ------------------------------------------------------------------
    # Redraw
    # ------------------------------------------------------------------

    def _redraw(self):
        """Push updated layout to the canvas widget."""
        layout = self.tree.get_tree_layout()
        self.canvas.update_tree(layout, self.highlighted_key)

        leaves = self.tree.get_all_leaves()
        self.leaf_seq_label.setText(
            " → ".join(str(k) for k in leaves) if leaves else "—"
        )


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────
def run():
    """Launch the B+ Tree PyQt6 application."""
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle("Fusion")   # Consistent cross-platform look
    window = BPlusTreeApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()