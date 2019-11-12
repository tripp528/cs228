import pygame
import constants
import os

class HUNT_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth,constants.pygameWindowDepth))
        self.duckPosition = 1

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
        # determine where on screen to draw:
        if (constants.handQuadrant == 1):
            base_xVal = base_xVal / 2
            base_yVal = base_yVal / 2
            tip_xVal = tip_xVal / 2
            tip_yVal = tip_yVal / 2
        elif (constants.handQuadrant == 4):
            base_xVal = (base_xVal / 2) + constants.pygameWindowWidth / 2
            base_yVal =(base_yVal / 2) + constants.sceneHeight
            tip_xVal = (tip_xVal / 2) + constants.pygameWindowWidth / 2
            tip_yVal = (tip_yVal / 2) + constants.sceneHeight

        pygame.draw.line(self.screen, (0,0,0), (base_xVal,base_yVal), (tip_xVal,tip_yVal), thickness)

    def drawHelpfulAnimation(self):
        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.sceneHeight

        img = pygame.image.load(os.path.join('img', 'wifi.jpeg'))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

    def drawCenterHand(self, direction):
        filename = direction + ".png"

        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.sceneHeight

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

    def drawDuck(self, number,signDisplayTime,maxSignDisplayTime, dead=False):
        filename = str(number) + ".png"
        if dead==True:
            filename = "dead.png" 

        x = (constants.pygameWindowWidth / constants.numberOfRocks) * self.duckPosition
        percentTimePassed = float(signDisplayTime)/float(maxSignDisplayTime)
        y = int(constants.rockSize * percentTimePassed) + constants.rockSize/constants.numberOfRocks  # = percentage of time used / how much space

        width = constants.duckWidth
        height = constants.duckHeight

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

        # self.drawGestureForNumber(number)

    def drawRocks(self):
        filename = "rock.png"

        for i in range(constants.numberOfRocks):
            x = (constants.pygameWindowWidth / constants.numberOfRocks) * i
            y = constants.rockSize

            width = constants.rockSize
            height = constants.rockSize

            img = pygame.image.load(os.path.join('img', filename))
            img = pygame.transform.scale(img, (width, height))

            self.screen.blit(img, (x,y))

    def drawScene(self):
        filename = "scene.png"

        x = 0
        y = 0

        width = constants.pygameWindowWidth
        height = constants.sceneHeight

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

    def displaySuccess(self):
        filename = "success.png"

        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.sceneHeight

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))

    def displayFail(self):
        filename = "fail.png"

        x = constants.pygameWindowWidth / 2
        y = 0

        width = constants.pygameWindowWidth / 2
        height = constants.sceneHeight

        img = pygame.image.load(os.path.join('img', filename))
        img = pygame.transform.scale(img, (width, height))

        self.screen.blit(img, (x,y))



    def displaySessionVsAll(self,db):

        x = 0
        y = constants.sceneHeight

        width = constants.pygameWindowWidth / 2
        height = constants.infoHeight

        font = pygame.font.Font('freesansbold.ttf', constants.fontsize)
        leftMargin = 20

        # this session
        thisSessionScore = db.getThisSessionPercent()
        text = font.render("This Session: " + "{:.0f}".format(thisSessionScore) + "%", \
                            True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(text, (x + leftMargin,y))
        y += constants.fontsize * 1.5
        greenWidth = (thisSessionScore) * width/100
        redWidth = (100 - thisSessionScore) * width/100
        pygame.draw.line(self.screen, (0,255,0), (x,y), (x + greenWidth,y), constants.fontsize/4)
        pygame.draw.line(self.screen, (255,0,0), (x + greenWidth,y), (x + greenWidth + redWidth,y), constants.fontsize/4)
        y += constants.fontsize * .5

        #total
        totalScore = db.getAllSessionPercent(db.currentUser)
        text = font.render("All Sessions: " + "{:.0f}".format(totalScore) + "%", \
                            True, (0, 0, 0), (255, 255, 255))
        self.screen.blit(text, (x + leftMargin,y))
        y += constants.fontsize  * 1.5
        greenWidth = (totalScore) * width/100
        redWidth = (100 - totalScore) * width/100
        pygame.draw.line(self.screen, (0,255,0), (x,y), (x + greenWidth,y), constants.fontsize/4)
        pygame.draw.line(self.screen, (255,0,0), (x + greenWidth,y), (x + greenWidth + redWidth,y), constants.fontsize/4)
        y += constants.fontsize  * .5

        self.displayLeaderBoard(db,x,y,width,font,leftMargin)


    def displayLeaderBoard(self, db, x, y, width, font,leftMargin):
        #display header
        text = font.render("Leader Board:", True, (0, 0, 0), (255, 255, 255))
        y += constants.fontsize
        self.screen.blit(text, (x + leftMargin,y))

        # display list
        top3 = db.getTopUsers()
        for i in range(len(top3)):
            text = font.render(str(i+1) + ". " + top3[i][0] + ": " + "{:.0f}".format(top3[i][1]) + "%", \
                                True, (0, 0, 0), (255, 255, 255))
            y += constants.fontsize
            self.screen.blit(text, (x + leftMargin,y))

        # your rank
        text = font.render("Your Rank: " + str(db.getYourRank()), True, (102,102,0), (255, 255, 255))
        y += constants.fontsize
        self.screen.blit(text, (x + leftMargin,y))

    def displayWarmColdBar(self, correctSignCount, timeForSignToCount):
        x = width = constants.pygameWindowWidth / 2
        y = constants.sceneHeight
        width = constants.pygameWindowWidth / 2

        constants.fontsize = 30 # TODO have these values scale with screen size
        font = pygame.font.Font('freesansbold.ttf', constants.fontsize)
        leftMargin = 20

        progress = float(correctSignCount) / float(timeForSignToCount) * 100
        # print(progress,": ",correctSignCount, "/", timeForSignToCount)
        orangeWidth = (progress) * width/100
        blueWidth = (100 - progress) * width/100
        pygame.draw.line(self.screen, (255,140,0), (x,y), (x + orangeWidth,y), constants.fontsize/2)
        pygame.draw.line(self.screen, (30,144,255), (x + orangeWidth,y), (x + orangeWidth + blueWidth,y), constants.fontsize/2)
