
import ninja
import mapGen
import pygame
import mainGame
import pygamegame
import global_data
import compute_stuff
import time as globalTime

class NinjaRPG(pygamegame.PygameGame):

    def init(self):
        self.mainGame = mainGame.game
        self.map_editor = mapGen.mapGen()

        self.gHeight = self.height/20
        self.tCount = 0
        # game state
        self.gState = "splash"
        # Menu states
        self.menuStates = ['menu_playGame', 'menu_createLevel', 'menu_createBG', 'menu_leaveGame']
        self.menuState = 0

        # All other images in a dictionary
        self.scaledImages = {}
        self.rawImgs = {}
        
        # loading screen
        img = pygame.image.load("D:/Coursework/15-112 (CS)/Term Project/Ninja Side-Scroller/loadingScreen.jpg")
        self.rawImgs['loading'] = img
        self.scaledImages['loading'] = pygame.transform.scale(img, (1280, 720))

        # splash screen
        img = pygame.image.load("D:/Coursework/15-112 (CS)/Term Project/Ninja Side-Scroller/splashScreen2.png")
        self.rawImgs['splash'] = img
        self.scaledImages['splash'] = pygame.transform.scale(img, (1280, 720))

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
        
    def keyPressed(self, keyCode, modifier):
        if self.gState == "splash":
            if keyCode == pygame.K_SPACE:
                self.gState = "menu"
            elif keyCode == pygame.K_1:
                self.gState = "map gen"
                self.map_editor.run()
            elif keyCode == pygame.K_2:
                self.gState = "bg gen"

        elif self.gState == "menu":
            if keyCode == pygame.K_1:
                self.gState = "map gen"
                self.map_editor.run()
            elif keyCode == pygame.K_2:
                self.gState = "bg gen"
            elif keyCode == pygame.K_UP:
                self.menuState = (self.menuState-1)%4
            elif keyCode == pygame.K_DOWN:
                self.menuState = (self.menuState+1)%4
            elif keyCode == pygame.K_RETURN or keyCode == pygame.K_SPACE:
                if self.menuStates[self.menuState] == 'menu_playGame':
                    # CHANGE THIS
                    # So it goes to new menu with option to load or auto-gen level
                    self.gState = "play"
                    self.mainGame.run()
                elif self.menuStates[self.menuState] == 'menu_createLevel':
                    self.gState = "map gen"
                    self.map_editor.run()
                elif self.menuStates[self.menuState] == 'menu_createBG':
                    self.gState = "bg gen"
                elif self.menuStates[self.menuState] == 'menu_leaveGame':
                    pygame.quit()
                
        elif self.gState == "play":
            if keyCode == pygame.K_ESCAPE:
                self.mainGame.quit()
            
        elif self.gState == "map gen":
            if keyCode == pygame.K_ESCAPE:
                self.map_editor.quit()

    def timerFired(self, dt):
        self.tCount += 1
        if self.gState == "splash":
            if self.tCount%240 == 0:
                self.gState = "menu"

    def redrawAll(self, screen):
        brown = (186, 182, 171)
        seagreen = (143,188,143)
        green = (34,139,34)
        screen.fill(brown)
        if self.gState == "splash":
            # Background image
            img = self.scaledImages['splash']
            screen.blit(img, (0, 0))
            # BLIT IMAGE INSTEAD
            text = "Swarnim K presents..."
            self.blitText(screen, text, (self.width/5, self.height/5))
            text = "NOW LOADING..."
            self.blitText(screen, text, (self.width*(4/5), self.height*(4/5)))
            
        elif self.gState == "menu":
            img = self.scaledImages[self.menuStates[self.menuState]]
            screen.blit(img, (0, 0))

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
        currFont = pygame.font.SysFont(None, 32)
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
            
        elif self.hero.state == "jumpUp":
            img = self.hero.getImage("jumpUp")
        
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

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
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