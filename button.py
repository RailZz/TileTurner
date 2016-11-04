import pygame
from pygame.locals import *
import pygbutton
from pybackground import draw_background

true = True
false = False

PYGBUTTON_FONT = pygame.font.SysFont('comicsansms', 20)

BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)


class PygButton(object):
    def __init__(self, rect = None, caption = '', bgcolor = LIGHTGRAY, fgcolor = BLACK, font = None, normal = "button.jpg", down = None, highlight = None):
        if rect is None:
            self._rect = pygame.Rect(0, 0, 30, 60)
        else:
            self._rect = pygame.Rect(rect)
            
        self.caption_ = caption
        self.bgcolor_ = bgcolor
        self.fgcolor_ = fgcolor
        
        if font is None:
            self.font_ = PYGBUTTON_FONT
        else:
            self.font_ = font
            
        self.buttonDown = false
        self.mouseOverButton = false
        self.lastMouseDownOverButton = false
        self.visible_ = true
        self.customSurfaces = false
        
        if normal is None:
            self.surfaceNormal = pygame.Surface(self._rect.size)
            self.surfaceDown = pygame.Surface(self._rect.size)
            self.surfaceHighlight = pygame.Surface(self._rect.size)
            self.update()
        else:
            self.setSurfaces(normal, down, highlight)
        
    
    def setSurfaces(self, normalSurface, downSurface = None, highlightSurface = None):
        if downSurface is None:
            downSurface = normalSurface
        if highlightSurface is None:
            highlightSurface = normalSurface
            
        if type(normalSurface) == str:
            self.origSurfaceNormal = pygame.image.load(normalSurface)
        if type(downSurface) == str:
            self.origSurfaceDown = pygame.image.load(downSurface)
        if type(highlightSurface) == str:
            self.origSurfaceHighlight = pygame.image.load(highlightSurface)        
            
        if self.origSurfaceNormal.get_size() != self.origSurfaceDown.get_size() != self.origSurfaceHighlight.get_size():
            raise Exception('Bad image size')
        
        self.surfaceNormal = self.origSurfaceNormal
        self.surfaceDown = self.origSurfaceDown
        self.surfaceHighlight = self.origSurfaceHighlight
        self.customSurfaces = True
        self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))
    
    def draw(self, surfaceObj):
        if self.visible_:
            if self.buttonDown:
                surfaceObj.blit(self.surfaceDown, self._rect)
            elif self.mouseOverButton:
                surfaceObj.blit(self.surfaceHighlight, self._rect)
            else:
                surfaceObj.blit(self.surfaceNormal, self._rect)
                
    def update(self):
        if self.customSurfaces:
            self.surfaceNormal    = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
            self.surfaceDown      = pygame.transform.smoothscale(self.origSurfaceDown, self._rect.size)
            self.surfaceHighlight = pygame.transform.smoothscale(self.origSurfaceHighlight, self._rect.size)
            return
        
        w = self._rect.width
        h = self._rect.height
        
        self.surfaceNormal.fill(self.bgcolor_)
        self.surfaceDown.fill(self.bgcolor_)
        self.surfaceHighlight.fill(self.bgcolor_)
    
        # draw caption text for all buttons
        captionSurf = self.font_.render(self.caption_, True, self.fgcolor_, self.bgcolor_)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceDown.blit(captionSurf, captionRect)
    
        # draw border for normal button
        pygame.draw.rect(self.surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.surfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))
    
        # draw border for down button
        pygame.draw.rect(self.surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self.surfaceDown, GRAY, (2, 2), (w - 3, 2))
    
        # draw border for highlight button
        self.surfaceHighlight = self.surfaceNormal
        
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
    
    def show(self):
        self.visible_ = true
    
    def hide(self):
        self.visible_ = false
    
    def handleEvent(self, eventObj):
        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self.visible_:
            return []
        
        retVal = []
        
        hasExited = false
        if not self.mouseOverButton and self._rect.collidepoint(eventObj.pos):
            self.mouseOverButton = true
            self.mouseEnter(eventObj)
            retVal.append('enter')
        elif self.mouseOverButton and not self._rect.collidepoint(eventObj.pos):
            self.mouseOverButton = false
            hasExited = true
            
        if self._rect.collidepoint(eventObj.pos):
            if eventObj.type == MOUSEMOTION:
                self.mouseMove(eventObj)
                retVal.append('move')
            elif eventObj.type == MOUSEBUTTONDOWN:
                self.buttonDown = true
                self.lastMouseDownOverButton = true
                self.mouseDown(eventObj)
                retVal.append('down')
        else:
            if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                self.lastMouseDownOverButton = false
                
        doMouseClick = false
        if eventObj.type == MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                doMouseClick = true
            self.lastMouseDownOverButton = false
            
            if self.buttonDown:
                self.buttonDown = false
                self.mouseUp(eventObj)
                retVal.append('up')
                
            if doMouseClick:
                self.buttonDown = false
                self.mouseClick(eventObj)
                retVal.append('click')
        
        if hasExited:
            self.mouseExit(eventObj)
            retVal.append('exit')
        
        return retVal
                