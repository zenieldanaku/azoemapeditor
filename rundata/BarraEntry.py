from widgets import BaseWidget, Entry, BaseBoton
from renderer import Renderer
from constantes import *
from globales import GLOBALES as G, Resources as r
import os
from pygame import Surface,draw

class barraEntry (BaseWidget):
    def __init__(self):
        super().__init__()
        nombre = 'Barra_Entry'
        self.x,self.y = 0,18*C
        self.w,self.h = 24*C,1*C
        self.image = Surface((self.w,self.h))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.image.fill(gris)
        draw.rect(self.image,negro,(0,0,self.w-2,self.h-2),2)
        self.focusable = False
        texto = os.getcwd().split('\\')
        self.entry = Entry(5,self.y+5,int(self.rect.w/3)*2,'/'.join(texto))
        Renderer.addWidget(self)
        elementos = [
            {"nom":'Abrir',"cmd":self.Abrir,"scr":"A"},
            {"nom":'Guardar',"cmd":self.Guardar,"scr":"G"},
            {"nom":'Set_imagen_fondo',"cmd":self.Set_imagen_fondo,"scr":"Fd"},
            {"nom":'Set_imagen_colisiones',"cmd":self.Set_imagen_colisiones,"scr":"Cl"}]
        
        Renderer.addWidget(self.entry,1)
        x = int(self.rect.w/3)*2+4
        for e in elementos:
            boton = BaseBoton(x+4,self.y+3,e['nom'],e['cmd'],e['scr'])
            x = boton.rect.right-2
            Renderer.addWidget(boton,2)
    
    def Abrir(self):
        texto = self.entry.devolver_texto()
        try:
            G.cargar_mapa(texto)
        except:
            G.estado = 'Error: El archivo no existe.'
    
    def Guardar(self):
        texto = self.entry.devolver_texto()
        try:
            G.guardar_mapa(texto)
            G.estado = "Mapa '"+texto+"' guardado."
        except: 
            G.estado ='Error: Es necesario cargar un mapa.'
    
    def _cargar_imagen(self):
        try:
            imagen = r.cargar_imagen(G.ruta)
            return imagen
        except Exception as Description:
            G.estado = str(Description)
    
    def Set_imagen_fondo(self):
        imagen = self._cargar_imagen()
        G.IMG_actual = 'Fondo'
        G.IMG_fondo = imagen
        
    def Set_imagen_colisiones(self):
        imagen = self._cargar_imagen()
        G.IMG_actual = 'Colisiones'
        G.IMG_colisiones = imagen
    
    def update(self):
        G.ruta = self.entry.devolver_texto()