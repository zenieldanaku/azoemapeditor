from globales import Sistema as Sys, EventHandler, C, color
from pygame import Rect,Surface,draw
from widgets import Marco, Label

class barraEstado (Marco):
    _estado = ''
    lblEstado = None
    
    def __init__(self,**opciones):
        self.nombre = 'BarraEstado'
        super().__init__(0,16*C+19,20*C+8,26,**opciones)
        
        self._estado = ''
        self.lblEstado = Label(self,'Estado',self.x+4,self.y+3)
        self.draw_area = Rect(4,3,self.w-8,self.h-8)
        EventHandler.addWidget(self.lblEstado,2)
    
    def mostrar_estado(self,mensaje):
        bgcolor = color(self.opciones.get('colorFondo', 'sysElmFace'))
        if mensaje != self._estado:
            self._estado = mensaje
            self.image.fill(bgcolor,self.draw_area)
            self.lblEstado.setText(mensaje)
            
    def update(self):
        msj = Sys.estado
        self.mostrar_estado(msj)
        self.dirty = 1
    