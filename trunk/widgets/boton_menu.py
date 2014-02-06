from .basewidget import BaseWidget
from libs.textrect import render_textrect
from pygame import Rect,font,mouse
from constantes import *

class BotonMenu(BaseWidget):
    nombre = ''
    menu = None
    command = None
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
        self.dirty = 1
    
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
                elif self.command != None:
                    print('command!')
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