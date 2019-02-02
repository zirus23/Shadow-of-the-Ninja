
## THIS FILE IS ONLY USED TO TEST THE TREE GENERATOR

import pygamegame
import treeGen
import pygame
import random

class DisplayTree(pygamegame.PygameGame):

    def init(self):
        self.tCount = 0
        self.layer = 0
        self.treeX = 0
        self.scrollX = 0
        self.tree = treeGen.Tree(self.treeX, self.height)
        self.treesBG = []
        self.treesMG = []
        self.treesFG = []
        self.saveSurface = False
        self.drawLevel = 0
        self.autoGrow = True
    
    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_SPACE:
            self.treeX += self.width//5
            self.tree = treeGen.Tree(self.treeX, self.height)
            self.trees.append(self.tree)
            # self.tree.drawLevel = 0
            self.autoGrow = False
        elif keyCode == pygame.K_UP:
            self.tree.drawLevel += 1
        elif keyCode == pygame.K_DOWN:
            self.tree.drawLevel -= 1
        elif keyCode == pygame.K_RETURN:
            self.autoGrow = True
        elif keyCode == pygame.K_1:
            self.layer = (self.layer + 1)%3

    def timerFired(self, time):
        self.tCount += 1

        if self.treeX > 1280*5:
            self.autoGrow = False
            self.saveSurface = True

        if self.autoGrow:
            self.treeX += random.randint(self.width//10, self.width//5)
            print (self.treeX)
            self.tree = treeGen.Tree(self.treeX, self.height - 120)
            if self.tree.layer == 0:
                self.treesFG.append(self.tree)
            elif self.tree.layer == 1:
                self.treesMG.append(self.tree)
            elif self.tree.layer == 2:
                self.treesBG.append(self.tree)

    def saveToFile(self, screen):
        pygame.image.save(screen, "../ram images/forest.png")
        print ("saved")

    def redrawAll(self, screen):
        # only draw once and save
        if self.saveSurface:
            print ("drawingBG")
            for tree in self.treesBG:
                color = (45, 45, 46)
                scrollX = 0
                tree.drawSelf(screen, color, 15, scrollX)
            print ("drawingMG")
            for tree in self.treesMG:
                color = (30, 30, 31)
                scrollX = 0
                tree.drawSelf(screen, color, 15, scrollX)
            print ("drawingFG")
            for tree in self.treesFG:
                color = (15, 15, 16)
                scrollX = 0
                tree.drawSelf(screen, color, 15, scrollX)
                        
            # # GROW ANIMATION
            # layer = self.trees[-1].layer
            # color = (80*layer, 80*layer, 80*layer)
            # self.trees[-1].drawSelf(screen, color, self.tree.drawLevel, self.scrollX)
            self.saveToFile(screen)
            pygame.quit()
    
    def __init__(self, width=1280, height=720, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()
        
    def run(self):
        clock = pygame.time.Clock()
        dispSurface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        screen = pygame.Surface((1280*5, 720), pygame.SRCALPHA)
        screen.set_alpha(0)
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(10000)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    self.rightMousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                    self.rightMouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 2):
                    self.rightMouseDrag(*(event.pos))
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
            pygame.display.update()

        pygame.quit()

testRun = DisplayTree()

testRun.run()