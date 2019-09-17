import pickle
import os
from pygameWindow_Del03 import PYGAME_WINDOW

class READER:

    def __init__(self):
        self.getNumberOfGestures()
        self.pygameWindow = PYGAME_WINDOW()

    def getNumberOfGestures(self):
        path, dirs, files = next(os.walk('userData'))
        self.numGestures = len(files)

    def Print_Gestures(self):
        for gestureNumber in range(self.numGestures):
            pickle_in = open("userData/gesture" + str(gestureNumber) + ".p","rb")
            gestureData = pickle.load(pickle_in)
            pickle_in.close()
            print(gestureData)

    def Draw_Gestures(self):
        pass
