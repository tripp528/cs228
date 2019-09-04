import pygame
import constants

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
