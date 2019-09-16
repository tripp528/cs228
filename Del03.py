import sys
sys.path.insert(0, "..")
import Leap
import constants

import random
from pygameWindow import PYGAME_WINDOW
from Deliverable import DELIVERABLE

deliverable = DELIVERABLE(Leap.Controller(),PYGAME_WINDOW(),400,400,800,-800,800,-800)

deliverable.Run_Forever()
