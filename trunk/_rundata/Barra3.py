from widgets import BarraMenu, Entry, BaseBoton
from renderer import Renderer
from constantes import *
from globales import GLOBALES as G
import os

class barra3 (BarraMenu):
    def __init__(self):
        nombre = 'Menu_3'
        x,y = 0,18*C
        w,h = 24*C,1*C
        
        super().__init__(nombre,x,y,w,h)
        self.focusable = False
        texto = os.getcwd().split('\\')
        self.entry = Entry(5,y+5,int(self.rect.w/3)*2,'/'.join(texto))
        Renderer.addWidget(self)
        elementos = [
            {"nom":'Abrir',"cmd":self.Abrir,"scr":"A"},
            {"nom":'Guardar',"cmd":self.Guardar,"scr":"G"}]
        
        Renderer.addWidget(self.entry,1)
        x = int(self.rect.w/3)*2+4
        for e in elementos:
            boton = BaseBoton(x+4,y+3,e['nom'],e['cmd'],e['scr'])
            x = boton.rect.right-2
            Renderer.addWidget(boton,2)
    
    def Abrir(self):
        try: G.cargar_mapa(''.join(self.entry.texto))
        except: pass
    
    def Guardar(self):
        try: G.guardar_mapa(''.join(self.entry.texto))
        except: pass