import sys
import random
import pickle
import numpy as np

#local imports
sys.path.insert(0, "..")
import constants
from pygameWindow import PYGAME_WINDOW
sys.path.insert(0, "../..")
import Leap

#drawing globals
pygameWindow = PYGAME_WINDOW()
controller = Leap.Controller()
x = 400
y = 400
xMin = 800
xMax = -800
yMin = 800
yMax = -800

#classifier globals
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

while True:
    pygameWindow.Prepare()

    frame = controller.frame()
    if (len(frame.hands) > 0):
        k = 0
        Handle_Frame(frame)
        # print(testData)
        testData = CenterData(testData)
        predictedClass = clf.Predict(testData)
        print(predictedClass)
    else:
        # print("no hand")
        pass


    pygameWindow.Reveal()
