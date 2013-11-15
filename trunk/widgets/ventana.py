from .basewidget import BaseWidget
from pygame import Rect,Surface
from constantes import *

class Ventana(BaseWidget):
    def __init__(self,tamanio):
        super().__init__()
        self.rect = Rect((0,0),tamanio)
        self.nombre = 'ventana'
        self.image = Surface(self.rect.size)
        self.image.fill(gris)