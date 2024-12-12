#id1: 322334426
#name1: Inbal Avidov
#username1: inbalavidov
#id2: 212047196
#name2: Inbal Moryles
#username2: inbalmoryles


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
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		if self.key is None:
			return False
		else:
			return True


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None

	def height(self):
		root = self.get_root
		return root.height if root else -1

	def update_height(self, node):
		node.height = 1 + max(self.height(node.left), self.height(node.right))

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
				node = node.left
			else:
				node = node.right
			e += 1

		if is_insert: return prev_node, e
		else: return None, e

	def search(self, key):
		node = self.root
		x,e = self.search_from_node(node, key, 1, False)
		return x,e


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

		while node.is_real_node():
			while node.key > key:
				node = node.parent
				e += 1
			node , e = self.search_from_node(node, key, e, False)
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
	def insert(self, key, val):
		new_node = AVLNode(key, val)
		node = self.get_root()

		node, e = self.search_from_node(node, key, 1, True)
		if node.key < key:
			node.left = new_node
		else:
			node.right = new_node
		#update height and balance tree
		return None, -1, -1


	def rotate_left(self, node):
		right_child = node.right
		node.right = right_child.left
		if right_child.left.is_real_node:
			right_child.left.parent = node
			node.left = right_child.left
		right_child.parent = node.parent
		if not node.parent:
			self.root = right_child
		elif node == node.parent.right:
			node.parent.right = right_child
		else:
			node.parent.left = right_child
		left_child.left = node
		node.parent = right_child

	def rotate_right(self, node):
		left_child = node.left
		node.left = left_child.right
		if left_child.right.is_real_node:
			left_child.right.parent = node
			node.right = left_child.right
		left_child.parent = node.parent
		if not node.parent:
			self.root = left_child
		elif node == node.parent.left:
			node.parent.left = left_child
		else:
			node.parent.right = left_child
		left_child.right = node
		node.parent = left_child


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

		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
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
		if max_node.key < key :
			max_node.right = tree2_root
		else :
			min_node = self.min_node()
			min_node.left = tree2_root
			#balance the tree
		tree2 = None





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
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def in_order_to_arr(self, node, arr):
		if not node.is_real_node:
			return arr
		self.in_order_to_arr(node.left, arr)
		arr.append((node.key , node.value))
		self.in_order_to_arr(node.right, arr)

	def avl_to_array(self):
		return self.in_order_to_arr(self.root, [])


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		node = get_root(self)
		if node is None:
			return None
		if not node.right.is_real_node():
			return self
		else:
			while node.is_real_node():
				node = node.right
			return node

	def min_node(self):
		node = get_root(self)
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
			array = avl_to_array(self)
			return len(array)




	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root

	####tree printer
	def print_tree(self):
		def _print(node, indent="", last=True):
			if node:
				print(indent, "`- " if last else "|- ", f"({node.key}, {node.value})", sep="")
				indent += "   " if last else "|  "
				_print(node.left, indent, False)
				_print(node.right, indent, True)

		_print(self.root)

tree = AVLTree()
elements = [(10, "A"), (20, "B"), (30, "C"), (40, "D"), (50, "E"), (25, "F")]
for key, value in elements:
	tree.insert(key, value)

tree.print_tree()