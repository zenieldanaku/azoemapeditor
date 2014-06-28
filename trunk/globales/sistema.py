from pygame import image, quit as py_quit, Rect
from pygame.sprite import DirtySprite
from sys import exit as sys_exit
from .constantes import *
from .mapa import Mapa
import os.path

class Sistema:
    MAPA = None
    estado = ''
    ruta = ''
    IMG_ID = -1
    IMGs_cargadas = {}
    HabilitarTodo = False
    portapapeles = None
    preferencias = {}
    
    @staticmethod
    def cargar_imagen(layer):
        img = Resources.cargar_imagen(Sistema.ruta)
        Sistema.IMG_ID += 1
        
        spr = DirtySprite()
        spr.image = img
        spr.idx = Sistema.IMG_ID
        spr.rect = spr.image.get_rect()
        spr._layer = layer
        spr.dirty = 2
        Sistema.IMGs_cargadas[spr.idx] = spr
    
    @staticmethod
    def habilitarItems(lista_de_items):
        for item in lista_de_items:
            if hasattr(item,'serHabilitado'):
                item.serHabilitado()
    
    @staticmethod
    def deshabilitarItems(lista_de_items):
        for item in lista_de_items:
            if hasattr(item,'serDeshabilitado'):
                item.serDeshabilitado()

    @staticmethod
    def setRutaFondo(ruta):
        try:
            Sistema.ruta = ruta
            _ruta = 'maps/fondos/'+os.path.split(ruta)[1]
            Sistema.cargar_imagen(LAYER_FONDO)
            Sistema.MAPA.script["capa_background"]["fondo"] = _ruta
        except:
            Sistema.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def setRutaColis(ruta):
        try:
            Sistema.ruta = ruta
            _ruta = 'maps/colisiones/'+os.path.split(ruta)[1]
            Sistema.cargar_imagen(LAYER_COLISIONES)
            Sistema.MAPA.script["capa_background"]["colisiones"]= _ruta
        except:
            Sistema.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def addRef(nombre,ruta):
        _ruta = ruta.replace('\\','/')
        if nombre not in Sistema.MAPA.script['refs']:
            Sistema.MAPA.script['refs'][nombre] = _ruta
            
    @staticmethod
    def nuevoMapa():
        Sistema.HabilitarTodo = True
        Sistema.MAPA = Mapa()
    
    @staticmethod
    def abrirMapa(ruta):
        try:
            data = Resources.abrir_json(ruta)
            Sistema.MAPA = Mapa()
            Sistema.MAPA.cargar(data)
        except:
            Sistema.estado = 'Error: El archivo no existe.'
    
    @staticmethod
    def guardarMapa(ruta):
        try:
            data = Sistema.MAPA.guardar()
            Resources.guardar_json(ruta,data)
            Sistema.estado = "Mapa '"+ruta+"' guardado."
        except: 
            Sistema.estado ='Error: Es necesario cargar un mapa.'
    
    @staticmethod
    def cerrarMapa():
        Sistema.MAPA = None
        Sistema.IMGs_cargadas.clear()
        Sistema.IMG_ID = -1
        Sistema.HabilitarTodo = False
    
    @staticmethod
    def salir():
        py_quit()
        sys_exit()
    
    @staticmethod
    def copiar(elemento):
        Sistema.portapapeles = elemento.copy()
    
    @staticmethod
    def pegar(destino):
        from renderer import Renderer
        widget = Renderer.getWidget(destino)
        if hasattr(widget,'pegar'):
            if Sistema.HabilitarTodo:
                widget.pegar(Sistema.portapapeles)