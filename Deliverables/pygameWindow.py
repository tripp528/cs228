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

        # self.drawGestureForNumber(number)

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

    def displayFail(self):
        filename = "fail.png"

        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

    def displayAttemptCount(self,db):

        x = 0
        y = constants.pygameWindowDepth / 2

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        fontsize = 30 # TODO have these values scale with screen size
        font = pygame.font.Font('freesansbold.ttf', fontsize)
        leftMargin = 20

        #display header
        text = font.render("Digit scores:", True, (0, 0, 0), (255, 255, 255))
        y += fontsize
        self.screen.blit(text, (x + leftMargin,y))

        # display list
        digitCounts =  db.getStats(db.currentUser,attribute="score")
        for digit in digitCounts:
            text = font.render(str(digit) + ": " + str(digitCounts[digit]), \
                                True, (0, 0, 0), (255, 255, 255))
            y += fontsize
            self.screen.blit(text, (x + leftMargin,y))

    def displaySessionVsAll(self,db):

        x = 0
        y = constants.pygameWindowDepth / 2

        width = constants.pygameWindowWidth / 2
        height = constants.pygameWindowDepth / 2

        fontsize = 30 # TODO have these values scale with screen size
        font = pygame.font.Font('freesansbold.ttf', fontsize)
        leftMargin = 20

        # this session
        thisSessionScore = db.getThisSessionPercent()
        text = font.render("This Session: " + "{:.0f}".format(thisSessionScore) + "%", \
                            True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(text, (x + leftMargin,y))
        y += fontsize * 1.5
        greenWidth = (thisSessionScore) * width/100
        redWidth = (100 - thisSessionScore) * width/100
        pygame.draw.line(self.screen, (0,255,0), (x,y), (x + greenWidth,y), fontsize/4)
        pygame.draw.line(self.screen, (255,0,0), (x + greenWidth,y), (x + greenWidth + redWidth,y), fontsize/4)
        y += fontsize * .5

        #total
        totalScore = db.getAllSessionPercent(db.currentUser)
        text = font.render("All Sessions: " + "{:.0f}".format(totalScore) + "%", \
                            True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(text, (x + leftMargin,y))
        y += fontsize  * 1.5
        greenWidth = (totalScore) * width/100
        redWidth = (100 - totalScore) * width/100
        pygame.draw.line(self.screen, (0,255,0), (x,y), (x + greenWidth,y), fontsize/4)
        pygame.draw.line(self.screen, (255,0,0), (x + greenWidth,y), (x + greenWidth + redWidth,y), fontsize/4)
        y += fontsize  * .5

        self.displayLeaderBoard(db,x,y,width,fontsize,font,leftMargin)


    def displayLeaderBoard(self, db, x, y, width, fontsize, font,leftMargin):
        #display header
        text = font.render("Leader Board:", True, (0, 0, 0), (255, 255, 255))
        y += fontsize
        self.screen.blit(text, (x + leftMargin,y))

        # display list
        top3 = db.getTopUsers()
        for i in range(len(top3)):
            text = font.render(str(i+1) + ". " + top3[i][0] + ": " + "{:.0f}".format(top3[i][1]) + "%", \
                                True, (0, 0, 0), (255, 255, 255))
            y += fontsize
            self.screen.blit(text, (x + leftMargin,y))

        # your rank
        text = font.render("Your Rank: " + str(db.getYourRank()), True, (102,102,0), (255, 255, 255))
        y += fontsize
        self.screen.blit(text, (x + leftMargin,y))

    def displayWarmColdBar(self, correctSignCount, timeForSignToCount):
        x = 0
        y = constants.pygameWindowDepth * 7 / 8
        width = constants.pygameWindowWidth / 2

        fontsize = 30 # TODO have these values scale with screen size
        font = pygame.font.Font('freesansbold.ttf', fontsize)
        leftMargin = 20

        progress = float(correctSignCount) / float(timeForSignToCount) * 100
        print(progress,": ",correctSignCount, "/", timeForSignToCount)
        orangeWidth = (progress) * width/100
        blueWidth = (100 - progress) * width/100
        pygame.draw.line(self.screen, (255,140,0), (x,y), (x + orangeWidth,y), fontsize/2)
        pygame.draw.line(self.screen, (30,144,255), (x + orangeWidth,y), (x + orangeWidth + blueWidth,y), fontsize/2)
