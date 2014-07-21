from pygame import image, Rect
import json

class Resources:
    
    @staticmethod
    def abrir_json (archivo):
        ex = open(archivo,'r')
        data = json.load(ex)
        ex.close()
        return data
    
    @staticmethod
    def guardar_json (archivo,datos,odenar=True):
        ex = open(archivo,'w')
        if odenar:
            json.dump(datos,ex, sort_keys=True,indent=4, separators=(',', ': '))
        else:
            json.dump(datos,ex)
        ex.close()
    
    @staticmethod
    def cargar_imagen(ruta):
        ar = image.load(ruta).convert_alpha()
        return ar
     
    @staticmethod
    def split_spritesheet(ruta,w=32,h=32):
        spritesheet = Resources.cargar_imagen(ruta)
        ancho = spritesheet.get_width()
        alto = spritesheet.get_height()
        tamanio = w,h
        sprites = []
        for y in range(int(alto/h)):
            for x in range(int(ancho/w)):
                rect = Rect((int(ancho/(ancho/w))*x,int(alto/(alto/h))*y),tamanio)
                sprites.append(spritesheet.subsurface(rect))
        return sprites