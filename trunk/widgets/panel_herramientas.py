from .basewidget import BaseWidget
from constantes import *
from pygame import Surface,draw

class PanelHerramientas(BaseWidget):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.nombre = 'herramientas'
        self.image = Surface((w,h))
        self.image.fill(gris)
        self.rect = self.image.get_rect(topleft=(x,y))
        draw.rect(self.image,negro,(0,0,w-2,h-2),2)