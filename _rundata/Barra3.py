from widgets import BarraMenu
from renderer import Renderer
from constantes import *

class barra3 (BarraMenu):
    def __init__(self):
        nombre = 'Menu_3'
        x,y = 0,18*C
        w,h = 24*C,1*C
                
        super().__init__(nombre,x,y,w,h)
        Renderer.addWidget(self)