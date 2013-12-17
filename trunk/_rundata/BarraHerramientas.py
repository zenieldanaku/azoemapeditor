from widgets import barra_menu
from renderer import Renderer
from constantes import *

class barraHerramientas (barra_menu.BarraMenu):
    def __init__(self):
        nombre = 'BarraHerramientas'
        x,y = 0,C
        w,h = 24*C,1*C
                
        super().__init__(nombre,x,y,w,h)
        Renderer.addWidget(self)