
class Graph(object):
    def __init__(self, board):
        self.board = board
        self.width = len(board[0])
        self.height = len(board)
        self.walls = set()
        self.spikes = set()
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 1 or board[row][col] == 2:
                    self.walls.add((row,col))
                if board[row][col] == 3:
                    self.spikes.add((row,col))
                    # add layer above as well for convenience of death check
                    self.spikes.add((row-1,col))
        # adding the roof to walls
        row = 0
        for col in range(len(board[0])):
            self.walls.add((row, col))

    def cost(self, node):
        # deprioritizing spikes to avoid unless only possible solutions is through spikes, which we check for at the end
        x, y, jumpVal = node
        if (x, y) in self.spikes:
            return 200
        else:
            return 1
    
    def neighbors(self, node):
        # assuming quad-directional movement so as to not move diagonally
        # through walls or spikes. (Our jump movement is also represented in 
        # quad-directional movement form.)
        x, y, jumpVal = node
        neighborList = []
        
        # N1 - (x, y+1)
        if (x, y+1) not in self.walls and (x,y+1) not in self.spikes:
            inAir = True
            if jumpVal%2 == 0:
                if jumpVal-2 < 0:
                    neighborList.append((x, y+1, 0))
                else:
                    neighborList.append((x, y+1, jumpVal-2))
            else:
                if jumpVal-1<0:
                    neighborList.append((x, y+1, 0))
                else:
                    neighborList.append((x, y+1, jumpVal-1))
        else:
            # block under is floor
            inAir = False
            jumpVal = 0

        if jumpVal < 14:
            # N2 - (x+1, y)
            if (x+1, y) not in self.walls and (x+1,y) not in self.spikes:
                if not inAir:
                    neighborList.append((x+1, y, jumpVal))
                else:
                    neighborList.append((x+1, y, jumpVal+1))
            # N3 - (x-1, y)
            if (x-1, y) not in self.walls and (x-1,y) not in self.spikes:
                if x-1>=0:
                    if not inAir:
                        neighborList.append((x-1, y, jumpVal))
                    else:
                        neighborList.append((x-1, y, jumpVal+1))
            # N4 - (x, y-1)
            if (x, y-1) not in self.walls and (x,y-1) not in self.spikes:
                if y-1>=0:
                    if jumpVal%2 == 0:
                        neighborList.append((x, y-1, jumpVal+2))
                    else:
                        neighborList.append((x, y-1, jumpVal+1))
        return neighborList

class SimpleQueue(object):
    def __init__(self):
        self.queue = []
    
    def isEmpty(self):
        return len(self.queue) == 0
    
    def insertNode(self, item , priority):
        # doing this makes lowest priority the first element
        self.queue.insert(priority, item)
        # self.queue.insert(5000//priority, item) # this creates reverse list
        # so we can pop from end with O(1) instead of O(n)
    
    def getNextNode(self):
        # gets the highest priority item in current queue
        return self.queue.pop(0)

## Cite and use this if my queue is too slow
# """using heapq implemetation from  https://www.redblobgames.com/pathfinding/a-star/implementation.html"""
# import heapq
# 
# class PriorityQueue:
#     def __init__(self):
#         self.elements = []
#     
#     def empty(self):
#         return len(self.elements) == 0
#     
#     def insertNode(self, item, priority):
#         heapq.heappush(self.elements, (priority, item))
#     
#     def get(self):
#         return heapq.heappop(self.elements)[1]
##


# NOTE: Although I'm calling this an A* check (which is a combination of 
# dijkstra's algorithm and breadth first search), this isn't exactly A* since I had 
# to factor in the JUMP ability and death by spikes, so this finds the shortest 
# safe way to clear the level. If no such path exists, then a new level is 
# generated and checked. This process is repeated until a solvable level is 
# created.

# Like a*, this is a unique combination that uses logic from both breadth first 
# search, best first search and dijkstra's. This took me 15+ hours of reasearch and 
# almost 10 hours of coding and debugging to implement.

def aStarSearch(graph, start, goal):
    print (start, goal)
    print ("A* algorithm initiated")
    maxJumpValue = 14 # edit based on adaptation article
    # open list is the list of cells currently being considered to be part of
    # the final path
    openList = SimpleQueue()
    # start has priority of 0 and jumpVal of 0
    openList.insertNode((start[0], start[1], 0), 0)
    # maps each node to the one visited before it. Helps backtrack path.
    prevOfNode = {}
    prevOfNode[start] = None
    # maps each visited node to the cost of getting there from start
    # also helps keep track of which nodes have been visited
    pathScore = {}
    pathScore[(start[0], start[1])] = 0
    
    while not openList.isEmpty():

        currNode = openList.getNextNode()
        currX, currY, currJumpVal = currNode

        if (currX, currY) == goal:
            return tracePath(prevOfNode, (start[0],start[1],0),
                                          (goal[0], goal[1], currJumpVal), graph)
            
        for newNode in graph.neighbors(currNode):
            newX, newY, newJumpVal = newNode
            newCost = pathScore[(currX, currY)] + graph.cost(currNode)
            
            if (newX, newY) not in pathScore or newCost < pathScore[(newX, newY)]:               
                pathScore[(newX, newY)] = newCost
                # f(node) = g(node) + h(node) where f is the path score,
                # g is the cost to reach node, and h is the expected cost of
                # reaching the goal from this node.
                # called priority for ease of logic in SimpleQueue class
                priority = newCost + heuristic(goal, (newX, newY))
                openList.insertNode(newNode, priority)
                prevOfNode[newNode] = currNode

    # if no path was found
    if goal not in pathScore:
        return None
    else:
        return tracePath(prevOfNode, start, goal, graph)
    
def tracePath(prevOfNode, start, goal, graph):
    # if spike in path, return None. else backtrack through and return the path
    curr = goal
    path = []
    while curr != start:
        path.append(curr)
        prev = prevOfNode[curr]
        curr = prev
        if curr in graph.spikes:
            return None
    path.reverse()
    print ("Succesfully found path:\n", path)
    return path
    
# I did this first with an euclidean heuristic and then a manhattan heuristic,
# but both proved to be too slow so I came up with my own heuristic which is
# much much faster but only works with side-scrollers like this one.
# This heuristic takes advantage of the knowledge that wherever we are on the
# level, the goal WILL be to our right. This fact prevents over-estimation of 
# heuristic and keeps our heuristic admissible.

def heuristic(goal, node):
    goalCol = goal[1]
    nodeCol = node[1]
    return abs(goalCol - nodeCol)
