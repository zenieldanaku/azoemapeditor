from globales import GLOBALES as G,Resources as r, SharedFunctions as shared
from widgets import Marco, Boton, FileDiag
from pygame.sprite import LayeredDirty
from pygame import draw, Surface
from renderer import Renderer
from constantes import *
from . import crear_ejemplo
import os.path

class barraHerramientas (Marco):
    
    def __init__(self, **opciones):
        super().__init__(0,C,24*C,C,**opciones)
        self.nombre = 'BarraHerramientas'
        self.botones = []
        elementos = [
            {"nom":'Nuevo',"cmd":shared.nuevoMapa,"scr":"N"},
            {"nom":'Abrir',"cmd":lambda:FileDiag({'scr':'A','tipo':'A','cmd':shared.abrirMapa}),"scr":"A"},
            {"nom":'Guardar',"cmd":self.Guardar,"scr":"G"},
            {"nom":'barra'},
            {"nom":'Cortar',"cmd":self.Cortar,"scr":"X"},
            {"nom":'Copiar',"cmd":self.Copiar,"scr":"C"},
            {"nom":'Pegar',"cmd":self.Pegar,"scr":"P"},
            {"nom":'barra'},
            {"nom":'SetImgFondo',"cmd":lambda:FileDiag({'scr':'A','tipo':'A','cmd':shared.setRutaFondo}),"scr":"Fd"},
            {"nom":'SetImgColisiones',"cmd":lambda:FileDiag({'scr':'A','tipo':'A','cmd':shared.setRutaColis}),"scr":"Cl"},
            {"nom":'barra'},
            {"nom":'addMob',"cmd":lambda:FileDiag({'scr':'A','tipo':'A','cmd':self.addMob}),"scr":"Mb"},
            {"nom":'addProp',"cmd":lambda:FileDiag({'scr':'A','tipo':'A','cmd':self.addProp}),"scr":"Pr"},
            ]
        x = self.x
        for e in elementos:
            if e['nom'] != 'barra':
                boton = Boton(self,x+6,C+4,e['nom'],e['cmd'],e['scr'])
                x = boton.rect.right-2
                self.botones.append(boton)
                Renderer.addWidget(boton,2)
            else:
                draw.line(self.image,color('sysElmShadow'),[x+7,3],[x+7,27],1)
                draw.line(self.image,color('sysElmLight'),[x+8,3],[x+8,27],1)
                x = x+8
    
    def Guardar(self):
        #tendría que fijarse si hay cambios.
        FileDiag({'scr':'G','tipo':'G','cmd':shared.guardarMapa})

    # barra
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    
    def addMob(self,ruta):
        #sprite = r.split_spritesheet(ruta)
        #nombre = os.path.split(ruta)[1][0:-4]
        #print(nombre)
        crear_ejemplo(32,32)
        
    def addProp(self,ruta):
        sprite = r.cargar_imagen(ruta)
        nombre = os.path.split(ruta)[1][0:-4]
        print(nombre)
    
    def update(self):
        if G.HabilitarTodo:
            G.habilitarItems(self.botones[2:])
        else:
            G.deshabilitarItems(self.botones[2:])