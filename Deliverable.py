import sys
sys.path.insert(0, "..")
import Leap
import constants

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


    def scaleValue(self,val, min, max, windowMin, windowMax):
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

    def Handle_Vector_From_Leap(self,v):

        xVal = float(v[0])
        yVal = float(v[2])

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

    def Handle_Bone(self,bone, thickness):
        global xMin,xMax,yMin,yMax
        base = bone.prev_joint
        base_xVal, base_yVal = self.Handle_Vector_From_Leap(base)
        tip = bone.next_joint
        tip_xVal, tip_yVal = self.Handle_Vector_From_Leap(tip)
        self.pygameWindow.Draw_Black_Line(base_xVal,base_yVal,tip_xVal,tip_yVal, thickness)

    def Handle_Finger(self,finger):
        for b in range(0,4):
            bone = finger.bone(b)
            self.Handle_Bone(bone, 8 - b * 2)


    def Handle_Frame(self,frame):
        global x, y
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.Handle_Finger(finger)

    def Run_Forever(self):
        while True:
            self.pygameWindow.Prepare()

            frame = self.controller.frame()
            if (len(frame.hands) > 0):
                self.Handle_Frame(frame)
            else:
                print("no hand")


            self.pygameWindow.Reveal()
