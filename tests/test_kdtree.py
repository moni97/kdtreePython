#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# In[1]:


from weighted_kdtree import kdtree
import unittest
import numpy as np


# In[35]:


class TestKDTree(unittest.TestCase):
    
    # __init__ method
    def test_init_points_without_weights(self):
        kdtreeRoot = kdtree.KDTree([(12.34, 34.21)])
        self.assertEqual(kdtreeRoot.root.val, (12.34, 34.21), "Wrong values")
        self.assertEqual(kdtreeRoot.weights, None, "Weights present")
    
    def test_buildKdTree_single_point_with_weight(self):
        kdtreeRoot = kdtree.KDTree([(-12,-34)], [10])
        self.assertEqual(kdtreeRoot.root.val, (-12, -34), "Wrong values")
        self.assertEqual(kdtreeRoot.root.weight["weight"], 10)
        
    def test_buildKdTree_multiple_points_with_weight1(self):
        kdtreeRoot = kdtree.KDTree([(12,34), (25,36), (9,10), (5, 15), (30, 20), (20, 27)], [10, 20, 5, 15, 25, 30])
        self.assertEqual(kdtreeRoot.root.val, (20, 27), "Wrong values")
        self.assertEqual(kdtreeRoot.root.weight["weight"], 30, "Weights incompatible")
        
    def test_buildKdTree_multiple_points_with_weight2(self):
        kdtreeRoot = kdtree.KDTree([(12,34), (-25,36), (9,-10)], [10, 20, 30])
        self.assertEqual(kdtreeRoot.root.val, (9, -10), "Wrong values")
        self.assertEqual(kdtreeRoot.root.weight["weight"], 30, "")
    
    def test_buildKdTree_multiple_points_with_weight(self):
        kdtreeRoot = kdtree.KDTree([(12,34), (25,36)], [10, 20])
        self.assertEqual(kdtreeRoot.root.val, (25,36), "Wrong values")
        self.assertEqual(kdtreeRoot.root.weight["weight"], 20, "")
        
    def test_buildKdTree_single_point_with_weight(self):
        kdtreeRoot = kdtree.KDTree([(-12,-34)], [10])
        self.assertEqual(kdtreeRoot.root.val, (-12, -34), "Wrong values")
        self.assertEqual(kdtreeRoot.root.weight["weight"], 10)
    
    def test_buildKdTree_with_incompatible_weights1(self):
        self.assertRaises(ValueError, kdtree.KDTree, ([(12,34), (25,36), (9,10)], [10, 20]))
        
    def test_buildKdTree_with_incompatible_weights2(self):
        self.assertRaises(ValueError, kdtree.KDTree, ([(12,34), (25,36), (9,10,12)]))

    # Testing preorder traversal
    def test_preorderTraversal1(self):
        preorderTraversal = kdtree.KDTree.preorderTraversal(kdtree.KDTree([(12,34), (25,36), (9,10), (5, 15), (30, 20), (20, 27)]).root)
        self.assertEqual(preorderTraversal[0], [(9, 10)], "Order is incorrect")

     # Testing preorder traversal
    def test_preorderTraversal2(self):
        preorderTraversal = kdtree.KDTree.preorderTraversal(kdtree.KDTree([(12,34), (25,36), (9,10)], [10, 20, 30]).root)
        self.assertEqual(preorderTraversal[1], [(25, 36)] , "Order is incorrect")
        
     # Testing preorder traversal
    def test_dfs(self):
        dfs = kdtree.KDTree.dfs(kdtree.KDTree([(12,34), (25,36), (9,10), (5, 15), (30, 20), (20, 27)]).root)
        self.assertEqual(len(dfs['[(20, 27), 0, 6, None, None, None]']), 2, "Root node doesn't have two children")

    # NN
    def test_nnKdTree1(self):
        root = kdtree.KDTree([(12,34), (25,36), (9,10), (5, 15), (30, 20), (20, 27)]).root
        self.assertEqual(len(kdtree.KDTree.nnKDTree((8,6), root, 10, 1)), 1)
        
    def test_nnKdTree2(self):
        root = kdtree.KDTree([(12,34), (25,36), (9,10), (5, 15), (30, 20), (20, 27)]).root
        self.assertEqual(len(kdtree.KDTree.nnKDTree((8,6), root, 10, 2)), 2)

    def test_nnKdTree3(self):
        root = kdtree.KDTree([(12,34), (25,36), (9,10), (5, 15), (30, 20), (20, 27)]).root
        self.assertEqual(len(kdtree.KDTree.nnKDTree((12, 23), root, 5, 2)), 0)

unittest.main(argv=[''], verbosity=2, exit=False)