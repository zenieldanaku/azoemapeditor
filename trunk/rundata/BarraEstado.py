from pygame import Rect,Surface,draw
from globales import GLOBALES as G
from widgets import Marco, Label
from renderer import Renderer
from colores import color
from constantes import *

class barraEstado (Marco):
    _estado = ''
    lblEstado = None
    
    def __init__(self,**opciones):
        super().__init__(0,19*C,24*C,1*C,**opciones)
        self.nombre = 'BarraEstado'
        self._estado = ''
        self.lblEstado = Label(self,'Estado',self.x+4,self.y+5)
        self.draw_area = Rect(4,5,self.w-8,self.h-8)
        Renderer.addWidget(self)
        Renderer.addWidget(self.lblEstado,2)
    
    def mostrar_estado(self,mensaje):
        bgcolor = color(self.opciones.get('colorFondo', 'sysElmFace'))
        if mensaje != self._estado:
            self._estado = mensaje
            self.image.fill(bgcolor,self.draw_area)
            self.lblEstado.setText(mensaje)
            
    def update(self):
        msj = G.estado
        self.mostrar_estado(msj)
        self.dirty = 1
    