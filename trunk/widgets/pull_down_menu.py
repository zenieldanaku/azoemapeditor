from .basewidget import BaseWidget
from pygame.sprite import LayeredDirty
from pygame import Surface
from constantes import *
from renderer import Renderer
from .boton_menu import boton_menu

class PullDownMenu (BaseWidget):
    botones = None
    def __init__(self,nombres,x,y):
        self.botones = LayeredDirty()
        alto,ancho = 0,0
        h = 0
        for n in range(len(nombres)):
            boton = boton_menu(nombres[n],x,((h+1)*n)+y)
            w,h = boton.image.get_size()
            alto += h+1
            if w > ancho: ancho = w
            self.botones.add(boton)
            boton.visible = False
            boton.enabled = False
            Renderer.addWidget(boton,3)
        
        super().__init__()
        image = Surface((ancho,alto))
        image.fill(gris)
        self.image = image
        self.rect = self.image.get_rect(topleft = (x,y))
        Renderer.addWidget(self,2)
        self.visible = False
        self.dirty = 2