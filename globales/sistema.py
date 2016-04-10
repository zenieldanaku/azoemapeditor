from azoe.engine.RLE import decode, descomprimir, deserialize
from azoe.engine import Resources, EventHandler, Portapapeles
from .constantes import LAYER_FONDO, LAYER_COLISIONES, C
from pygame import image, quit as py_quit, Rect, mouse
from pygame.sprite import DirtySprite
from sys import exit as sys_exit
from os import getcwd, path
from .mapa import Proyecto

class Sistema:
    PROYECTO = None
    estado = ''
    referencias = {'fondo':None,'colisiones':None,
                   'props':None,'mobs':None,'ambiente':None}
    KeyCombinations = []
    IMG_FONDO = None
    capa_actual = None
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
        widget = EventHandler.get_widget('Grilla.Canvas')
        imagen = widget.render()
        Resources.guardar_imagen(imagen,ruta)
        cls.estado = 'Imagen '+ruta+' guardada exitosamente'
        cls.PROYECTO.script['colisiones'] = ruta
    
    @classmethod
    def nuevoProyecto(cls,data):
        cls.cerrarProyecto()
        cls.referencias.update(data)
        cls.habilitar_todo(True)
        cls.PROYECTO = Proyecto(data)
    
    @classmethod
    def abrirProyecto(cls,ruta):
        data = Resources.abrir_json(ruta)
        cls.PROYECTO = Proyecto(data)
        cls.PROYECTO.cargar(data)
        
        for key in data:
            if key == 'fondo':
                if data[key] != "":
                    cls.setRutaFondo(data[key])
            elif key == 'props' or key == 'mobs':
                widget = EventHandler.get_widget('Grilla.Canvas')
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
                        if key == 'props':
                            w,h = sprite.get_size()
                        elif key == 'mobs':
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
        cls.habilitar_todo(True)
    
    @classmethod
    def guardarProyecto(cls,ruta):
        try:
            data = cls.PROYECTO.guardar()
            Resources.guardar_json(ruta,data,False)
            cls.estado = "Proyecto '"+ruta+"' guardado exitosamente."
            cls.Guardado = ruta
        except: 
            cls.estado ='Error: Es necesario cargar un mapa.'
    
    @classmethod
    def cerrarProyecto(cls):
        cls.PROYECTO = None
        cls.IMG_FONDO = None
        cls.habilitar_todo(False)
        for key in cls.referencias:
            cls.referencias[key] = None
        EventHandler.contents.update()
    
    @classmethod
    def exportarMapa(cls,ruta):
        try:
            mapa = cls.PROYECTO.exportarMapa()
            Resources.guardar_json(ruta,mapa)
            cls.estado = "Mapa '"+ruta+"' exportado correctamente."
        except: 
            cls.estado ='Error: No se pudo exportar el mapa.'
    
    @staticmethod
    def habilitar_todo(control):
        for nombre in EventHandler.widgets:
            if nombre == 'PanelSimbolos.AreaPrev':
                simbolos = EventHandler.widgets[nombre]
            else:
                widget = EventHandler.widgets[nombre]
                if hasattr(widget,'habilitar'):
                    widget.habilitar(control)
        simbolos.habilitar(control)
        
    @staticmethod
    def salir():
        py_quit()
        sys_exit()
    
    @classmethod
    def cortar(cls):
        elemento = cls.selected
        if elemento != None:
            parent = EventHandler.get_widget(elemento.parent)
            cls.Portapapeles.cortar(elemento)
            parent.tiles.remove(elemento)
        
    @classmethod
    def copiar(cls):
        elemento = cls.selected
        if elemento != None:
            cls.Portapapeles.copiar(elemento.copiar())
        
    @classmethod
    def pegar(cls):
        widget = EventHandler.get_widget('Grilla.Canvas')
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
                    