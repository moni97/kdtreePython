# kdtreePython
KDTree implementation with the support of weights. Each node created will be associated with a weight. Every node stores the weight associated to that package, the minimum weight in that subtree and the maximum weight.

Example:

1. Creating kdtree
```
from weighted_kdtree import kdtree
points = [(12,34), (25,36), (9,10), (5, 15), (30, 20), (20, 27)]
weights = [10, 20, 12, 20, 30, 28]
kd_tree = kdtree.KDTree(points, weights)
```

2. Preorder Traversal 
```
kdtree.KDTree.preorderTraversal(kd_tree.root)
[[(9, 10)], [(12, 34)], [(5, 15)], [(30, 20)], [(25, 36)], [(20, 27)]]
```

3. Weights
```
kd_tree.root.val, kd_tree.root.weight["weight"],  kd_tree.root.weight["minWeight"],  kd_tree.root.weight["maxWeight"]
((20, 27), 28, 30, 10)
```
4. Nearest Neighbor
```
kdtree.KDTree.nnKDTree((10, 20), kd_tree.root, 15, 3)
[(10.04987562112089, (9, 10)),
 (12.206555615733702, (20, 27)),
 (14.142135623730951, (12, 34))]
```
Future work:
Following weights related methods are to be added soon:
1. nearestNeighbor
2. Find points in a query rectangle with a weight threshold
3. Point with minimum weight in a query rectangle
4. Point with maximum weight in a query rectangle