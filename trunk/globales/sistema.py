from .constantes import LAYER_FONDO, LAYER_COLISIONES
from pygame import image, quit as py_quit, Rect
from pygame.sprite import DirtySprite
from sys import exit as sys_exit
from .resources import Resources
from .eventhandler import EventHandler
from .mapa import Mapa, Proyecto
from os import getcwd

class Sistema:
    MAPA = None
    PROYECTO = None
    estado = ''
    ruta = ''
    referencias = {}

    IMG_FONDO = None
    capa_actual = None
    HabilitarTodo = False
    portapapeles = None
    preferencias = {}
    Guardado = False
    fdProyectos = getcwd()+'\\proyectos'
    fdAssets = getcwd()+'\\assets'
    fdExport = getcwd()+'\\export'
    fdLibs = getcwd()+'\\libs'
    
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
    def cargar_imagen(layer):
        spr = DirtySprite()      
        spr.image = Resources.cargar_imagen(Sistema.ruta)
        spr.rect = spr.image.get_rect()
        spr._layer = layer
        spr.dirty = 2
        
        Sistema.IMG_FONDO = spr

    @staticmethod
    def setRutaFondo(ruta):
        try:
            Sistema.ruta = ruta
            Sistema.cargar_imagen(LAYER_FONDO)
            Sistema.PROYECTO.script["fondo"] = ruta
            Sistema.capa_actual = LAYER_FONDO
        except:
            Sistema.estado = 'No se ha selecionado ninguna imagen'
    
    #@staticmethod
    #def setRutaColis(ruta):
    #    try:
    #        Sistema.ruta = ruta
    #        #_ruta = Sistema.referencias['colisiones']+os.path.split(ruta)[1]
    #        Sistema.cargar_imagen(LAYER_COLISIONES)
    #        Sistema.PROYECTO.script["colisiones"]= ruta
    #    except:
    #        Sistema.estado = 'No se ha selecionado ninguna imagen'
    
    @staticmethod
    def addItem(nombre,ruta,grupo):
        root = Sistema.PROYECTO.script[grupo]
        if nombre not in root:
            root[nombre] = [[]]
            index = 0
            Sistema.addRef(nombre,ruta)
        else:
            root[nombre].append([])
            index = len(root[nombre])-1
        return index
    
    @staticmethod
    def updateItemPos(nombre,grupo,index,pos):
        Sistema.PROYECTO.script[grupo][nombre][index] = pos
    
    @staticmethod
    def addRef(nombre,ruta):
        #chapuza: nombre deberia ser distinto de filename.
        if nombre not in Sistema.PROYECTO.script['refs']:
            Sistema.PROYECTO.script['refs'][nombre] = ruta
            
    @staticmethod
    def nuevoProyecto(data):
        Sistema.referencias.update(data)
        Sistema.HabilitarTodo = True
        Sistema.PROYECTO = Proyecto()
    
    def abrirProyecto(ruta):
        Sistema.PROYECTO = Proyecto()
        ar = Resources.abrir_json(ruta)
        for key in ar:
            Sistema.PROYECTO[key] = ar[key]
            Sistema.ruta = ar[key]
            if key == 'fondo':
                if ar[key] != "":
                    Sistema.cargar_imagen(LAYER_FONDO)
                    Sistema.capa_actual = LAYER_FONDO
            elif key == 'colisiones':
                if ar[key] != "":
                    Sistema.cargar_imagen(LAYER_COLISIONES)
            elif key == 'props' or key == 'mobs':
                widget = EventHandler.getWidget('Grilla.Canvas')
                for item in ar[key]:
                    nombre,_ruta = item,ar['refs'][item]
                    if key == 'props':   sprite = Resources.cargar_imagen(_ruta)
                    elif key == 'mobs':
                        sprite = Resources.split_spritesheet(_ruta)[0]
                        
                    idx = -1
                    for pos in ar[key][item]:
                        if len(pos) != 0:
                            idx+=1
                            datos = {'nombre':nombre,'image':sprite,'tipo':'Prop','grupo':key,'ruta':_ruta,"pos":pos,"index":idx}
                            widget.addTile(datos)
            elif key == 'referencias':
                Sistema.referencias = ar[key]
        Sistema.Guardado = ruta
        Sistema.HabilitarTodo = True
    
    def guardarProyecto(ruta):
        try:
            data = Sistema.PROYECTO.guardar()
            Resources.guardar_json(ruta,data,False)
            Sistema.estado = "Proyecto '"+ruta+"' guardado."
            Sistema.Guardado = ruta
        except: 
            Sistema.estado ='Error: Es necesario cargar un mapa.'
    
    @staticmethod
    def cerrarProyecto():
        Sistema.Proyecto = None
        Sistema.IMGs_cargadas.clear()
        Sistema.IMG_ID = -1
        Sistema.HabilitarTodo = False
    
    @staticmethod
    def abrirMapa(ruta):
        try:
            data = Resources.abrir_json(ruta)
            Sistema.MAPA = Mapa()
            Sistema.MAPA.cargar(data)
        except:
            Sistema.estado = 'Error: El archivo no existe.'
    
    @staticmethod
    def exportarMapa(ruta):
        try:
            data = Sistema.PROYECTO.guardar()
            Resources.guardar_json(ruta,data)
            Sistema.estado = "Mapa '"+ruta+"' guardado."
            Sistema.Guardado = ruta
        except: 
            Sistema.estado ='Error: Es necesario cargar un mapa.'
    
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