MAINMENU = 0
LEVEL = 1
NEXTLEVEL = 2
CHOOSELEVEL = 3

state = 0
score = 0

def getState():
    return state

def setState(x):
    global state
    state = x
    
def getScore():
    return score

def setScore(x):
    global score
    score = x