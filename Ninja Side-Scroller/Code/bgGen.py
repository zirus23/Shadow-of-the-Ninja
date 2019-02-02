# BACKGROUND image generation engine

import os
import sys
import random
import pygame
import treeGen
import mainGame
import pygamegame
import mountainGen
import global_data
import inputHandler
import compute_stuff
import auto_generation
import time as globalTime

class bgGen(pygamegame.PygameGame):

    def init(self):
        self.scrollX = 0
        self.scrollY = 0
        self.scrolldx = 40
        self.tCount = 0
        self.isMousePressed = False
        self.mouseHeld = False
        self.mouseDragVisited = set() # to prevent continually rewriting memory
        self.currObject = None
        self.startCell = None
        self.endCell = None
        self.hoverCell = None
        self.gState = "load"
        self.treeX = 0
        self.levelList = []
        self.drawLevel = 15
        self.drawLevelsplash = 0
        self.mountainDrawPercent = 100
        self.autoGrow = False
        self.saveLevelName = ""
        self.showGrid = False
        self.currLayer = 0
        self.currTreeType = 0
        self.toggleUI = True
        # same seed generates same tree each time
        self.currTree = treeGen.Tree(self.width//2, int(self.height*(2/3)), seed=None) 
        self.saveSurface = False
        # each is list of tree class instances
        self.treesBG = [] # layer 1
        self.treesMG = [] # layer 2
        self.treesFG = [] # layer 3
        # each is list of mountain class instances
        # greater noise = less jaggy mountains
        tempColor = ((self.currLayer+1)*15,(self.currLayer+1)*15,(self.currLayer+1)*15)
        self.mountainRange = None
        self.mountainRangeBG = None
        self.mountainRangeMG = None
        self.mountainRangeFG = None
        
        self.levelName = ""
        self.regenBackground = True
        self.updateBG = True
        # EDITING PARAMETERS
        self.treeDensity = 10
        self.treeSpacing = 4*self.width//self.treeDensity
        self.mountainNoise = 10
        self.mountainHeight = 10
        self.mountainDrawHeight = self.mountainHeight*self.height//20

        # creating emtpy screen list
        self.screenObjList = [[0 for i in range((1280*5)//50)] 
                              for j in range(720//50)]

        # GUI object keys and positions on screen
        self.objKeys = {}
        self.objKeys['delete'] = 0
        # colliding obj keys (single digit)
        self.objKeys['floor'] = 1
        self.objKeys['wall'] = 2
        self.objKeys['spike'] = 3
        # non-colliding objs (double digit obj keys)
        self.objKeys['grass'] = 11

        # Postions on screen w.r.t 50x50 cells (no scroll)
        # self.GUIobjs = [self.currLayer, self.mountainNoise, self.treeDensity, self.mountainHeight, self.currTreeType]
        self.GUIpos = {}
        self.GUIpos['0'] = (1, 1) # curr layer
        self.GUIpos['1'] = (3, 1) # mountain noise
        self.GUIpos['2'] = (5, 1) # tree density
        self.GUIpos['3'] = (7, 1) # mountain height
        self.GUIpos['4'] = (9, 1) # curr tree type
        
        # GUI Text buttons. Each button maps to start cell and length in cells
        # of the button. Added to this as buttons are created.
        self.buttons = {}

        # All other images in a dictionary
        self.scaledImgs = {}
        self.rawImgs = {}
        
        # wall
        img = pygame.image.load("../Level images/basic wall.png")
        self.rawImgs['wall'] = img
        self.scaledImgs['wall'] = pygame.transform.scale(img, (50, 50))

        # floor
        img = pygame.image.load("../Level images/floor 1.png")
        self.rawImgs['floor'] = img
        self.scaledImgs['floor'] = pygame.transform.scale(img, (50, 50))
        
        # spike
        img = pygame.image.load("../Level images/spike.png")
        self.rawImgs['spike'] = img
        self.scaledImgs['spike'] = pygame.transform.scale(img, (50, 50))

        # scroll
        img = pygame.image.load("../Level images/scroll.png")
        self.rawImgs['scroll'] = img
        self.scaledImgs['scroll'] = pygame.transform.scale(img, (1280, 100))

        # scroll2
        img = pygame.image.load("../Level images/scroll2.png")
        self.rawImgs['scroll2'] = img
        self.scaledImgs['scroll2'] = pygame.transform.scale(img, (600, 720))

        # blank vert scroll menu
        img = pygame.image.load("../Level images/empty scroll.png")
        self.rawImgs['vertScrollMenu'] = img
        self.scaledImgs['vertScrollMenu'] = pygame.transform.scale(img, (150, 600))

        # delete
        img = pygame.image.load("../Level images/delete.png")
        self.rawImgs['delete'] = img
        self.scaledImgs['delete'] = pygame.transform.scale(img, (50, 50))

        # loading screen
        img = pygame.image.load("../loadingScreen.jpg")
        self.rawImgs['loading'] = img
        self.scaledImgs['loading'] = pygame.transform.scale(img, (1280, 720))

        # background
        img = pygame.image.load("../bg2.jpg")
        self.scaledImgs['background'] = pygame.transform.scale(img, (1280*5, 720))
        self.scaledImgs['rawBG'] = self.scaledImgs['background']
        # TRY MONOCOLOR to see if speeds up source alpha read for png images
        # img = pygame.Surface((1280*5, 720))
        # img.fill(color)
        # self.scaledImgs['background'] = img

    def mousePressed(self, x, y):
        self.mouseX, self.mouseY = x, y
        if self.gState == "map":
            self.isMousePressed = True
            # No scroll for GUI selections
            row = y//50
            col = (x + 0)//50
            # Check button presses, returns boolean
            pressedButton = self.checkButtonPress(row, col)
            # invalidate all other actions
            if pressedButton:
                self.currObject = None
                # self.startCell = None
                # self.endCell = None
                # self.hoverCell = None

            # object selection (object being the icon on the gui)
            for key in self.GUIpos:
                if (row, col) == self.GUIpos[key]:
                    print (self.treesBG, self.treesMG, self.treesFG)
                    if self.currLayer == 0:
                        self.treesBG = []
                    elif self.currLayer == 1:
                        self.treesMG = []
                    elif self.currLayer == 2:
                        self.treesFG = []
                    print (self.treesBG, self.treesMG, self.treesFG)
                    self.updateBackground()

                # else:
                #     gHeight = self.getgHeight(self.mouseX+self.scrollX)
                #     if gHeight is not None:
                #         x, y = self.mouseX + self.scrollX, 720 - gHeight
                #         self.currTree = treeGen.Tree(x, y)
                #     if self.currLayer == 0:
                    #     self.treesBG.append(self.currTree)
                    # elif self.currLayer == 1:
                    #     self.treesMG.append(self.currTree)
                    # elif self.currLayer == 2:
                    #     self.treesFG.append(self.currTree)
                #         self.updateBG = True

        elif self.gState == "load":
            row, col = y//50, x//50
            self.checkButtonPress(row, col)

    def checkButtonPress(self, row, col):
        for button in self.buttons:
            bRow, bCol = self.buttons[button][0]
            bSize = self.buttons[button][1]
            for i in range(bSize + 1):
                if (row, col) == (bRow, bCol + i):
                    if button == 'auto-complete':
                        self.genBiomes()
                    elif button == 'cancel':
                        mainGame.game.run()
                    elif button == 'save':
                        self.gState = "save"
                        self.user_input = inputHandler.TextInput()

                    elif button == 'load':
                        self.gState = "load"
                    # all other cases button is level name
                    elif self.gState == "load":
                        levelName = button
                        self.levelName = levelName
                        board = compute_stuff.readLevelFromFile(levelName, "levels")
                        self.screenObjList = board
                        self.gState = "map"

    def genBiomes(self):
        # Save current values
        prevLayer = self.currLayer
        prevHeight = self.mountainHeight
        prevNoise = self.mountainNoise
        prevDensity = self.treeDensity
        prevTreeType = self.currTreeType
        self.treesBG = []
        self.treesMG = []
        self.treesFG = []
        self.mountainRangeBG = None
        self.mountainRangeMG = None
        self.mountainRangeFG = None

        # Draw on screen by template 1 (mountains)
        def autoMountains():
            # BG Layer
            self.currLayer = 0
            self.mountainNoise = 5
            self.mountainHeight = 8
            self.genMountains()
            # MG Layer
            self.currLayer = 1
            self.mountainNoise = 10
            self.mountainHeight = 12
            self.genMountains()
            # FG Layer
            self.currLayer = 2
            self.mountainNoise = 15
            self.mountainHeight = 16
            self.currTreeType = 0
            self.treeDensity = 1
            self.genMountains()
            self.genTrees()
        
        def autoTrees():
            # BG Layer
            self.currLayer = 0
            self.mountainNoise = 5
            self.mountainHeight = 14
            self.genMountains()
            # MG Layer
            self.currLayer = 1
            self.currTreeType = 1
            self.treeDensity = 20
            self.genTrees()
            # FG Layer
            self.currLayer = 2
            self.currTreeType = 0
            self.treeDensity = 10
            self.genTrees()

        # Generate either tree biomes or mountain biomes
        random.choice([autoMountains, autoTrees])()
        # random.choice([autoMountains(), autoTrees()])
        # Reset previous values
        self.currLayer = prevLayer
        self.mountainHeight = prevHeight
        self.mountainNoise = prevNoise
        self.treeDensity = prevDensity
        self.currTreeType = prevTreeType

    def getgHeight(self):
        col = self.mouseX//50
        board = self.screenObjList
        if col > 0 and col < len(board[0]):
            for row in range(len(board)):
                if board[row][col] != 0:
                    gHeight = col*50
                    return gHeight
        return None

    def mouseReleased(self, x, y):
        self.mouseX = x
        self.mouseY = y
        self.isMousePressed = False
        if self.mouseHeld:
            self.startCell = None
            self.hoverCell = None
            self.endCell = None
            self.currObject = None
            self.mouseHeld = False
            self.mouseDragVisited = set()

    def mouseMotion(self, x, y):
        self.mouseX = x
        self.mouseY = y
        self.mouseCol = (x + self.scrollX)//50
        self.mouseRow = (y)//50

        # highlighting selection live
        if self.startCell is not None:
            self.hoverCell = (self.mouseRow, self.mouseCol)

    def mouseDrag(self, x, y):
        # if mouse is dragged then our highlight and stuff are invalidated
        if self.mouseHeld == False:
            self.startCell = None
            self.hoverCell = None
            self.endCell = None
        self.mouseHeld = True
        self.mouseCol = (x + self.scrollX)//50
        self.mouseRow = y//50

    def keyPressed(self, keyCode, modifier):
        # Map editing
        if self.gState == "map":
            # Esc to exit
            if keyCode == pygame.K_ESCAPE:
                mainGame.game.run()
            # del to del hovered object
            elif keyCode == pygame.K_DELETE:
                if self.currLayer == 0:
                    self.treesBG = []
                    self.mountainRangeBG = None
                if self.currLayer == 1:
                    self.treesMG = []
                    self.mountainRangeMG = None
                if self.currLayer == 2:
                    self.treesFG = []
                    self.mountainRangeFG = None
            elif keyCode == pygame.K_g:
                self.toggleUI = not self.toggleUI

            # SORRY IF YOU DON"T HAVE A NUMPAD :(
            # LAYER forth and back
            elif keyCode == pygame.K_2 or keyCode == pygame.K_KP2:
                if self.currLayer > 0: 
                    self.currLayer -= 1
            elif keyCode == pygame.K_8 or keyCode == pygame.K_KP8:
                if self.currLayer < 2:
                    self.currLayer += 1
            # MOUNTAIN NOISE up and down
            elif keyCode == pygame.K_9 or keyCode == pygame.K_KP9:
                if self.mountainNoise < 20:
                    self.mountainNoise += 1
                    self.genMountains() # regen each press
            elif keyCode == pygame.K_7 or keyCode == pygame.K_KP7:
                if self.mountainNoise > 1:
                    self.mountainNoise -= 1
                    self.genMountains()
            # MOUNTAIN HEIGHT up and down
            elif keyCode == pygame.K_UP or keyCode == pygame.K_3 or keyCode == pygame.K_KP3:
                if self.mountainHeight > 0:
                    self.mountainHeight -= 1
                    self.mountainDrawHeight = self.mountainHeight*self.height//20
                    self.genMountains() # regen each press
            elif keyCode == pygame.K_DOWN or keyCode == pygame.K_1 or keyCode == pygame.K_KP1:
                if self.mountainHeight < 20:
                    self.mountainHeight += 1
                    self.mountainDrawHeight = self.mountainHeight*self.height//20
                    self.genMountains()
            # TREE DENSITY up and down
            elif keyCode == pygame.K_6 or keyCode == pygame.K_KP6:
                if self.currLayer == 0:
                    self.treesBG = []
                if self.currLayer == 1:
                    self.treesMG = []                
                if self.currLayer == 2:
                    self.treesFG = []
                if self.treeDensity < 20:
                    self.treeDensity += 1
                    self.treeSpacing = self.width//self.treeDensity
                    self.genTrees() # regen each press
            elif keyCode == pygame.K_4 or keyCode == pygame.K_KP4:
                if self.currLayer == 0:
                    self.treesBG = []
                if self.currLayer == 1:
                    self.treesMG = []                
                if self.currLayer == 2:
                    self.treesFG = []
                if self.treeDensity > 0:
                    self.treeDensity -= 1
                    self.treeSpacing = self.width//self.treeDensity
                    self.genTrees()
            # TREE TYPE toggle
            elif keyCode == pygame.K_5 or keyCode == pygame.K_KP5:
                if self.currLayer == 0:
                    self.treesBG = []
                if self.currLayer == 1:
                    self.treesMG = []                
                if self.currLayer == 2:
                    self.treesFG = []
                if self.currTreeType == 1:
                    self.currTreeType = 0
                elif self.currTreeType == 0:
                    self.currTreeType = 1
   
        # Saving level
        elif self.gState == "save":
            if keyCode == pygame.K_RETURN:
                self.saveSurface = True
                levelName = self.levelName
                self.gState = "map"
            elif keyCode == pygame.K_ESCAPE:
                self.gState = "map"

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        self.tCount += 1
        # right and left arrow to scroll (scroll if held)
        if self.gState == "map":
            # drag and draw
            if self.mouseHeld:
                if self.currObject is not None:
                    row, col = self.mouseRow, self.mouseCol
                    if row < len(self.screenObjList) and col < len(self.screenObjList[0]):
                        if (row, col) not in self.mouseDragVisited:
                            self.mouseDragVisited.add((row, col))
                            currObjKey = self.objKeys[self.currObject]
                            self.screenObjList[row][col] = currObjKey

            if self.isKeyPressed(pygame.K_RIGHT):
                if self.scrollX <= 1280*4 - 20:
                    self.scrollX += self.scrolldx
                else:
                    self.scrollX = 1280*4
            elif self.isKeyPressed(pygame.K_LEFT):
                if self.scrollX >= 20:
                    self.scrollX -= self.scrolldx
                else:
                    self.scrollX = 0
        elif self.gState == "load":
            # call at short intervals
            if self.tCount % 30 == 0:
                self.levelList = os.listdir("../levels")
                
        elif self.gState == "save":
            self.user_input.update(self.input_events)

    # recursively calls itself to generate trees
    def genTrees(self):
        if self.currLayer == 0:
            self.treesBG = []
        if self.currLayer == 1:
            self.treesMG = []                
        if self.currLayer == 2:
            self.treesFG = []
        def wrappedFunc():
            range = (int(self.treeSpacing/2), int(self.treeSpacing*(3/2)))
            self.treeX += random.randint(range[0], range[1])
            if self.currLayer == 0:
                tree = treeGen.Tree(self.treeX - self.scrollX, 600, self.currTreeType)
                tree.layer = 0
                self.treesBG.append(tree)
            if self.currLayer == 1:
                tree = treeGen.Tree(self.treeX - self.scrollX, 600, self.currTreeType)
                tree.layer = 1
                self.treesMG.append(tree)
            if self.currLayer == 2:
                tree = treeGen.Tree(self.treeX - self.scrollX, 600, self.currTreeType)
                tree.layer = 2
                self.treesFG.append(tree)
            # recursive calls until board is filled
            if self.treeX < 1280*5:
                wrappedFunc()
            else:
                self.treeX = 10

    def genMountains(self):
        noise = self.mountainNoise
        startX = 0
        length = 1280*5
        foot = 720
        height = self.mountainDrawHeight
        color = ((3-self.currLayer)*15+10,
                 (3-self.currLayer)*15+10,
                 (3-self.currLayer)*15+10)
        if self.currLayer == 0:
            self.mountainRangeBG = mountainGen.MountainRange(startX, height, length, foot, noise, color)
        elif self.currLayer == 1:
            self.mountainRangeMG = mountainGen.MountainRange(startX, height, length, foot, noise, color)
        elif self.currLayer == 2:
            self.mountainRangeFG = mountainGen.MountainRange(startX, height, length, foot, noise, color)

    def redrawAll(self, screen):
        # background
        screen.blit(self.scaledImgs['background'], (0 - self.scrollX, 0))
        
        if self.tCount < 300:
            screen.fill((200,200,200))
            if self.autoGrow == False:
                self.drawLevelsplash = 0
                self.autoGrow = True
            else:
                if self.tCount%4 == 0:
                    self.drawLevelsplash += 1
                if self.drawLevelsplash >= 15:
                    self.autoGrow = False
                    self.tCount = 300
            # tree arguments
            self.currTree.drawSelf(screen, (10,10,10), self.drawLevelsplash)
            # blit arguments
            x = self.width/2 - 50
            y = self.height*(3/4)
            row = y//50
            col = x//50
            self.blitText(screen, "Loading..", row, col)
            
        else:
            # Draw GUI
            # start = globalTime.time()
            if self.gState == "map":
                # draw mountains and trees
                # note: thread together
                self.drawMountains(screen)
                self.drawTrees(screen)
                self.drawPlacedObjects(screen)
                if self.toggleUI:
                    self.drawScroll(screen)
                    self.drawICONS(screen)
                    # self.drawCurrObject(screen)

            elif self.gState == "load":
                self.drawLoadMenu(screen)

            elif self.gState == "save":
                scrollX = 0
                # draw on self.layer1
                if self.mountainRangeBG is not None:
                    self.mountainRangeBG.drawSelf(self.layer1, 0)
                for tree in self.treesBG:
                    color = (40, 40, 41)
                    tree.drawSelf(self.layer1, color, 15, scrollX)
                # draw on self.layer2
                if self.mountainRangeMG is not None:
                    self.mountainRangeMG.drawSelf(self.layer2, 0)
                for tree in self.treesMG:
                    color = (25,25,26)
                    tree.drawSelf(self.layer2, color, 15, scrollX)
                # draw on self.layer3
                if self.mountainRangeFG is not None:
                    self.mountainRangeFG.drawSelf(self.layer3, 0)
                for tree in self.treesFG:
                    color = (10,10,11)
                    tree.drawSelf(self.layer3, color, 15, scrollX)
                self.saveToFile()
                self.saveSurface = False

    def saveToFile(self):
        # board = list of tree class instances and mountain class instance
        l1 = self.layer1
        l2 = self.layer2
        l3 = self.layer3
        board = None
        if self.levelName is not None:
            levelName = self.levelName
        else:
            levelName = "Level1"
        compute_stuff.saveLevelToFile(board, levelName, "bgLevels", l1, l2, l3)
        self.gState = "map"

    def drawMountains(self, screen):
        # draw mountains
        scrollX = self.scrollX
        if self.mountainRangeBG is not None:
            self.mountainRangeBG.drawSelf(screen, scrollX)
        if self.mountainRangeMG is not None:
            self.mountainRangeMG.drawSelf(screen, scrollX)
        if self.mountainRangeFG is not None:
            self.mountainRangeFG.drawSelf(screen, scrollX)

    def drawTrees(self, screen):
        for tree in self.treesBG:
            if tree.x - self.scrollX > 0 and tree.x - self.scrollX < 1280:
                color = (40, 40, 41)
                scrollX = self.scrollX
                tree.drawSelf(screen, color, self.drawLevel, scrollX)
        for tree in self.treesMG:
            if tree.x - self.scrollX > 0 and tree.x - self.scrollX < 1280:
                color = (25, 25, 26)
                scrollX = self.scrollX
                tree.drawSelf(screen, color, self.drawLevel, scrollX)
        for tree in self.treesFG:
            if tree.x - self.scrollX > 0 and tree.x - self.scrollX < 1280:
                color = (10, 10, 11)
                scrollX = self.scrollX
                tree.drawSelf(screen, color, self.drawLevel, scrollX)

    def drawPlacedObjects(self, screen):
        # visited is set of tuples of locations already drawn
        visited = set()
        # creating functions for each object then calling as nescessary
        def drawWall(screen, x, y):
            screen.blit(self.scaledImgs['wall'], (x, y))

        def drawFloor(screen, x, y):
            screen.blit(self.scaledImgs['floor'], (x, y))
            
        def drawSpike(screen, x, y):
            screen.blit(self.scaledImgs['spike'], (x, y))
        
        for row in range(len(self.screenObjList)):
            for col in range(len(self.screenObjList[0])):
                if (row, col) not in visited:
                    curr = self.screenObjList[row][col]
                    visited.add((row, col))
                    if curr is not 0:
                        x = col*50 - self.scrollX
                        y = row*50
                        # Only need to draw the floor for bg gen
                        if curr == 1:
                            drawFloor(screen, x, y)
                        elif curr == 2:
                            drawWall(screen, x, y)
                        # elif curr == 3:
                        # drawSpike(screen, x, y)

    def drawScroll(self, screen):
        screen.blit(self.scaledImgs['scroll'], (0, 625))
        screen.blit(self.scaledImgs['vertScrollMenu'], (0, 0))

    def drawICONS(self, screen):
        # SHOWING EDITOR NUMBERS
        self.GUIobjs = [self.currLayer, self.mountainNoise, self.treeDensity, 20-self.mountainHeight, self.currTreeType]
        for item in range(len(self.GUIobjs)):
            if item != self.currObject:
                row, col = self.GUIpos[str(item)] # mapped nums to locations
                text = str(self.GUIobjs[item])
                self.blitText(screen, text, row, col)

        instructions = ["-2 Layer 8+", "-7 Noise 9+", "-4 Density 6+", "-1 Height 3+", "5 -> Tall/Short"]
        row = -1
        for item in instructions:
            row += 2
            col = 21
            self.blitText(screen, item, row, col)
        
        # Toggle instruction
        self.blitText(screen, "Press 'G' to toggle UI", row+2, col-11)    
        

        # LABELLED BUTTON LOCATIONS
        # draw autocomplete button
        row, col = 13, 18
        self.buttons['auto-complete'] = ((row, col), 7)
        # draw return to game button
        row, col = 13, 1
        self.buttons['cancel'] = ((row, col), 6)
        # draw load button
        row, col = 13, 15
        self.buttons['load'] = ((row, col), 2)
        # draw save button
        row, col = 13, 12
        self.buttons['save'] = ((row, col), 2)

    # Draws given text at row and col with surrounding rectangle
    def blitText(self, screen, text, row, col):
        x, y = col*50, row*50
        currFont = pygame.font.Font("../fonts/ScriptFont.ttf", 50)
        antialias = True
        color = (255, 255, 255)
        bg = None
        textImg = currFont.render(text, antialias, color, bg)
        textW, textH = textImg.get_rect().width, textImg.get_rect().height
        x = x + (50 - textW%50)//2
        y = y - textH//2 + 25
        screen.blit(textImg, (x, y))

    def drawCurrObject(self, screen):
        pass

    def drawLoadMenu(self, screen):
        # draw return to game button
        screen.blit(self.scaledImgs['scroll2'], (360, 0))
        i = 0
        for level in self.levelList:
            i += 1
            text = level.replace(".txt", "")
            row, col = 1 + i, 13
            self.blitLoadLevelText(screen, text, row, col)
            
    def blitLoadLevelText(self, screen, text, row, col):
        currFont = pygame.font.Font("../fonts/ScriptFont.ttf", 50)
        antialias = True
        color = (255, 255, 255)
        bg = None
        textImg = currFont.render(text, antialias, color, bg)
        textW, textH = textImg.get_rect().width, textImg.get_rect().height        
        x, y = col*50, row*50
        x = x + (50 - textW%50)//2 - textW//2
        y = y - textH//2 + 25
        textColWidth = textW//50 + 1
        self.buttons[text] = ((row, col - textColWidth//2), textColWidth) # +1 rather than 1 less
        screen.blit(textImg, (x, y))

    def drawSaveScreen(self, screen):
        pass
    
    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1280, height=720, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (150, 120, 125)
        pygame.init()
        self.input_events = None

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.layer1 = pygame.Surface((self.width*5, self.height), pygame.SRCALPHA)
        self.layer1.set_alpha(0)
        self.layer2 = pygame.Surface((self.width*5, self.height), pygame.SRCALPHA)
        self.layer2.set_alpha(0)
        self.layer3 = pygame.Surface((self.width*5, self.height), pygame.SRCALPHA)
        self.layer3.set_alpha(0)
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(50)
            self.timerFired(time)
            self.input_events = pygame.event.get()
            for event in self.input_events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))                
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    sys.exit()
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.update()

        pygame.quit()

def main():
    bg_editor = bgGen()
    bg_editor.run()

if __name__ == '__main__':
    main()