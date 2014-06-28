from pygame import Rect,Surface
from . import BaseWidget
from globales import color

class Ventana(BaseWidget):
    def __init__(self,tamanio,**opciones):
        super().__init__(**opciones)
        self.rect = Rect((0,0),tamanio)
        self.nombre = 'ventana'
        self.image = Surface(self.rect.size)
        self.image.fill(color(opciones.get('colorFondo', 'sysElmFace')))
        self.focusable = False