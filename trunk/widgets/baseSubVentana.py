from pygame import Rect, font
from libs.textrect import render_textrect
from . import Marco

class subVentana(Marco):
    x,y,w,h = 0,0,0,0
    layer = 3
    
    def __init__(self,x,y,w,h,**opciones):      
        super().__init__(x,y,w,h,**opciones)
        self.titular(self.nombre)
    
    def titular(self,texto):
        fuente = font.SysFont('verdana',12)
        rect = Rect(2,2,self.w-4,fuente.get_height()+1)
        render = render_textrect(texto,fuente,rect,(255,255,255),(0,0,0))
        self.image.blit(render,rect)