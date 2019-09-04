import random
from pygameWindow import PYGAME_WINDOW

pygameWindow = PYGAME_WINDOW()
x = 400
y = 400

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

while True:
    pygameWindow.Prepare()

    pygameWindow.Draw_Black_Circle(x,y)
    Perturb_Circle_Position()

    pygameWindow.Reveal()
