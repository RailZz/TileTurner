import pygame
from pygame.locals import *
import tkinter
from drawText import *

root = tkinter.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()

textLen = 150
difCol = 50
textHeight = 30

false = False
true = True

class ChooseLevel:
    
    def __init__(self, level):
        
        self.maxLevel = level
        
        self.visible_ = false
        
        self.UPSPACE = 100
        self.LEFTSPACE = (width - textLen * 5 - difCol * 4) // 2
        
        self.lastLevelDown = -1
        
        
    def draw(self, surfaceObj):
        if self.visible_:
            drawText("Choose level", surfaceObj, (10, 10, 200, 60), 72)
            for i in range(1, self.maxLevel + 1):
                coll = (i - 1) // 20
                pos = (i - 1) % 20
                drawText("Level " + str(i), surfaceObj, (self.LEFTSPACE + coll * textLen + coll * difCol, self.UPSPACE + pos * textHeight), 20)
            
    def hide(self):
        self.visible_ = false
        
    def show(self):
        self.visible_ = true
        
    def getLevel(self, posTuple):
        
        pos = [posTuple[0], posTuple[1]]
        pos[0] -= self.LEFTSPACE
        pos[1] -= self.UPSPACE
        if pos[0] < 0 or pos[1] < 0:
            return -1
        if pos[0] > 5 * (textLen + difCol) or pos[1] > 20 * textHeight:
            return -1
        
        delWidth = pos[0] % (textLen + difCol)
        if delWidth > textLen:
            return -1
        
        col = pos[0] // (textLen + difCol)
        line = pos[1] // textHeight
        
        return col * 20 + line + 1
        
            
    def handleEvent(self, eventObj):
        
        if eventObj.type not in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
            return ''
        
        pos = eventObj.pos
        
        if eventObj.type == MOUSEBUTTONDOWN:
            
            self.lastLevelDown = self.getLevel(pos)
            
        elif eventObj.type == MOUSEBUTTONUP:
            
            if self.getLevel(pos) == self.lastLevelDown and self.lastLevelDown <= self.maxLevel and self.lastLevelDown != -1:
                
                return self.lastLevelDown
        
        return ''
        
        