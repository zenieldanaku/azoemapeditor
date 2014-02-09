from mapa import Mapa
import json

class GLOBALES:
    MAPA = None
    
    def nuevo_mapa():
        GLOBALES.MAPA = Mapa()
    
    def guardar_mapa(ruta):
        data = GLOBALES.MAPA.guardar()
        Resources.guardar_json(ruta,data)

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