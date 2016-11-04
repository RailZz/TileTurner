import pygame
from pygame.locals import *
import os
import tkinter
from pybackground import *

root = tkinter.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenwidth()

true = True
false = False

class Header(pygame.sprite.Sprite):
    
    def __init__(self):
        
        super(Header, self).__init__()
        
        self.rect = (width // 2 - 103, height // 2 - 400, 206, 140)
        
        self.image = pygame.image.load("header.png")
        
        self.visible = true
        
    def draw(self, surfaceObj):
        if self.visible:
            surfaceObj.blit(self.image, self.rect)
            
    def show(self):
        self.visible_ = true
    
    def hide(self):
        self.visible_ = false
        draw_background()        
        