from pygame import image, quit as py_quit, Rect
from pygame.sprite import DirtySprite
from sys import exit as sys_exit
from constantes import *
from mapa import Mapa
import json,os.path

class GLOBALES:
    MAPA = None
    estado = ''
    ruta = ''
    IMG_ID = -1
    IMGs_cargadas = {}
    HabilitarTodo = False
    portapapeles = None
    preferencias = {}
    
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
        spr.dirty = 2
        GLOBALES.IMGs_cargadas[spr.idx] = spr
    
    def habilitarItems(lista_de_items):
        for item in lista_de_items:
            if hasattr(item,'serHabilitado'):
                item.serHabilitado()
    
    def deshabilitarItems(lista_de_items):
        for item in lista_de_items:
            if hasattr(item,'serDeshabilitado'):
                item.serDeshabilitado()
    
class Resources:
    
    @staticmethod
    def abrir_json (archivo):
        ex = open(archivo,'r')
        data = json.load(ex)
        ex.close()
        return data
    
    @staticmethod
    def guardar_json (archivo,datos):
        ex = open(archivo,'w')
        json.dump(datos,ex, sort_keys=True,indent=4, separators=(',', ': '))
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
                sprites.append(spritesheet.subsurface(Rect(((int(ancho/(ancho/w))*x,
                                                            int(alto/(alto/h))*y),
                                                            tamanio))))
        return sprites

class SharedFunctions:
    @staticmethod
    def setRutaFondo(ruta):
        try:
            GLOBALES.ruta = ruta
            _ruta = 'maps/fondos/'+os.path.split(ruta)[1]
            GLOBALES.cargar_imagen(LAYER_FONDO)
            GLOBALES.MAPA.script["capa_background"]["fondo"] = _ruta
        except:
            GLOBALES.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def setRutaColis(ruta):
        try:
            GLOBALES.ruta = ruta
            _ruta = 'maps/colisiones/'+os.path.split(ruta)[1]
            GLOBALES.cargar_imagen(LAYER_COLISIONES)
            GLOBALES.MAPA.script["capa_background"]["colisiones"]= _ruta
        except:
            GLOBALES.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def addSprite(ruta,sprite,nombre):
        if type(sprite) == list:
            _spr = sprite[0]
        
        GLOBALES.ruta = ruta
        
    @staticmethod
    def nuevoMapa():
        GLOBALES.HabilitarTodo = True
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
    
    @staticmethod
    def cerrarMapa():
        GLOBALES.MAPA = None
        GLOBALES.IMGs_cargadas.clear()
        GLOBALES.IMG_ID = -1
        GLOBALES.HabilitarTodo = False
    
    @staticmethod
    def salir():
        py_quit()
        sys_exit()
    
    @staticmethod
    def copiar(elemento):
        GLOBALES.portapapeles = elemento.copy()
    
    @staticmethod
    def pegar(destino):
        from renderer import Renderer
        widget = Renderer.getWidget(destino)
        if hasattr(widget,'pegar'):
            if GLOBALES.HabilitarTodo:
                widget.pegar(GLOBALES.portapapeles)