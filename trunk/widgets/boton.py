from libs.textrect import render_textrect
from pygame import font,Rect,draw
from . import BaseWidget
from constantes import *

class Boton(BaseWidget):
    comando = None
    def __init__(self,x,y,nombre,cmd,texto,descripcion=''):
        super().__init__()
        self.x,self.y = x,y
        self.nombre = nombre
        self.comando = cmd
        self.img_uns = self._crear(texto,negro,negro)
        self.img_sel = self._crear(texto,cian_claro,negro)
        self.img_pre = self._crear(texto,cian_claro,blanco)
        self.descripcion = descripcion
        
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(x,y))
    
    def  _crear(self,texto,color,color_marco):
        fuente = font.SysFont('verdana',16)
        rect = Rect(0,0,28,25)
        render = render_textrect(texto,fuente,rect,color,gris,1)
        marco = Rect(rect.topleft,(rect.w-2,rect.h-2))
        draw.rect(render,color_marco,marco,2)
        return render
    
    def serElegido(self):
        self.image = self.img_sel
    
    def serDeselegido(self):
        self.image = self.img_uns
    
    def serPresionado(self):
        self.image = self.img_pre
        self.comando()
    
    def update(self):
        self.dirty = 1
        
    def onMouseOver(self):
        self.serElegido()

    def onMouseOut(self):
        self.serDeselegido()
        
    def onMouseDown(self,button):
        if button == 1:
            self.serPresionado()
    
    def onMouseUp(self, dummy):
        self.serElegido()

    def __repr__(self):
        return 'Boton '+self.nombre