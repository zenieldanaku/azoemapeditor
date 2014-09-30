from pygame import Rect, font
from libs.textrect import render_textrect
from . import Marco, Boton
from globales import EventHandler

class subVentana(Marco):
    x,y,w,h = 0,0,0,0
    layer = 4
    
    def __init__(self,x,y,w,h,nombre,titular=True,**opciones):
        super().__init__(x,y,w,h,**opciones)
        if titular:
            self.titular(nombre)
        self.btnCerrar = Boton(self,x+w-16,y+1,'Cerrar',
                               lambda:EventHandler.delWidget(self),'X',
                               **{'fontSize':12,'w':16,'h':18})
        self.agregar(self.btnCerrar)
    
    def titular(self,texto):
        fuente = font.SysFont('verdana',12)
        rect = Rect(2,2,self.w-4,fuente.get_height()+1)
        render = render_textrect(texto,fuente,rect,(255,255,255),(0,0,0))
        self.image.blit(render,rect)