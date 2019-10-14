import pygame
import constants
import os

class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth,constants.pygameWindowDepth))

    def Prepare(self):
        self.screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def Reveal(self):
        pygame.display.update()

    def Draw_Black_Circle(self,x,y):
        pygame.draw.circle(self.screen,(0,0,0),(x,y),15)

    def Draw_Black_Line(self,base_xVal,base_yVal,tip_xVal,tip_yVal, thickness):
        # print(base_xVal,base_yVal,tip_xVal,tip_yVal)
        pygame.draw.line(self.screen, (0,0,0), (base_xVal,base_yVal), (tip_xVal,tip_yVal), thickness)

    def drawHelpfulAnimation(self):
        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        img = pygame.image.load(os.path.join('img', 'wifi.jpeg'))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

    def drawCenterHand(self, direction):
        filename = direction + ".png"

        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))
