from pygame import image
from pygame.sprite import DirtySprite
from mapa import Mapa
import json

class GLOBALES:
    MAPA = None
    estado = ''
    ruta = ''
    ID_actual = -1
    IMG_ID = -1
    IMGs_cargadas = {}
    HabilitarTodo = False
    
    def guardar_mapa(ruta):
        data = GLOBALES.MAPA.guardar()
        Resources.guardar_json(ruta,data)
    
    def cargar_mapa(ruta):
        data = Resources.abrir_json(ruta)
        GLOBALES.MAPA = Mapa()
        GLOBALES.MAPA.cargar(data)
    
    def cargar_imagen(layer):
        img = Resources.cargar_imagen(GLOBALES.ruta)
        GLOBALES.IMG_ID += 1
        
        spr = DirtySprite()
        spr.image = img
        spr.idx = GLOBALES.IMG_ID
        spr.rect = spr.image.get_rect()
        spr._layer = layer
        GLOBALES.IMGs_cargadas[spr.idx] = spr
    
    def habilitarItems(lista_de_items):
        for item in lista_de_items:
            if hasattr(item,'serHabilitado'):
                item.serHabilitado()
        
class Resources:
    def abrir_json (archivo):
        ex = open(archivo,'r')
        data = json.load(ex)
        ex.close()
        return data
    
    def guardar_json (archivo,datos):
        ex = open(archivo,'w')
        json.dump(datos,ex, sort_keys=True,indent=4, separators=(',', ': '))
        ex.close()
    
    def cargar_imagen(ruta):
        ar = image.load(ruta).convert_alpha()
        return ar

class SharedFuntions:
    @staticmethod
    def setRutaFondo(ruta):
        try:
            GLOBALES.ruta = ruta
            GLOBALES.cargar_imagen(1)
        except:
            GLOBALES.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def setRutaColis(ruta):
        try:
            GLOBALES.ruta = ruta
            GLOBALES.cargar_imagen(0)
        except:
            GLOBALES.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def nuevoMapa():
        GLOBALES.MAPA = Mapa()
    
    @staticmethod
    def abrirMapa(ruta):
        try:
            GLOBALES.cargar_mapa(ruta)
        except:
            GLOBALES.estado = 'Error: El archivo no existe.'
    
    @staticmethod
    def guardarMapa(ruta):
        try:
            GLOBALES.guardar_mapa(ruta)
            GLOBALES.estado = "Mapa '"+ruta+"' guardado."
        except: 
            GLOBALES.estado ='Error: Es necesario cargar un mapa.'
        