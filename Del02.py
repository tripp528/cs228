import sys
sys.path.insert(0, "..")
import Leap
import constants

import random
from pygameWindow import PYGAME_WINDOW

pygameWindow = PYGAME_WINDOW()
controller = Leap.Controller()
x = 400
y = 400
xMin = 1000
xMax = -1000
yMin = 1000
yMax = -1000

def Perturb_Circle_Position():
    global x, y
    fourSidedDieRoll = random.randint(1,4)
    if fourSidedDieRoll == 1:
        x -= 1
    elif fourSidedDieRoll == 2:
        x += 1
    elif fourSidedDieRoll ==  3:
        y -= 1
    else:
        y += 1

def scaleValue(val, min, max, windowMin, windowMax):
    if (max - min != 0):
        fullWidth = max - min
        distanceFromMin = val - min
        distanceFromMinPercent = float(distanceFromMin) / float(fullWidth)
        print("distanceFromMinPercent: ", distanceFromMinPercent)

        windowWidth = windowMax - windowMin
        distanceFromWindowMin = distanceFromMinPercent * windowWidth
        return int(distanceFromWindowMin)

    else:
        return val


def Handle_Frame(frame):
    global x, y
    hand = frame.hands[0]
    fingers = hand.fingers
    indexFingerList = fingers.finger_type(Leap.Finger.TYPE_INDEX)
    indexFinger = indexFingerList[0]
    distalPhalanx = indexFinger.bone(Leap.Bone.TYPE_DISTAL)
    tip = distalPhalanx.next_joint
    print(tip)
    xVal = int(tip[0])
    yVal = int(tip[1])

    #handle bounds of screen
    global xMin,xMax,yMin,yMax
    if ( xVal < xMin ):
        xMin = xVal
    if ( xVal > xMax ):
        xMax = xVal
    if ( yVal < yMin ):
        yMin = yVal
    if ( yVal > yMax ):
        yMax = yVal
    print(xMin,xMax,yMin,yMax)

    x = scaleValue(xVal, xMin, xMax, 0, constants.pygameWindowWidth)
    y = constants.pygameWindowDepth - scaleValue(yVal, yMin, yMax, 0, constants.pygameWindowDepth)

    print("ScaledX: ", x, "scaledY: ", y)

while True:
    pygameWindow.Prepare()

    # Perturb_Circle_Position()
    frame = controller.frame()
    if (len(frame.hands) > 0):
        Handle_Frame(frame)
        pygameWindow.Draw_Black_Circle(x,y)

    else:
        print("no hand")


    pygameWindow.Reveal()
