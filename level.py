import pygame
import sys
from pygame.locals import *
import tkinter
from tile import Tile
from pybackground import *
from drawText import *
from state import setScore
from time import time

root = tkinter.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
#width, height = 800, 600

TILESIZE = 40
LEVELBORDER = 6
TILESEPARATE = 0

false = False
true = True

neigh = [[], [], [], [], [], []]
neigh[1] = [1]
neigh[2] = [1, 2]
neigh[3] = [1, 3]
neigh[4] = [1, 2, 3]
neigh[5] = [0, 1, 2, 3]

dx = [0, -1, 0, 1]
dy = [-1, 0, 1, 0]

def invertDir(Dir):
    if Dir in [0, 2]:
        return 2 - Dir
    return 4 - Dir

class Level:
    
    def __init__(self, level):
        self.level_ = level
        self.dataFile = open("levels/level" + str(level) + ".pavel")
        self.height_, self.width_, self.badTilesCount = [int(i) for i in self.dataFile.readline().split()]
        
        self.LEFTRIGHTSIDES = (width - TILESIZE * self.width_ - TILESEPARATE * (self.width_ - 1)) // 2
        self.UPDOWNSIDES = (height - TILESIZE * self.height_ - TILESEPARATE * (self.height_ - 1)) // 2        
        
        self.field = []
        
        self.badtiles = []
        
        for i in range(self.height_):
            s = self.dataFile.readline()
            inputString = s[1:-1].split(')(')
            self.field.append([])
            for q in range(self.width_):
                self.field[i].append((int(inputString[q][0]), int(inputString[q][2])))
                
        self.dataFile.close()
        
        self.tiles = []
        #fout = open("out.txt", "w")
        for i in range(self.height_):
            self.tiles.append([None] * self.width_)
            for q in range(self.width_):
                posX = self.LEFTRIGHTSIDES + LEVELBORDER + TILESIZE * q + TILESEPARATE * q
                posY = self.UPDOWNSIDES + LEVELBORDER + TILESIZE * i + TILESEPARATE * i
                #print(posX, posY, file = fout)
                self.tiles[i][q] = Tile(self.field[i][q][0], self.field[i][q][1],
                                        (posX, posY, 40, 40))
                
        #fout.close()
        
        scoreFile = open('levels/score' + str(level) + ".pavel")
        self.score = int(scoreFile.readline().strip())
        scoreFile.close()
        
        self.finished_ = false
        
        self.turnCount = 0
        self.timeBegin = time()
        
        self.lastMouseDownOverTile = false
        self.lastTileDown = (-1, -1)
        self.visible_ = true
        
    def draw(self, surfaceObj):
        if self.visible_:
            if not self.finished_:
                drawText("Best score: " + str(self.score), pygame.display.get_surface(), (10, 80, 200, 30), 36)
            for i in range(self.height_):
                for q in range(self.width_):
                    if (i, q) in self.badtiles:
                        self.tiles[i][q].draw("Lit")
                    else:
                        self.tiles[i][q].draw()
        
    def show(self):
        self.visible_ = true

    def hide(self):
        self.visible_ = false
        draw_background()
        
    def getTile(self, posTuple):
        pos = [posTuple[0], posTuple[1]]
        pos[0] -= self.LEFTRIGHTSIDES
        pos[1] -= self.UPDOWNSIDES
        if pos[0] < 0 or pos[1] < 0:
            return (-1, -1)
        if pos[0] > self.width_ * TILESIZE + (self.width_ - 1) * TILESEPARATE or pos[1] > self.height_ * TILESIZE + (self.height_ - 1) * TILESEPARATE:
            return (-1, -1)
        
        delWidth = pos[0] % (TILESIZE + TILESEPARATE)
        delHeight = pos[1] % (TILESIZE + TILESEPARATE)
        if delWidth > TILESIZE or delHeight > TILESIZE:
            return (-1, -1)
        
        posX = pos[0] // (TILESIZE + TILESEPARATE)
        posY = pos[1] // (TILESIZE + TILESEPARATE)
        
        return (posY, posX)
    
    def badTile(self, posX, posY):
        if posX < 0 or posX >= self.height_ or posY < 0 or posY >= self.width_:
            return true
        return false
    
    def isDirectIn(self, posX, posY, Dir):
        if self.badTile(posX, posY):
            return false
        myNeigh = []
        for i in neigh[self.tiles[posX][posY].tileType_]:
            myNeigh.append(i)
        myTurn = self.tiles[posX][posY].tilePos_
        for i in range(len(myNeigh)):
            myNeigh[i] = (myNeigh[i] + myTurn) % 4       
            
        if Dir in myNeigh:
            return true
        return false
    
    def checkTile(self, posX, posY):
        if self.badTile(posX, posY):
            return 0
        myNeigh = []
        for i in neigh[self.tiles[posX][posY].tileType_]:
            myNeigh.append(i)
        myTurn = self.tiles[posX][posY].tilePos_
        for i in range(len(myNeigh)):
            myNeigh[i] = (myNeigh[i] + myTurn) % 4
        
        for i in myNeigh:
            if not self.isDirectIn(posX + dx[i], posY + dy[i], invertDir(i)):
                return 1
        
        return 0
    
    def checkTiles(self, posX, posY):
        return self.checkTile(posX, posY) + self.checkTile(posX - 1, posY) + self.checkTile(posX + 1, posY) + self.checkTile(posX, posY - 1) + self.checkTile(posX, posY + 1)
    
    def hint(self):
        for i in range(self.height_):
            for q in range(self.width_):
                if self.checkTile(i, q) == 0:
                    self.badtiles.append((i, q))
    
    
    def handleEvent(self, eventObj):
        if eventObj.type not in (MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self.visible_:
            return []
        
        retVal = []
        
        pos = eventObj.pos
        
        hasExited = false
        if eventObj.type == MOUSEBUTTONDOWN:
            self.lastTileDown = self.getTile(pos)
        elif eventObj.type == MOUSEBUTTONUP:
            if self.getTile(pos) == self.lastTileDown and self.lastTileDown != (-1, -1) and len(self.lastTileDown) == 2 and not self.badTile(self.lastTileDown[0], self.lastTileDown[1]):
                
                self.turnCount += 1
                
                self.badtiles.clear()
                
                tilesWasBad = self.checkTiles(self.lastTileDown[0], self.lastTileDown[1])
                
                self.tiles[self.lastTileDown[0]][self.lastTileDown[1]].turn()
                
                tilesAreBad = self.checkTiles(self.lastTileDown[0], self.lastTileDown[1])
                
                self.badTilesCount += (tilesAreBad - tilesWasBad)
                #print(self.badTilesCount)
                if self.badTilesCount == 0:
                    
                    timeSpent = time() - self.timeBegin
                    self.Score = int(5000 - self.turnCount * 6 - timeSpent * 10) * 10
                    setScore(self.Score)
                    #print(self.Score)
                    
                    retVal.append('finished')
                    
                    self.finished_ = true
                    
        return retVal
                
            