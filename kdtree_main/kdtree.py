import statistics
import numpy as np
import sys
from graphviz import Digraph 

class Node:
    def __init__(self, val, axis=0, count = 0, weight = None, minWeight=None, maxWeight=None, mini=None, maxi=None):
        self.right = self.left = None
        self.val = val
        self.axis = axis
        self.count = count
        self.weight = None
        if weight:
            self.weight = {
                "weight": weight,
                "minWeight": minWeight,
                "maxWeight": maxWeight,
                "minnode" : mini,
                "maxnode" : maxi
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
    def addWeight(self, points, sortedWeights, median):
        w = median[1] if len(median) > 1 else 0

        if len(points) > 1:
            minw = sortedWeights[0][1]
            nodemin = sortedWeights[0][0]
            maxw = sortedWeights[-1][1]
            nodemax = sortedWeights[-1][0]
        else:
            minw = None
            nodemin = None
            maxw = None
            nodemax = None

        return w, minw, maxw, nodemin, nodemax
    
    @classmethod
    def buildTreeWithMedian(self, points, hyperplaneAxis=0):
        dim = len(points[0][0])
        nxtHyperplaneAxis = (hyperplaneAxis + 1) % dim

        if len(points) == 1:
            return Node(points[0][0], hyperplaneAxis, 1, points[0][1] if len(points[0]) > 1 else 0,
                        points[0][1] if len(points[0]) > 1 else 0, points[0][1] if len(points[0]) > 1 else 0,
                        points[0][0], points[0][0])

        medianIndex = len(points) // 2
        sortedPoints = sorted(points, key=lambda x: x[0][hyperplaneAxis])

        median = sortedPoints[medianIndex]
        leftPoints = sortedPoints[:medianIndex]
        rightPoints = sortedPoints[medianIndex + 1:]
        sortedWeights = []

        if (len(points[0]) > 1):
            sortedWeights = sorted(points, key=lambda x: x[1])
            weight, minWeight, maxWeight, mini, maxi = self.addWeight(points, sortedWeights, median)
        currNode = Node(median[0], hyperplaneAxis, len(points), weight, minWeight, maxWeight, mini, maxi)
        currNode.left = self.buildTreeWithMedian(leftPoints, nxtHyperplaneAxis) if len(leftPoints) > 0 else []
        currNode.right = self.buildTreeWithMedian(rightPoints, nxtHyperplaneAxis) if len(rightPoints) > 0 else []

        return currNode

    @classmethod
    def checkRight(self, node, bottom_left, top_right):
        if (len(node.val) > 0) and (node.val[0] > bottom_left[0]) and (node.val[0] < top_right[0]) and (
                node.val[1] > bottom_left[1]) and (node.val[1] < top_right[1]):
            return True
        return False

    @classmethod
    def checkLeft(self, node, top_left, bottom_right):
        if (len(node.val) > 0) and (node.val[0] < bottom_right[0]) and (node.val[0] > top_left[0]) and (
                node.val[1] < top_left[1]) and (node.val[1] > bottom_right[1]):
            return True
        return False

    @classmethod
    def isLeaf(self,node):
        if node == None:
            return False
        if node.left == None and node.right == None:
            return True
        return False

    @classmethod
    def ToNode(self,node):
        N = Node(node)
        return N

    @classmethod
    def Slope(self, p1, p2):
        if p1[0] == p2[0]:
            print('Collinear points')
            return
        else:
            slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
        return slope

    @classmethod
    def Rectangle(slope, p1, p2):
        if slope == None:
            print('Collinear Points')
            return []
        if slope > 0:
            x0 = [p1[0], p2[1]]
            x1 = p2
            x2 = [p2[0], p1[1]]
            x3 = p1
        else:
            x0 = p1
            x1 = [p2[0], p1[1]]
            x2 = p2
            x3 = [p1[0], p2[1]]
        return [x0, x1, x2, x3]

    @classmethod
    def Check(self, node, c):
        if type(node) == list:
            if (c[1][0] > node[0] > c[0][0]) and (c[0][1] > node[1] > c[3][1]):
                return 1
        return 0

    @classmethod
    def MaxQuery(self, node, p1, p2, coordinates=None):
        if coordinates == None:
            slope = self.Slope(p1, p2)
            coordinates = self.Rectangle(slope, p1, p2)
        if len(coordinates) == 0 or node == None:
            return 0
        curr = node
        maxi = 0
        left = None
        right = None
        if curr != None and type(curr) != list:
            left = curr.left
            right = curr.right
        if type(left) == list:
            left = None
        if type(right) == list:
            right = None
        if curr != None and type(curr) != list and curr.weight != None:
            if self.Check(curr.weight['maxnode'], coordinates):
                maxi = curr.weight['maxWeight']
                return maxi
        if left == None and right == None:
            return
        m1 = self.MaxQuery(left, p1, p2, coordinates)
        m2 = self.MaxQuery(right, p1, p2, coordinates)
        if m1 != None and m2 != None:
            maxi = max(maxi, m1, m2)
        return maxi

    @classmethod
    def MinQuery(self, node, p1, p2, coordinates=None):
        if coordinates == None:
            slope = self.Slope(p1, p2)
            coordinates = self.Rectangle(slope, p1, p2)
        if len(coordinates) == 0 or node == None:
            return 0
        curr = node
        mini = 0
        left = None
        right = None
        if curr != None and type(curr) != list:
            left = curr.left
            right = curr.right
        if type(left) == list:
            left = None
        if type(right) == list:
            right = None
        if curr != None and type(curr) != list and curr.weight != None:
            if self.Check(curr.weight['maxnode'], coordinates):
                maxi = curr.weight['maxWeight']
                return maxi
        if left == None and right == None:
            return
        m1 = self.MinQuery(left, p1, p2, coordinates)
        m2 = self.MiQuery(right, p1, p2, coordinates)
        if m1 != None and m2 != None:
            maxi = min(maxi, m1, m2)
        return mini

    @classmethod
    def CountQueryPoints(self, node, p1, p2, slope=None, weight=None):
        NoOfPoints = 0
        if slope==None:
            slope = self.Slope(p1, p2)
        if weight == None:
            weight = 0
        if slope != None:
            # NON-LEAF NODE
            if isLeaf(node) == 0:
                # Current Node
                # RIGHT DIAGONAL
                if slope > 0 and node.weight != None:
                    NoOfPoints += int(self.checkRight(node, p1, p2)) and int(node.weight['weight'] >= weight)
                # LEFT DIAGONAL
                elif slope < 0 and node.weight != None:
                    NoOfPoints += int(self.checkLeft(node, p1, p2)) and int(node.weight['weight'] >= weight)
                # Next Node
                Nl = self.ToNode(node.left) if type(node.left) == list else node.left
                Nr = self.ToNode(node.right) if type(node.right) == list else node.right
                NoOfPoints += self.CountQueryPoints(Nl, p1, p2, slope, weight)
                NoOfPoints += self.CountQueryPoints(Nr, p1, p2, slope, weight)
            else:
                # LEAF NODE
                # RIGHT DIAGONAL
                if slope > 0 and self.checkRight(node, p1, p2) and node.weight != None and node.weight['weight'] >= weight:
                    NoOfPoints += 1
                # LEFT DIAGONAL
                if slope < 0 and self.checkLeft(node, p1, p2) and node.weight != None and node.weight['weight'] >= weight:
                    NoOfPoints += 1
        return NoOfPoints

    @classmethod
    def Point(root, p1, p2, slope):
        if slope != None:
            res, stack = [], [root]
            while stack:
                node = stack.pop()
                if type(node) == list and node != None:
                    node = self.ToNode(node)
                if node != None:
                    print(node.val)
                    if slope > 0 and self.checkRight(node, p1, p2):
                        res.insert(0, node.val)
                    elif slope < 0 and self.checkLeft(node, p1, p2):
                        res.insert(0, node.val)
                    else:
                        stack.append(node.left)
                        stack.append(node.right)
        return res

    @classmethod
    def Query(node, p1, p2):
        slope = self.Slope(p1, p2)
        p = self.Point(node, p1, p2, slope)
        return p

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