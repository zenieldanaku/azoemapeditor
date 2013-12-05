from .basewidget import BaseWidget
from constantes import *
from pygame import Rect,Surface,draw
from pygame.sprite import LayeredDirty
from renderer import Renderer
from .boton_menu import boton_menu

class Menu_barra(BaseWidget):
    botones = None
    
    def __init__(self,nom_menu,x,y,w,h,botones):
        super().__init__()
        self.botones = LayeredDirty()
        self.nombre = nom_menu
        self.rect = Rect(x,y,w,h)
        self.image = Surface(self.rect.size)
        self.image.fill(gris)
        draw.rect(self.image,negro,(0,0,w-2,h-2),2)
        
        prev  = 0
        for btn in botones:
            boton = boton_menu(btn,prev+4,6)
            prev = boton.rect.right
            self.botones.add(boton)
            Renderer.addWidget(boton,2)
        
        self.botones.draw(self.image)