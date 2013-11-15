from .basewidget import BaseWidget
from constantes import *
from pygame import Rect,Surface,draw,font
from pygame.sprite import LayeredDirty
from libs.textrect import render_textrect
from renderer import render_engine


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
    
        for b in range(len(botones)):
            boton = boton_menu(botones[b])
            boton.rect.topleft = ((boton.image.get_width()+20)*b)+4,6
            self.botones.add(boton)
            render_engine.addWidget(boton,2)
        
        self.botones.draw(self.image)
            
class boton_menu(BaseWidget):
    nombre = ''
    
    def __init__(self,nombre):
        super().__init__()
        self.nombre = nombre
        self.layer = 2
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,negro,gris,1)
        self.image = render
        self.rect = render.get_rect()
