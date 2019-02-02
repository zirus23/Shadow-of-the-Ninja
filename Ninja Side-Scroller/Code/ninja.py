
import global_data
import pygame

class Ninja(object):
    def __init__(self):
        #Shortening names
        self.screenWidth = global_data.data.screenWidth
        self.screenHeight = global_data.data.screenHeight
        
        # x and y pos
        self.x = 200
        gHeight = self.screenHeight*(2/3)
        self.y = self.screenHeight*(2/3)
        self.xDir = 1
        self.width = 100
        self.height = 100
        self.state = "idle"
        # x velocity
        self.dx = 0
        # x accn
        self.dv = 15
        # Jump velocity
        self.default_jumpVel = 50
        self.jumpVel = self.default_jumpVel
        self.freeFallVel = 0
        # Frames for animation
        self.frame = 0
        # HERO Actions
        self.dash = False
        self.jump = False
        self.wallclimb = False
        self.dubJump = False
        self.dashFrame = 0
        # Run images
        self.runImages = []
        for i in range(8):
            str = "../Hero images/Running frames/run - Copy (%d).png" % (i+1)
            img = pygame.image.load(str)
            img = pygame.transform.scale(img, (100, 100))
            self.runImages.append(img)
        self.runFrameNum = len(self.runImages)

        # Idle images
        self.idleImages = []
        for i in range(1, 2):
            str = "../Hero images/Idle frames/idle %d.png" %i
            img = pygame.image.load(str)
            img = pygame.transform.scale(img, (100, 100))
            self.idleImages.append(img)
        self.idleFrameNum = len(self.idleImages)

        #Dash Images
        self.dashImg = pygame.Surface((100,100))
        self.dashImg = pygame.transform.scale(self.dashImg, (400, self.screenHeight//5))
        
        # Jump images
        self.jumpImages = {}
        path = "../Hero images/jumpUp.png"
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (100, 100))
        self.jumpImages["jumpUp"] = img
        path = "../Hero images/jumpDown.png"
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (100, 100))
        self.jumpImages["jumpDown"] = img

    def getImage(self, state, index = 0):
        self.frame += 1
        if state == "idle":
            if self.xDir == 1:
                img = self.idleImages[int(self.frame%self.idleFrameNum)]
            elif self.xDir == -1:
                img = self.idleImages[int(self.frame%self.idleFrameNum)]
                img = pygame.transform.flip(img, True, False)
        elif state == "run":
            if self.xDir == 1:
                img = self.runImages[int(index)]
            elif self.xDir == -1:
                img = self.runImages[int(index)]
                img = pygame.transform.flip(img, True, False)
        elif state == "jumping":
            if self.jumpVel > 0 or self.freeFallVel < 0:
                img = self.jumpImages["jumpUp"]
                if self.xDir == -1:
                    img = pygame.transform.flip(img, True, False)
            else:
                img = self.jumpImages["jumpDown"]
                if self.xDir == -1:
                    img = pygame.transform.flip(img, True, False)
        return img
    
    def drawDash(self, screen):
        screen.blit(self.dashImg, (self.x - 400*self.xDir, self.y))