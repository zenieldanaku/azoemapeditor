from pygame import Rect,Surface,draw, Color
from widgets import BaseWidget
from renderer import Renderer
from constantes import *
from colores import color as k

class PanelSimbolos(BaseWidget):
    x,y,w,h = 0,0,0,0
    
    def __init__(self,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysElmFace'
        if 'colorGrilla' not in opciones:
            opciones['colorGrilla'] = Color(150,200,200)
        if 'colorMarco' not in opciones:
            opciones['colorMarco'] = Color(0,0,0)
        super().__init__(**opciones)
        self.x,self.y = 18*C-1,2*C,
        self.w,self.h = 6*C,16*C-1
        self.nombre = 'panel_simbolos'
        self.image = self.dibujar_grilla()
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        Renderer.addWidget(self)
    
    def dibujar_grilla(self):
        grilla_surf = Surface((self.w,self.h))
        grilla_surf.fill(k(self.opciones['colorFondo']))
        marco = Rect(0,0,self.w-1,self.h-1)
        for i in range(1*C,16*C,C):
            draw.line(grilla_surf, k(self.opciones['colorGrilla']), (i,marco.top), (i,marco.bottom),1)
            draw.line(grilla_surf, k(self.opciones['colorGrilla']), (marco.left,i), (marco.right,i),1)
        draw.rect(grilla_surf, k(self.opciones['colorMarco']), marco, 2)
        
        return grilla_surf