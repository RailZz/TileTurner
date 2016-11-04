import pygame
from pygame.locals import *

def drawText(text, surfaceObj, rect, fontSize):
    font = pygame.font.SysFont("greyscalebasic", fontSize)
    text = font.render(text, True, (0, 0, 0))
    surfaceObj.blit(text, rect)