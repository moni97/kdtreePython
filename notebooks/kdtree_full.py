import statistics
import numpy as np
import sys
from graphviz import Digraph 

class Node:
    def __init__(self, val, axis=0, count = 0, weight = None):
        self.right = self.left = None
        self.val = val
        self.axis = axis
        self.count = count
        self.weight = None
        if weight:
            self.weight = {
                "weight": weight["weight"],
                "minWeight": weight["minWeight"],
                "maxWeight": weight["maxWeight"]
            }
class KDTree:
    def __init__(self, points, weights = None):
        if len(points) == 0 or not self.isPointsInSameDimension(points):
            raise ValueError("Problem in points: either it is empty or the dimensions")
   
        self.weights = None
        if not weights or len(weights) == 0:
            self.points = [[point] for point in points]
        else:
            if len(points) != len(weights):
                raise ValueError("Dimensions of points and weights does not match")
            self.points = [[point, weight] for point, weight in zip(points, weights)]
            self.weights = weights
        self.root = self.buildKdTree(self.points)
    
    @classmethod
    def isPointsInSameDimension(self, points):
        dimension = len(points[0])
        for pt in points:
            if len(pt) != dimension:
                return False
        return True
    
    @classmethod
    def getNodeParameters(self, points, axis, noOfPoints = 1, weights = None):
        weight = {"weight": None, "minWeight": None, "maxWeight": None}

        if weights:
            weight["weight"] = points[1]
            weight["minWeight"] = weights[-1][1]
            weight["maxWeight"] = weights[0][1]
        elif len(points) > 1:
            weight["weight"] = weight["minWeight"] = weight["maxWeight"] = points[1]
        return [points[0], axis, noOfPoints, weight]
        
    @classmethod
    def buildKdTree(self, points, hyperplaneAxis = 0):
        dim = len(points[0][0])
        nxtHyperplaneAxis = (hyperplaneAxis + 1) % dim
        
        if len(points) == 1:
            parameters = self.getNodeParameters(points[0], hyperplaneAxis)
            return Node(*parameters)

        medianIndex = len(points) // 2
        sortedPoints = sorted(points, key=lambda x: x[0][hyperplaneAxis])

        median = sortedPoints[medianIndex]
        leftPoints = sortedPoints[:medianIndex]
        rightPoints = sortedPoints[medianIndex + 1:]
        sortedWeights = None

        if (len(points[0]) > 1):
            sortedWeights = sorted(points, key=lambda x: x[1])
        
        parameters = self.getNodeParameters(median, hyperplaneAxis, len(points), sortedWeights)
        currNode = Node(*parameters)
        
        currNode.left = self.buildKdTree(leftPoints, nxtHyperplaneAxis) if len(leftPoints) > 0 else []
        currNode.right = self.buildKdTree(rightPoints, nxtHyperplaneAxis) if len(rightPoints) > 0 else []
        return currNode
    
    @classmethod
    def preorderTraversal(self, root):
        res, stack = [], [root]
        while stack:
            node = stack.pop()
            if node:
                if node.weight:
                    res.insert(0, [node.val])
                else:
                    res.insert(0, [node.val])
                stack.append(node.left)
                stack.append(node.right)
        return res
    
    @classmethod
    def dfs(self, root):
        res, stack = {}, [root]
        while stack:
            for i in range(len(stack)):
                node = stack.pop(0)
                if node:
                    stack.append(node.left)
                    stack.append(node.right)
                    childNodes = [node.left, node.right]
                    parentKey = [
                            node.val, 
                            node.axis,
                            node.count,
                            node.weight["weight"] if node.weight else 0,
                            node.weight["minWeight"] if node.weight else 0,
                            node.weight["maxWeight"] if node.weight else 0
                                ]
                    res[str(parentKey)] = []
                    for child in childNodes:
                        if child:
                            res[str(parentKey)].append(str([
                                child.val,
                                child.axis,
                                child.count,
                                child.weight["weight"] if child.weight else 0,
                                child.weight["minWeight"] if child.weight else 0,
                                child.weight["maxWeight"] if child.weight else 0
                            ]))
        return res

    @classmethod
    def nnKDTree(self, queryPoint, root, threshold, noOfPoints):
        listOfNeighbors = []
        return self.nnKDTreeRec(queryPoint, root, threshold, noOfPoints, listOfNeighbors)

    @classmethod
    def getDistacne(self, p1, p2, metric="eucledian"):
        if metric == "eucledian":
            retValue = (p1[0] - p2[0]) ^ 2 + (p1[1] - p2[1]) ^ 2
        return retValue

    @classmethod
    def nnKDTreeRec(self, queryPoint, root, threshold, noOfPoints, listOfNeighbors):
        if not root:
            return listOfNeighbors
        else:
            if self.getDistacne(root.val, queryPoint) <= threshold and len(listOfNeighbors) < noOfPoints:
                listOfNeighbors.append(root.val)
            if root.left == None and root.right == None:
                return listOfNeighbors
            else:
                T1, T2 = None, None
                query = queryPoint[0] if root.axis == 0 else queryPoint[1]
                currRoot = root.val[0] if root.axis == 0 else root.val[1]

                if query < root.val[0] if root.axis == 0 else root.val[1]:
                    T1 = root.left
                    T2 = root.right
                else:
                    T1 = root.right
                    T2 = root.left
                leftList = self.nnKDTreeRec(queryPoint, T1, threshold, noOfPoints, listOfNeighbors)
                if len(leftList) < noOfPoints and self.getDistacne(root.val, queryPoint) <= threshold:
                    rightList = self.nnKDTreeRec(queryPoint, root.right, threshold, noOfPoints, listOfNeighbors)
                else:
                    rightList = self.nnKDTreeRec(queryPoint, root.right, threshold, noOfPoints, listOfNeighbors)
        return listOfNeighbors

    @classmethod
    def checkRight(self, node : Node, bottom_left : list, top_right : list) -> bool:
        if (node.val[0] > bottom_left[0]) and (node.val[0] < top_right[0]) and (node.val[1] > bottom_left[1]) and (node.val[1] < top_right[1]):
            return True
        else:
            return False

    @classmethod
    def checkLeft(self, node : Node, top_left : list, bottom_right : list) -> bool:
        if (node.val[0] > bottom_right[0]) and (node.val[0] < top_left[0]) and (node.val[1] > top_left[1]) and (node.val[1] < bottom_right[1]):
            return True
        else:
            return False
    
    @classmethod
    def isLeaf(self, node : Node) -> bool:
        if node==None:
            return False
        if node.left==None and node.right==None:
            return True
        return False

    @classmethod
    def ToNode(self, node : list) -> Node:
        N = Node(node)
        return N

    @classmethod
    def CountQueryPoints(self, node : Node, p1 : list, p2 : list) ->int:

        NoOfPoints = 0
        if p1[0]==p2[0]:
            print('Collinear points')
            return
        else:
            slope = (p2[1] - p1[1])/(p2[0] - p1[0])

            if slope == 0:
                print('Collinear points')
                return

            else:
                #RIGHT DIAGONAL
                if isLeaf(node) and slope > 0:
                    if checkRight(node, p1, p2):
                        NoOfPoints += 1

                #LEFT DIAGONAL
                elif isLeaf(node) and slope < 0:
                    if checkLeft(node, p1, p2):
                        NoOfPoints += 1

                else:
                    #RIGHT DIAGONAL
                    if slope > 0:
                        NoOfPoints += int(checkRight(node,p1,p2)==True)

                    #LEFT DIAGONAL    
                    if slope < 0:
                        NoOfPoints += int(checkLeft(node,p1,p2)==True)

                    if type(node.left) == list: 
                        Nl = Node(node.left)
                    else: 
                        Nl = node.left
                    if type(node.right) == list: 
                        Nr = Node(node.right)
                    else: 
                        Nr = node.right
                    NoOfPoints += CountQueryPoints(Nl, p1, p2)
                    NoOfPoints += CountQueryPoints(Nr, p1, p2)

        return NoOfPoints

    @classmethod
    def Max(self, root):
        Max, stack = [], []
        cur = root
        while cur or stack:
            while cur:
                stack.append(cur)
                Max.append(cur.weight)
                cur = cur.left
            cur = stack.pop()
            cur = cur.right
            node = stack.pop()
        return max(Max)

    @classmethod
    def Min(self, root):
        Max, stack = [], []
        cur = root
        while cur or stack:
            while cur:
                stack.append(cur)
                Max.append(cur.weight)
                cur = cur.left
            cur = stack.pop()
            cur = cur.right
            node = stack.pop()
        return min(Max)
    
    @classmethod
    def visualizeGraph(self, treeList):
        dot = Digraph(comment='Tree')
        for node in treeList:
            dot.node(node)

        for node, edges in treeList.items():
            for edge in edges:
                dot.edge(node, edge)

        dot.render('tree', view=True)