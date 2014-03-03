from widgets import BaseWidget, OpcionMenu
from pygame.sprite import LayeredDirty
from pygame import Surface
from constantes import *
from renderer import Renderer

class CascadaMenu (BaseWidget):
    opciones = None
    
    def __init__(self,opciones,x,y,h,j=0):
        super().__init__()
        self.opciones = LayeredDirty()
        alto,ancho, = 0,0
        for n in range(len(opciones)):
            _nom = opciones[n]['nom']
            dy = (n+1)*h+5+j
            if 'cmd' in opciones[n]:
                opt = opciones[n]['cmd']
            else:
                opt = None
            opcion = OpcionMenu(_nom,[x,dy],opt,self)
            w,h = opcion.image.get_size()
            if 'csc' in opciones[n]:
                opcion.command = CascadaMenu(opciones[n]['csc'],x+w+1,dy,dy-5,h)
            alto += h+1
            if w > ancho: ancho = w
            self.opciones.add(opcion)

        image = Surface((ancho,alto-7))
        image.fill(gris)
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y+5))
        self._visible = 0
        Renderer.addWidget(self,3)
        for op in self.opciones:
            Renderer.addWidget(op,3)
        self.dirty = 2
    
    def showMenu(self):
        self._visible = 1
        for opcion in self.opciones:
            opcion._visible = True
            opcion.enabled = True
            opcion.focusable = True
    
    def hideMenu(self):
        self._visible = 0
        for opcion in self.opciones:
            opcion._visible = False
            opcion.enabled = False
            opcion.focusable = False