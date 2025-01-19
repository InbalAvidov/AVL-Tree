''' In order to run the tester:
    1.  Make sure your AVLTree.py file and AVLTreeTester2022.py
        file are both in the same directory.
    2.  Run your AVLTree.py file
    3.  Run the AVLTreeTester2022.py file
    4.  Your grade should be written in the terminal.
        Only failed tests will be presented in the terminal,
        together with the AssertionError that made them fail.
        
        
    Note: if you want to see the time each test took, add the following commands:
    1. Add this to def setUp(cls) method - cls.start_time = time.time()
    2. Add this method:
        def tearDown(self):
            t = time.time() - self.start_time
            print("%s: %.3f " % (self.id()[31:], t))
'''
    

import time
import unittest, random
import numpy as np
from AVLTree import AVLNode , AVLTree


GRADE = 0
MAX_GRADE = 70
TESTS = 26
SCORE_PER_TEST = MAX_GRADE/TESTS

class AVLTreeTester2022(unittest.TestCase):

    
    @staticmethod
    def add_points(x: float):
        global GRADE
        GRADE += x


    @staticmethod
    def in_order(tree: AVLTree):
        lst = []
        def in_order_rec(node: AVLNode, in_order_lst: list[str]):
            if node is not None and node.is_real_node():
                in_order_rec(node.left, in_order_lst)
                in_order_lst.append(node.value)
                in_order_rec(node.right, in_order_lst)
        in_order_rec(tree.root, lst)
        return lst


    @classmethod
    def setUp(cls):
        cls.tree = AVLTree()
        cls.tree_2 = AVLTree()

    @staticmethod
    def create_tree(values, random_order = False):
        if random_order: random.shuffle(values)
        tree = AVLTree()
        for val in values:
            tree.insert(val ,str(val))
        return tree


    def test_basic_avl_node_get(self):
        self.tree.insert(2,"2")
        self.tree.insert(1,"1") #    '2'
        self.tree.insert(3,"3") # '1'   '3'
        root = self.tree.root
        self.assertTrue(root.is_real_node(), "FAIL - root should be a real node")
        self.assertEqual(root.height, 1)
        self.assertTrue(root.left.is_real_node())
        self.assertTrue(root.right.is_real_node())
        self.assertEqual(root.left.height, 0)
        self.assertEqual(root.right.height, 0)
        self.assertEqual(root.left.parent, root)
        self.assertEqual(root.right.parent, root)
        self.add_points(SCORE_PER_TEST)


    def test_empty_tree(self):
        self.assertTrue(self.tree.size() == 0, "FAIL - tree.empty() on a new tree should return True")
        self.add_points(SCORE_PER_TEST)



    def test_do_10000_insertions_and_deletions(self):
        avl_tree = AVLTree()
        for i in range(10000):
            avl_tree.insert(i, "num" + str(i))
        # Check tree size after insertions
        self.assertEqual(avl_tree.size() , 10000 , "FAIL - after 10000 insertions, size should be 10000")

        for i in range(10000):
            avl_tree.delete(avl_tree.root)

        self.assertEqual(avl_tree.size() , 0 , "FAIL - after deleting all nodes size should be 0")
        self.add_points(SCORE_PER_TEST)

    def test_order_after_insertions(self):
        test_list = [23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000]
        avl_tree = AVLTree()
        for num in test_list:
            avl_tree.insert(num , str(num))

        self.assertEqual(avl_tree.root.height , 3 , "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - height of root should be 3")
        self.assertEqual(avl_tree.root.key , 23 , "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root should be 23")
        self.assertEqual(avl_tree.root.left.key , 2 , "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root's left son should be 2")
        self.assertEqual(avl_tree.root.right.key, 60, "FAIL - after inserting 23 , 4 , 60 , 999 , 33 , 2 , 1 , 1000 - root's right son should be 60")
        self.add_points(SCORE_PER_TEST)


    def test_delete_first_check_size(self):
        real_length = 0
        for i in range(100):
            self.tree.insert(i,str(i))
            real_length += 1
            self.assertEqual(real_length , self.tree.size() , "FAIL: Tree size incorrect")
        for i in range(99):
            self.tree.delete(self.tree.search(i)[0])
            real_length -= 1
            self.assertEqual(real_length, self.tree.size(), "FAIL: Tree size incorrect")

        self.add_points(SCORE_PER_TEST)
        



    def test_avl_to_array_identical_vals(self):
        lst = [i for i in range(1000)]
        copy = []
        for i in range(1000):
            copy.append((i , str(i)))
        random.shuffle(lst)
        T = self.create_tree(lst)
        self.assertEqual(copy,T.avl_to_array(), "FAIL - avl_to_array() is not consistent with the insertion order provided")
        self.add_points(SCORE_PER_TEST)


    def test_avl_to_array_random(self):

        python_list_numbers = []

        for i in range(50):
            random_number = random.randint(0,10000)
            while random_number in python_list_numbers:
                random_number = random.randint(0,10000)
            python_list_numbers.append(random_number)
            self.tree.insert(random_number,str(random_number))

        python_list_numbers.sort()
        python_list = []
        for num in python_list_numbers:
            python_list.append((num , str(num)))
        avl_list = self.tree.avl_to_array()
        self.assertEqual(python_list, avl_list, "FAIL - problem in avl_to_array")
        self.add_points(SCORE_PER_TEST)



    def test_size_of_empty_tree(self):
        self.assertEqual(self.tree.size(), 0, "FAIL - size() on an empty tree should return 0")
        self.tree.insert(0,"0")
        self.assertNotEqual(self.tree.size(), 0, "FAIL - tree.length() on a non-empty tree should not return 0")
        self.assertEqual(self.tree.size(), 1, "FAIL - size() a tree with one node should return 1")
        self.add_points(SCORE_PER_TEST)
    

    def test_length_after_insert(self):
        length = 0
        for i in range(10):
            self.tree.insert(10-i,"insert_number_"+str(i))
            length += 1
            self.assertEqual(length, self.tree.size(), "FAIL - Length error, first loop, iteration {}".format(str(i)))
        more_to_add = [11 ,12 ,13 ,14 ,15 ,16 ,17, 18, 19 ,20]
        for i in more_to_add:
            self.tree.insert(i,"insert_number_"+str(i))
            length += 1
            self.assertEqual(length, self.tree.size(), "FAIL - Length error, second loop, iteration {}".format(str(i)))
        self.add_points(SCORE_PER_TEST)

    def test_length_after_many_insertions(self):
        length = 0
        avl_tree = AVLTree()
        in_tree = []

        for i in range(100):

            rand_num = random.randint(0, 10000)

            while rand_num in in_tree:
                rand_num = random.randint(0, 10000)

            avl_tree.insert(rand_num , str(rand_num))
            in_tree.append(rand_num)
            length += 1
            self.assertEqual(length, avl_tree.size(), "FAIL - Length error, third loop, iteration {}".format(str(i)))

        self.add_points(SCORE_PER_TEST)

    def test_size_after_delete(self):
        for i in range(1000):
            self.tree.insert(i,str(i))
        for j in range(999):
            self.tree.delete(self.tree.root)
            self.assertEqual(self.tree.size(), 999 - j, "FAIL - Length error")
        self.tree.delete(self.tree.root)
        self.assertEqual(self.tree.size(), 0, "FAIL - Length error after deleting all the nodes from the list")
        self.add_points(SCORE_PER_TEST)



    def test_split_simple(self):
        avl_tree = AVLTree()
        avl_tree.insert(4, "D")
        avl_tree.insert(2, "B")
        avl_tree.insert(6, "F")
        avl_tree.insert(1, "A")
        avl_tree.insert(3, "C")
        avl_tree.insert(5, "E")
        avl_tree.insert(7, "G")

        key = 4
        left_tree, right_tree = avl_tree.split(avl_tree.search(key)[0])

        left_tree_list = left_tree.avl_to_array()
        actual_left_list = [(1 , "A") , (2 , "B") , (3 , "C")]
        self.assertEqual(left_tree_list , actual_left_list , "FAIL - Split didn't assign correct nodes to splitted trees")
        right_tree_list = right_tree.avl_to_array()
        actual_right_list = [(5, "E") , (6, "F") , (7, "G")]
        self.assertEqual(right_tree_list , actual_right_list , "FAIL - Split didn't assign correct nodes to splitted trees")

        self.add_points(SCORE_PER_TEST)



    def test_join_simple(self):
        left_tree = AVLTree()
        left_tree.insert(2, "B")
        left_tree.insert(1, "A")

        right_tree = AVLTree()
        right_tree.insert(4, "D")
        right_tree.insert(6, "F")
        right_tree.insert(5, "E")

        key = 3

        left_tree.join(right_tree, key, "C")
        correct_array = [(1, "A") , (2, "B") , (3 , "C") , (4, "D") , (5, "E") , (6, "F")]
        self.assertEqual(left_tree.avl_to_array() , correct_array)
        self.add_points(SCORE_PER_TEST)


    def test_non_succesful_search(self):
        self.assertEqual(self.tree.search(0)[0], None, "FAIL - tree.search() on an empty tree should return -1")
        for i in range(10):
            self.tree.insert(i, str(i))
        self.assertEqual(self.tree.search(11)[0], None, "FAIL - tree.search() should return None " \
                                                        "whenever val is not in the tree")
        self.add_points(SCORE_PER_TEST)
    
    
    def test_search(self):
        for i in range(100):
            self.tree.insert(i,str(i))
        for i in range(100):
            self.assertEqual(self.tree.search(i)[0].key,i)
            self.assertEqual(self.tree.search(i)[0].value, str(i))
        self.add_points(SCORE_PER_TEST)
    

    def test_search_complex(self):
        N = 100
        T = self.create_tree([i for i in range(N)],random_order=True)
        in_order = self.in_order(T)
        lst = [str(i) for i in range(N)]
        for i in range(N):
            lst[T.search(i)[0].key] = str(i)
        self.assertEqual(in_order,lst)
        self.add_points(SCORE_PER_TEST)

    
    def test_search_after_delete(self):
        N = 100
        T = self.create_tree([i for i in range(N)], random_order=True)
        for i in range(N):
            self.assertNotEqual(T.search(i)[0], None, "FAIL - search should return None iff str({}) is not in the tree".format(i))
            T.delete(T.search(i)[0])
            self.assertEqual(T.search(i)[0], None, "FAIL - search should return None iff str({}) is not in the tree".format(i))
        self.add_points(SCORE_PER_TEST)


    def test_big_join(self):
        N = 100

        left_tree_list = []
        for i in range(N):
            left_tree_list.append((i , str(i)) )
        right_tree_list = []
        for i in range(N+5, 2*N+5):
            right_tree_list.append((i, str(i)))
        left_tree = self.create_tree([i for i in range(N)], random_order=True)
        right_tree = self.create_tree([i for i in range(N+5, 2*N+5)] , random_order=True)

        join_key = N+2
        left_tree.join(right_tree , join_key , str(join_key))
        left_tree_list.append((join_key , str(join_key)))
        left_tree_list.extend(right_tree_list)

        self.assertEqual(left_tree_list , left_tree.avl_to_array() , "FAIL in joining big trees")
        self.add_points(SCORE_PER_TEST)

    def test_big_split(self):
        N = 1000
        avl_tree = self.create_tree([i for i in range(N)], random_order=True)
        split_key = 787
        right_tree , left_tree = avl_tree.split(avl_tree.search(split_key)[0])

        right_tree_list = []
        for i in range(787):
            right_tree_list.append((i , str(i)))

        left_tree_list = []
        for i in range(788, N):
            left_tree_list.append((i , str(i)))

        self.assertEqual(left_tree_list, left_tree.avl_to_array(), "FAIL in splitting big tree")
        self.assertEqual(right_tree_list, right_tree.avl_to_array(), "FAIL in splitting big tree")
        self.add_points(SCORE_PER_TEST)

    def test_inserts_and_avl_node_functions(self):
        # Example from https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99
        node_list = [41 , 20 , 65 , 11, 29, 50 , 91, 31 , 72 , 99]
        avl_tree = self.create_tree(node_list)

        # Check get_key and get_value
        for i in node_list:
            self.assertEqual(i , avl_tree.search(i)[0].key, "FAIL - get key")
            self.assertEqual(str(i), avl_tree.search(i)[0].value, "FAIL - get value")
        self.add_points(SCORE_PER_TEST)

        # Check root properties
        self.assertEqual(41, avl_tree.root.key , "FAIL - In https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99 root should be 41")
        self.assertNotEqual(False, avl_tree.root.is_real_node())


        self.add_points(SCORE_PER_TEST)

        # Check get parent
        roots_right_son = avl_tree.root.right
        roots_left_son = avl_tree.root.left
        self.assertEqual(avl_tree.root , roots_right_son.parent , "FAIL in get parent")
        self.assertEqual(avl_tree.root, roots_left_son.parent, "FAIL in get parent")
        self.add_points(SCORE_PER_TEST)

        # Check heights
        roots_right_right_grandson = roots_right_son.right
        self.assertEqual(1, roots_right_right_grandson.height, "FAIL in tree heights")
        self.assertEqual(3, avl_tree.root.height, "FAIL in tree heights")
        self.assertEqual(2, roots_right_son.height, "FAIL in tree heights")
        self.add_points(SCORE_PER_TEST)

        # Check is real node on real nodes
        self.assertNotEqual(False , roots_right_son.is_real_node())
        self.assertNotEqual(False, roots_left_son.is_real_node())
        self.add_points(SCORE_PER_TEST)

        # Check tree formation
        self.assertEqual(65 , roots_right_son.key , "FAIL - In https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99 root's right son is 65")
        #self.assertEqual(5 , roots_right_son.size , "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99") Test removed for 2024A
        self.assertEqual(20, roots_left_son.key, "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99")
        #self.assertEqual(4 , roots_left_son.size , "FAIL - tree size incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99") #Test removed for 2024A

        self.assertEqual(91 , roots_right_right_grandson.key , "FAIL - tree formation incorrect in https://visualgo.net/en/bst?mode=AVL&create=41,20,65,11,29,50,91,31,72,99")
        self.add_points(SCORE_PER_TEST)


        # Check virtual node properties
        childless_nodes = [avl_tree.search(11)[0], avl_tree.search(31)[0], avl_tree.search(50)[0], avl_tree.search(72)[0],
                           avl_tree.search(99)[0]]
        for node in childless_nodes:
            self.assertFalse(node.right.is_real_node() , "FAIL - is_real_node returns true for virtual node")
            self.assertFalse(node.left.is_real_node() , "FAIL - is_real_node returns true for virtual node")
            self.assertEqual(None, node.right.right, "FAIL - get_right should return None for a virtual node")
            self.assertEqual(None, node.right.left, "FAIL - get_left should return None for a virtual node")
            self.assertEqual(None, node.left.right, "FAIL - get_right should return None for a virtual node")
            self.assertEqual(None, node.left.left, "FAIL - get_left should return None for a virtual node")
        self.add_points(SCORE_PER_TEST)



    @classmethod
    def tearDownClass(self):
        super()
        # print("\n\n")
        # print("==Tester Results:==")
        # print("  # Of Tests: {}    ".format(NUMBER_OF_TESTS))
        # print("Successful Tests: {}".format(PASSED_TESTS))
        # print(" Failed Tests: {}   ".format(NUMBER_OF_TESTS - PASSED_TESTS))
        # print("The Final Grade is: ")
        # print("  {} out of {}      ".format(round(GRADE,1), MAX_GRADE))
        # print("\n\n")
        print(GRADE)

if __name__ == '__main__':
    unittest.main(verbosity = 0)
    #Change verbosity = 0 or verbosity = 2 for less/more details from tests

    