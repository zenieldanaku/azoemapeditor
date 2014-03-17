from globales import GLOBALES as G,Resources as r
from widgets import Marco, Boton, FileDiag
from pygame.sprite import LayeredDirty
from pygame import draw, Surface
from renderer import Renderer
from constantes import *

class barraHerramientas (Marco):
    #botones = None
    def __init__(self, **opciones):
        super().__init__(0,C,24*C,C,**opciones)
        self.nombre = 'BarraHerramientas'
        elementos = [
            {"nom":'Nuevo',"cmd":self.Nuevo,"scr":"N"},
            {"nom":'Abrir',"cmd":self.Abrir,"scr":"A"},
            {"nom":'Guardar',"cmd":self.Guardar,"scr":"G"},
            {"nom":'barra'},
            {"nom":'Cortar',"cmd":self.Cortar,"scr":"X"},
            {"nom":'Copiar',"cmd":self.Copiar,"scr":"C"},
            {"nom":'Pegar',"cmd":self.Pegar,"scr":"P"},
            {"nom":'barra'},
            {"nom":'SetImgFondo',"cmd":self.Set_imagen_fondo,"scr":"Fd"},
            {"nom":'SetImgColisiones',"cmd":self.Set_imagen_colisiones,"scr":"Cl"}]
        x = self.x
        for e in elementos:
            if e['nom'] != 'barra':
                boton = Boton(self,x+6,C+4,e['nom'],e['cmd'],e['scr'])
                x = boton.rect.right-2
                Renderer.addWidget(boton,2)
            else:
                draw.line(self.image,color('sysElmShadow'),[x+7,3],[x+7,27],1)
                draw.line(self.image,color('sysElmLight'),[x+8,3],[x+8,27],1)
                x = x+8
    
    def Nuevo(self):
        G.nuevo_mapa()
    
    def Abrir(self):
        FileDiag({'scr':'A','tipo':'A','cmd':self.abrirMapa})

    def Guardar(self):
        FileDiag({'scr':'G','tipo':'G','cmd':self.guardarMapa})

    # barra
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    # barra

    def Set_imagen_fondo(self):
        FileDiag({'scr':'A','tipo':'A','cmd':self.setRutaFondo})
        
    def Set_imagen_colisiones(self):
        FileDiag({'scr':'A','tipo':'A','cmd':self.setRutaColis})
        
    @staticmethod
    def setRutaFondo(ruta):
        G.ruta = ruta
        G.cargar_imagen('Fondo')
    
    @staticmethod
    def setRutaColis(ruta):
        G.ruta = ruta
        G.cargar_imagen('Colisiones')
    
    @staticmethod
    def abrirMapa(ruta):
        try:
            G.cargar_mapa(ruta)
        except:
            G.estado = 'Error: El archivo no existe.'
    
    @staticmethod
    def guardarMapa(ruta):
        try:
            G.guardar_mapa(ruta)
            G.estado = "Mapa '"+ruta+"' guardado."
        except: 
            G.estado ='Error: Es necesario cargar un mapa.'