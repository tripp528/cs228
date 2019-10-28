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

    def drawNumber(self, number):
        filename = str(number) + ".png"

        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

        self.drawGestureForNumber(number)

    def drawGestureForNumber(self, number):
        filename = str(number) + "_ASL" + ".png"

        x = constants.pygameWindowWidth / 2
        y = constants.pygameWindowDepth / 2

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

    def displaySuccess(self):
        filename = "success.png"

        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

    def displayAttemptCount(self,db):
        filename = "success.png"

        x = 0
        y = constants.pygameWindowDepth / 2

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        fontsize = 30 # TODO have these values scale with screen size
        font = pygame.font.Font('freesansbold.ttf', fontsize)
        leftMargin = 20

        #display header
        text = font.render("Digit attempt count:", True, (0, 0, 0), (255, 255, 255))
        y += fontsize
        self.screen.blit(text, (x + leftMargin,y))

        # display list
        digitCounts =  db.getDigitCounts()
        for digit in digitCounts:
            text = font.render(str(digit) + ": " + str(digitCounts[digit]), \
                                True, (0, 0, 0), (255, 255, 255))
            y += fontsize
            self.screen.blit(text, (x + leftMargin,y))
