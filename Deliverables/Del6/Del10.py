import sys
import random
import pickle
import numpy as np
import random

#local imports
sys.path.insert(0, "..")
import constants
from pygameWindow import PYGAME_WINDOW
from Dict import DataBase
sys.path.insert(0, "../..")
import Leap

# load user DataBase
db = DataBase()
db.login()

#program globals
programState = 0
timeCentered = 0
totalItems = [1,2,3,4,5,6,7,8,9,0]

if ( len(db.getActiveDigits()) > 0 ):
    scaffoldedItems = db.getActiveDigits()
else :
    scaffoldedItems = {1,}

numberGoal = random.sample(scaffoldedItems,1)[0]
signDisplayTime = 0
maxSignDisplayTime = 30
correctSignCount = 0
successDisplayTime = 0
failDisplayTime = 0
timeForSignToCount = maxSignDisplayTime/3


#drawing globals
pygameWindow = PYGAME_WINDOW()
controller = Leap.Controller()
xMin = 800
xMax = -800
yMin = 800
yMax = -800

# classifier globals
# sys.path.insert(0, "")
clf = pickle.load( open('userData/classifier.p','rb') )
testData = np.zeros((1,30),dtype='f')
k = 0

def CenterData(set):
    for i in range(3):
        set[0, ::3] = set[0, ::3] - set[0, ::3].mean()
        set[0, 1::3] = set[0, 1::3] - set[0, 1::3].mean()
        set[0, 2::3] = set[0, 2::3] - set[0, 2::3].mean()
    return set

def scaleValue(val, min, max, windowMin, windowMax):
    if (max - min != 0):
        fullWidth = max - min
        distanceFromMin = val - min
        distanceFromMinPercent = float(distanceFromMin) / float(fullWidth)
        # print("distanceFromMinPercent: ", distanceFromMinPercent)

        windowWidth = (windowMax - windowMin)/2 ## Makes it draw in upper left quadrant
        distanceFromWindowMin = distanceFromMinPercent * windowWidth
        return int(distanceFromWindowMin)

    else:
        return val

def Handle_Vector_From_Leap(v):

    xVal = float(v[0])
    yVal = float(v[2])

    # dynamically scale screen
    global xMin,xMax,yMin,yMax
    if ( xVal < xMin ):
        xMin = xVal
    if ( xVal > xMax ):
        xMax = xVal
    if ( yVal < yMin ):
        yMin = yVal
    if ( yVal > yMax ):
        yMax = yVal

    xVal = scaleValue(xVal, xMin, xMax, 0, constants.pygameWindowWidth)
    yVal = scaleValue(yVal, yMin, yMax, 0, constants.pygameWindowDepth)

    xVal_unscaled = float(v[0])
    yVal_unscaled = float(v[2])

    return xVal, yVal#, xVal_unscaled, yVal_unscaled

def Handle_Bone(b, bone, thickness):
    global xMin,xMax,yMin,yMax, k, testData

    base = bone.prev_joint
    base_xVal_scaled, base_yVal_scaled = Handle_Vector_From_Leap(base)

    tip = bone.next_joint
    tip_xVal_scaled, tip_yVal_scaled = Handle_Vector_From_Leap(tip)

    pygameWindow.Draw_Black_Line(base_xVal_scaled,base_yVal_scaled, \
                                 tip_xVal_scaled,tip_yVal_scaled, thickness)

    # store the data for prediction
    if (b==0 or  b==3) :
        # print("k =",k)
        testData[0,k] = float(tip[0])
        testData[0,k+1] = float(tip[1])
        testData[0,k+2] = float(tip[2])
        k += 3

def Handle_Finger(finger):
    for b in range(0,4):
        bone = finger.bone(b)
        Handle_Bone(b, bone, 8 - b * 2)


def Handle_Frame(frame):
    global x, y
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)

def isHandCentered(frame):

    baseMiddleFinger = frame.hands[0].fingers[2].bone(1).prev_joint
    x, y = baseMiddleFinger[0], baseMiddleFinger[2]

    direction = "centered"
    if x > 50:
        direction = "left"
    if x < -50:
        direction = "right"
    if y > 50:
        direction = "up"
    if y < -50:
        direction = "down"

    return direction

