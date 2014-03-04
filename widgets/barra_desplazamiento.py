from pygame import Rect,Surface,mouse
from .basewidget import BaseWidget
from constantes import *

class Scroll(BaseWidget):
    parent = None
    cursor = None    
    def __init__(self,x,y,w,h,parent):
        super().__init__()
        self.parent = parent
        self.image = Surface((w,h))
        self.image.fill(blanco)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.x,self.y = x,y
        self.w,self.h = h,w
        if self.w > self.h:
            self.nombre = 'barra_H'
            rx,ry = 0,self.w//2
        else:
            self.nombre = 'barra_V'
            rx,ry = self.h//2,0
            
        self.cursor = Cursor(self,rx,ry)
        
    def redibujar(self,x,y):
        self.image.fill(blanco)
        if self.w > self.h:
            dx,dy = 0,y-(self.y+8)
            x,y = self.x,y-8
        else:
            dx,dy = x-(self.x+8),0
            x,y = x-8,self.y
        self.image.blit(self.cursor.image,(dx,dy))
        self.cursor.relx,self.cursor.rely = dx,dy
        return x,y
    
    def onMouseDown(self,button):
        if button == 1:
            self.cursor.pressed = True
    
    def onMouseUp(self,button):
        if button == 1:
            if self.cursor.pressed:
                self.cursor.pressed = False
                x,y = mouse.get_pos()
                dx,dy = self.redibujar(x,y)
                self.cursor.reposicionar(dx,dy)
    
    def onMouseOver(self):
        if self.cursor.pressed:
            x,y = mouse.get_pos()
            dx,dy = self.redibujar(x,y)
            self.cursor.reposicionar(dx,dy)
    
    def update(self):
        self.dirty = 1

class Cursor(BaseWidget):
    size = 0,0
    pressed = False
    relx,rely = 0,0
    def __init__(self,macro,rx,ry):
        super().__init__()
        self.size = 1/2*C,1/2*C
        self.relx,self.rely = rx,ry
        self.image = Surface(self.size)
        self.image.fill(violeta)
        self.rect = self.image.get_rect()
        self.pressed = False
        self.dirty = 1
        self.barra = macro
        self.barra.image.blit(self.image,[rx,ry])
        
        if self.barra.w > self.barra.h:
            self.nombre = 'cursor_H'
        else:
            self.nombre = 'cursor_V'
    
    def reposicionar(self,x,y):
        self.rect.x = x
        self.rect.y = y
        self.dirty = 1