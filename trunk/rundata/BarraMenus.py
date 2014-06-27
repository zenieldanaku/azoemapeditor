from pygame import Surface,draw
from widgets import Marco
from renderer import Renderer
from constantes import C
from colores import color
from .menus import *

class barraMenus (Marco):
    menus = {}
    def __init__(self, **opciones):
        super().__init__(0,0,24*C,19,False,**opciones)
        self.nombre = 'Barra_Menus'
        self.menus = {}
        self.image.fill(color(opciones.get('colorFondo', 'sysMenBack')))
        prev  = 0
        for menu_nom in ['Archivo','Editar','Mapa','Simbolo']:
            menu = eval('Menu_'+menu_nom+'(prev,3,self)')
            prev = menu.boton.rect.right
            self.menus[menu.nombre] = menu
        Renderer.addWidget(self)
    
    def onFocusIn(self):
        super().onFocusIn()
        self.ocultarMenus()
        
    def onFocusOut(self):
        super().onFocusOut()
        for menu in self.menus:
            self.menus[menu].hideMenu()
    
    def soloUnMenu(self,_menu=None):
        if _menu != None:
            for menu in self.menus:
                if menu != _menu.nombre:
                    self.menus[menu].hideMenu()
        self.menus[_menu.nombre].showMenu()
    
    def ocultarMenus(self):
        for menu in self.menus:
            self.menus[menu].hideMenu()