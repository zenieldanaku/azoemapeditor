from widgets import BarraMenu,BaseBoton
from renderer import Renderer
from constantes import *
from pygame.sprite import LayeredDirty
from pygame import draw

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
            {"nom":'Abrir',"cmd":self.Abrir,"scr":"A"},
            {"nom":'Guardar',"cmd":self.Guardar,"scr":"G"},
            {"nom":'barra'},
            {"nom":'Cortar',"cmd":self.Cortar,"scr":"X"},
            {"nom":'Copiar',"cmd":self.Copiar,"scr":"C"},
            {"nom":'Pegar',"cmd":self.Pegar,"scr":"P"}]
        
        for e in elementos:
            if e['nom'] != 'barra':
                boton = BaseBoton(x+4,C+3,e['nom'],e['cmd'],e['scr'])
                x = boton.rect.right-2
                self.botones.add(boton)
                Renderer.addWidget(boton,2)
            else:
                #Surface, color, start_pos, end_pos, width=1
                draw.line(self.image,negro,[x+4,3],[x+4,27],2)
                x = x+5
    
    def Nuevo(self):
        print('boton nuevo')
    def Abrir(self):
        print('boton abrir')
    def Guardar(self):
        print('boton guardar')
    
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    