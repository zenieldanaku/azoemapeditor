from .basewidget import BaseWidget
from libs.textrect import render_textrect
from pygame import Rect,font
from constantes import *

class OpcionMenu(BaseWidget):
    nombre = ''
    
    def __init__(self,nombre,pos,cmd,menu):
        super().__init__()
        self.nombre = nombre
        self.visible = False
        self.enabled = False
        self.focusable = False
        self.command = cmd
        self.menu = menu
        self.img_des = self.crear(self.nombre,negro)
        self.img_sel = self.crear(self.nombre,cian_claro)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1
    
    def crear(self,nombre,color):
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,color,gris,1)
        return render
    
    def onMouseOver(self):
        from .cascada_menu import CascadaMenu
        if self.enabled:
            self.image = self.img_sel
            if isinstance(self.command,CascadaMenu):
                self.command.showMenu()
    
    def onMouseOut(self):
        self.image = self.img_des
    
    def onMouseDown(self,button):
        self.comando()
        self.menu.hideMenu()
    
    def onFocusOut(self):
        super().onFocusOut()
        self.enabled=False
    
    def onFocusIn(self):
        super().onFocusIn()
        self.comando()
        self.menu.hideMenu()
    
    def comando (self):
        from .cascada_menu import CascadaMenu
        if isinstance(self.command,CascadaMenu):
            self.command.showMenu()
        else:
            self.command()