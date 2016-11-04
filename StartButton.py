import pygame
import sys
import pygbutton
import os
from pygame.locals import *
from button import PygButton
from level import Level

BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)



class StartButton(PygButton):
    
    def __init__(self, rect = None, caption = 'Begin Game', bgcolor = LIGHTGRAY, fgcolor = BLACK, font = None, normal = "buttons/BeginButton.jpg", down = None, highlight = None):
        super(StartButton, self).__init__(rect, caption, bgcolor, fgcolor, font, normal, down, highlight)
        
    def mouseClick(self, event):
        pass
    def mouseEnter(self, event):
        pass
    def mouseMove(self, event):
        pass
    def mouseExit(self, event):
        pass
    def mouseDown(self, event):
        pass
    def mouseUp(self, event):
        pass