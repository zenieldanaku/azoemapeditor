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
        self.descripcion = descripcion
        
        self.img_uns = self._crear(texto,negro,gris, gris_oscuro_bisel,gris_claro_bisel)
        self.img_sel = self._crear(texto,cian_claro,gris, gris_oscuro_bisel,gris_claro_bisel)
        self.img_pre = self._crear(texto,cian_claro,gris, gris_claro_bisel,gris_oscuro_bisel)
        
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(x,y))
    
    def  _crear(self, texto, color_texto, color_fondo, color_marco1, color_marco2):
        fuente = font.SysFont('verdana',16)
        rect = Rect(0,0,28,25)
        render = render_textrect(texto,fuente,rect,color_texto,color_fondo,1)
        draw.line(render, color_marco1, (0,rect.h-3),(rect.w-3,rect.h-3), 2)
        draw.line(render, color_marco1, (rect.w-3,rect.h-2),(rect.w-3,0), 2)
        draw.lines(render, color_marco2, False, [(rect.w-2,0),(0,0),(0,rect.h-4)], 2)
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
        
    def onMouseIn(self):
        super().onMouseIn()
        self.serElegido()

    def onMouseOut(self):
        super().onMouseOut()
        self.serDeselegido()
        
    def onMouseDown(self,button):
        if button == 1:
            self.serPresionado()
    
    def onMouseUp(self, dummy):
        self.serElegido()

    def __repr__(self):
        return 'Boton '+self.nombre