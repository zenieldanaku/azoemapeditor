from pygame import Rect, font, mouse
from libs.textrect import render_textrect
from . import Marco, Boton
from globales import EventHandler, ANCHO, ALTO

class subVentana(Marco):
    x,y,w,h = 0,0,0,0
    layer = 4
    pressed = False
    def __init__(self,w,h,nombre,titular=True,**opciones):
        _r = Rect(0,0,w,h)
        _r.center=Rect(0,0,ANCHO,ALTO).center
        x,y = _r.topleft
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
    
    def onMouseOver(self):
        x,y = mouse.get_pos()
        rect = Rect(self.x+2,self.y+2,self.w-4,17)
        if rect.collidepoint((x,y)):
            if self.pressed:
                print('ajá!')
    
    def onMouseDown(self,button): self.pressed = True
    def onMouseUp(self,button):   self.pressed = False
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()