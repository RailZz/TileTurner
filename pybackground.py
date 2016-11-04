import pygame
import os
from pygame.locals import *

def load_background(name, colorkey = None):
    image = pygame.image.load(name)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)    
    return image, image.get_rect()

def draw_background():
    screen = pygame.display.get_surface()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    back, back_rect = load_background("background.jpg")
    screen.blit(back, (0, 0))
    pygame.display.flip()
    return back   