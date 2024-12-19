# id1: 322334426
# name1: Inbal Avidov
# username1: inbalavidov
# id2: 212047195
# name2: Inbal Moryles
# username2: inbalmoryles

import math

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        if key is None:
            self.left = None
            self.right = None
            self.parent = None
            self.height = -1
            self.size = 0
        else:
            self.left = AVLNode(None, None)
            self.right = AVLNode(None, None)
            self.parent = None
            self.height = 0
            self.size = 1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        if self.key is None:
            return False
        else:
            return True

    def balance_factor(self):
        return self.left.height - self.right.height

    def update_height(self):
        if self.is_real_node():
            self.height = 1 + max(self.left.height if self.left and self.left.is_real_node() else -1,
                                  self.right.height if self.right and self.right.is_real_node() else -1)
        else:
            self.height = -1

    def update_size(self):
        if self.is_real_node():
            self.size = 1 + self.left.size + self.right.size
        else:
            self.size = 0

    def __repr__(self):
        return "(" + str(self.key) + ":" + str(self.value) + ")"


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        self.root = None

    def set_root(self, node):
        self.root = node

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def search_from_node(self, node, key, e, is_insert):
        prev_node = None
        while node.is_real_node():
            if not is_insert:
                if node.key == key:
                    return node, e + 1
            else:
                prev_node = node
            if node.key < key:
                node = node.right
            else:
                node = node.left
            e += 1

        if is_insert:
            return prev_node, e
        else:
            return None, e

    def search(self, key):
        node = self.root
        x, e = self.search_from_node(node, key, 1, False)
        return x, e

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def finger_search(self, key):
        node = self.max_node()
        e = 1

        while node is not None:
            while node.key > key and node.parent is not None:
                node = node.parent
                e += 1

            node, e = self.search_from_node(node, key, e, False)
            break
        return node, e

    def finger_search_from_insert(self, key, node):
        e = 1

        while node is not None:
            while node.key > key and node.parent is not None:
                node = node.parent
                e += 1

            node, e = self.search_from_node(node, key, e, True)
            break
        return node, e

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    ## fix me

    ###  need to add h and make more readable
    def insert(self, key, val):
        new_node = AVLNode(key, val)
        root = self.get_root()
        if not root:
            self.root = new_node
            return new_node, 0, 0
        else:
            node, e = self.search_from_node(root, key, 0, True)
            if node.key < key:
                node.right = new_node
            else:
                node.left = new_node
            new_node.parent = node
            new_node, e, h = self.balance_after_insert(new_node, node, e, 0)
            return new_node, e, h

    def balance_after_insert(self, new_node, node, e=0, h=0):
        while node:
            prev_node_height = node.height
            node.update_height()
            node.update_size()
            if prev_node_height != node.height: h += 1
            if node.parent is not None:
                bf = node.parent.balance_factor()
            else:
                bf = node.balance_factor()
            if abs(bf) < 2 and prev_node_height == node.height:
                return new_node, e, h
            elif abs(bf) < 2 and prev_node_height != node.height:
                node = node.parent
            else:
                self.balance_tree(node, bf)
                new_node.update_height()
                new_node.update_size()
                self.update_to_root(new_node)
                break
        return new_node, e, h

    def balance_tree(self, node, bf):
        """Rebalance the tree."""
        if bf < -1:  # if first child right child
            if node.balance_factor() > 0:  # if second child is left child
                self.rotate_right(node)
                self.rotate_left(node.parent.parent)
            else:  # if second child is right child
                self.rotate_left(node.parent)
        else:  # if first child left child
            if node.balance_factor() > 0:  # if second child is left child
                self.rotate_right(node.parent)
            else:  # if second child is right child
                self.rotate_left(node)
                self.rotate_right(node.parent.parent)
        node.left.update_height()
        node.left.update_size()
        node.right.update_height()
        node.right.update_size()

    def update_to_root(self, node):
        while node.parent is not None:
            node.update_height()
            node.update_size()
            node = node.parent
        node.update_height()
        node.update_size()
        return None

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left.is_real_node():
            right_child.left.parent = node
        right_child.parent = node.parent
        if not node.parent:
            self.root = right_child
        elif node == node.parent.right:
            node.parent.right = right_child
        else:
            node.parent.left = right_child
        right_child.left = node
        right_child.left.update_height()
        right_child.left.update_size()
        node.parent = right_child
        node.parent.update_height()
        # node.update_size()
        node.parent.update_size()

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right.is_real_node:
            left_child.right.parent = node
        left_child.parent = node.parent

        if not node.parent:
            self.root = left_child
        elif node == node.parent.left:
            node.parent.left = left_child
        else:
            node.parent.right = left_child
        left_child.right = node
        node.parent = left_child

        left_child.right.update_height()
        node.parent.update_height()
        node.parent.update_size()
        left_child.right.update_size()

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    def finger_insert(self, key, val):
        new_node = AVLNode(key, val)
        max_node = self.max_node()
        if not max_node:
            self.root = new_node
            return new_node, 0, 0
        else:
            node, e = self.finger_search_from_insert(key, max_node)
            if node.key < key:
                node.right = new_node
            else:
                node.left = new_node
            new_node.parent = node
            new_node, e, h = self.balance_after_insert(new_node, node, e, 0)
            return new_node, e, h

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    ##need to handle the tree heights
    def delete(self, node):
        # Case 1: Node has no children (leaf)
        if not node.left.is_real_node() and not node.right.is_real_node():
            if not node.parent:  # Node is root
                self.root = AVLNode(None, None)
            elif node == node.parent.left:
                node.parent.left = AVLNode(None, None)
            else:
                node.parent.right = AVLNode(None, None)

        # Case 2: Node has one child
        elif not node.left.is_real_node() or not node.right.is_real_node():
            child = node.left if node.left.is_real_node() else node.right

            if not node.parent:  # Node is root
                self.root = child
            elif node == node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child

            child.parent = node.parent

        # Case 3: Node has two children
        else:
            # Find in-order successor (smallest in the right subtree)
            successor = self.get_successor(node.right)
            node.key = successor.key  # Replace key with successor's key
            node.value = successor.value
            self.delete(successor)  # Recursively delete successor

            # Rebalance the tree
            # node = node.parent
            while node:
                node.update_height()
                bf = node.parent.balance_factor()
                self.balance_tree(node, bf)
                self.update_to_root(node)
                node = node.parent

    def get_successor(self, node):
        # Get the node with the smallest key in the subtree
        while node and node.left and node.left.is_real_node():  # Added checks for None
            node = node.left
        return node

    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """

    def join(self, tree2, key, val):
        max_node = self.max_node()
        tree2_root = tree2.get_root()
        node = max_node
        if max_node.key < key:
            max_node.right = tree2_root
        else:
            min_node = self.min_node()
            node = min_node
            min_node.left = tree2_root
        while node:
            node.update_height()
            bf = node.parent.balance_factor()
            self.balance_tree(node, bf)
            self.update_to_root(node)
            node = node.parent

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """

    def split(self, node):
        t1 = AVLTree()
        t2 = AVLTree()
        if node.left.is_real_node():
            node.left.parent = None
            t1.set_root(node.left)

        if node.right.is_real_node():
            node.right.parent = None
            t2.set_root(node.right)

        curr = node
        while curr.parent is not None:
            parent = curr.parent
            # parent_tree = AVLTree(parent)
            if curr == parent.left:  # curr node is left child
                if parent.right.is_real_node():
                    right_tree = AVLTree()
                    parent.left = AVLNode(None, None)
                    parent.right.parent = None
                    right_tree.set_root(parent.right)
                    t2.insert(parent.key, parent.value)
                    t2.join(right_tree, parent.right.key, parent.right.value)
            else:  # curr node is right child
                if parent.left.is_real_node():
                    left_tree = AVLTree()
                    parent.right = AVLNode(None, None)
                    parent.left.parent = None
                    left_tree.set_root(parent.left)
                    t1.insert(parent.key, parent.value)
                    t1.join(left_tree, parent.left.key, parent.left.value)
            curr = parent

        self.set_root(None)
        return t1, t2

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def in_order_to_arr(self, node, arr):
        if node.is_real_node():
            self.in_order_to_arr(node.left, arr)
            arr.append((node.key, node.value))
            self.in_order_to_arr(node.right, arr)
        return arr

    def avl_to_array(self):
        arr = self.in_order_to_arr(self.root, [])
        return arr

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """

    def max_node(self):
        node = self.get_root()
        if node is None:
            return None
        if not node.right.is_real_node():
            return node
        else:
            parent = node
            while node.is_real_node():
                parent = node
                node = node.right
            return parent

    def min_node(self):
        node = self.get_root()
        if node is None:
            return None
        if not node.left.is_real_node():
            return self
        else:
            while node.left.is_real_node():
                node = node.left
            return node

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        if not self:
            return 0
        else:
            root = self.get_root()
            return root.size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    def print_tree(self):
        def _print(node, indent="", last=True):
            if node:
                print(indent, "`- " if last else "|- ", f"({node.key}, {node.value} , {node.height}, {node.size})",
                      sep="")
                indent += "   " if last else "|  "
                _print(node.left, indent, False)
                _print(node.right, indent, True)

        _print(self.root)


def main():
    tree1 = AVLTree()
    tree2 = AVLTree()
    elements1 = [(10, "A"), (20, "B"), (30, "C"), (40, "D"), (50, "E"), (25, "F"), (60, "t")]
    elements2 = [(1, "A"), (2, "B"), (3, "C"), (4, "D"), (5, "E"), (6, "t")]
    # elements = [(10, "A"), (20, "B"), (30, "C")]
    for key, value in elements1:
        tree1.insert(key, value)
        
    tree1.finger_insert(35, "K")
    tree1.finger_insert(34, "q")
    tree1.finger_insert(33, "w")
    tree1.finger_insert(32, "s")
    tree1.finger_insert(31, "qx")
    # tree1.print_tree()

    # print("original tree")
    # tree1.print_tree()
    # print()
    # tree2.print_tree()
    # print()
    # tree1.join(tree2 , 3 , "C")
    # print("after join")
    tree1.print_tree()

    node_to_insert = tree1.search(30)[0]
    t1, t2 = tree1.split(node_to_insert)
    print("tree1:")
    t1.print_tree()
    print("tree2:")
    t2.print_tree()


if __name__ == '__main__':
    main()