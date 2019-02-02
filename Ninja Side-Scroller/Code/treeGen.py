
# generates 2d list. Its a list of all "depths" of recursion and each with all
# nodes at that depth

import pygame
import math
import random
import time as global_time

class Tree(object):
    def __init__(self, x, y, type = 0, seed = None):
        # x and y are the position of its bottom center
        self.x = x
        self.y = y
        self.drawLevel = 1
        if seed is not None:
            random.seed(seed)
        # self.nodes stores tuples of (parentNodeXY, xnode, ynode, recurseLevel)        
        self.nodes = [self.generateBushyTop(), self.generateTallTree()][type]
        # self.generateTallTree()])
        self.layer = random.randint(0,2)

    def generateBushyTop(self):
        nodes = {}
        maxLevel = 6
        for i in range(maxLevel+1):
            nodes[str(i)] = []
        # dt is deviation in angle from center for current node
        dt = 0
        # currNode are parent nodes at each level
        currNode = self.x, self.y
        r = random.randint(100, 200)
        def genNode(currNode, currLevel, dt, r):
            if currLevel > maxLevel:
                return
            # create new nodes from curr node
            newNodes = []
            x1, y1 = currNode
            r *= 0.7
            # as many new nodes as current level (each new node sprouts more)
            for i in range(currLevel):
                # i plays no effect here besides to call this multiple times
                # random angle (biased by dt)
                t = dt + random.choice([-1,1])*random.randint(3, 5)*2**currLevel
                dt = t
                t = math.radians(t)
                # x is sin component since t is angle with vertical
                x2 = x1 + int(r*math.sin(t)) # int() gives slight bias but
                y2 = y1 - int(r*math.cos(t)) # saves ton of memory
                newNodes.append((x2, y2, dt))
                # do we modify main nodelist here?
                nodes[str(currLevel)].append(((x1,y1), x2, y2, currLevel))
            # call recursively for each with increment in level until max level
            for newNode in newNodes:
                x = newNode[0]
                y = newNode[1]
                dt = newNode[2]
                genNode((x,y), currLevel+1, dt, r)
        genNode(currNode, 1, dt, r)
        return nodes

    def generateTallTree(self):
        nodes = {}
        maxLevel = 6
        for i in range(maxLevel+1):
            nodes[str(i)] = []
        # dt is deviation in angle from center for current node
        dt = 0
        # currNode are parent nodes at each level
        currNode = self.x, self.y
        r = random.randint(170, 220)
        def genNode(currNode, currLevel, dt, r):
            if currLevel > maxLevel:
                return
            # create new nodes from curr node
            newNodes = []
            x1, y1 = currNode
            r *= 0.8
            numNodes = random.randint(1, currLevel*2) # how many branches?
            # as many new nodes as current level (each new node sprouts more)
            for i in range(numNodes):
                # i plays no effect here besides to call this multiple times
                # random angle (biased by dt)
                t = dt + random.choice([-1,1])*random.randint(2, 4)*1.6**currLevel
                dt = t
                t = math.radians(t)
                # x is sin component since t is angle with vertical
                x2 = x1 + int(r*math.sin(t)) # int() gives slight bias but
                y2 = y1 - int(r*math.cos(t)) # saves ton of memory
                newNodes.append((x2, y2, dt))
                # do we modify main nodelist here?
                nodes[str(currLevel)].append(((x1,y1), x2, y2))
            # call recursively for each with increment in level until max level
            for newNode in newNodes:
                x = newNode[0]
                y = newNode[1]
                dt = newNode[2]
                genNode((x,y), currLevel+1, dt, r)
        genNode(currNode, 1, dt, r)
        return nodes

    def drawSelf(self, screen, color, drawLevel, scrollX=0):
        # for node in self.nodes:
            # draw line from parent node to node for each node
        if drawLevel > 2*len(self.nodes):
            drawLevel = 2*len(self.nodes)
        for i in range(drawLevel):
            for node in self.nodes[str(i//2)]:
                parent = node[0]
                child = (node[1], node[2])
                nodeLevel = i//2
                width = int(30*0.75**nodeLevel)
                if i%2 == 0:
                    mid = ((parent[0]+child[0])//2, (parent[1]+child[1])//2)
                    x1, y1 = parent[0], parent[1]
                    x2, y2 = mid[0], mid[1]
                    pygame.draw.line(screen, color, (x1 - scrollX, y1), (x2 - scrollX, y2), width)
                else:
                    x1, y1 = parent[0], parent[1]
                    x2, y2 = child[0], child[1]
                    pygame.draw.line(screen, color, (x1 - scrollX, y1), (x2 - scrollX, y2), width)
