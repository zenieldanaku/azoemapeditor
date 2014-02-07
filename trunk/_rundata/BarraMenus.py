from widgets import BarraMenu
from renderer import Renderer
from constantes import *
from .menus import *

class barraMenus (BarraMenu):
    menus = {}
    def __init__(self):
        nombre = 'Barra_Menus'
        self.menus = {}
        x,y = 0,0
        w,h = 24*C,1*C
        super().__init__(nombre,x,y,w,h)
        prev  = 0
        for menu_nom in ['Archivo','Editar','Mapa','Simbolo']:
            menu = eval('Menu_'+menu_nom+'(prev+4,6,self)')
            prev = menu.boton.rect.right
            self.menus['Menu '+menu_nom] = menu
        Renderer.addWidget(self)
    
    def onFocusIn(self,_menu=None):
        super().onFocusIn()
        if _menu != None:
            for menu in self.menus:
                self.menus[menu].hideMenu()
            self.menus[_menu.nombre].showMenu()
        
    def onFocusOut(self):
        super().onFocusOut()
        for menu in self.menus:
            self.menus[menu].hideMenu()