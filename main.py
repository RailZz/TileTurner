import pygame
import sys
import os
import pygbutton
import tkinter
from pygame.locals import *

from button import PygButton
from StartButton import StartButton
from NextButton import NextButton
from ContinueButton import ContinueButton
from MenuButton import MenuButton
from ExitButton import ExitButton
from HintButton import HintButton
from ChooseLevelButton import ChooseLevelButton

from drawText import *
from header import Header
from pybackground import draw_background
from state import *
from level import Level
from ChooseLevel import ChooseLevel

root = tkinter.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenwidth()
os.environ['SDL_VIDEO_CENTERED'] = '1'
#height, width = 800, 600

startButton = StartButton((width // 2 - 95, height // 2 - 180, 190, 60)) 
nextButton = NextButton((width // 2 - 95, height // 2 - 50, 190, 60))
continueButton = ContinueButton((width // 2 - 95, height // 2 - 250, 190, 60))
menuButton = MenuButton((width - 200, 10, 190, 60))
exitButton = ExitButton((width // 2 - 95, height // 2 - 40, 190, 60))
hintButton = HintButton((width - 400, 10, 190, 60))
chooseLevelButton = ChooseLevelButton((width // 2 - 95, height // 2 - 110, 190, 60))


headerImage = Header()

levelInput = open("levelToPlayDoc.txt")
maxLevel = int(levelInput.readline().strip())
levelInput.close()
levelToPlay = maxLevel
level = None
bk = None
chooseLevel = None
prevScore = 0
newScore = 0
 
def printScore(prevScore, newScore, surfaceObj, curLevel):
    if prevScore >= newScore:
        drawText("Your score is: " + str(prevScore), surfaceObj, (10, 60, 200, 40), 36)
    else:
        drawText("Your score is: " + str(newScore) + " NEW!", surfaceObj, (10, 60, 200, 40), 36)
        scoreFile = open('levels/score' + str(curLevel) + ".pavel", "w")
        print(newScore, file = scoreFile)
        scoreFile.close()

def init_window():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    #pygame.display.set_mode((height, width))
    pygame.display.set_caption("TileTurner")

    
def input(events):
    global level
    global levelToPlay
    global newScore
    global prevScore
    global chooseLevel
    global maxLevel
    for event in events:
        if getState() == 0:
            
            startFeedback = []
            continueFeedback = []
            exitFeedback = []
            chooseLevelFeedback = []
            
            startFeedback = startButton.handleEvent(event)
            continueFeedback = continueButton.handleEvent(event)
            exitFeedback = exitButton.handleEvent(event)
            chooseLevelFeedback = chooseLevelButton.handleEvent(event)
            
            headerImage.draw(pygame.display.get_surface())            
            startButton.draw(pygame.display.get_surface())
            continueButton.draw(pygame.display.get_surface())
            exitButton.draw(pygame.display.get_surface())
            chooseLevelButton.draw(pygame.display.get_surface())
            
            if 'click' in startFeedback:
                
                startButton.hide()
                continueButton.hide()
                exitButton.hide()
                chooseLevelButton.hide()
                headerImage.hide()
                draw_background()
                
                menuButton.show()
                hintButton.show()
                
                menuButton.draw(pygame.display.get_surface())
                hintButton.draw(pygame.display.get_surface())
                
                levelToPlay = 1
                level = Level(levelToPlay)
                prevScore = level.score
                level.draw(pygame.display.get_surface())
                
                drawText("Level " + str(levelToPlay), pygame.display.get_surface(), (10, 10, 200, 60), 72)
                setState(1)
                
            elif 'click' in continueFeedback:
                
                startButton.hide()
                continueButton.hide()
                exitButton.hide()
                chooseLevelButton.hide()
                headerImage.hide()
                draw_background()
                
                menuButton.show()
                hintButton.show()
                
                menuButton.draw(pygame.display.get_surface())
                hintButton.draw(pygame.display.get_surface())
                
                level = Level(levelToPlay)
                prevScore = level.score
                level.draw(pygame.display.get_surface())
                
                drawText("Level " + str(levelToPlay), pygame.display.get_surface(), (10, 10, 200, 60), 72)
                setState(1)  
                
            elif 'click' in chooseLevelFeedback:
                
                startButton.hide()
                continueButton.hide()
                exitButton.hide()
                chooseLevelButton.hide()
                headerImage.hide()
                draw_background()
                
                menuButton.show()
                chooseLevel = ChooseLevel(maxLevel)
                chooseLevel.show()
                
                menuButton.draw(pygame.display.get_surface())
                chooseLevel.draw(pygame.display.get_surface())
                
                setState(3)
                
            elif 'click' in exitFeedback:
                
                sys.exit(0)
                
        elif getState() == 1:
            
            levelFeedback = []
            menuFeedback = []
            hintFeedback = []
            
            levelFeedback = level.handleEvent(event)
            menuFeedback = menuButton.handleEvent(event)
            hintFeedback = hintButton.handleEvent(event)
            
            level.draw(pygame.display.get_surface())
            menuButton.draw(pygame.display.get_surface())
            hintButton.draw(pygame.display.get_surface())
            
            drawText("Level " + str(levelToPlay), pygame.display.get_surface(), (10, 10, 200, 60), 72)  
            
            if 'finished' in levelFeedback:
                
                levelToPlay += 1
                maxLevel = max(maxLevel, levelToPlay)
                level.hint()
                
                newScore = getScore()
                
                outCurLevel = open("levelToPlayDoc.txt", "w")
                print(maxLevel, file = outCurLevel)
                outCurLevel.close() 
                
                setState(2)
                
                hintButton.hide()
                draw_background()
                
                nextButton.show()
                
                drawText("Level completed", pygame.display.get_surface(), (10, 10, 180, 40), 48)
                printScore(prevScore, newScore, pygame.display.get_surface(), levelToPlay - 1)
                nextButton.draw(pygame.display.get_surface())
                menuButton.draw(pygame.display.get_surface())
                level.draw(pygame.display.get_surface())
                
            elif 'click' in menuFeedback:
                
                menuButton.hide()
                hintButton.hide()
                level.hide()
                
                headerImage.show()
                startButton.show()
                continueButton.show()
                exitButton.show()
                chooseLevelButton.show()
                
                headerImage.draw(pygame.display.get_surface()) 
                startButton.draw(pygame.display.get_surface())
                continueButton.draw(pygame.display.get_surface())
                chooseLevelButton.draw(pygame.display.get_surface())
                exitButton.draw(pygame.display.get_surface())
                
                setState(0)
                
            elif 'click' in hintFeedback:
                
                level.hint()
                
                level.draw(pygame.display.get_surface())
                menuButton.draw(pygame.display.get_surface())
                hintButton.draw(pygame.display.get_surface())
                
        elif getState() == 2:
            
            nextFeedback = []
            menuFeedback = []
            
            nextFeedback = nextButton.handleEvent(event)
            menuFeedback = menuButton.handleEvent(event)
            
            nextButton.draw(pygame.display.get_surface())
            menuButton.draw(pygame.display.get_surface())
            level.draw(pygame.display.get_surface())
            printScore(prevScore, newScore, pygame.display.get_surface(), levelToPlay - 1)
            
            if 'click' in nextFeedback:
                
                nextButton.hide()
                
                draw_background()
                
                hintButton.show()
                
                level = Level(levelToPlay)
                prevScore = level.score
                level.show()
                
                level.draw(pygame.display.get_surface())
                menuButton.draw(pygame.display.get_surface())
                hintButton.draw(pygame.display.get_surface())
                
                drawText("Level " + str(levelToPlay), pygame.display.get_surface(), (10, 10, 200, 60), 72)
                setState(1) 
                
            elif 'click' in menuFeedback:
                
                nextButton.hide()
                menuButton.hide()
                level.hide()
                
                headerImage.show()
                startButton.show()
                continueButton.show()
                chooseLevelButton.show()
                exitButton.show()
                
                headerImage.draw(pygame.display.get_surface()) 
                startButton.draw(pygame.display.get_surface())
                continueButton.draw(pygame.display.get_surface())
                chooseLevelButton.draw(pygame.display.get_surface())
                exitButton.draw(pygame.display.get_surface())
                
                setState(0)                
                
        elif getState() == 3:
            
            menuFeedback = []
            chooseLevelFeedback = []
            
            menuFeedback = menuButton.handleEvent(event)
            chooseLevelFeedback = chooseLevel.handleEvent(event)
            
            menuButton.draw(pygame.display.get_surface())
            chooseLevel.draw(pygame.display.get_surface())
            
            if 'click' in menuFeedback:

                chooseLevel.hide()
                menuButton.hide()
                
                draw_background()
                
                headerImage.show()
                startButton.show()
                continueButton.show()
                chooseLevelButton.show()
                exitButton.show()
                
                headerImage.draw(pygame.display.get_surface()) 
                startButton.draw(pygame.display.get_surface())
                continueButton.draw(pygame.display.get_surface())
                chooseLevelButton.draw(pygame.display.get_surface())
                exitButton.draw(pygame.display.get_surface())
                
                setState(0)     
            
            if chooseLevelFeedback != '':
                
                chooseLevel.hide()
                
                draw_background()
                
                levelToPlay = chooseLevelFeedback
                
                level = Level(levelToPlay)
                prevScore = level.score
                level.show()
                hintButton.show()
                menuButton.show()

                level.draw(pygame.display.get_surface())
                menuButton.draw(pygame.display.get_surface())
                hintButton.draw(pygame.display.get_surface())
                
                drawText("Level " + str(levelToPlay), pygame.display.get_surface(), (10, 10, 200, 60), 72)
                setState(1) 
                
        pygame.display.flip()     
        
        if (event.type == QUIT):
            sys.exit(0)
        else:
            pass

def action():
    while 1:
        input(pygame.event.get())

def main():
    init_window()
    bk = draw_background()
    
    nextButton.hide()
    menuButton.hide()
    hintButton.hide()
    
    action()
    
if __name__ == '__main__':
    main()