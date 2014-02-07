from widgets import BaseWidget, BotonMenu
from pygame.sprite import LayeredDirty
from pygame import Surface
from constantes import *
from renderer import Renderer

class BaseMenu (BaseWidget):
    botones = None
    visible = 0
    nombre = ''
    def __init__(self,nombres,x,y):
        super().__init__()
        self._visible = 0
        self.botones = LayeredDirty()
        alto,ancho = 0,0
        h = 0
        for n in range(len(nombres)):
            boton = BotonMenu(nombres[n],x,((h+1)*n)+y)
            w,h = boton.image.get_size()
            alto += h+1
            if w > ancho: ancho = w
            self.botones.add(boton)
            boton.visible = 0
            boton.enabled = False
            Renderer.addWidget(boton,3)
        
        image = Surface((ancho,alto))
        image.fill(gris)
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))
        Renderer.addWidget(self,2)
        self.dirty = 2