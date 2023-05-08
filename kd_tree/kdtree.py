import statistics
import numpy as np
import sys
from graphviz import Digraph 

class Node:
    def __init__(self, val, axis=0, count = 0, weight = None, minWeight=None, maxWeight=None):
        self.right = self.left = None
        self.val = val
        self.axis = axis
        self.count = count
        self.weight = None
        if weight:
            self.weight = {
                "weight": weight,
                "minWeight": minWeight,
                "maxWeight": maxWeight
            }
class KDTree: 
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
    def buildKdTree(self, points, weights = None):
        if not weights:
            points = [[point] for point in points]
        else:
            if len(points) != len(weights):
                print("Incompatible len of points and weights")
                return
            points = [[point, weight] for point, weight in zip(points, weights)]
        return self.buildTreeWithMedian(points)
    
    @classmethod
    def buildTreeWithMedian(self, points, hyperplaneAxis = 0):
        dim = len(points[0][0])
        nxtHyperplaneAxis = (hyperplaneAxis + 1) % dim
        if len(points) == 1:
            return Node(points[0][0], hyperplaneAxis, 1, points[0][1] if len(points[0]) > 1 else 0, points[0][1] if len(points[0]) > 1 else 0, points[0][1] if len(points[0]) > 1 else 0)

        medianIndex = len(points) // 2
        sortedPoints = sorted(points, key=lambda x: x[0][hyperplaneAxis])

        median = sortedPoints[medianIndex]
        leftPoints = sortedPoints[:medianIndex]
        rightPoints = sortedPoints[medianIndex + 1:]
        sortedWeights = []

        if (len(points[0]) > 1):
            sortedWeights = sorted(points, key=lambda x: x[1])
        currNode = Node(median[0], hyperplaneAxis, len(points), median[1] if len(median) > 1 else 0, sortedWeights[0][1] if (len(points[0]) > 1) else 0, sortedWeights[-1][1] if (len(points[0]) > 1 and len(sortedWeights) > 1) else 0)
        currNode.left = self.buildTreeWithMedian(leftPoints, nxtHyperplaneAxis) if len(leftPoints) > 0 else []
        currNode.right = self.buildTreeWithMedian(rightPoints, nxtHyperplaneAxis) if len(rightPoints) > 0 else []
        return currNode
    
    @classmethod
    def visualizeGraph(self, treeList):
        dot = Digraph(comment='Tree')
        for node in treeList:
            dot.node(node)

        for node, edges in treeList.items():
            for edge in edges:
                dot.edge(node, edge)

        dot.render('tree', view=True)

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
                        Nl = ToNode(node.left)
                    else: 
                        Nl = node.left
                    if type(node.right) == list: 
                        Nr = ToNode(node.right)
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
    def nnKDTree(self, queryPoint, root, threshold, noOfPoints):
        listOfNeighbors = []
        return self.nnKDTreeRec(queryPoint, root, threshold, noOfPoints, listOfNeighbors)

    @classmethod
    def squareDistance(self, p1, p2):
        retValue = abs((p1[0] - p2[0]) ^ 2 - (p1[1] - p2[1]) ^ 2)
        print("p1: ", p1, "p2: ", p2, "print val: ", retValue)
        return retValue

    @classmethod
    def nnKDTreeRec(self, queryPoint, root, threshold, noOfPoints, listOfNeighbors):
        if not root:
            return listOfNeighbors
        else:
            if self.squareDistance(root.val, queryPoint) < threshold and len(listOfNeighbors) < noOfPoints:
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
                if len(leftList) < noOfPoints and self.squareDistance(root.val, queryPoint) < threshold:
                    rightList = self.nnKDTreeRec(queryPoint, root.right, threshold, noOfPoints, listOfNeighbors)
                else:
                    rightList = self.nnKDTreeRec(queryPoint, root.right, threshold, noOfPoints, listOfNeighbors)
        return listOfNeighbors