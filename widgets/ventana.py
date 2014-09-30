from pygame import Rect,Surface
from . import BaseWidget
from globales import color, EventHandler

class Ventana(BaseWidget):
    focusable = False
    def __init__(self,tamanio,**opciones):
        super().__init__(**opciones)
        self.rect = Rect((0,0),tamanio)
        self.nombre = 'ventana'
        self.image = Surface(self.rect.size)
        self.image.fill(color(opciones.get('colorFondo', 'sysElmFace')))
        EventHandler.addWidget(self,0)
        EventHandler.currentFocus = self