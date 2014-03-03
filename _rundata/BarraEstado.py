from widgets import BarraMenu, Label
from renderer import Renderer
from constantes import *
from pygame import Rect
from globales import GLOBALES as G

class barraEstado (BarraMenu):
    _estado = ''
    
    def __init__(self):
        nombre = 'estado'
        x,y = 0,19*C
        w,h = 24*C,1*C
                
        super().__init__(nombre,x,y,w,h)
        Renderer.addWidget(self)
        self.draw_area = Rect(4,5,w-6,h-8)
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
    