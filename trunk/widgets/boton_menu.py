from .basewidget import BaseWidget
from libs.textrect import render_textrect
from pygame import Rect,font,mouse
from constantes import *

class BotonMenu(BaseWidget):
    nombre = ''
    menu = None
    
    def __init__(self,menu,nombre,x,y):
        super().__init__()
        self.nombre = nombre
        self.menu = menu
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
        
    def onMouseDown (self,button):
        if button == 1:
            self.menu.barra.onFocusIn(self.menu)
            
    def onFocusOut(self):
        self.menu.onFocusOut()
        super().onFocusOut()
   
    def onMouseOver(self):
        self.image = self.img_sel
    
    def onMouseOut(self):
        self.image = self.img_des
    
    def update(self):
        self.dirty = 1
    