def HandleState3(): # hand is centered and the digit is correct for 10 frames
    global successDisplayTime, programState, numberGoal, scaffoldedItems, totalItems
    print(successDisplayTime)

    if successDisplayTime < 10:
        successDisplayTime += 1
        pygameWindow.displaySuccess()

    else:
        # increment in DataBase before numbergoal is switched, reset signDisplayTime
        db.digitAttempted(numberGoal,correct=True)

        # add a new number if 3 out of the last 5 attempts were correct
        currentNumbersMastered = True
        for digit in scaffoldedItems:
            if (db.getStats(db.currentUser,attribute="score")[digit] < 3):
                currentNumbersMastered = False

        if (currentNumbersMastered):
            numberGoal = totalItems[len(scaffoldedItems)]
            scaffoldedItems.add(totalItems[len(scaffoldedItems)])
            print(scaffoldedItems)
        else:
            numberGoal = random.sample(scaffoldedItems,1)[0]

        print("numberGoal:", numberGoal)

        successDisplayTime = 0

        if (len(frame.hands) == 0):
            programState = 0
        elif (isHandCentered(frame) != "centered"):
            programState = 1
        else:
            programState = 2


def HandleState2(): # hand is centered, trying to sign
    global k, programState, correctSignCount, testData, numberGoal, failDisplayTime,signDisplayTime,maxSignDisplayTime, timeForSignToCount

    if (len(frame.hands) == 0):
        programState = 0
    elif (isHandCentered(frame) != "centered"):
        programState = 1
    else:

        k = 0

        # determine how long to show the sign instruction on screen
        if (numberGoal in db.getStats(db.currentUser)):
            if ("score" in db.getStats(db.currentUser)[numberGoal]):
                timeToShowSign = maxSignDisplayTime - 3*db.getStats(db.currentUser)[numberGoal]["score"]
            else:
                timeToShowSign = maxSignDisplayTime
        else:
            timeToShowSign = maxSignDisplayTime
        if signDisplayTime < timeToShowSign:
            pygameWindow.drawGestureForNumber(numberGoal)

        # if the time isn't up for this attempt, increment and get user to try to sign
        if signDisplayTime < maxSignDisplayTime:
            signDisplayTime += 1

            pygameWindow.drawNumber(numberGoal)
            Handle_Frame(frame)

            #Classify stuff:
            userAttempt = CenterData(testData)
            predictedClass = clf.Predict(userAttempt)

            if predictedClass == numberGoal:
                #TURN THE HAND GREEN,
                correctSignCount += 1
            else:
                correctSignCount = 0

            # figure out how long the user needs to  be right for it to count
            if (numberGoal in db.getStats(db.currentUser)):
                if ("score" in db.getStats(db.currentUser)[numberGoal]):
                    # needs to be smaller than maxSignDisplayTime
                    timeForSignToCount = maxSignDisplayTime/3 - 1.5*db.getStats(db.currentUser)[numberGoal]["score"]
                else:
                    timeForSignToCount = maxSignDisplayTime/3
            else:
                timeForSignToCount = maxSignDisplayTime/3

            # show the sign until its supposed to dissapear.
            if correctSignCount >= timeForSignToCount:
                correctSignCount = 0
                signDisplayTime = 0
                programState = 3

        # once time is up, change scores, display failed, then switch numbers
        else:
            # show fail message
            if failDisplayTime < 10:
                failDisplayTime += 1
                pygameWindow.displayFail()

            # once fail message is over
            else:
                signDisplayTime = 0
                failDisplayTime = 0

                # increment the count of how many times this user has seen this digit
                db.digitAttempted(numberGoal,correct=False)
                numberGoal = random.sample(scaffoldedItems,1)[0]
                print(numberGoal)



def HandleState1(): # hand is in the frame but not consistantly centered
    global k, programState, timeCentered

    if (len(frame.hands) == 0):
        programState = 0
    elif (isHandCentered(frame) == "centered" and timeCentered >= 10):
        programState = 2
    else:
        timeCentered += 1
        k = 0
        Handle_Frame(frame)

        # get where hand is in relation to center
        direction = isHandCentered(frame)
        pygameWindow.drawCenterHand(direction)

        if direction != "centered":
            timeCentered = 0

def HandleState0(): # hand is not in the frame
    global programState

    if (len(frame.hands) > 0):
        programState = 1
    else:
        pygameWindow.drawHelpfulAnimation()

while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    pygameWindow.displaySessionVsAll(db)
    pygameWindow.displayWarmColdBar(correctSignCount, timeForSignToCount)

    # handle state
    if programState == 0:
        HandleState0()
    elif programState == 1:
        HandleState1()
    elif programState == 2:
        HandleState2()
    elif programState == 3:
        HandleState3()


    pygameWindow.Reveal()
