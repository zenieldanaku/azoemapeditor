from widgets import BarraMenu
from renderer import Renderer
from constantes import *

class barraEstado (BarraMenu):
    def __init__(self):
        nombre = 'estado'
        x,y = 0,19*C
        w,h = 24*C,1*C
                
        super().__init__(nombre,x,y,w,h)
        Renderer.addWidget(self)