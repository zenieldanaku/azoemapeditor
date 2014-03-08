from pygame.sprite import LayeredDirty
from widgets import Marco,Boton
from globales import GLOBALES as G
from pygame import draw, Surface
from renderer import Renderer
from constantes import *

class barraHerramientas (Marco):
    #botones = None
    def __init__(self, **opciones):
        super().__init__(0,C,24*C,C,**opciones)
        self.nombre = 'BarraHerramientas'
        #self.botones = LayeredDirty()
        elementos = [
            {"nom":'Nuevo',"cmd":self.Nuevo,"scr":"N"},
            {"nom":'barra'},
            {"nom":'Cortar',"cmd":self.Cortar,"scr":"X"},
            {"nom":'Copiar',"cmd":self.Copiar,"scr":"C"},
            {"nom":'Pegar',"cmd":self.Pegar,"scr":"P"}]
        x = self.x
        for e in elementos:
            if e['nom'] != 'barra':
                boton = Boton(x+6,C+4,e['nom'],e['cmd'],e['scr'])
                x = boton.rect.right-2
                #self.botones.add(boton)
                Renderer.addWidget(boton,2)
            else:
                draw.line(self.image,gris_oscuro_bisel,[x+6,3],[x+6,27],1)
                draw.line(self.image,gris_claro_bisel,[x+7,3],[x+7,27],1)
                x = x+7
    
    def Nuevo(self):
        G.nuevo_mapa()
        
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    