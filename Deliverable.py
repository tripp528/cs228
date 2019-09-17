import sys
sys.path.insert(0, "..")
import Leap
import constants
import numpy as np
import pickle

class DELIVERABLE:

    def __init__(self,controller, pygameWindow, x, y, xMin, xMax, yMin, yMax):
        self.pygameWindow = pygameWindow
        self.controller = controller
        self.x = x
        self.y = y
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0
        self.gestureData = np.zeros((5,4,6),dtype='f')
        self.gestureNumber = 0

    def Save_Gesture(self):
        pickle_out = open("userData/gesture"+str(self.gestureNumber)+".p","wb")
        pickle.dump(self.gestureData, pickle_out)
        pickle_out.close()
        self.gestureNumber += 1

    def Recording_Is_Ending(self):
        if (self.currentNumberOfHands == 1 and self.previousNumberOfHands == 2):
            return True
        else:
            return False

    def scaleValue(self,val, min, max, windowMin, windowMax):
        if (max - min != 0):
            fullWidth = max - min
            distanceFromMin = val - min
            distanceFromMinPercent = float(distanceFromMin) / float(fullWidth)

            windowWidth = windowMax - windowMin
            distanceFromWindowMin = distanceFromMinPercent * windowWidth
            return int(distanceFromWindowMin)

        else:
            return val

    def Handle_Vector_From_Leap(self,v):

        xVal = float(v[0])
        yVal = float(v[2]) #ACTUALLY Z VALUE

        # dynamically scale screen
        # global xMin,xMax,yMin,yMax
        if ( xVal < self.xMin ):
            self.xMin = xVal
        if ( xVal > self.xMax ):
            self.xMax = xVal
        if ( yVal < self.yMin ):
            self.yMin = yVal
        if ( yVal > self.yMax ):
            self.yMax = yVal

        xVal = self.scaleValue(xVal, self.xMin, self.xMax, 0, constants.pygameWindowWidth)
        yVal = self.scaleValue(yVal, self.yMin, self.yMax, 0, constants.pygameWindowDepth)
        return xVal, yVal

    def Handle_Bone(self,bone,thickness,fingerIndex,boneIndex):
        global xMin,xMax,yMin,yMax
        base = bone.prev_joint
        base_xVal, base_yVal = self.Handle_Vector_From_Leap(base)
        tip = bone.next_joint
        tip_xVal, tip_yVal = self.Handle_Vector_From_Leap(tip)

        lineColor = (0,0,0)
        if (self.currentNumberOfHands == 1):
            lineColor = (0,222,0)
        elif (self.currentNumberOfHands == 2):
            lineColor = (222,0,0)
        self.pygameWindow.Draw_Line(base_xVal,base_yVal,tip_xVal,tip_yVal, thickness, lineColor)

        #store data
        if self.Recording_Is_Ending():
            self.gestureData[fingerIndex,boneIndex,0] = base[0]
            self.gestureData[fingerIndex,boneIndex,1] = base[1]
            self.gestureData[fingerIndex,boneIndex,2] = base[2]
            self.gestureData[fingerIndex,boneIndex,3] = tip[0]
            self.gestureData[fingerIndex,boneIndex,4] = tip[1]
            self.gestureData[fingerIndex,boneIndex,5] = tip[2]

    def Handle_Finger(self,finger,fingerIndex):
        for boneIndex in range(0,4):
            bone = finger.bone(boneIndex)
            self.Handle_Bone(bone, 8 - boneIndex * 2,fingerIndex,boneIndex)

    def Handle_Frame(self,frame):
        global x, y
        hand = frame.hands[0]
        fingers = hand.fingers
        for fingerIndex in range(len(fingers)):
            finger = fingers[fingerIndex]
            self.Handle_Finger(finger,fingerIndex)
        if self.Recording_Is_Ending():
            print(self.gestureData)
            self.Save_Gesture()


    def Run_Once(self):
        self.pygameWindow.Prepare()
        frame = self.controller.frame()
        self.currentNumberOfHands = len(frame.hands)

        if (self.currentNumberOfHands > 0):
            self.Handle_Frame(frame)

        self.previousNumberOfHands = self.currentNumberOfHands
        self.pygameWindow.Reveal()

    def Run_Forever(self):
        while True:
            self.Run_Once()
