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
        FileDiag({'scr':'A','cmd':lambda:print('abrir achivo')})
        #texto = self.entry.devolver_texto()
        #try:
        #    G.cargar_mapa(texto)
        #except:
        #    G.estado = 'Error: El archivo no existe.'
    
    def Guardar(self):
        FileDiag({'scr':'G','cmd':lambda:print('guardar achivo')})
        #texto = self.entry.devolver_texto()
        #try:
        #    G.guardar_mapa(texto)
        #    G.estado = "Mapa '"+texto+"' guardado."
        #except: 
        #    G.estado ='Error: Es necesario cargar un mapa.'
    # barra
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    # barra
    def Set_imagen_fondo(self):
        try:
            imagen = r.cargar_imagen(G.ruta)
            G.IMG_actual = 'Fondo'
            G.IMG_fondo = imagen
            if G.MAPA != None:
                ruta = G.ruta.strip('/'.join(os.getcwd().split('\\')))
                G.MAPA.actualizar({'key':'fondo','value':'maps/fondos/'+ruta})
            G.estado = ''    
        except Exception as Description:
            G.estado = str(Description)
        
    def Set_imagen_colisiones(self):
        try: 
            imagen = r.cargar_imagen(G.ruta)
            G.IMG_actual = 'Colisiones'
            G.IMG_colisiones = imagen
            if G.MAPA != None:
                ruta = G.ruta.strip('/'.join(os.getcwd().split('\\')))
                G.MAPA.actualizar({'key':'colisiones','value':'maps/colisiones/'+ruta})
            G.estado = ''
        except Exception as Description:
            G.estado = str(Description)
    