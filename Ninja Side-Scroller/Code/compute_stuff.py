
import random
import pygame

# take list of tuples as input, being item and weight
# assumed that total of all weights is 100
def weightedRandom(*args):
    numItems = len(args)
    sum = 0
    assorted = []
    for item in args:
        sum += item[1]
        assorted.append((item[0], sum))
    
    choice = random.randint(1, 100)
    for i in range(len(assorted)):
        if sum > assorted[i][1] and sum <= assorted[i+1][1]:
            return assorted[i+1][0]

def saveLevelToFile(board, levelName, folder = "levels", l1 = None, l2 = None, l3 = None):
    if folder == "levels":
        file = open("../%s/%s.txt" % (folder, levelName), "w")
        text = ""
        for row in board:
            for item in row:
                text += "."
                text += str(item)
            text += "\n"
        file.write(text)
        file.close
    elif folder == "bgLevels":
        # 3 layers saved seperately as images
        pygame.image.save(l1, "../bgLevels/%s_layer1.png" % levelName)
        pygame.image.save(l2, "../bgLevels/%s_layer2.png" % levelName)
        pygame.image.save(l3, "../bgLevels/%s_layer3.png" % levelName)
        # also board is list of tree and mountain classes
        # save each tree and mountain nodeList to file and re-initiate new ones
        # with these nodes overwriting their own

# returns level as 2d list
def readLevelFromFile(levelName, folder = "levels"):
    path = "../%s/%s.txt" % (folder, levelName)
    file = open(path, "r")
    text = file.read()
    board = []
    for row in text.split("\n"):
        curr = []
        for item in row.split("."):
            if item != "":
                curr.append(int(item))
        if curr != []:
            board.append(curr)
    return board