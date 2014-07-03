from .constantes import LAYER_FONDO, LAYER_COLISIONES
from pygame import image, quit as py_quit, Rect
from pygame.sprite import DirtySprite
from sys import exit as sys_exit
from .resources import Resources
from .mapa import Mapa
import os.path

class Sistema:
    MAPA = None
    estado = ''
    ruta = ''
    referencias = {}
    IMG_ID = -1
    IMGs_cargadas = {}
    HabilitarTodo = False
    portapapeles = None
    preferencias = {}
    Guardado = False
    
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
            _ruta = Sistema.referencias['fondo']+os.path.split(ruta)[1]
            Sistema.cargar_imagen(LAYER_FONDO)
            Sistema.MAPA.script["capa_background"]["fondo"] = _ruta
        except:
            Sistema.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def setRutaColis(ruta):
        try:
            Sistema.ruta = ruta
            _ruta = Sistema.referencias['colisiones']+os.path.split(ruta)[1]
            Sistema.cargar_imagen(LAYER_COLISIONES)
            Sistema.MAPA.script["capa_background"]["colisiones"]= _ruta
        except:
            Sistema.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def addProp(nombre,ruta):
        root = Sistema.MAPA.script['capa_ground']['props']
        if nombre not in root:
            root[nombre] = [[]]
            index = 0
            Sistema.addRef(nombre,Sistema.referencias['props'])
        else:
            root[nombre].append([])
            index = len(root[nombre])-1
        return index
    
    
    @staticmethod
    def addRef(nombre,ruta):
        #chapuza: nombre deberia ser distinto de filename.
        if nombre not in Sistema.MAPA.script['refs']:
            Sistema.MAPA.script['refs'][nombre] = ruta+nombre+'.png'
            
    @staticmethod
    def nuevoMapa(data):
        Sistema.referencias.update(data)
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
            Sistema.Guardado = ruta
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
        from . import EventHandler
        widget = EventHandler.getWidget(destino)
        if hasattr(widget,'pegar'):
            if Sistema.HabilitarTodo:
                widget.pegar(Sistema.portapapeles)