import pygame
from pygame.locals import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, tileType, tilePos, rect):
        pygame.sprite.Sprite.__init__(self)
        self.tileType_ = tileType
        self.tilePos_ = tilePos
        self.posX, self.posY = rect[0], rect[1]
        self.imageName = "tiles/tile" + str(self.tileType_) + str(self.tilePos_) + ".jpg"
        self.image = pygame.image.load(self.imageName)
        self.image = self.image.convert()
        
    def draw(self, suf = ''):
        self.imageName = "tiles/tile" + str(self.tileType_) + str(self.tilePos_) + suf + ".jpg"
        self.image = pygame.image.load(self.imageName)
        self.image = self.image.convert()        
        screen = pygame.display.get_surface()
        screen.blit(self.image, (self.posX, self.posY))
        
    def turn(self):
        self.tilePos_ += 1
        self.tilePos_ %= 4
        self.imageName = "tiles/tile" + str(self.tileType_) + str(self.tilePos_) + ".jpg"
        self.image = pygame.image.load(self.imageName)
        self.image = self.image.convert()  
        
        
        
        