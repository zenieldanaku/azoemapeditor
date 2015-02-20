from .constantes import LAYER_FONDO, LAYER_COLISIONES, C
from pygame import image, quit as py_quit, Rect, mouse
from pygame.sprite import DirtySprite
from sys import exit as sys_exit
from .resources import Resources
from .eventhandler import EventHandler
from .mapa import Mapa, Proyecto
from .portapapeles import Portapapeles
from .RLE import decode, descomprimir, deserialize
from os import getcwd

class Sistema:
    MAPA = None
    PROYECTO = None
    estado = ''
    ruta = ''
    referencias = {}
    KeyCombinations = []
    IMG_FONDO = None
    capa_actual = None
    HabilitarTodo = False
    Portapapeles = None
    selected = None
    preferencias = {}
    Guardado = False
    iconos = []
    fdProyectos = getcwd()+'\\proyectos'
    fdAssets = getcwd()+'\\assets'
    fdExport = getcwd()+'\\export'
    fdLibs = getcwd()+'\\libs'
    DiagBox = None
    DiagMODE = False
    
    @classmethod
    def init(cls):
        cls.iconos = cls.cargar_iconos()
        cls.capa_actual = LAYER_FONDO
        cls.Portapapeles = Portapapeles()
    
    @staticmethod
    def cargar_iconos():
        nombres = 'nuevo,abrir,guardar,cortar,copiar,pegar,grilla,grilla_tog,guardar_dis,cortar_dis,copiar_dis,pegar_dis,grilla_dis,mob,prop,borrar,ver_cls,ver_fondo,ver_dis,mob_dis,prop_dis,borrar_dis,fondo,fondo_dis'.split(',')
        ruta = getcwd()+'/iconos.png'
        return Resources.cargar_iconos(nombres,ruta,19,17)
    
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

    @classmethod
    def setRutaFondo(cls,ruta):
        try:
            spr = DirtySprite()  
            spr.image = Resources.cargar_imagen(ruta)
            w,h = spr.image.get_size()
            if w <= C*15 or h < C*15:
                raise IOError()
            
            spr.rect = spr.image.get_rect()
            spr._layer = LAYER_FONDO
            spr.dirty = 2
            
            cls.IMG_FONDO = spr
            cls.PROYECTO.script["fondo"] = ruta
            cls.capa_actual = LAYER_FONDO
            cls.estado = ''
        except:
            cls.estado = 'No se ha selecionado una imagen válida'
    
    @classmethod
    def GuardarMapaDeColisiones(cls,ruta):
        widget = EventHandler.getWidget('Grilla.Canvas')
        imagen = widget.render()
        Resources.guardar_imagen(imagen,ruta)
        cls.estado = 'Imagen '+ruta+' guardada exitosamente'
    
    @classmethod
    def addItem(cls,nombre,ruta,grupo,code):
        root = cls.PROYECTO.script[grupo]
        if nombre not in root:
            root[nombre] = [[]]
            index = 0
            cls.addRef(nombre,ruta,code)
        else:
            if cls.PROYECTO.script['refs'][nombre]['code'] == code:
                root[nombre].append([])
                index = len(root[nombre])-1
            else:
                nombre+='_'+str(len(cls.PROYECTO.script['refs']))
                index = cls.addItem(nombre,ruta,grupo,code)
                
        return index
    
    @classmethod
    def updateItemPos(cls,nombre,grupo,index,pos,layer=0,rot=0):
        x,y = pos
        cls.PROYECTO.script[grupo][nombre][index] = x,y,layer,rot
    
    @classmethod
    def addRef(cls,nombre,ruta,code):
        #chapuza: nombre deberia ser distinto de filename.
        if nombre not in cls.PROYECTO.script['refs']:
            cls.PROYECTO.script['refs'][nombre] = {'ruta':ruta,'code':code}
            
    @classmethod
    def nuevoProyecto(cls,data):
        cls.cerrarProyecto()
        cls.referencias.update(data)
        cls.HabilitarTodo = True
        cls.PROYECTO = Proyecto(data)
    
    @classmethod
    def abrirProyecto(cls,ruta):
        data = Resources.abrir_json(ruta)
        cls.PROYECTO = Proyecto(data)
        
        for key in data:
            cls.PROYECTO[key] = data[key]
            cls.ruta = data[key]
            if key == 'fondo':
                if data[key] != "":
                    cls.cargar_imagen(LAYER_FONDO)
                    cls.capa_actual = LAYER_FONDO
            #elif key == 'colisiones':
            #    if ar[key] != "":
            #        Sistema.cargar_imagen(LAYER_COLISIONES)
            elif key == 'props' or key == 'mobs':
                widget = EventHandler.getWidget('Grilla.Canvas')
                for item in data[key]:
                    nombre = item
                    _ruta = data['refs'][item]['ruta']
                    _cols = data['refs'][item]['code']
                    
                    if key == 'props':
                        sprite = Resources.cargar_imagen(_ruta)
                        tipo = 'Prop'
                    elif key == 'mobs':
                        sprite = Resources.split_spritesheet(_ruta)
                        tipo = 'Mob'
                    
                    colision = None
                    if _cols != None:
                        w,h = sprite[0].get_size()
                        colision = deserialize(decode(descomprimir(_cols)),w,h)
                    
                    idx = -1
                    for pos in data[key][item]:
                        rot = pos[3]
                        if type(sprite) == list: image = sprite[rot]
                        else:                    image = sprite
                        if len(pos) != 0:
                            idx+=1
                            datos = {"nombre":nombre,"image":image,"tipo":tipo,
                                     "grupo":key,"ruta":_ruta,"pos":pos,
                                     "index":idx,"colisiones":colision,'rot':rot}
                            widget.addTile(datos)
            elif key == 'referencias':
                cls.referencias = data[key]
        cls.Guardado = ruta
        cls.HabilitarTodo = True
    
    @classmethod
    def guardarProyecto(cls,ruta):
        try:
            data = cls.PROYECTO.guardar()
            Resources.guardar_json(ruta,data,False)
            cls.estado = "Proyecto '"+ruta+"' guardado."
            cls.Guardado = ruta
        except: 
            cls.estado ='Error: Es necesario cargar un mapa.'
    
    @classmethod
    def cerrarProyecto(cls):
        cls.PROYECTO = None
        cls.IMG_FONDO = None
        cls.HabilitarTodo = False
        EventHandler.contents.update()
    
    @classmethod
    def abrirMapa(cls,ruta):
        try:
            data = Resources.abrir_json(ruta)
            cls.MAPA = Mapa()
            cls.MAPA.cargar(data)
        except:
            cls.estado = 'Error: El archivo no existe.'
    
    @classmethod
    def exportarMapa(cls,ruta):
        try:
            data = cls.PROYECTO.guardar()
            Resources.guardar_json(ruta,data)
            cls.estado = "Mapa '"+ruta+"' guardado."
            cls.Guardado = ruta
        except: 
            cls.estado ='Error: Es necesario cargar un mapa.'
    
    @staticmethod
    def salir():
        py_quit()
        sys_exit()
    
    @classmethod
    def cortar(cls):
        elemento = cls.selected
        if elemento != None:
            parent = EventHandler.getWidget(elemento.parent)
            cls.Portapapeles.cortar(elemento)
            parent.tiles.remove(elemento)
        
    @classmethod
    def copiar(cls):
        elemento = cls.selected
        if elemento != None:
            cls.Portapapeles.copiar(elemento.copiar())
        
    @classmethod
    def pegar(cls):
        widget = EventHandler.getWidget('Grilla.Canvas')
        cls.Portapapeles.pegar(widget)
    
    @classmethod
    def update(cls):
        key = EventHandler.key
        cls.KeyCombinations.clear()
        
        if key != None:
            if EventHandler.control:
                cls.KeyCombinations.append('Ctrl')
            if EventHandler.alt:
                cls.KeyCombinations.append('Alt')
            cls.KeyCombinations.append(key.upper())
        
        if cls.KeyCombinations != []:
            combination = '+'.join(cls.KeyCombinations)
            for widget in EventHandler.contents:
                if type(widget.KeyCombination) == str:
                    if combination == widget.KeyCombination:
                        print('anda!')
                else:
                    widget.KeyCombination(combination)
        
        if cls.DiagBox != None:
            if cls.DiagMODE == False:
                for widget in EventHandler.contents:
                    if hasattr(widget,'parent'):
                        if widget != cls.DiagBox and widget.parent != cls.DiagBox:
                            widget.enabled = False
                cls.DiagMODE = True
            else:
                if cls.DiagBox.update():
                    cls.DiagBox = None
                    for widget in EventHandler.contents:
                        if hasattr(widget,'parent'):
                            if widget != cls.DiagBox and widget.parent != cls.DiagBox:
                                widget.enabled = True
                    cls.DiagMODE = False
                    