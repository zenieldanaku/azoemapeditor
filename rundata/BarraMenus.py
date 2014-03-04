from widgets import BaseWidget
from renderer import Renderer
from constantes import *
from .menus import *
from pygame import Surface,draw

class barraMenus (BaseWidget):
    menus = {}
    def __init__(self):
        super().__init__()
        nombre = 'Barra_Menus'
        self.menus = {}
        self.x,self.y = 0,0
        self.w,self.h = 24*C,1*C
        self.image = Surface((self.w,self.h))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.image.fill(gris)
        draw.rect(self.image,negro,(0,0,self.w-2,self.h-2),2)
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