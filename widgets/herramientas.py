from .basewidget import BaseWidget
from constantes import *
from pygame import Rect,Surface,draw

class Herramientas(BaseWidget):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.nombre = 'herramientas'
        self.rect = Rect(x,y,w,h)
        self.image = Surface(self.rect.size)
        self.image.fill(gris)
        draw.rect(self.image,negro,(0,0,w-2,h-2),2)