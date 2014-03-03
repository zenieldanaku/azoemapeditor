from .basewidget import BaseWidget
from pygame import Surface,Rect,draw
from constantes import *
from globales import GLOBALES as G

class Grilla(BaseWidget):
    x,y,w,h = 0,0,0,0
    
    def __init__(self,x,y,w,h):
        super().__init__()
        self.w,self.h = w,h
        self.x,self.y = x,y
        self.image = Surface((self.w,self.h))
        self.image.fill(gris)
        self.grilla = self.dibujar_grilla()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.nombre = 'grilla'
    
    def dibujar_grilla(self):
        marco = Rect(0,0,self.w-1,self.h-1)
        for i in range(1*C,16*C,C):
            draw.line(self.image, blanco, (i,marco.top), (i,marco.bottom),1)
            draw.line(self.image, blanco, (marco.left,i), (marco.right,i),1)
        draw.rect(self.image, negro, marco, 2)
    
    def update(self):
        if G.IMG_fondo != None:
            image = G.IMG_fondo
            if image.get_width() > self.w or image.get_height() > self.h:
                image = image.subsurface((0,0,self.w,self.h))
            self.image = image
        else:
            self.image.fill(gris)
        self.dibujar_grilla()
        self.dirty = 1