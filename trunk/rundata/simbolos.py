from widgets import BaseWidget
from constantes import *
from pygame import Rect,Surface,draw
from renderer import Renderer

class PanelSimbolos(BaseWidget):
    x,y,w,h = 0,0,0,0
    
    def __init__(self):
        super().__init__()
        self.x,self.y = 18*C-1,2*C,
        self.w,self.h = 6*C,16*C-1
        self.nombre = 'panel_simbolos'
        self.image = self.dibujar_grilla()
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        Renderer.addWidget(self)
    
    def dibujar_grilla(self):
        grilla_surf = Surface((self.w,self.h))
        grilla_surf.fill(gris)
        marco = Rect(0,0,self.w-1,self.h-1)
        for i in range(1*C,16*C,C):
            draw.line(grilla_surf, cian_oscuro, (i,marco.top), (i,marco.bottom),1)
            draw.line(grilla_surf, cian_oscuro, (marco.left,i), (marco.right,i),1)
        draw.rect(grilla_surf, negro, marco, 2)
        
        return grilla_surf