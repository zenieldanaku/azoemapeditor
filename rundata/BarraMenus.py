from azoe import EventHandler, color, Marco
from pygame import Surface,draw
from globales import C
from .menus import *

class barraMenus (Marco):
    menus = {}
    layer = 1
    def __init__(self, **opciones):
        self.nombre = 'Barra_Menus'
        super().__init__(0,0,24*C,19,False,**opciones)
        
        self.menus = {}
        self.image.fill(color(opciones.get('colorFondo', 'sysMenBack')))
        prev  = 0
        for menu_nom in ['Archivo','Editar','Mapa']:
            menu = eval('Menu_'+menu_nom+'(self,prev,3)')
            prev = menu.boton.rect.right
            self.menus[menu.nombre] = menu
   
    def on_focus_in(self):
        super().on_focus_in()
        self.ocultarMenus()
        
    def on_focus_out(self):
        super().on_focus_out()
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
    
    def update(self):
        for menu in self.menus:
            self.menus[menu].update()
    