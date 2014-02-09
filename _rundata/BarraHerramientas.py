from widgets import BarraMenu,BaseBoton
from renderer import Renderer
from constantes import *
from pygame.sprite import LayeredDirty
from pygame import draw
from globales import GLOBALES as G

class barraHerramientas (BarraMenu):
    botones = None
    def __init__(self):
        self.nombre = 'BarraHerramientas'
        self.botones = LayeredDirty()
        self.focusable = False
        x,y = 0,C
        w,h = 24*C,1*C
        super().__init__(self.nombre,x,y,w,h)
        Renderer.addWidget(self)
        elementos = [
            {"nom":'Nuevo',"cmd":self.Nuevo,"scr":"N"},
            {"nom":'barra'},
            {"nom":'Cortar',"cmd":self.Cortar,"scr":"X"},
            {"nom":'Copiar',"cmd":self.Copiar,"scr":"C"},
            {"nom":'Pegar',"cmd":self.Pegar,"scr":"P"}]
        
        for e in elementos:
            if e['nom'] != 'barra':
                boton = BaseBoton(x+6,C+4,e['nom'],e['cmd'],e['scr'])
                x = boton.rect.right-2
                self.botones.add(boton)
                Renderer.addWidget(boton,2)
            else:
                draw.line(self.image,negro,[x+6,3],[x+6,27],2)
                x = x+7
    
    def Nuevo(self): G.nuevo_mapa()
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    