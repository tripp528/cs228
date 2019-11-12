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
xMin = 800
xMax = -800
yMin = 800
yMax = -800

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
    return xVal, yVal

def Handle_Bone(bone, thickness):
    global xMin,xMax,yMin,yMax
    base = bone.prev_joint
    base_xVal, base_yVal = Handle_Vector_From_Leap(base)
    tip = bone.next_joint
    tip_xVal, tip_yVal = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(base_xVal,base_yVal,tip_xVal,tip_yVal, thickness)

def Handle_Finger(finger):
    for b in range(0,4):
        bone = finger.bone(b)
        Handle_Bone(bone, 8 - b * 2)


def Handle_Frame(frame):
    global x, y
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)

while True:
    pygameWindow.Prepare()

    frame = controller.frame()
    if (len(frame.hands) > 0):
        Handle_Frame(frame)
    else:
        print("no hand")


    pygameWindow.Reveal()
