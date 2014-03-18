from pygame import image
from mapa import Mapa
import json

class GLOBALES:
    MAPA = None
    estado = ''
    ruta = ''
    IMG_fondo = None
    IMG_colisiones = None
    IMG_actual = ''
    IMG_ID = -1
    IMGs_cargadas = []
    
    def guardar_mapa(ruta):
        data = GLOBALES.MAPA.guardar()
        Resources.guardar_json(ruta,data)
    
    def cargar_mapa(ruta):
        data = Resources.abrir_json(ruta)
        GLOBALES.MAPA = Mapa()
        GLOBALES.MAPA.cargar(data)
    
    def cargar_imagen(dest):
        img = Resources.cargar_imagen(GLOBALES.ruta)
        if dest == 'Fondo':
            GLOBALES.IMG_fondo = img
        elif dest == 'Colisiones':
            GLOBALES.IMG_colisiones = img
        GLOBALES.IMG_actual = dest
        GLOBALES.IMG_ID += 1
        GLOBALES.IMGs_cargadas.append({'img':img, 'ID':GLOBALES.IMG_ID})
        
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
            GLOBALES.cargar_imagen('Fondo')
        except:
            GLOBALES.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def setRutaColis(ruta):
        try:
            GLOBALES.ruta = ruta
            GLOBALES.cargar_imagen('Colisiones')
        except:
            GLOBALES.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def nuevoMapa():
        GLOBALES.MAPA = Mapa()
        GLOBALES.IMG_fondo = None
        GLOBALES.IMG_colisiones = None
        GLOBALES.IMG_actual = ''
    
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
        