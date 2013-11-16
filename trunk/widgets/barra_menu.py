from .basewidget import BaseWidget
from constantes import *
from pygame import Rect,Surface,draw,font
from pygame.sprite import LayeredDirty
from libs.textrect import render_textrect
from renderer import Renderer


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
            boton = boton_menu(btn)
            boton.rect.topleft = prev+4,6
            prev = boton.rect.right
            self.botones.add(boton)
            Renderer.addWidget(boton,2)
        
        self.botones.draw(self.image)
            
class boton_menu(BaseWidget):
    nombre = ''
    
    def __init__(self,nombre):
        super().__init__()
        self.nombre = nombre
        self.layer = 2
        self.image = self.crear_boton()
        self.rect = self.image.get_rect()
    
    def crear_boton(self):
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(self.nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(self.nombre,fuente,rect,negro,gris,1)
        return render