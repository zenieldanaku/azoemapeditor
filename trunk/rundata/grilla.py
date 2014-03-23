from widgets import BaseWidget, ScrollH, ScrollV, Boton, Marco, Canvas
from pygame.sprite import DirtySprite, LayeredDirty
from pygame import Surface,Rect,draw,font,K_SPACE
from globales import GLOBALES as G
from renderer import Renderer
from constantes import *
from colores import color
import os

class grilla(Marco):
    canvas = None
    ScrollX = None
    ScrollY = None
    BtnVerGr = None
    BtnVerCapa = None
    verGrilla = False
    verRegla = False
    def __init__(self):
        super().__init__(2*C,2*C,15*C+15,15*C+16,False)
        self.nombre = 'Grilla'
        self.canvas = Canvas(self,self.x+16,self.y+16,32*C,32*C,(15*C,15*C))
        self.canvas.ScrollX = ScrollH(self.canvas,self.x+16,self.y+self.h)
        self.canvas.ScrollY = ScrollV(self.canvas,self.x+self.w,self.y+16)
        self.canvas.Grilla = _grilla(self,self.x+16,self.y+16,15*C,15*C)
        self.BtnVerGr = Boton(self,3,15*C+12,'BtnVerGr',self.cmdVerGr,'Gr')
        self.BtnVerCapa = Boton(self,3,16*C+7,'BtnVerCapa',self.cmdVerCapa,'Cp')
        self.BtnVerRegla = Boton(self,3,17*C+2,'BtnVerCapa',self.cmdVerRegla,'Rg')
        self.ReglaX = ReglaH(self,self.x+16,self.y,15*C)
        self.ReglaY = ReglaV(self,self.x,self.y+16,15*C)
        self.ReglaHandler = HandlerRegla(self,self.x,self.y)
        
        self.canvas.ScrollX.enabled = False
        self.canvas.ScrollY.enabled = False
        self.BtnVerCapa.serDeshabilitado()
        self.BtnVerGr.serDeshabilitado()
        self.BtnVerRegla.serDeshabilitado()
        
        Renderer.addWidget(self)
        Renderer.addWidget(self.canvas)
        Renderer.addWidget(self.canvas.ScrollX)
        Renderer.addWidget(self.canvas.ScrollY)
        Renderer.addWidget(self.BtnVerGr,3)
        Renderer.addWidget(self.BtnVerCapa,3)
        Renderer.addWidget(self.BtnVerRegla,3)
        
    #Funciones de comando para los botones        
    def cmdVerGr(self):
        if self.verGrilla:
            self.quitar(self.canvas.Grilla)
            self.verGrilla = False
        else:
            self.agregar(self.canvas.Grilla)
            self.verGrilla = True
        
    def cmdVerCapa(self):
        self.canvas.capas.switch_layer(0,1)
        
    def cmdVerRegla(self):
        if self.verRegla:
            self.quitar(self.ReglaX)
            self.quitar(self.ReglaY)
            self.quitar(self.ReglaHandler)
            self.verRegla = False
        else:
            self.agregar(self.ReglaX)
            self.agregar(self.ReglaY)
            self.agregar(self.ReglaHandler)
            self.verRegla = True
   
    def update(self):        
        if G.HabilitarTodo:
            if not self.canvas.ScrollX.enabled: self.canvas.ScrollX.enabled = True
            if not self.canvas.ScrollY.enabled: self.canvas.ScrollY.enabled = True
            if not self.BtnVerCapa.enabled: self.BtnVerCapa.serHabilitado()
            if not self.BtnVerGr.enabled: self.BtnVerGr.serHabilitado()
            if not self.BtnVerRegla.enabled: self.BtnVerRegla.serHabilitado()
        
        self.dirty = 1
        
class _grilla(BaseWidget):
    def __init__(self,parent,x,y,w,h,**opciones):
        super().__init__(**opciones)
        self.x,self.y = x,y
        self.parent = parent
        self.focusable = False
        self.nombre = self.parent.nombre+'._grilla'
        self.image = self._crear(w,h)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _crear(w,h):
        marco = Rect(0,0,w,h)
        base = Surface(marco.size)
        for i in range(1*C,16*C,C):
            draw.line(base, (125,255,255), (i,marco.top), (i,marco.bottom),1)
            draw.line(base, (125,255,255), (marco.left,i), (marco.right,i),1)
        base.set_colorkey((0,0,0))
        
        return base

class BaseRegla(BaseWidget):
    def __init__(self,parent,x,y,**opciones):
        super().__init__(**opciones)        
        self.x,self.y = x,y
        self.parent = parent

class ReglaH(BaseRegla):
    def __init__(self,parent,x,y,w,**opciones):
        super().__init__(parent,x,y,**opciones)
        self.nombre = self.parent.nombre+'.ReglaH'
        self.image = self.crear(w)
        self.w,self.h = w,self.image.get_height()
        self.rect = self.image.get_rect(topleft =(self.x,self.y))
    
    @staticmethod
    def crear(w):
        fuente = font.SysFont('verdana',8)
        regla = Surface((w,C//2))
        regla.fill((255,255,255),(1,1,w-2,14))
        j = -1
        for i in range(1,16):
            j+=1
            draw.line(regla,(0,0,0),(i*C,0),(i*C,16))
            digitos = [i for i in str(j*C)]
            gx = 0
            for d in range(len(digitos)):
                render = fuente.render(digitos[d],True,(0,0,0),(255,255,255))
                dx = (i-1)*C+gx+4
                regla.blit(render,(dx,4))
                gx += 4
                
        return regla

class ReglaV(BaseRegla):
    def __init__(self,parent,x,y,h,**opciones):
        super().__init__(parent,x,y,**opciones)
        self.nombre = self.parent.nombre+'.ReglaV'
        self.image = self.crear(h)
        self.w,self.h = self.image.get_width(),h
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def crear(h):
        fuente = font.SysFont('verdana',8)
        regla = Surface((C//2,h))
        regla.fill((255,255,255),(1,1,14,h-2))
        
        j = -1
        for i in range(1,16):
            j+=1
            draw.line(regla,(0,0,0),(0,i*C),(16,i*C))
            digitos = [i for i in str(j*C)]
            gy = 0
            for d in range(len(digitos)):
                render = fuente.render(digitos[d],True,(0,0,0),(255,255,255))
                dy = (i-1)*C+gy+1
                regla.blit(render,(4,dy))
                gy += 9
    
        return regla

class HandlerRegla(BaseWidget):
    selected = False
    pressed = False
    def __init__(self,parent,x,y,**opciones):
        super().__init__(**opciones)        
        self.x,self.y = x,y
        self.parent = parent
        self.image = self._crear()
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.w,self.h = self.image.get_size()
    
    @staticmethod
    def _crear():
        imagen =  Surface((16,16))
        imagen.fill((255,255,255),(1,1,15,15))
        draw.line(imagen,(0,0,0),(0,10),(15,10))
        draw.line(imagen,(0,0,0),(10,0),(10,15))
        return imagen

    def onMouseDown(self,button):
        self.pressed = True
    
    def onMouseIn(self):
        super().onMouseIn()
        self.ToggleSel(True)
        self.dirty = 1
        
    def onMouseOut(self):
        super().onMouseOut()
        self.ToggleSel(False)
        self.dirty = 1
        
    def ToggleSel(self,select):
        if select:
            draw.line(self.image,(125,255,255),(1,10),(15,10))
            draw.line(self.image,(125,255,255),(10,1),(10,15))
        else:
            draw.line(self.image,(0,0,0),(0,10),(15,10))
            draw.line(self.image,(0,0,0),(10,0),(10,15))