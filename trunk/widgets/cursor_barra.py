from .basewidget import BaseWidget
from pygame import Surface
from constantes import *

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