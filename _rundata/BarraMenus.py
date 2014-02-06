from widgets import BarraMenu
from renderer import Renderer
from constantes import *
from .menus import *

class barraMenus (BarraMenu):
    def __init__(self):
        nombre = 'Barra_Menus'
        x,y = 0,0
        w,h = 24*C,1*C
        super().__init__(nombre,x,y,w,h)
        prev  = 0
        for menu_nom in ['Archivo','Editar','Mapa','Simbolo']:
            boton = self.establecer_boton(menu_nom,prev+4,6)
            prev = boton.rect.right
            boton.menu = eval('Menu_'+menu_nom+'(*boton.rect.bottomleft)')
        self.botones.draw(self.image)
        Renderer.addWidget(self)