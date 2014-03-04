from widgets import BaseWidget,BaseBoton
from renderer import Renderer
from constantes import *
from pygame.sprite import LayeredDirty
from pygame import draw, Surface
from globales import GLOBALES as G

class barraHerramientas (BaseWidget):
    botones = None
    def __init__(self):
        super().__init__()
        self.nombre = 'BarraHerramientas'
        self.botones = LayeredDirty()
        self.x,self.y = 0,C
        self.w,self.h = 24*C,1*C
        self.image = Surface((self.w,self.h))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.image.fill(gris)
        draw.rect(self.image,negro,(0,0,self.w-2,self.h-2),2)
        Renderer.addWidget(self)
        elementos = [
            {"nom":'Nuevo',"cmd":self.Nuevo,"scr":"N"},
            {"nom":'barra'},
            {"nom":'Cortar',"cmd":self.Cortar,"scr":"X"},
            {"nom":'Copiar',"cmd":self.Copiar,"scr":"C"},
            {"nom":'Pegar',"cmd":self.Pegar,"scr":"P"}]
        x = self.x
        for e in elementos:
            if e['nom'] != 'barra':
                boton = BaseBoton(x+6,C+4,e['nom'],e['cmd'],e['scr'])
                x = boton.rect.right-2
                self.botones.add(boton)
                Renderer.addWidget(boton,2)
            else:
                draw.line(self.image,negro,[x+6,3],[x+6,27],2)
                x = x+7
    
    def Nuevo(self):
        G.nuevo_mapa()
        
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    