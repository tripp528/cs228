import pickle
import os
import time

from pygameWindow_Del03 import PYGAME_WINDOW
import constants

class READER:

    def __init__(self):
        self.getNumberOfGestures()
        self.pygameWindow = PYGAME_WINDOW()
        self.xMin = -constants.pygameWindowWidth
        self.xMax = constants.pygameWindowWidth
        self.yMin = -constants.pygameWindowDepth
        self.yMax = constants.pygameWindowDepth

    def getNumberOfGestures(self):
        path, dirs, files = next(os.walk('userData'))
        self.numGestures = len(files)

    def Print_Gestures(self):
        for gestureNumber in range(self.numGestures):
            pickle_in = open("userData/gesture" + str(gestureNumber) + ".p","rb")
            gestureData = pickle.load(pickle_in)
            pickle_in.close()
            print(gestureData)

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

    def Draw_Gesture(self, gestureNumber):
        self.pygameWindow.Prepare()

        pickle_in = open("userData/gesture" + str(gestureNumber) + ".p","rb")
        gestureData = pickle.load(pickle_in)
        pickle_in.close()
        #draw it
        for fingerIndex in range(5):
            for boneIndex in range(4):
                currentBone = gestureData[fingerIndex,boneIndex,:]
                xBaseNotYetScaled = currentBone[0]
                yBaseNotYetScaled = currentBone[2] # ACTUALLY Z
                xTipNotYetScaled = currentBone[3]
                yTipNotYetScaled = currentBone[5] # ACTUALLY Z
                base_xVal = self.scaleValue(xBaseNotYetScaled, self.xMin, self.xMax, 0, constants.pygameWindowWidth)
                base_yVal = self.scaleValue(yBaseNotYetScaled, self.yMin, self.yMax, 0, constants.pygameWindowDepth)
                tip_xVal = self.scaleValue(xTipNotYetScaled, self.xMin, self.xMax, 0, constants.pygameWindowWidth)
                tip_yVal = self.scaleValue(yTipNotYetScaled, self.yMin, self.yMax, 0, constants.pygameWindowDepth)

                self.pygameWindow.Draw_Line(base_xVal,base_yVal,tip_xVal,tip_yVal, 4, (0,0,222))
        self.pygameWindow.Reveal()
        time.sleep(0.3)

    def Draw_Each_Gesture_Once(self):
        for gestureNumber in range(self.numGestures):
            self.Draw_Gesture(gestureNumber)

    def Draw_Gestures(self):
        while(True):
            self.Draw_Each_Gesture_Once()
