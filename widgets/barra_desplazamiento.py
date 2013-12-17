from pygame import Rect,Surface,mouse
from .basewidget import BaseWidget
from .cursor_barra import Cursor
from constantes import *

class Scroll(BaseWidget):
    cursor = None
    
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = Surface((w,h))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.image.fill(blanco)
        self.x,self.y = x,y
        self.w,self.h = h,w
        if self.w > self.h:
            self.nombre = 'barra_H'
        else:
            self.nombre = 'barra_V'
        self.cursor = Cursor(self)
        self.crear_cursor()
        self.dirty = 2
        
    def crear_cursor(self):
        if self.w > self.h: # horizontal
            pos = (0,self.w/2)
            tl = self.x,self.w/2+2*C
        else: # vertical
            pos = (self.h/2,0)
            tl = self.h/2+2*C+2,self.y
            #no sé porque tiene que ser tan complicada esa función...
        
        cursor_rect = Rect(pos,self.cursor.rect.size)
        self.image.blit(self.cursor.image,cursor_rect)
        self.cursor.rect.topleft = tl
    
    def redibujar(self,x,y):
        size = self.cursor.rect.size
        self.image.fill(blanco)
        if self.w > self.h:
            dx,dy = 0,y-(self.y+8)
            x,y = self.x,y-8
        else:
            dx,dy = x-(self.x+8),0
            x,y = x-8,self.y
        self.image.blit(self.cursor.image,((dx,dy),size))
        self.dirty = 2
        return x,y
    
    def onMouseDown(self,event):
        if event.button == 1:
            x,y = mouse.get_pos()
            if self.cursor.rect.collidepoint(x,y):
                self.cursor.pressed = True
    
    def onMouseUp(self,event):
        if event.button == 1:
            x,y = mouse.get_pos()
            if self.rect.collidepoint(x,y):
                if self.cursor.pressed:
                    self.cursor.pressed = False
                    dx,dy = self.redibujar(x,y)
                    self.cursor.reposisionar(dx,dy)