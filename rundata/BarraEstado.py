from widgets import BaseWidget, Label
from renderer import Renderer
from constantes import *
from pygame import Rect,Surface,draw
from globales import GLOBALES as G

class barraEstado (BaseWidget):
    _estado = ''
    
    def __init__(self):
        super().__init__()
        self.nombre = 'estado'
        self.x,self.y = 0,19*C
        self.w,self.h = 24*C,1*C
        self.image = Surface((self.w,self.h))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.image.fill(gris)
        draw.rect(self.image,negro,(0,0,self.w-2,self.h-2),2)
        Renderer.addWidget(self)
        self.draw_area = Rect(4,5,self.w-8,self.h-8)
        self._estado = ''
    
    def mostrar_estado(self,mensaje):
        if mensaje != self._estado:
            self._estado = mensaje
            self.image.fill(gris,self.draw_area)
            estado = Label(mensaje)
            self.image.blit(estado.image, self.draw_area)
            
    def update(self):
        msj = G.estado
        self.mostrar_estado(msj)
        self.dirty = 1
    