#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

# In[12]:


from kd_tree.kdtree import KDTree, Node
import unittest
import numpy as np


# In[51]:


class TestKDTree(unittest.TestCase):
    def setUp(self):
        self.kdTree = KDTree()
        self.kdTreeRoot = self.kdTree.buildKdTree(np.array([(12,34), (25,36), (9,10)]))
    
    def test_buildKdTree_without_weights(self):
        self.assertEqual(self.kdTreeRoot.weight, None, "Weights present")
    
    def test_buildKdTree_with_weights(self):
        kdTreeWithWeights = self.kdTree.buildKdTree(np.array([(12,34), (25,36), (9,10)]), [10, 20, 30])
        self.assertEqual(kdTreeWithWeights.weight["weight"], 10)
    
    def test_buildKdTree_with_incompatible_weights(self):
        kdTreeWithWeights = self.kdTree.buildKdTree(np.array([(12,34), (25,36), (9,10)]), [10, 20])
        self.assertEqual(kdTreeWithWeights.weight["weight"], 10)
    
    def test_isLeaf(self):
        res = self.kdTree.isLeaf(self.kdTreeRoot.left)
        self.assertEqual(res, True, "Incorrect value")

# unittest.main(argv=[''], verbosity=2, exit=False)
if __name__ == '__main__':
    unittest.main()

