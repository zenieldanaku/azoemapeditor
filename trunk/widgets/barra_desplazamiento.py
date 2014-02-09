from pygame import Rect,Surface,mouse
from .basewidget import BaseWidget
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
    
    def onMouseDown(self,button):
        if button == 1:
            self.cursor.pressed = True
    
    def onMouseUp(self,button):
        if button == 1:
            if self.cursor.pressed:
                self.cursor.pressed = False
                x,y = mouse.get_pos()
                dx,dy = self.redibujar(x,y)
                self.cursor.reposisionar(dx,dy)
    
    def onMouseOver(self):
        if self.cursor.pressed:
            x,y = mouse.get_pos()
            dx,dy = self.redibujar(x,y)
            self.cursor.reposisionar(dx,dy)

class Cursor(BaseWidget):
    size = 0,0
    pressed = False
    def __init__(self,macro):
        self.size = 1/2*C,1/2*C
        super().__init__()
        self.image = Surface(self.size)
        self.image.fill(violeta)
        self.rect = self.image.get_rect()
        self.pressed = False
        self.dirty = 2
        self.barra = macro
        
        if self.barra.w > self.barra.h:
            self.nombre = 'cursor_H'
        else:
            self.nombre = 'cursor_V'
    
    def reposisionar(self,x,y):
        self.rect.x = x
        self.rect.y = y
        self.dirty = 2
        return self.rect.x,self.rect.y 