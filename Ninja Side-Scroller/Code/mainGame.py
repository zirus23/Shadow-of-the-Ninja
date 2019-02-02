
# PLAY GAME -->
#       NEW GAME
#       AUTO-GEN LEVEL
#       BROWSE LEVELS
# CREATE LEVEL -->
#       RUN MAP GEN
# CREATE BACKGROUND -->
#       RUN BG GEN
# LEAVE GAME --> sys.exit()

import os
import sys
import ninja
import bgGen
import mapGen
import pygame
import pygamegame
import pathfinding
import global_data
import compute_stuff
import auto_generation
import time as globalTime

class NinjaRPG(pygamegame.PygameGame):

    def init(self, state = "splash"):
        self.hero = ninja.Ninja()
        self.map_editor = mapGen.mapGen()
        self.bgEditor = bgGen.bgGen()
        self.gHeight = self.height/20
        self.tCount = 0
        self.levelList = []
        self.currLevelName = None
        self.pause = 0
        self.gravity = 4
        self.levelState = "play" # play, victory, defeat
        # game state
        self.gState = state
        self.scrollX = 0
        self.scrollY = 0
        # creating emtpy screen list
        self.screenObjList = [[0 for i in range((1280*5)//50)] 
                              for j in range(720//50)]
        # Menu states
        self.menuStates = ['menu_playGame', 'menu_createLevel', 'menu_createBG', 'menu_leaveGame']
        self.menuState = 0
        self.playMenuStates = ['play_newGame', 'play_autoGen', 'play_loadLevel', 'play_backToMenu']

        # Music for menu
        pygame.mixer.music.load("../Music/menu.wav")
        pygame.mixer.music.play(-1)

        # All other images in a dictionary
        self.scaledImages = {}
        self.rawImgs = {}
        
        # GUI Text buttons. Each button maps to start cell and length in cells
        self.buttons = {}

        # dev variables
        self.showGrid = False
        self.showPath = False

        # wall
        img = pygame.image.load("../Level images/basic wall.png")
        self.rawImgs['wall'] = img
        self.scaledImages['wall'] = pygame.transform.scale(img, (50, 50))

        # floor
        img = pygame.image.load("../Level images/floor 1.png")
        self.rawImgs['floor'] = img
        self.scaledImages['floor'] = pygame.transform.scale(img, (50, 50))

        # spike
        img = pygame.image.load("../Level images/spike.png")
        self.rawImgs['spike'] = img
        self.scaledImages['spike'] = pygame.transform.scale(img, (50, 50))

        # delete
        img = pygame.image.load("../Level images/delete.png")
        self.rawImgs['delete'] = img
        self.scaledImages['delete'] = pygame.transform.scale(img, (50, 50))

        # loading screen
        img = pygame.image.load("../loadingScreen.jpg")
        self.rawImgs['loading'] = img
        self.scaledImages['loading'] = pygame.transform.scale(img, (1280, 720))

        # splash screen
        img = pygame.image.load("../splashScreen2.png")
        self.rawImgs['splash'] = img
        self.scaledImages['splash'] = pygame.transform.scale(img, (1280, 720))

        # scroll2
        img = pygame.image.load("../Level images/scroll2.png")
        self.rawImgs['scroll2'] = img
        self.scaledImages['scroll2'] = pygame.transform.scale(img, (600, 720))
        
        # menu (selection: play)
        img = pygame.image.load("../Level images/menu_playGame.png")
        self.rawImgs['menu_playGame'] = img
        self.scaledImages['menu_playGame'] = pygame.transform.scale(img, (1280, 720))
        
        # menu (selection: create level)
        img = pygame.image.load("../Level images/menu_createLevel.png")
        self.rawImgs['menu_createLevel'] = img
        self.scaledImages['menu_createLevel'] = pygame.transform.scale(img, (1280, 720))
        
        # menu (selection: create BG)
        img = pygame.image.load("../Level images/menu_createBG.png")
        self.rawImgs['menu_createBG'] = img
        self.scaledImages['menu_createBG'] = pygame.transform.scale(img, (1280, 720))

        # menu (selection: leave game)
        img = pygame.image.load("../Level images/menu_leaveGame.png")
        self.rawImgs['menu_leaveGame'] = img
        self.scaledImages['menu_leaveGame'] = pygame.transform.scale(img, (1280, 720))

        # play menu (selection: new game)
        img = pygame.image.load("../Level images/play_newGame.png")
        self.rawImgs['play_newGame'] = img
        self.scaledImages['play_newGame'] = pygame.transform.scale(img, (1280, 720))
        
        # play menu (selection: auto gen)
        img = pygame.image.load("../Level images/play_autoGen.png")
        self.rawImgs['play_autoGen'] = img
        self.scaledImages['play_autoGen'] = pygame.transform.scale(img, (1280, 720))
        
        # play menu (selection: load level)
        img = pygame.image.load("../Level images/play_loadLevel.png")
        self.rawImgs['play_loadLevel'] = img
        self.scaledImages['play_loadLevel'] = pygame.transform.scale(img, (1280, 720))

        # play menu (selection: back to game)
        img = pygame.image.load("../Level images/play_backToMenu.png")
        self.rawImgs['play_backToMenu'] = img
        self.scaledImages['play_backToMenu'] = pygame.transform.scale(img, (1280, 720))
        
        # victory image
        img = pygame.image.load("../Level images/victory.png")
        self.rawImgs['victory'] = img
        self.scaledImages['victory'] = pygame.transform.scale(img, (975, 675))

        # defeat image
        img = pygame.image.load("../Level images/defeat.png")
        self.rawImgs['defeat'] = img
        self.scaledImages['defeat'] = pygame.transform.scale(img, (975, 675))
        
        self.generateLevelImage()

    def generateLevelImage(self):
        # main background image
        background = pygame.image.load("../bg2.jpg")
        background = pygame.transform.scale(background, (1280*5, 720))
        
        # blit trees and mountains onto background
        try:
            bgLayer1 = pygame.image.load("../bgLevels/%s_layer1.png" % self.currLevelName)
            background.blit(bgLayer1, (0,0))
            bgLayer2 = pygame.image.load("../bgLevels/%s_layer2.png" % self.currLevelName)
            background.blit(bgLayer2, (0,0))
            bgLayer3 = pygame.image.load("../bgLevels/%s_layer3.png" % self.currLevelName)
            background.blit(bgLayer3, (0,0))
        except:
            print ("No custom BG\nLoading default...")
            bgLayer1 = pygame.image.load("../bgLevels/default_level_layer1.png")
            background.blit(bgLayer1, (0,0))
            bgLayer2 = pygame.image.load("../bgLevels/default_level_layer2.png")
            background.blit(bgLayer2, (0,0))
            bgLayer3 = pygame.image.load("../bgLevels/default_level_layer3.png")
            background.blit(bgLayer3, (0,0))        
        
        # blit level onto background (pass in background as screen)
        # Draw basic objects (change to advanced later)
        self.drawLevel(background)
        
        # finally, save the modified background
        self.scaledImages['bg'] = background
        self.rawImgs['bg'] = background

    def mousePressed(self, x, y):
        if self.gState == "load":
            self.isMousePressed = True
            # No scroll for GUI selections
            row = y//50
            col = (x + 0)//50
            # Check button presses
            self.checkButtonPress(row, col)

    def checkButtonPress(self, row, col):
        for button in self.buttons:
            bRow, bCol = self.buttons[button][0]
            bSize = self.buttons[button][1]
            for i in range(bSize + 1):
                if (row, col) == (bRow, bCol + i):
                    if self.gState == "load":
                        levelName = button
                        self.currLevelName = levelName
                        board = compute_stuff.readLevelFromFile(levelName)
                        self.screenObjList = board
                        self.generateLevelImage()
                        self.gState = "play"

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_ESCAPE:
            if self.gState == "splash":
                if keyCode == pygame.K_ESCAPE:
                    sys.exit()
            elif self.gState == "menu":
                if keyCode == pygame.K_ESCAPE:
                    sys.exit()
            elif self.gState == "play menu":
                if keyCode == pygame.K_ESCAPE:
                    self.gState = "menu"
            elif self.gState == "play":
                if keyCode == pygame.K_ESCAPE:
                    self.init("menu")

        if self.gState == "splash":
            if keyCode == pygame.K_SPACE:
                self.gState = "menu"

        elif self.gState == "menu":
            if keyCode == pygame.K_UP:
                self.menuState = (self.menuState-1)%4
            elif keyCode == pygame.K_DOWN:
                self.menuState = (self.menuState+1)%4
            elif keyCode == pygame.K_RETURN or keyCode == pygame.K_SPACE:
                if self.menuStates[self.menuState] == 'menu_playGame':
                    # CHANGE THIS
                    # So it goes to new menu with option to load or auto-gen level
                    self.gState = "play menu"
                elif self.menuStates[self.menuState] == 'menu_createLevel':
                    self.gState = "map gen"
                    self.map_editor.run()
                elif self.menuStates[self.menuState] == 'menu_createBG':
                    self.bgEditor.run()
                elif self.menuStates[self.menuState] == 'menu_leaveGame':
                    pygame.quit()

        elif self.gState == "play menu":
            if keyCode == pygame.K_UP:
                self.menuState = (self.menuState-1)%4
            elif keyCode == pygame.K_DOWN:
                self.menuState = (self.menuState+1)%4
            elif keyCode == pygame.K_RETURN or keyCode == pygame.K_SPACE:
                if self.playMenuStates[self.menuState] == 'play_newGame':
                    self.screenObjList = compute_stuff.readLevelFromFile("Level1")
                    # regen since level has changed
                    self.generateLevelImage()
                    self.gState = "play"
                elif self.playMenuStates[self.menuState] == 'play_autoGen':
                    board = self.screenObjList
                    self.screenObjList = auto_generation.autoCompleteMap(board)
                    self.generateLevelImage()
                    self.gState = "play"
                elif self.playMenuStates[self.menuState] == 'play_loadLevel':
                    self.gState = "load"
                elif self.playMenuStates[self.menuState] == 'play_backToMenu':
                    self.gState = "menu"

        elif self.gState == "play" and self.levelState == "play":
            if keyCode == pygame.K_LEFT:
                self.hero.xDir = -1
                self.hero.dx = -self.hero.dv
            elif keyCode == pygame.K_RIGHT:
                self.hero.xDir = 1
                self.hero.dx = self.hero.dv
            elif keyCode == pygame.K_LSHIFT:
                self.hero.dash = True
            elif keyCode == pygame.K_SPACE:
                if self.hero.jump == False:
                    self.hero.jumpVel = self.hero.default_jumpVel
                    self.hero.jump = True
                else:
                    if self.hero.dubJump == False:
                        self.hero.jumpVel = self.hero.default_jumpVel*(0.9)
                        self.hero.dubJump = True
            elif keyCode == pygame.K_l:
                levelName = input("\nEnter level name here:\n")
                try:
                    board = compute_stuff.readLevelFromFile(levelName)
                except:
                    board = compute_stuff.readLevelFromFile("default_level")
                self.screenObjList = board
                self.generateLevelImage()
                self.gState = "play"
            # show grid
            elif keyCode == pygame.K_g:
                self.showGrid = not self.showGrid
            # elif keyCode == pygame.K_p:
            #     self.showPath = True
        elif self.gState == "play" and self.levelState == "defeat":
                if keyCode == pygame.K_SPACE:
                    self.levelReset()
                    self.levelState = "play"
                
        elif self.gState == "map gen":
            if keyCode == pygame.K_ESCAPE:
                self.map_editor.quit()

    def keyReleased(self, keyCode, modifier):
        if self.gState == "play":
            if keyCode == pygame.K_LEFT:
                self.hero.dx = 0
            elif keyCode == pygame.K_RIGHT:
                self.hero.dx = 0
            elif keyCode == pygame.K_p:
                self.showPath = False

    def timerFired(self, dt):
        self.tCount += 1
        # All of timerfired goes inside this if
        if self.gState == "play":
            # update gHeight
            self.gHeight = self.getgHeight()
            # Move Hero
            self.checkCollisions()
            # scroll
            # herowidth = 100
            if self.hero.x > self.width//3 and self.hero.x < 1280*5-self.width//3:
                if self.hero.x - self.scrollX >= (2/3)*self.width:
                    self.scrollX = self.hero.x - (2/3)*self.width
                elif self.hero.x - self.scrollX <= (1/3)*self.width:
                    self.scrollX = self.hero.x - (1/3)*self.width
            # Gravity and jumps
            # freefall
            if self.hero.jump == False:
                # above ground
                if self.hero.y < self.height - self.gHeight:
                    self.hero.y -= self.hero.freeFallVel
                    self.hero.freeFallVel -= self.gravity
                    self.hero.state = "jumping"
                elif self.hero.y > self.height - self.gHeight:
                    self.hero.y = self.height - self.gHeight
                    self.hero.freeFallVel = 0

            # jump
            elif self.hero.jump:
                self.hero.y -= self.hero.jumpVel
                self.hero.jumpVel -= self.gravity
                if self.hero.y >= self.height - self.gHeight:
                    # Reset values for next jump
                    self.hero.jumpVel = self.hero.default_jumpVel
                    self.hero.jump = False
                    self.hero.dubJump = False
                    self.hero.y = self.height - self.gHeight

            # DASH effect
            if self.hero.dash:
                self.hero.jumpVel = 0
                self.hero.dashFrame += 1
                self.hero.x += 100*self.hero.xDir

                # CAP NUM OF ITERATIONS BASED ON PATH BLOCK (if needed)
                if self.hero.dashFrame >= 3:
                    self.hero.dash = False
                    self.hero.dashFrame = 0

        elif self.gState == "splash":
            if self.tCount%100 == 0:
                self.gState = "menu"

        elif self.gState == "load":
            # call at short intervals
            if self.tCount % 30 == 0:
                self.levelList = os.listdir("../levels")

    def checkCollisions(self):
        # set bounds
        rightBound = 1280*5 - 200
        leftBound = 100
        upperBound = 70
        lowerBound = 650
        heroRow = int(self.hero.y//50)
        heroCol = int(self.hero.x//50)

        if self.hero.y > lowerBound:
            self.hero.y = lowerBound
            # SHOULD THIS RETURN OR RESET LEVEL?
            return

        block2Above = self.screenObjList[heroRow-2][heroCol]
        block1Above = self.screenObjList[heroRow-1][heroCol]
        block2Right = self.screenObjList[heroRow][heroCol+2]
        block1Right = self.screenObjList[heroRow][heroCol+1]
        block2Left = self.screenObjList[heroRow][heroCol-2]
        block1Left = self.screenObjList[heroRow][heroCol-1]
        block1Below = self.screenObjList[heroRow+1][heroCol]

        if heroCol < (1280*5)//50 and heroCol >= 0 and \
           heroRow < 720//50 - 1 and heroRow >= 0:
            # VERT COLLISIONS
            if block2Above == 1 or block2Above == 2:
                upperBound = heroRow*50
                if block1Above == 1 or block1Above == 2:
                    upperBound = (heroRow+1)*50

            # SPIKES
            if block1Below == 3:
                self.levelState = "defeat"
                self.levelReset()

            # HORIZONTAL COLLISIONS
            if block2Right == 1 or block2Right == 2:
                rightBound = (heroCol+1)*50
                if block1Right == 1 or block1Right == 2:
                    rightBound = heroCol*50
            if block2Left == 1 or block2Left == 2:
                leftBound = heroCol*50
                if block1Left == 1 or block1Left == 2:
                    leftBound = (heroCol+1)*50
        if self.hero.x >= 100 and self.hero.x <= 1280*5 - 100:
            newX = self.hero.x + self.hero.dx
            if newX <= rightBound and newX >= leftBound:
                self.hero.x += self.hero.dx
            else:
                self.hero.dash = False
            # animation state
            if self.hero.dx is not 0:
                self.hero.state = "running"
            else:
                self.hero.state = "idle"

        if self.hero.x < leftBound:
            self.hero.x = leftBound
            self.hero.state = "idle"
        if self.hero.x > rightBound:
            self.hero.x = rightBound
            self.hero.state = "idle"

        if self.hero.y < upperBound:
            self.hero.y = upperBound
        if self.hero.y > lowerBound:
            self.hero.y = lowerBound

        # jump state overrides all besides dash
        if self.hero.jump:
            self.hero.state = "jumping"
        if self.hero.dash:
            self.hero.state = "running"
            
        # Victory
        if self.hero.x > 1280*5 - 400:
            self.levelState = "victory"
            self.levelReset()

    def levelReset(self):
        self.hero.x = 200
        self.hero.y = 500
        self.hero.dx = 0
        self.hero.dv = 15
        self.hero.xDir = 1
        self.hero.jumpVel = 0 # ?? 0 or default
        self.hero.freeFallVel = 0
        self.scrollX = 0
        self.hero.state = "idle"
        self.hero.jump = False
        self.hero.dash = False  # WHY NOT RESET????

    def getgHeight(self):
        heroCol = self.hero.x//50
        heroRow = self.hero.y//50
        board = self.screenObjList
        if heroCol < len(board[0]) and heroRow < len(board):    
            for row in range(int(heroRow), len(board)):
                if board[row][heroCol] != 0:
                    heightBlock = (row, heroCol)
                    gHeight = (len(board) - row + 1)*50
                    buffer = 7 # feet-to-image buffer
                    return gHeight + buffer
        # if for some reason above doesn't work
        return 50 + 7

    def redrawAll(self, screen):
        brown = (186, 182, 171)
        seagreen = (143,188,143)
        green = (34,139,34)
        screen.fill(brown)
        # try:
        if self.gState == "play":
            # Background image
            currBG = self.scaledImages['bg']
            screen.blit(currBG, (0 - self.scrollX, 0))

            # Draw ninja
            self.drawNinja(screen)
            
            if self.showGrid:
                self.drawGrid(screen)
                
            if self.showPath:
                self.drawPath(screen)
            
            # OVERLAY if WIN/LOSE STATE
            if self.levelState == "victory":
                # blit victory image
                img = self.scaledImages['victory']
                screen.blit(img, (150, 25))
            elif self.levelState == "defeat":
                img = self.scaledImages['defeat']
                # blit defeat image
                screen.blit(img, (150,25))

        elif self.gState == "splash":
            # Background image
            img = self.scaledImages['splash']
            screen.blit(img, (0, 0))
            
        elif self.gState == "menu":
            img = self.scaledImages[self.menuStates[self.menuState]]
            screen.blit(img, (0, 0))
            
        elif self.gState == "play menu":
            img = self.scaledImages[self.playMenuStates[self.menuState]]
            screen.blit(img, (0, 0))
        
        elif self.gState == "load":
            self.drawLoadMenu(screen)

        # Draw fps
        if self.tCount % 30 == 0:
            self.fps = global_data.data.fps
        self.blitText(screen, str(self.fps), (20, 20))

        # except:
        #     self.drawLoadingScreen(screen)

        #LAST LINE
        pygame.display.flip()

    def drawLevel(self, screen):
        # visited is set of tuples of locations already drawn
        visited = set()
        # creating functions for each object then calling as nescessary
        def drawWall(screen, x, y):
            screen.blit(self.scaledImages['wall'], (x, y))

        def drawFloor(screen, x, y):
            screen.blit(self.scaledImages['floor'], (x, y))
            
        def drawSpike(screen, x, y):
            screen.blit(self.scaledImages['spike'], (x, y))
        
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

    # create image with text and then blit image to screen
    def blitText(self, screen, text, xy):
        x, y = xy
        currFont = pygame.font.Font("../fonts/ScriptFont.ttf", 32)
        antialias = True
        color = (255, 255, 255)
        bg = None
        textImg = currFont.render(text, antialias, color, bg)
        textW, textH = textImg.get_rect().width, textImg.get_rect().height 
        screen.blit(textImg, (x - textW/2, y - textH/2))

    # Draws ninja    
    def drawNinja(self, screen):
        
        # Idle animation
        if self.hero.state == "idle":
            # Auto animated so doesn't need frame input
            img = self.hero.getImage("idle")

        # Run animation
        elif self.hero.state == "running":
            # Animation posed is a function of x position
            frame = ((self.tCount//3))%8
            img = self.hero.getImage("run", frame)
            
        elif self.hero.state == "jumping":
            img = self.hero.getImage("jumping")
        
        #Blit the selected image
        # hero.x and y are middle of hero
        heroDisplayX = (self.hero.x - self.hero.width/2) - self.scrollX
        heroDisplayY = (self.hero.y - self.hero.height/2) - self.scrollY
        screen.blit(img, (heroDisplayX, heroDisplayY))

        # highlight ninja hitbox
        if self.showGrid:
            x = self.hero.x - self.scrollX
            y = self.hero.y
            w, h = 100, 100
            pygame.draw.rect(screen, (255,255,255),
                            pygame.Rect(x - w//2, y - h//2, w, h), 2)

    def drawLoadingScreen(self, screen):
        screen.blit(self.loadingImg, (0,0))

    def drawGrid(self, screen):
        for row in range(720//50):
            for col in range((1280*5)//50):
                y1 = row*50
                x1 = col*50
                # 100*highlight modifies rgb value
                pygame.draw.line(screen, (0,0,0),
                                (x1 - self.scrollX, y1),
                                (x1 + 50 - self.scrollX, y1),
                                1) # line width
                pygame.draw.line(screen, (0,0,0),
                                (x1 - self.scrollX, y1),
                                (x1 - self.scrollX, y1 + 50),
                                1)
    
    def drawPath(self, screen):
        path = global_data.data.solvedPath
        for i in range(len(path)-1):
            pygame.draw.line(screen, (255,255,255),
                             (25 + path[i][1]*50 - self.scrollX,
                             25 + path[i][0]*50),
                             (25 + path[i+1][1]*50 - self.scrollX,
                             25 + path[i+1][0]*50),
                             5)
                             
    def findPath(self):
        # updates shortest path to level finish but currently only works without
        # game physics taken into account
        # a* however does take game physics into account
        board = self.screenObjList
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

    def drawLoadMenu(self, screen):
        # draw return to game button
        screen.blit(self.scaledImages['scroll2'], (360, 0))
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

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1280, height=720, fps=50, title="112 Pygame Game"):        
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

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
            # <fps counter>
            allFPS = []
            startTime = globalTime.time()
            # </fps counter>
            time = clock.tick(50)
            self.timerFired(time)
            for event in pygame.event.get():
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
                    playing = False

            self.redrawAll(screen)
            # <fps counter>
            endTime = globalTime.time()
            totalTime = endTime - startTime
            startTime = endTime
            # allFPS.append(totalTime)
            # # avg of last 10 frames
            # if len(allFPS) > 5:
            #     allFPS = allFPS[-5:]
            # avgTimePerFrame = sum(allFPS)/len(allFPS)
            global_data.data.fps = int(1/(totalTime))
        # </fps counter>
        pygame.quit()
    
game = NinjaRPG()

def main():
    game.run()
    
if __name__ == '__main__':
    main()