
import unittest
import sys
import KDTree


# In[70]:


class TestKDTree(unittest.TestCase):
    def test_buildKdtree(self):
        res = KDTree.buildKdTree(np.array([(86, 338), (164, 360), (75, 58)]))
        self.assertEqual(res)
if __name__ == '__main__':
    unittest.main()
