from azoe.widgets import BaseWidget, ScrollH, ScrollV, Boton, BotonToggle, Marco, ToolTip, BotonCerrar
from globales import Sistema as Sys, C, LAYER_COLISIONES,LAYER_FONDO
from .reglas import ReglaH, ReglaV, HandlerRegla
from .SpecialCanvas import SpecialCanvas
from pygame.sprite import LayeredDirty
from pygame import Surface,Rect,draw
from azoe import EventHandler, color
import os

class Grilla(Marco):
    canvas = None
    ScrollX = None
    ScrollY = None
    BtnVerGr = None
    BtnVerCapa = None
    verGrilla = False
    verRegla = False
    layer = 1
    def __init__(self):
        self.nombre = 'Grilla'
        super().__init__(0,19,15*C+15,15*C+16,False)
        
        self.canvas = SpecialCanvas(self,self.x+16,self.y+16,15*C,15*C,(15*C,15*C))
        self.canvas.ScrollX = ScrollH(self.canvas,self.x+16,self.y+self.h)
        self.canvas.ScrollY = ScrollV(self.canvas,self.x+self.w,self.y+16)
        self.canvas.Grilla = _grilla(self,self.x+16,self.y+16,15*C,15*C)
        
        i = Sys.iconos #alias
        
        self.BtnVerCapa = BotonToggle(self,19*C+6,23,'BtnVerCapa',self.cmdVerCapa,[i['ver_fondo'],i['ver_cls'],i['ver_dis']],"Alterna entre el mapa de colisiones y la imagen de fondo")
        self.BtnVerGr = BotonToggle(self,19*C+6,C+23,'BtnVerGr',self.cmdVerGr,[i['grilla'],i['grilla_tog'],i['grilla_dis']],"Muestra u oculta la grilla")
        self.BtnCerrarMapa = BotonCerrar(self,self.w+1,self.y,15,15,'BtnCerrarMapa',Sys.cerrarProyecto)
        self.canvas.ReglaX = ReglaH(self.canvas,self.x+15,self.y,15*C)
        self.canvas.ReglaY = ReglaV(self.canvas,self.x,self.y+15,15*C)
        self.canvas.HandlerRegla = HandlerRegla(self.canvas,self.x,self.y)
        
        self.agregar(self.canvas)
        self.agregar(self.canvas.ScrollX)
        self.agregar(self.canvas.ScrollY)
        self.agregar(self.BtnCerrarMapa)
        self.agregar(self.BtnVerGr)
        self.agregar(self.BtnVerCapa)
        self.agregar(self.canvas.ReglaX)
        self.agregar(self.canvas.ReglaY)
        self.agregar(self.canvas.HandlerRegla)
        
        self.habilitar(False)
    #Funciones de comando para los botones
    def cmdVerGr(self):
        if self.verGrilla:
            self.quitar(self.canvas.Grilla)
            self.verGrilla = False
        else:
            self.agregar(self.canvas.Grilla)
            self.verGrilla = True
        
    def cmdVerCapa(self):
        capas = self.canvas.capas
        capas.switch_layer(LAYER_COLISIONES,LAYER_FONDO)
        
        if Sys.capa_actual == LAYER_FONDO:
            Sys.capa_actual = LAYER_COLISIONES
        elif Sys.capa_actual == LAYER_COLISIONES:
            Sys.capa_actual = LAYER_FONDO
    
    def habilitar(self,control):
        if control:
            self.canvas.ScrollX.enabled = True
            self.canvas.ScrollY.enabled = True
            self.BtnVerCapa.serHabilitado()
            self.BtnVerGr.serHabilitado()
            self.canvas.ReglaX.enabled = True
            self.canvas.ReglaY.enabled = True
            self.canvas.HandlerRegla.enabled = True
            self.canvas.enabled = True
        else:
            self.canvas.ScrollX.enabled = False
            self.canvas.ScrollY.enabled = False
            self.BtnVerCapa.serDeshabilitado()
            self.BtnVerGr.serDeshabilitado()
            self.canvas.ReglaX.enabled = False
            self.canvas.ReglaY.enabled = False
            self.canvas.HandlerRegla.enabled = False
            self.canvas.enabled = False
        
    def update(self):
        if Sys.PROYECTO is None:
            self.BtnCerrarMapa.serDeshabilitado()
        else:
            if not self.BtnCerrarMapa.enabled:
                self.BtnCerrarMapa.serHabilitado()

class _grilla(BaseWidget):
    
    focusable = False
    def __init__(self,parent,x,y,w,h,**opciones):
        super().__init__(parent,**opciones)
        self.x,self.y = x,y
        self.nombre = self.parent.nombre+'._grilla'
        self.FONDO = self._crear(w,h,C)
        self.clip = Rect(0,0,15*C,15*C)
        self.image = self.FONDO.subsurface(self.clip)
        self.rect = self.FONDO.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _crear(w,h,cuadro):
        marco = Rect(0,0,w,h)
        base = Surface(marco.size)
        _color = (100,200,100)
        for x in range(cuadro,(h//cuadro)*cuadro,cuadro):
            draw.line(base, _color, (x,marco.top), (x,marco.bottom),1)
        for y in range(cuadro,(w//cuadro)*cuadro,cuadro):
            draw.line(base, _color, (marco.left,y-1), (marco.right,y-1),1)
            
        base.set_colorkey((0,0,0))
        
        return base
    
    def actualizar_tamanio(self,w,h):
        self.FONDO = self._crear(w,h,C)
        self.clip.topleft = 0,0
        self.image = self.FONDO.subsurface(self.clip)
        self.dirty = 1
    
    def scroll(self,dx,dy):
        self.clip.y += dy
        self.clip.x += dx
        try:
            self.image.set_clip(self.clip)
            self.image = self.FONDO.subsurface(self.clip)
            self.dirty = 1
        except:
            self.clip.y -= dy
            self.clip.x -= dx