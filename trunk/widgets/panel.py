from .basewidget import BaseWidget
from constantes import *
from pygame import Rect,Surface,draw

class PanelSimbolos(BaseWidget):
    x,y,w,h = 0,0,0,0
    def __init__(self,x,y,w,h):
        super().__init__()
        self.nombre = 'panel_simbolos'
        self.rect = Rect(x,y,w,h)
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.image = self.dibujar_grilla()
    
    def dibujar_grilla(self):
        grilla_surf = Surface((self.w,self.h))
        grilla_surf.fill(gris)
        marco = Rect(0,0,self.w-1,self.h-1)
        for i in range(1*C,16*C,C):
            draw.line(grilla_surf, cian_oscuro, (i,marco.top), (i,marco.bottom),1)
            draw.line(grilla_surf, cian_oscuro, (marco.left,i), (marco.right,i),1)
        draw.rect(grilla_surf, negro, marco, 2)
        
        return grilla_surf