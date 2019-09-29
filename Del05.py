import sys
sys.path.insert(0, "..")
import Leap
import constants

import random
from pygameWindow_Del03 import PYGAME_WINDOW
from Recorder import RECORDER

deliverable = RECORDER(Leap.Controller(),PYGAME_WINDOW(),400,400,800,-800,800,-800)

deliverable.Run_Forever()
