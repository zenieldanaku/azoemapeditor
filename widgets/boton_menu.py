from .basewidget import BaseWidget
from libs.textrect import render_textrect
from pygame import Rect,font,mouse
from constantes import *

class boton_menu(BaseWidget):
    nombre = ''
    menu = None
    resaltado = False
    
    def __init__(self,nombre,x,y):
        super().__init__()
        self.nombre = nombre
        self.layer = 2
        self.img_des = self.crear_boton(self.nombre,negro)
        self.img_sel = self.crear_boton(self.nombre,cian_claro)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.menu = self.establecer_menus(nombre)
        self.dirty = 1
        
    def establecer_menus (self,nombre):
        # esto es chapuza
        if nombre == 'Archivo': 
            menu_nom = ['Nuevo','Abrir...','Guardar','Guardar como...','Cerrar']
        elif nombre == 'Editar':
            menu_nom = ['Preferencias...']
        elif nombre == 'Mapa':
            menu_nom = ['Grilla...','Capas...']
        elif nombre == 'Símbolo':
            menu_nom = ['Mobs...','Props...']
        else:
            menu_nom = ['']
        
        if menu_nom != ['']:
            from .pull_down_menu import PullDownMenu
            # esto evita una referencia circular
            return PullDownMenu(menu_nom,*self.rect.bottomleft)
    
    def crear_boton(self,nombre,color):
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,color,gris,1)
        return render

    def onMouseDown (self,event):
        if event.button == 1:
            x,y = mouse.get_pos()
            if self.rect.collidepoint(x,y):
                if self.menu != None:
                    if self.menu.visible != True:
                        self.menu.visible = True
                        for boton in self.menu.botones:
                            boton.visible = True
                            boton.enabled = True
                    else:
                        self.menu.visible = False
                        for boton in self.menu.botones:
                            boton.visible = False
                            boton.enabled = False
                    self.dirty = 1
    
    def onFocusOut(self):
        super().onFocusOut()
        if self.menu != None:
            self.menu.visible = False
            for boton in self.menu.botones:
                boton.visible = False
            self.dirty = 1
    
    def onMouseOver(self,event):
        self.image = self.img_sel
        self.dirty = 1
    
    def onMouseOut(self):
        self.image = self.img_des
        self.dirty = 1