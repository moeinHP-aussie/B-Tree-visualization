"""
bplustree.py
------------
 OOP design.
"""


class BPlusNode:
    """
    Represents a single node in the B+ Tree.
    Can be either a leaf node or an internal node.
    """

    def __init__(self, is_leaf=False):
        self.keys = []          # List of keys stored in this node
        self.children = []      # Child pointers (only used in internal nodes)
        self.is_leaf = is_leaf  # True if this is a leaf node
        self.next = None        # Pointer to the next leaf node (leaf-level linked list)
        self.parent = None      # Pointer to parent node (helps during splits/merges)

    def __repr__(self):
        return f"BPlusNode(keys={self.keys}, is_leaf={self.is_leaf})"


class BPlusTree:
    """
    B+ Tree implementation.
    - All actual data lives in leaf nodes.
    - Internal nodes only store keys as routing guides.
    - Leaf nodes are linked together for easy range traversal.
    """

    def __init__(self, max_degree=4):
        """
        Parameters:
            max_degree (int): Maximum number of children an internal node can have.
                              A node can hold at most (max_degree - 1) keys.
        """
        if max_degree < 3:
            raise ValueError("Max degree must be at least 3.")
        self.max_degree = max_degree
        self.root = BPlusNode(is_leaf=True)  # Start with a single empty leaf node
        self.max_keys = max_degree - 1       # Maximum keys per node

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------

    def search(self, key):
        """
        Search for a key in the B+ Tree.

        Returns:
            True if the key exists, False otherwise.
        """
        leaf = self._find_leaf(key)
        return key in leaf.keys

    def _find_leaf(self, key):
        """
        Traverse from root down to the leaf node where 'key' should reside.
        """
        node = self.root
        while not node.is_leaf:
            # Decide which child to follow
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return node

    # ------------------------------------------------------------------
    # INSERT
    # ------------------------------------------------------------------

    def insert(self, key):
        """
        Insert a key into the B+ Tree.
        If the key already exists, insertion is skipped.
        """
        # Check for duplicate
        if self.search(key):
            return False  # Key already exists

        leaf = self._find_leaf(key)
        self._insert_into_leaf(leaf, key)

        # If leaf overflows, split it
        if len(leaf.keys) > self.max_keys:
            self._split_leaf(leaf)

        return True

    def _insert_into_leaf(self, leaf, key):
        """Insert a key into a leaf node in sorted order."""
        i = 0
        while i < len(leaf.keys) and leaf.keys[i] < key:
            i += 1
        leaf.keys.insert(i, key)

    def _split_leaf(self, leaf):
        """
        Split a leaf node that has overflowed.
        The right half stays in a new node; the middle key is pushed up to the parent.
        """
        mid = len(leaf.keys) // 2

        # Create new right leaf node
        new_leaf = BPlusNode(is_leaf=True)
        new_leaf.keys = leaf.keys[mid:]   # Right half goes to new node
        leaf.keys = leaf.keys[:mid]       # Left half stays in old node

        # Maintain the linked list of leaf nodes
        new_leaf.next = leaf.next
        leaf.next = new_leaf

        # Push the first key of the new leaf up to the parent
        push_up_key = new_leaf.keys[0]
        self._insert_into_parent(leaf, push_up_key, new_leaf)

    def _insert_into_parent(self, left_node, key, right_node):
        """
        After a split, insert the promoted key and new child into the parent node.
        If there is no parent (root was split), create a new root.
        """
        parent = left_node.parent

        if parent is None: # گره مورد نظر ربشه‌ هست
            # The split node was the root — create a brand new root
            new_root = BPlusNode(is_leaf=False)
            new_root.keys = [key]
            new_root.children = [left_node, right_node]
            left_node.parent = new_root
            right_node.parent = new_root
            self.root = new_root
            return

        # Find where to insert the key in the parent
        i = 0
        while i < len(parent.keys) and parent.keys[i] < key:
            i += 1
        parent.keys.insert(i, key)
        parent.children.insert(i + 1, right_node)
        right_node.parent = parent

        # If parent also overflows, split it too
        if len(parent.keys) > self.max_keys:
            self._split_internal(parent)

    def _split_internal(self, node):
        """
        Split an internal node that has overflowed.
        The middle key is pushed up (not copied — unlike leaf split).
        """
        mid = len(node.keys) // 2
        push_up_key = node.keys[mid]

        # Create new right internal node
        new_node = BPlusNode(is_leaf=False)
        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]

        # Update parent references for moved children
        for child in new_node.children:
            child.parent = new_node

        # Trim original node
        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        # Push the middle key up to the parent
        self._insert_into_parent(node, push_up_key, new_node)

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def delete(self, key):
        """
        Delete a key from the B+ Tree.
        Returns True if deleted, False if key was not found.
        After deletion, merges or borrows from siblings to maintain B+ Tree properties.
        """
        leaf = self._find_leaf(key)

        if key not in leaf.keys:
            return False  # Key not found

        leaf.keys.remove(key)

        # Update internal nodes that used this key as a routing key
        self._update_internal_keys(key, leaf)

        # Fix underflow (leaf has too few keys)
        min_keys = (self.max_keys + 1) // 2  # Minimum keys required
        if leaf != self.root and len(leaf.keys) < min_keys:
            self._fix_leaf_underflow(leaf)

        # If root became empty (tree shrinks in height)
        if not self.root.is_leaf and len(self.root.keys) == 0:
            self.root = self.root.children[0]
            self.root.parent = None

        return True

    def _update_internal_keys(self, deleted_key, leaf):
        """
        After deleting a key from a leaf, update any internal node routing keys
        that were using the deleted key.
        """
        node = leaf.parent
        while node is not None:
            if deleted_key in node.keys:
                idx = node.keys.index(deleted_key)
                # Replace with the new first key of the right subtree leaf
                replacement = self._get_leftmost_leaf_key(node.children[idx + 1])
                if replacement is not None:
                    node.keys[idx] = replacement
                else:
                    node.keys.pop(idx)
            node = node.parent

    def _get_leftmost_leaf_key(self, node):
        """Traverse down to find the smallest key in a subtree."""
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0] if node.keys else None

    def _fix_leaf_underflow(self, leaf):
        """
        Handle the case where a leaf node has fewer keys than the minimum.
        Strategy: Try to borrow from a sibling. If not possible, merge.
        """
        parent = leaf.parent
        if parent is None:
            return

        # Find the index of this leaf in the parent's children list
        idx = parent.children.index(leaf)
        min_keys = (self.max_keys + 1) // 2

        # Try borrowing from the right sibling
        if idx + 1 < len(parent.children):
            right_sibling = parent.children[idx + 1]
            if len(right_sibling.keys) > min_keys:
                # Borrow the first key of right sibling
                leaf.keys.append(right_sibling.keys.pop(0))
                parent.keys[idx] = right_sibling.keys[0]
                return

        # Try borrowing from the left sibling
        if idx - 1 >= 0:
            left_sibling = parent.children[idx - 1]
            if len(left_sibling.keys) > min_keys:
                # Borrow the last key of left sibling
                leaf.keys.insert(0, left_sibling.keys.pop())
                parent.keys[idx - 1] = leaf.keys[0]
                return

        # Cannot borrow — must merge
        if idx + 1 < len(parent.children):
            # Merge with right sibling
            right_sibling = parent.children[idx + 1]
            leaf.keys.extend(right_sibling.keys)
            leaf.next = right_sibling.next
            parent.keys.pop(idx)
            parent.children.pop(idx + 1)
        else:
            # Merge with left sibling
            left_sibling = parent.children[idx - 1]
            left_sibling.keys.extend(leaf.keys)
            left_sibling.next = leaf.next
            parent.keys.pop(idx - 1)
            parent.children.pop(idx)

        # Fix underflow in parent if needed
        if parent != self.root and len(parent.keys) < min_keys:
            self._fix_internal_underflow(parent)

    def _fix_internal_underflow(self, node):
        """
        Handle underflow in an internal node after a merge.
        Strategy: Try to borrow from a sibling. If not possible, merge.
        """
        parent = node.parent
        if parent is None:
            return

        idx = parent.children.index(node)
        min_keys = (self.max_keys + 1) // 2

        # Try borrowing from the right sibling
        if idx + 1 < len(parent.children):
            right_sibling = parent.children[idx + 1]
            if len(right_sibling.keys) > min_keys:
                # Pull down parent's separator key, push right sibling's first key up
                node.keys.append(parent.keys[idx])
                parent.keys[idx] = right_sibling.keys.pop(0)
                moved_child = right_sibling.children.pop(0)
                moved_child.parent = node
                node.children.append(moved_child)
                return

        # Try borrowing from the left sibling
        if idx - 1 >= 0:
            left_sibling = parent.children[idx - 1]
            if len(left_sibling.keys) > min_keys:
                node.keys.insert(0, parent.keys[idx - 1])
                parent.keys[idx - 1] = left_sibling.keys.pop()
                moved_child = left_sibling.children.pop()
                moved_child.parent = node
                node.children.insert(0, moved_child)
                return

        # Merge with sibling
        if idx + 1 < len(parent.children):
            right_sibling = parent.children[idx + 1]
            node.keys.append(parent.keys.pop(idx))
            node.keys.extend(right_sibling.keys)
            for child in right_sibling.children:
                child.parent = node
            node.children.extend(right_sibling.children)
            parent.children.pop(idx + 1)
        else:
            left_sibling = parent.children[idx - 1]
            left_sibling.keys.append(parent.keys.pop(idx - 1))
            left_sibling.keys.extend(node.keys)
            for child in node.children:
                child.parent = left_sibling
            left_sibling.children.extend(node.children)
            parent.children.pop(idx)

        # Recurse upward if needed
        if parent != self.root and len(parent.keys) < min_keys:
            self._fix_internal_underflow(parent)

    # ------------------------------------------------------------------
    # UTILITY: Build tree layout for visualization
    # ------------------------------------------------------------------

    def get_tree_layout(self):
        """
        Perform a breadth-first traversal of the tree and return
        a level-by-level list of nodes for drawing purposes.

        Returns:
            A list of levels. Each level is a list of dicts with:
                - 'keys': list of keys in the node
                - 'is_leaf': bool
        """
        if self.root is None:
            return []

        layout = []
        current_level = [self.root]

        while current_level:
            level_data = []
            next_level = []
            for node in current_level:
                level_data.append({
                    'keys': list(node.keys),
                    'is_leaf': node.is_leaf,
                    'node': node   # keep reference for drawing edges
                })
                if not node.is_leaf:
                    next_level.extend(node.children)
            layout.append(level_data)
            current_level = next_level

        return layout

    def get_all_leaves(self):
        """
        Return all keys stored in leaf nodes (in sorted order)
        by following the linked list of leaves.
        """
        result = []
        node = self.root
        # Go to the leftmost leaf
        while not node.is_leaf:
            node = node.children[0]
        # Follow next pointers
        while node is not None:
            result.extend(node.keys)
            node = node.next
        return result
