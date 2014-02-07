from widgets import BaseWidget, BotonMenu, OpcionMenu
from pygame.sprite import LayeredDirty,DirtySprite
from pygame import Surface,Rect
from constantes import *
from renderer import Renderer

class BaseMenu (BaseWidget):
    opciones = None
    _visible = 0
    nombre = ''
    def __init__(self,nombre,ops,x,y):
        super().__init__()
        self.boton = BotonMenu(self,nombre,x,y)
        self.opciones = LayeredDirty()
        Renderer.addWidget(self.boton,4)
        alto,ancho,h = 0,0,self.boton.rect.h
        for n in range(len(ops)):
            _nom = ops[n]['nom']
            _cmd = ops[n]['cmd']
            _pos = x,(n+1)*h+5
            opcion = OpcionMenu(_nom,_pos,_cmd,self)
            w,h = opcion.image.get_size()
            alto += h+1
            if w > ancho: ancho = w
            self.opciones.add(opcion)
        
        image = Surface((ancho,alto))
        image.fill(gris)
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,self.boton.h))
        self._visible = 0
        Renderer.addWidget(self,2)
        for op in self.opciones:
            Renderer.addWidget(op,2)
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
    
    def onFocusOut(self):
        super().onFocusOut()
        self.hideMenu()