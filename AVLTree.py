# id1: 322334426
# name1: Inbal Avidov
# username1: inbalavidov
# id2: 212047195
# name2: Inbal Moryles
# username2: inbalmoryles

import math
import random

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value, node=None):
        self.key = key
        self.value = value
        if key is None:  # no key, creating a virtual node
            self.left = None  # left child of virual node is None
            self.right = None  # right child of virual node is None
            self.parent = node
            self.height = -1
        else:  # key has not None value, creating a real node
            self.left = AVLNode(None, None)  # left child is virtual node
            self.right = AVLNode(None, None)  # right child is virtual node
            self.parent = node
            self.height = 0
            self.left.parent = self
            self.right.parent = self

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    # checking if the node has None as key
    def is_real_node(self):
        if self.key is None:
            return False
        else:
            return True

    # return balance factor
    def balance_factor(self):
        return self.left.height - self.right.height

    # update node height
    def update_height(self):
        if self.is_real_node():
            # If the node is a real node, calculate the height based on its children.
            left_height = self.left.height if self.left and self.left.is_real_node() else -1
            right_height = self.right.height if self.right and self.right.is_real_node() else -1
            self.height = 1 + max(left_height, right_height)
        else:
            # If it's a virtual node, set the height to -1
            self.height = -1


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        self.root = None
        self.size = 0
        self.max = None

    # setting root to empty tree
    def set_root(self, node):
        self.root = node

    #setting tree size
    def set_size(self, size_to_add):
        self.size = self.size + size_to_add
    
    #setting max node of the tree
    def set_max(self, node):
        self.max = node

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    # searching toward down from specific node.
    # in case the function is called from insert\finger_insert function
    # we return the node who is going to be the new node parent
    # in case the function is called from search\finger_search function
    # we return the node if found or None if not
    def search_from_node(self, node, key, e , is_insert):
        prev_node = None
        while node.is_real_node():
            if not is_insert:  # the case of node.key == key is not possible in insert
                if node.key == key:
                    return node, e
            else:  # save the node's parent for insert
                prev_node = node
            if node.key < key:
                node = node.right
            else:
                node = node.left
            e += 1  # in every step down on a path in the tree, increase e

        if is_insert:
            return prev_node, e  # return the node we want to be the parent of the new node
        else:
            return None, e  # in regular search, case we didnt find the key

    # searching node from root
    def search(self, key):
        node = self.root
        # calling to search_from_node with the root and is_insert= False
        x, e = self.search_from_node(node, key, 1, False)
        return x, e

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    # searching from max_node
    def finger_search(self, key, is_insert=False):
        node = self.max_node()
        e = 1
        # going up from max_node until we get to the first node that his key is smaller then the key that we search
        # or until root
        while node is not None:
            if key == node.left.key : return node.left, e
            else:
                while node.key > key and node.parent is not None:
                    node = node.parent
                    e += 1
                # search toward down from the node we found
                node, e = self.search_from_node(node, key, e, is_insert)
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

    # insert new node to the tree, search the new node parent from root
    def insert(self, key, val):
        new_node = AVLNode(key, val)
        root = self.get_root()
        if not root:  # if the tree is empty, set new node to root
            self.root = new_node
            self.set_size(1) #increase tree's size by 1
            self.set_max(new_node) #setting root as max node
            return new_node, 0, 0
        else:
            node, e = self.search_from_node(root, key, 0, True)  # find the new node parent
            # and the number of edges from root to the parent

            # setting the new node as child of the parent
            if node.key < key:
                node.right = new_node
            else:
                node.left = new_node
            new_node.parent = node 

            new_node, h = self.balance_after_insert(new_node, node, 0)  # balance the tree after insertion
            self.set_size(1) #update size

            #if the new node's key is bigger the current max, set new node as max node
            if self.max:
                if key > self.max.key: self.set_max(new_node)
            return new_node, e, h


    def balance_after_insert(self, new_node, node, h=0):
        while node:
            prev_node_height = node.height  # saving prev height for comparison
            node.update_height()
            bf = node.balance_factor()
            if abs(bf) < 2 and prev_node_height == node.height:  # bf is legal and height didnt change, finish
                return new_node, h
            elif abs(bf) < 2 and prev_node_height != node.height:
                h += 1 #promote case, h+=1
                node = node.parent # bf is legel but height has changed, check parent
            else:  # balance tree
                self.balance_tree(node, bf)
                new_node.update_height()
                return new_node, h
        return new_node, h


    def balance_tree(self, node, bf):
        """Rebalance the tree."""
        if bf > 1: # if node left heavy
            if node.left.balance_factor() < 0: # if node's left child is right heavy
                self.rotate_left(node.left)
            self.rotate_right(node)
                # Right heavy
        else: # if node right heavy
            if node.right.balance_factor() > 0: # if node's right child is left heavy
                self.rotate_right(node.right)
            self.rotate_left(node)
        return None


    def rotate_left(self, node):
        right_child = node.right  # Identify the right child of the node that will become the new root after rotation.

        # Move the left subtree of the right child to be the right subtree of the current node.
        node.right = right_child.left
        if right_child.left.is_real_node():  # Check if the left child of the right node is a real node.
            right_child.left.parent = node  # Update the parent pointer of the moved subtree.

        # Update the parent pointer of the right child to point to the current node's parent.
        right_child.parent = node.parent
        if not node.parent:  # If the current node is the root, update the tree's root pointer.
            self.root = right_child
        elif node == node.parent.right:  # If the node is a right child, update its parent's right pointer.
            node.parent.right = right_child
        else:  # Otherwise, update its parent's left pointer.
            node.parent.left = right_child

        # Update the left child of the right child to be the current node.
        right_child.left = node

        # Update the parent pointer of the current node to point to the right child.
        node.parent = right_child
        node.left.parent = node
        node.right.parent = node

        right_child.left.update_height()
        node.parent.update_height()


    def rotate_right(self, node):
        left_child = node.left  # Identify the left child of the node that will become the new root after rotation.

        # Move the right subtree of the left child to be the left subtree of the current node.
        node.left = left_child.right
        if left_child.right.is_real_node:  # Check if the right child of the left node is a real node.
            left_child.right.parent = node  # Update the parent pointer of the moved subtree.

        # Update the parent pointer of the left child to point to the current node's parent.
        left_child.parent = node.parent
        if not node.parent:  # If the current node is the root, update the tree's root pointer.
            self.root = left_child
        elif node == node.parent.left:  # If the node is a left child, update its parent's left pointer.
            node.parent.left = left_child
        else:  # Otherwise, update its parent's right pointer.
            node.parent.right = left_child

        # Update the right child of the left child to be the current node.
        left_child.right = node

        # Update the parent pointer of the current node to point to the left child.
        node.parent = left_child
        node.left.parent = node
        node.right.parent = node

        left_child.right.update_height()
        node.parent.update_height()
        return None

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

    # insert new node to the tree, search the new node parent from max node
    def finger_insert(self, key, val):
        new_node = AVLNode(key, val)
        if self.root is None:  # if the tree is empty, set new node to root
            self.root = new_node
            self.set_size(1) #increase tree's size by 1
            self.set_max(new_node) #setting root as max node
            return new_node, 0, 0
        else:
            node = self.finger_search(key, True)[0]  # find the new node parent

            # setting the new node as child of the parent
            if node.key < key:
                node.right = new_node
            else:
                node.left = new_node
            new_node.parent = node

            if key > self.max.key : 
                self.set_max(new_node) #setting new node as max node
                e = 1
            else :
                e = self.finger_search(key, False)[1] # get number of edges between max node and the new node

            new_node, h = self.balance_after_insert(new_node, node, 0)  # balance the tree after insertion
            self.set_size(1)  #increase tree's size by 1

            return new_node, e, h

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        node_key = node.key
        # Case 1: Node has no children (leaf)
        if not node.left.is_real_node() and not node.right.is_real_node():
            if not node.parent:  # Node is root
                self.root = None  # set the root to None
            elif node == node.parent.left:
                node.parent.left = AVLNode(None, None, node.parent)
            else:
                node.parent.right = AVLNode(None, None, node.parent)

        # Case 2: Node has one child
        elif not node.left.is_real_node() or not node.right.is_real_node():
            child = node.left if node.left.is_real_node() else node.right  # child of the node we delete

            if not node.parent:  # Node is root
                self.root = child  # setting the one child to be the root
            elif node == node.parent.left:  # node is left child
                node.parent.left = child
            else:  # node is right child
                node.parent.right = child

            child.parent = node.parent

        # Case 3: Node has two children
        else:
            # Find in-order successor (smallest in the right subtree)
            successor = self.get_successor(node.right)
            node.key, node.value = successor.key, successor.value  # Replace key and value with successor's key
            self.delete(successor)  # Recursively delete successor

        # #go up on the path to the root from the node, update heights and balance if needed
        
        while node:
            node.update_height()  # Update the height of the current node
            balance_factor = node.balance_factor() 
            if abs(balance_factor) > 1:
                self.balance_tree(node, balance_factor)

            node = node.parent  # Move up the tree

        # Update tree's size
        self.set_size(-1)

        if self.max: #if the tree has max node
            if node_key == self.max.key: #if we delete the max node, update max
                self.update_max()
        return None


    def get_successor(self, node):
        # Get the node with the smallest key in the subtree
        while node.left.is_real_node():  # continue while there is left child
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
    or the oppo
    
    
    site way
    """

    def join(self, tree2, key, val):
        new_node = AVLNode(key, val)  # creating new node to join trees
        # get roots of both trees for comparison
        tree1_root = self.get_root()
        tree2_root = tree2.get_root()

        # Handle edge cases where both trees are empty, setting new node to be self's root and max node
        if tree1_root is None and tree2_root is None:
            self.set_root(new_node)
            self.set_max(new_node)
            return None

        #  Handle edge cases where one tree is empty
        if tree1_root is None:
            tree2.insert(new_node.key, new_node.value) #join with one node is equal to insert
            self.set_root(tree2.root) # set self to the tree we want ro return
            self.set_max(tree2.max) #set max node
            tree2.set_root(None) # making tree2 unusable
            return None

        if tree2_root is None:
            self.insert(new_node.key, new_node.value) #join with one node is equal to insert
            return None

        # Determine which tree is taller and direction to attach
        if tree1_root.height > tree2_root.height:
            if tree1_root.key > tree2_root.key:
                flag = True
            else:
                flag = False
            higher, shorter, attach_left = self, tree2, flag

        # elif tree1_root.height < tree2_root.height:
        else:
            if tree1_root.key > tree2_root.key:
                flag = False
            else:
                flag = True
            higher, shorter, attach_left = tree2, self, flag

        # Attach the shorter tree to the taller tree
        shorter_root = shorter.root
        curr_node = higher.root

        while shorter_root.height < curr_node.height:  # find the right node to attach trees, according to heights
            prev_node = curr_node
            curr_node = curr_node.left if attach_left else curr_node.right  # curr node is the node to attach to in the higher tree
            if not curr_node.is_real_node():  # in case curr_node is a viryual node return to his father and break
                curr_node = prev_node
                break

        parent = curr_node.parent
        # setting shorter root and curr node as new node childrens
        if attach_left:
            new_node.right, new_node.left = curr_node, shorter_root
        else:
            new_node.left, new_node.right = curr_node, shorter_root

        # setting parent
        curr_node.parent = new_node
        shorter_root.parent = new_node
        new_node.parent = parent

        # check that the curr node is not the root of higher tree
        if parent:
            # setting the new node to be child of the curr node parent and setting virtual node as child in case of None child
            # this can happen when join is called from split with leaf
            if attach_left:
                parent.left = new_node
            else:
                parent.right = new_node

        # setting new node as root of higher tree
        else:
            higher.set_root(new_node)

        # setting self root as higher root in case self is the shorter one
        tree2_max = tree2.max
        if self.max and tree2_max : #if there is max node to both trees
            if tree2_max.key > self.max.key : #if tree2's max node is greater the tree1's max node set max
                self.set_max(tree2_max)
        
        #if tree2 is the higher tree, set higher's root to be self's root
        if higher.root == tree2.root:
            self.set_root(higher.get_root()) 

        #go up on the path to the root from the new node, update heights and balance if needed
        node = new_node

        while node:
            node.update_height() 
            balance_factor = node.balance_factor()
            if abs(balance_factor) > 1:
                self.balance_tree(node, balance_factor)

            node = node.parent

        #make tree2 to וnusable
        tree2.set_root(None)
        return None


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
        t1, t2 = AVLTree(), AVLTree()

        # initialize t1 and t2 as left and right subtrees of the split node
        if node.left.is_real_node():
            node.left.parent = None
            t1.set_root(node.left)
        if node.right.is_real_node():
            node.right.parent = None
            t2.set_root(node.right)

        # going up the tree until root for spliting and joining subtrees
        curr = node
        while curr.parent is not None:
            parent = curr.parent
            if curr == parent.left:  # Current node is the left child
                # join parent's right subtree to t2 tree
                if parent.right.is_real_node():
                    if t2.get_root() is None:  # t2 is empty
                        t2.set_root(parent.right)  # set the right subtree of parent as t2
                        parent.right.parent = None  # remove edge between the node and his parent
                        t2.insert(parent.key, parent.value)  # add parent to t2
                    else:
                        right_tree = AVLTree() 
                        right_tree.set_root(parent.right) #set the right subtree of parent as right tree
                        parent.right.parent = None  # remove edge between the node and his parent
                        t2.join(right_tree, parent.key, parent.value)
                else:
                    t2.insert(parent.key, parent.value) #insert the parent to t2 in case the parent has no right child
                # Remove current connection
                parent.left = None

            else:  # Current node is the right child
                # join parent's left subtree to t1 tree
                if parent.left.is_real_node():
                    if t1.get_root() is None:  # t2 is empty
                        t1.set_root(parent.left)  # set the left subtree of parent as t1
                        parent.left.parent = None  # remove edge between the node and his parent
                        t1.insert(parent.key, parent.value)  # add parent to t1
                    else:
                        left_tree = AVLTree()
                        left_tree.set_root(parent.left) #set the left subtree of parent as right tree
                        parent.left.parent = None # remove edge between the node and his parent
                        t1.join(left_tree, parent.key, parent.value)
                else:
                    t1.insert(parent.key, parent.value)  #insert the parent to t1 in case the parent has no left child
                # Remove current connection
                parent.right = None

            # Move up the tree
            curr = parent

        # Clear the root of the original tree
        self.set_root(None)
        #set max for both trees
        t1.update_max() 
        t2.update_max()

        return t1, t2

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def in_order_to_arr(self, node, arr):
        if node is None:
            return arr
        if node.is_real_node():
            self.in_order_to_arr(node.left, arr)  # Recursively traverse the left subtree
            arr.append((node.key, node.value))  # Append the current node's key and value
            self.in_order_to_arr(node.right, arr)  # Recursively traverse the right subtree
        return arr

    def avl_to_array(self):
        arr = self.in_order_to_arr(self.root, [])  # creating array of nodes using in order
        return arr

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        return self.max 
    
    def update_max(self):
        node = self.get_root()
        if node is None:  # if the tree is empty, return None
            return
        if not node.right.is_real_node():  # if there is no right child, the root is the maximum node
            self.set_max(node)
        else:  # travel down the right subtree to find the rightmost node
            parent = node
            while node.is_real_node():  # Continue until a virtual node is reached
                parent = node  # Keep track of the last real node
                node = node.right
            self.set_max(parent)  # Return the last real node encountered

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root  # return root

    def print_tree(self):
        def _print(node, indent="", last=True):
            if node:
                print(indent, "`- " if last else "|- ",
                      f"({node.key}, {node.value}, {node.height}, {node.parent.key if node.parent else 'None'})",
                      sep="")
                indent += "   " if last else "|  "
                _print(node.left, indent, False)
                _print(node.right, indent, True)

        _print(self.root)



def main():
    def count_inversions(arr):
        n = len(arr)
        inv_count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] > arr[j]:
                    inv_count += 1
        return inv_count

    def randomized_swap_sorted_array(arr):
        n = len(arr)
        for i in range(n-1):  # עובר מהאינדקס השני מהסוף עד הראשון
            if random.random() < 0.5:  # סיכוי של חצי
                arr[i], arr[i+1] = arr[i+1], arr[i]
        return arr
    
    tree1 = AVLTree()
    #tree2 = AVLTree()
    # arr = randomized_swap_sorted_array(elements1)
    # print(count_inversions(arr))
    
    # elements2 = [(10, "A"),(5, "A"),(20, "A"),(15, "A")]
    # #     # 3 = [(10, "A"), (20, "B"), (30, "C")]
    #for j in range(5,6):    
    k = 0
    sums = []
    while k < 20  :
            #arr = randomized_swap_sorted_array(elements1)
            # cnt = count_inversions(arr)
            # print(cnt)
            # sums.append(cnt)
        tree2 = AVLTree()
        elements1 = [(i,"A") for i in range(1, (111*(2**1))+1)]
        sum = 0
        #arr = randomized_swap_sorted_array(elements1)
        random.shuffle(elements1)
        for key, value in elements1:
            e = tree2.finger_insert(key, value)[1]
            sum += e
        #print(sum)
        sums.append(sum)
            
            # sums.append(count_inversions(elements1))
            # sums.append(sum)
        k += 1
    all = 0
    for i in range(len(sums)):
        all += sums[i]
    print(all//20)



if __name__ == '__main__':
    main()