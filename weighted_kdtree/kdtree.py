import statistics
import numpy as np
import sys
from graphviz import Digraph 
import heapq
import math

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
                if node.weight and node.weight["weight"]:
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
        neighborsList = []
        heapq.heapify(neighborsList)
        return self.nnKDTreeRec(queryPoint, root, threshold, noOfPoints, neighborsList)

    @classmethod
    def getDistance(self, p1, p2, metric="eucledian"):
        if metric == "eucledian":
            retValue = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        return math.sqrt(retValue)
    
    @classmethod
    def getKNeighbors(self, points, k):
        res = []
        for i in range(k):
            dist, pt = heapq.heappop(points)
            res.append(pt)
        return res
    
    @classmethod
    def nnKDTreeRec(self, queryPoint, root, threshold, noOfPoints, listOfNeighbors):
        if not root:
            return listOfNeighbors
        else:
            distance = self.getDistance(root.val, queryPoint)
            if distance <= threshold:
                # Remove the point with largest distance and insert the new point
                if len(listOfNeighbors) >= noOfPoints:
                    heapq.heappushpop(listOfNeighbors, (distance, root.val))
                else:
                    heapq.heappush(listOfNeighbors, (distance, root.val))
            
                    
            # If root is leaf, return the list
            if root.left == None and root.right == None:
                return listOfNeighbors
            else:
                
                # Choose which list to go explore first
                T1, T2 = None, None
                query = queryPoint[0] if root.axis == 0 else queryPoint[1]
                currRoot = root.val[0] if root.axis == 0 else root.val[1]
                
                if query < currRoot:
                    T1 = root.left
                    T2 = root.right
                else:
                    T1 = root.right
                    T2 = root.left
                
                self.nnKDTreeRec(queryPoint, T1, threshold, noOfPoints, listOfNeighbors)
                if distance <= threshold and (len(listOfNeighbors) < noOfPoints or listOfNeighbors[-1][0] > self.getDistance(queryPoint, T2.val)):
                    self.nnKDTreeRec(queryPoint, T2, threshold, noOfPoints, listOfNeighbors)
        return listOfNeighbors