from widgets import barra_menu
from renderer import Renderer
from constantes import *

class barraMenus (barra_menu.BarraMenu):
    def __init__(self):
        nombre = 'Barra_Menus'
        x,y = 0,0
        w,h = 24*C,1*C
        botones = ['Archivo','Editar','Mapa','Símbolo']
        
        super().__init__(nombre,x,y,w,h,botones)
        Renderer.addWidget(self)