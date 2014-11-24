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
    
    @staticmethod
    def init():
        Sistema.iconos = Sistema.cargar_iconos()
        Sistema.capa_actual = LAYER_FONDO
        Sistema.Portapapeles = Portapapeles()
    
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

    @staticmethod
    def setRutaFondo(ruta):
        try:
            spr = DirtySprite()  
            spr.image = Resources.cargar_imagen(ruta)
            w,h = spr.image.get_size()
            if w <= C*15 or h < C*15:
                raise IOError()
            
            spr.rect = spr.image.get_rect()
            spr._layer = LAYER_FONDO
            spr.dirty = 2
            
            Sistema.IMG_FONDO = spr
            Sistema.PROYECTO.script["fondo"] = ruta
            Sistema.capa_actual = LAYER_FONDO
            Sistema.estado = ''
        except:
            Sistema.estado = 'No se ha selecionado una imagen válida'
    
    @staticmethod
    def GuardarMapaDeColisiones(ruta):
        widget = EventHandler.getWidget('Grilla.Canvas')
        imagen = widget.render()
        Resources.guardar_imagen(imagen,ruta)
        Sistema.estado = 'Imagen '+ruta+' guardada exitosamente'
    
    @staticmethod
    def addItem(nombre,ruta,grupo,code):
        root = Sistema.PROYECTO.script[grupo]
        if nombre not in root:
            root[nombre] = [[]]
            index = 0
            Sistema.addRef(nombre,ruta,code)
        else:
            if Sistema.PROYECTO.script['refs'][nombre]['code'] == code:
                root[nombre].append([])
                index = len(root[nombre])-1
            else:
                nombre+='_'+str(len(Sistema.PROYECTO.script['refs']))
                index = Sistema.addItem(nombre,ruta,grupo,code)
                
        return index
    
    @staticmethod
    def updateItemPos(nombre,grupo,index,pos,layer=0,rot=0):
        x,y = pos
        Sistema.PROYECTO.script[grupo][nombre][index] = x,y,layer,rot
    
    @staticmethod
    def addRef(nombre,ruta,code):
        #chapuza: nombre deberia ser distinto de filename.
        if nombre not in Sistema.PROYECTO.script['refs']:
            Sistema.PROYECTO.script['refs'][nombre] = {'ruta':ruta,'code':code}
            
    @staticmethod
    def nuevoProyecto(data):
        Sistema.cerrarProyecto()
        Sistema.referencias.update(data)
        Sistema.HabilitarTodo = True
        Sistema.PROYECTO = Proyecto(data)
    
    def abrirProyecto(ruta):
        data = Resources.abrir_json(ruta)
        Sistema.PROYECTO = Proyecto(data)
        
        for key in data:
            Sistema.PROYECTO[key] = data[key]
            Sistema.ruta = data[key]
            if key == 'fondo':
                if data[key] != "":
                    Sistema.cargar_imagen(LAYER_FONDO)
                    Sistema.capa_actual = LAYER_FONDO
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
                Sistema.referencias = data[key]
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
        Sistema.PROYECTO = None
        Sistema.IMG_FONDO = None
        Sistema.HabilitarTodo = False
        EventHandler.contents.update()
    
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
    def cortar():
        elemento = Sistema.selected
        if elemento != None:
            parent = EventHandler.getWidget(elemento.parent)
            Sistema.Portapapeles.cortar(elemento)
            parent.tiles.remove(elemento)
        
    @staticmethod
    def copiar():
        elemento = Sistema.selected
        if elemento != None:
            Sistema.Portapapeles.copiar(elemento.copiar())
        
    @staticmethod
    def pegar():
        widget = EventHandler.getWidget('Grilla.Canvas')
        Sistema.Portapapeles.pegar(widget)
    
    @staticmethod
    def update():
        key = EventHandler.key
        Sistema.KeyCombinations.clear()
        
        if key != None:
            if EventHandler.control:
                Sistema.KeyCombinations.append('Ctrl')
            if EventHandler.alt:
                Sistema.KeyCombinations.append('Alt')
            Sistema.KeyCombinations.append(key.upper())
        
        if Sistema.KeyCombinations != []:
            combination = '+'.join(Sistema.KeyCombinations)
            for widget in EventHandler.contents:
                if type(widget.KeyCombination) == str:
                    if combination == widget.KeyCombination:
                        print('anda!')
                else:
                    widget.KeyCombination(combination)
                   
