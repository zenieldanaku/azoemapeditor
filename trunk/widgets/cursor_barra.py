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
    
    def reposisionar(self,var):
        if self.barra.w > self.barra.h:
            self.rect.x = var
        else:
            self.rect.y = var
        self.image.fill(verde) # cuadro negro, issue 1
        self.dirty = 2
        return self.rect.x,self.rect.y 