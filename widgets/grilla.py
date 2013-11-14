from .basewidget import BaseWidget
from pygame import Surface,Rect,draw
from constantes import *

class Grilla(BaseWidget):
    x,y,w,h = 0,0,0,0
    
    def __init__(self,x,y,w,h):
        super().__init__()
        self.w,self.h = w,h
        self.x,self.y = x,y
        self.image = self.dibujar_grilla()
        self.rect = self.image.get_rect(topleft=(x,y))
    
    def dibujar_grilla(self):
        grilla_surf = Surface((self.w,self.h))
        grilla_surf.fill(gris)
        marco = Rect(0,0,self.w,self.h)
        for i in range(1*C,16*C,C):
            draw.line(grilla_surf, blanco, (i,marco.top), (i,marco.bottom),1)
            draw.line(grilla_surf, blanco, (marco.left,i), (marco.right,i),1)
        draw.rect(grilla_surf, negro, marco, 2)
        
        return grilla_surf
    
    def redibujar(self):
        self.image = dibujar_grilla()
