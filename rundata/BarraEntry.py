from globales import GLOBALES as G, Resources as r
from widgets import  Entry, Boton, Marco
from pygame import Surface,draw
from renderer import Renderer
from constantes import *
from colores import color
import os

class barraEntry (Marco):
    def __init__(self):
        super().__init__(0,18*C,24*C,1*C)
        self.nombre = 'Barra_Entry'
        self.focusable = False
        texto = os.getcwd().split('\\')
        self.entry = Entry(self,'EntryRuta',5,self.y+5,int(self.w/3)*2,'/'.join(texto))
        elementos = [
            {"nom":'Abrir',"cmd":self.Abrir,"scr":"A"},
            {"nom":'Guardar',"cmd":self.Guardar,"scr":"G"},
            {"nom":"barra"},
            {"nom":'SetImgFondo',"cmd":self.Set_imagen_fondo,"scr":"Fd"},
            {"nom":'SetImgColisiones',"cmd":self.Set_imagen_colisiones,"scr":"Cl"}]
        
        self.agregar(self.entry)
        x = int(self.rect.w/3)*2+4
        for e in elementos:
            if e['nom'] != 'barra':
                boton = Boton(self,x+4,self.y+3,e['nom'],e['cmd'],e['scr'])
                x = boton.rect.right-2
                Renderer.addWidget(boton,2)
            else:
                draw.line(self.image,color('sysElmShadow'),[x+6,3],[x+6,27],1)
                draw.line(self.image,color('sysElmLight'),[x+7,3],[x+7,27],1)
                x = x+8
    
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
    
    def Set_imagen_fondo(self):
        try:
            G.IMG_actual = 'Fondo'
            G.cargar_imagen('Fondo')
            if G.MAPA != None:
                ruta = G.ruta.strip('/'.join(os.getcwd().split('\\')))
                G.MAPA.actualizar({'key':'fondo','value':'maps/fondos/'+ruta})
        except Exception as Description:
            G.estado = str(Description)
        
    def Set_imagen_colisiones(self):
        try: 
            G.IMG_actual = 'Colisiones'
            G.cargar_imagen('Fondo')
            if G.MAPA != None:
                ruta = G.ruta.strip('/'.join(os.getcwd().split('\\')))
                G.MAPA.actualizar({'key':'colisiones','value':'maps/colisiones/'+ruta})
        except Exception as Description:
            G.estado = str(Description)
    
    def update(self):
        G.ruta = self.entry.devolver_texto()