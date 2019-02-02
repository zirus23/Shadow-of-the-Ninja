# LEVEL GENERATION ENGINE
# OPTIMISED FOR FAST AND SWIFT LEVEL CREATION AND EDITING

import os
import sys
import pygame
import mainGame
import pygamegame
import inputHandler
import global_data
import compute_stuff
import auto_generation
import time as globalTime

class mapGen(pygamegame.PygameGame):

    def init(self):
        self.objX = 0
        self.objY = 0
        self.scrollX = 0
        self.scrollY = 0
        self.scrolldx = 20
        self.tCount = 0
        # GUI actions
        self.isMousePressed = False
        self.mouseHeld = False
        self.mouseDragVisited = set() # to prevent continually rewriting memory
        self.currObject = None
        self.startCell = None
        self.endCell = None
        self.hoverCell = None
        self.gState = "map"
        self.levelList = []
        self.saveLevelName = ""

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
        self.GUIpos = {}
        self.GUIpos['floor'] = (1, 1)
        self.GUIpos['wall'] = (3, 1)
        self.GUIpos['spike'] = (5, 1)
        self.GUIpos['delete'] = (9, 1)

        # GUI Text buttons. Each button maps to start cell and length in cells
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
        self.scaledImgs['bg1'] = pygame.transform.scale(img, (1280*5, 720))

    def mousePressed(self, x, y):
        print (self.screenObjList)
        if self.gState == "map":
            self.isMousePressed = True
            # No scroll for GUI selections
            row = y//50
            col = (x + 0)//50
            # Check button presses
            pressedButton = self.checkButtonPress(row, col)
            # invalidate all other actions
            if pressedButton:
                self.currObject = None
                self.startCell = None
                self.endCell = None
                self.hoverCell = None

            # if no object is selected, enable object selection
            if self.currObject == None:
                for key in self.GUIpos:
                    if (row, col) == self.GUIpos[key]:
                        self.currObject = key
                        print ("Selected %s at cell (%d, %d)" %(key, row, col))
            else:
                # Add key for obj onto 2d list of screen cells
                if self.startCell == None:
                    self.startCell = (self.mouseRow, self.mouseCol)
                else:
                    self.endCell = (self.mouseRow, self.mouseCol)
                    # All selections made, now place object and undo highlights
                    self.placeObject()
                    print (self.currObject, self.startCell, self.endCell)
                    self.currObject = None
                    self.startCell = None
                    self.endCell = None
                    self.hoverCell = None

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
                        self.screenObjList = [[0 for i in range((1280*5)//50)] for j in range(720//50)] # optional line
                        board = self.screenObjList
                        self.screenObjList = auto_generation.autoCompleteMap(board)
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
                        board = compute_stuff.readLevelFromFile(levelName)
                        self.screenObjList = board
                        self.gState = "map"
        
    # Place object and reset selections
    def placeObject(self):
        startRow, startCol = self.startCell
        endRow, endCol = self.endCell
        if endRow >= len(self.screenObjList) or endCol >= len(self.screenObjList):
            return
        # Assign obj key to location on 2d list of screen
        # Must assign every cell between start and end cell        
        # 4 CASES
        if startRow <= endRow and startCol <= endCol:
            for row in range(startRow, endRow+1):
                for col in range(startCol, endCol+1):
                    self.screenObjList[row][col] = self.objKeys[self.currObject]
        elif startRow <= endRow and startCol > endCol:
            for row in range(startRow, endRow+1):
                for col in range(endCol, startCol+1):
                    self.screenObjList[row][col] = self.objKeys[self.currObject]
        elif startRow > endRow and startCol <= endCol:
            for row in range(endRow, startRow+1):
                for col in range(startCol, endCol+1):
                    self.screenObjList[row][col] = self.objKeys[self.currObject]
        elif startRow > endRow and startCol > endCol:
            for row in range(endRow, startRow+1):
                for col in range(endCol, startCol+1):
                    self.screenObjList[row][col] = self.objKeys[self.currObject]

    def mouseReleased(self, x, y):
        self.isMousePressed = False
        if self.mouseHeld:
            self.startCell = None
            self.hoverCell = None
            self.endCell = None
            self.currObject = None
            self.mouseHeld = False
            self.mouseDragVisited = set()

    def mouseMotion(self, x, y):
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
            # z to deselect object
            if keyCode == pygame.K_z:
                self.currObject = None
            # del to del hovered object
            elif keyCode == pygame.K_DELETE:
                self.screenObjList[self.mouseRow][self.mouseCol] = 0
        
        # Saving level
        elif self.gState == "save":
            if keyCode == pygame.K_RETURN:
                levelName = self.user_input.get_text()
                board = self.screenObjList
                compute_stuff.saveLevelToFile(board, levelName)
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

    def redrawAll(self, screen):
        try:
            screen.blit(self.scaledImgs['bg1'], (0 - self.scrollX, 0))
        except:
            screen.fill((200, 200, 200))
        
        if self.tCount < 5:
            screen.blit(self.scaledImgs['loading'], (0, 0))
        else:
            # Draw GUI
            # start = globalTime.time()
            if self.gState == "map":
                self.drawPlacedObjects(screen)
                self.drawGRID(screen)
                self.drawGridHighlight(screen)
                self.drawScroll(screen)
                self.drawICONS(screen)
                self.drawCurrObject(screen)
            elif self.gState == "load":
                self.drawLoadMenu(screen)
            elif self.gState == "save":
                self.drawSaveScreen(screen)
            # end = globalTime.time()
            # print (1/(end - start))

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
                        # Draw each object respective to key and location
                        if curr == 1:
                            drawFloor(screen, x, y)
                        elif curr == 2:
                            drawWall(screen, x, y)
                        elif curr == 3:
                            drawSpike(screen, x, y)
        
    def drawGRID(self, screen):
        for row in range(720//50):
            for col in range((1280*5)//50):
                y1 = row*50
                x1 = col*50
                # 100*highlight modifies rgb value
                if self.currObject == None:
                    pygame.draw.line(screen, (0,0,0),
                                    (x1 - self.scrollX, y1),
                                    (x1 + 50 - self.scrollX, y1),
                                    1) # line width
                    pygame.draw.line(screen, (0,0,0),
                                    (x1 - self.scrollX, y1),
                                    (x1 - self.scrollX, y1 + 50),
                                    1)
                else:
                    pygame.draw.line(screen, (0, 0, 0),
                                    (x1 - self.scrollX, y1),
                                    (x1 + 50 - self.scrollX, y1),
                                    3) # increased width
                    pygame.draw.line(screen, (0, 0, 0),
                                    (x1 - self.scrollX, y1),
                                    (x1 - self.scrollX, y1 + 50),
                                    3)

    def drawGridHighlight(self, screen):
        if self.startCell is not None and self.hoverCell is not None:
            startRow, startCol = self.startCell
            endRow, endCol = self.hoverCell
            if startRow <= endRow and startCol <= endCol:
                startX = startCol*50 - self.scrollX
                startY = startRow*50
                endX = (endCol+1)*50 - self.scrollX
                endY = (endRow+1)*50
            if startRow <= endRow and startCol > endCol:
                startX = (startCol+1)*50 - self.scrollX
                startY = startRow*50
                endX = endCol*50 - self.scrollX
                endY = (endRow+1)*50
            if startRow > endRow and startCol <= endCol:
                startX = startCol*50 - self.scrollX
                startY = (startRow+1)*50
                endX = (endCol+1)*50 - self.scrollX
                endY = endRow*50
            if startRow > endRow and startCol > endCol:
                startX = (startCol+1)*50 - self.scrollX
                startY = (startRow+1)*50
                endX = endCol*50 - self.scrollX
                endY = endRow*50
            
            # Draw 4 line segments to highlight hover area
            pygame.draw.line(screen, (240,240,0),
                            (startX, startY),
                            (endX, startY),
                            5)
            pygame.draw.line(screen, (240,240,0),
                            (startX, startY),
                            (startX, endY),
                            5)
            pygame.draw.line(screen, (240,240,0),
                            (startX, endY),
                            (endX, endY),
                            5)
            pygame.draw.line(screen, (240,240,0),
                            (endX, startY),
                            (endX, endY),
                            5)

    def drawScroll(self, screen):
        screen.blit(self.scaledImgs['scroll'], (0, 625))
        screen.blit(self.scaledImgs['vertScrollMenu'], (0, 0))

    def drawICONS(self, screen):
        self.GUIobjs = ['floor', 'wall', 'spike', 'delete']
        for item in self.GUIobjs:
            if item != self.currObject:
                row, col = self.GUIpos[item]
                x, y = col*50, row*50
                screen.blit(self.scaledImgs[item], (x, y))

        # draw autocomplete button
        text = "AUTO-COMPLETE"
        row, col = 13, 18
        self.buttons['auto-complete'] = ((row, col), 7)
        # self.blitText(screen, text, row, col)
        # draw return to game button
        text = "BACK TO GAME"
        row, col = 13, 1
        self.buttons['cancel'] = ((row, col), 6)
        # self.blitText(screen, text, row, col)
        # draw load button
        text = "LOAD"
        row, col = 13, 15
        self.buttons['load'] = ((row, col), 2)
        # self.blitText(screen, text, row, col)
        # draw save button
        text = "SAVE"
        row, col = 13, 12
        self.buttons['save'] = ((row, col), 2)
        # self.blitText(screen, text, row, col)

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
        # highlights selected obj by making bigger
        if self.currObject is not None:
            item = self.currObject
            row, col = self.GUIpos[item]
            x, y = col*50 - 5, row*50 - 5
            img = pygame.transform.scale(self.scaledImgs[item], (60, 60))
            screen.blit(img, (x, y))

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
        text1 = "TYPE LEVEL NAME"
        text2 = "PRESS ENTER TO SAVE"
        row, col = 3, 10
        x, y = col*50, row*50
        currFont = pygame.font.Font("../fonts/ScriptFont.ttf", 50)
        antialias = True
        color = (255, 255, 255)
        bg = None
        textImg1 = currFont.render(text1, antialias, color, bg)
        textImg2 = currFont.render(text2, antialias, color, bg)
        textW1, textH1 = textImg1.get_rect().width, textImg1.get_rect().height
        textW2, textH2 = textImg2.get_rect().width, textImg2.get_rect().height
        x1 = x + (50 - textW1%50)//2
        x2 = x + (50 - textW2%50)//2 - 50
        y1 = y - textH1//2 + 25
        y2 = y1 + 400
        screen.blit(textImg1, (x1, y1))
        screen.blit(textImg2, (x2, y2))
        
        # drawing input text
        textImg = self.user_input.get_surface()
        screen.blit(textImg, (10*50, 5*50))
    
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
                # elif (event.type == pygame.MOUSEMOTION and
                #       event.buttons[0] == 2):
                #     self.rightMouseDrag(*(event.pos))
                # elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                #     self.rightMouseReleased(*(event.pos))                
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