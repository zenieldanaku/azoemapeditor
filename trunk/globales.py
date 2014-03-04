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
    
    def nuevo_mapa():
        GLOBALES.MAPA = Mapa()
        GLOBALES.IMG_fondo = None
        GLOBALES.IMG_colisiones = None
        GLOBALES.IMG_actual = ''
    
    def guardar_mapa(ruta):
        data = GLOBALES.MAPA.guardar()
        Resources.guardar_json(ruta,data)
    
    def cargar_mapa(ruta):
        data = Resources.abrir_json(ruta)
        GLOBALES.MAPA = Mapa()
        GLOBALES.MAPA.cargar(data)
    
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