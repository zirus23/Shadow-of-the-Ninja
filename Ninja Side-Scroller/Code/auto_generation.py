
import random
import pathfinding
import global_data
import compute_stuff

# return filled board for map gen

attempts = 0

def autoCompleteMap(board):
    original = board
    # fill with base
    for col in range(len(board[0])):
        prev = board[-2][col]
        board[-2][col] = 2
        board[-1][col] = 1
    # generate uneven ground
    board = genFloor(board)
    board = genGap(board)
    board = placeSpikes(board)
    board = fillEmptyFloor(board)
    if not isLegal(board):
        attempts += 1
        # Since levels are random there is a rare chance that this takes too
        # many attempts even though the above functions are optimised
        # to be playable 90% of the time
        if attempts > 5:
            board = compute_stuff.readLevelFromFile("Level1")
            return board
        print ("Retrying auto generation")
        board = autoCompleteMap(original) # repeats until legal map is created
    return board

# SWARNIM's DETOUR of Terrain Generation (noise function that I came up with)
def genFloor(board, detour = 4, spread = 5, rFactor = 1):
    # input detour (vert height range (+- randomness factor))
    # spread is blocks per iteration (+- randomness factor)
    # choose random height in range for first few blocks (no gaps or vert blocks)
    # for next set choose same random range but centered at height of first
    # delete entire vertical cols in sets spread randomly across
    prevHeight = 0
    endBound = (1280*5)//50 - 1 #127
    # steps with spread
    for i in range(0, len(board[0]), spread): # fix step (should be step + r)
        groupSize = spread
        # + random.randint(-rFactor, rFactor)
        detourRandom = random.randint(-rFactor, rFactor)
        placementHeight = prevHeight + random.choice([1,-1])*random.randint(0, detour + detourRandom)
        # height checks
        if placementHeight > 11:
            placementHeight = 9
        elif placementHeight < 2:
            placementHeight = 2
        # set new height as prev height
        prevHeight = placementHeight
        for row in range(2, placementHeight):
            for col in range(i, i + groupSize):
                # end bound check
                if col < endBound:
                    board[len(board) - row - 1][col] = 2 # key for wall    
    return board

def genGap(board, minGaps = 2, maxGaps = 4, maxWidth = 6):
    numGaps = 0
    row = len(board) - 3
    # no gaps near start or end so +-10
    while numGaps < minGaps:
        col = random.randint(10, len(board[0]) - 10)
        numGaps += 1
        gapWidth = random.randint(3, maxWidth)
        for i in range(gapWidth):
            for r in range(len(board)):
                board[r][col+i] = 0 # none
            if gapWidth < 5:
                board[-1][col+i] = 3 # spikes
    return board

def placeSpikes(board, minClusters = 2, maxClusters = 5):
    numClusters = random.randint(minClusters, maxClusters)
    clustersPlaced = 0
    for row in range(6, len(board)):
        for col in range(10, len(board[0]) - 10):
            clusterSize = random.randint(2, 5)
            spaceAvailable = True
            for i in range(clusterSize):
                if not (board[row-1][col+i] == 0 and board[row][col+i] != 0):
                    spaceAvailable = False
            if spaceAvailable:
                clustersPlaced += 1
                if clustersPlaced > numClusters:
                    return board
                for i in range(clusterSize):
                    board[row-1][col+i] = 3 # spikes
    return board
    
def fillEmptyFloor(board):
    # places spikes in valleys
    row = -1
    for col in range(len(board[0])):
        if board[row-1][col] == 0:
            board[row][col] = 3
    return board

        
# Description of autocomplete's working
# Steps:
# 1. Generate floor terrain with ups and downs and gaps (detour noise based creation)
# 2. Generate random spikes with A* checks for playability (approximating game physics to single higher jump instead of double jump)
# 3. top off with roof and background elements like trees, and mountains

def isLegal(board):
    # starts at 4th col, with row based on gHeight
    colStart = 4
    colGoal = len(board[0])-5
    start = None
    goal = None
    for row in range(len(board)):
        if start is None:
            if board[row][colStart] != 0:
                start = (row-1, colStart) #first point of collision
        if goal is None:
            if board[row][colGoal] != 0:
                goal = (row-1, colGoal)
    
    graph = pathfinding.Graph(board)

    path = pathfinding.aStarSearch(graph, start, goal)
    
    if path is not None:
        global_data.data.solvedPath = path
        return True
    else:
        return False

def genAdvancedMap(board):
    return board
