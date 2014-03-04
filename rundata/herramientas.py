from pygame import Surface,draw
from widgets import BaseWidget
from renderer import Renderer
from constantes import *

class PanelHerramientas(BaseWidget):
    x,y,w,h = 0,0,0,0
    
    def __init__(self):
        super().__init__()
        self.x,self.y = 0,2*C
        self.w,self.h = 2*C,16*C
        self.nombre = 'herramientas'
        self.image = Surface((self.w,self.h))
        self.image.fill(gris)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        draw.rect(self.image,negro,(0,0,self.w-2,self.h-2),2)
        Renderer.addWidget(self)
        