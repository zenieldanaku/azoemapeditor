from widgets import BaseWidget, ScrollH, ScrollV, Boton, Marco, Canvas
from pygame.sprite import DirtySprite, LayeredDirty
from pygame import Surface,Rect,draw,font,K_SPACE
from globales import GLOBALES as G
from renderer import Renderer
from constantes import *
from colores import color
import os

class Grilla(Marco):
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
        self.canvas.Grilla = _grilla(self,self.x+16,self.y+16,32*C,32*C)
        self.BtnVerGr = Boton(self,3,15*C+12,'BtnVerGr',self.cmdVerGr,'Gr')
        self.BtnVerCapa = Boton(self,3,16*C+7,'BtnVerCapa',self.cmdVerCapa,'Cp')
        self.BtnVerRegla = Boton(self,3,17*C+2,'BtnVerCapa',self.cmdVerRegla,'Rg')
        self.canvas.ReglaX = ReglaH(self.canvas,self.x+15,self.y,32*C)
        self.canvas.ReglaY = ReglaV(self.canvas,self.x,self.y+15,32*C)
        self.ReglaHandler = HandlerRegla(self.canvas,self.x,self.y)
        
        self.canvas.ScrollX.enabled = False
        self.canvas.ScrollY.enabled = False
        self.BtnVerCapa.serDeshabilitado()
        self.BtnVerGr.serDeshabilitado()
        self.BtnVerRegla.serDeshabilitado()
        
        self.agregar(self.canvas)
        self.agregar(self.canvas.ScrollX)
        self.agregar(self.canvas.ScrollY)
        self.agregar(self.BtnVerGr)
        self.agregar(self.BtnVerCapa)
        self.agregar(self.BtnVerRegla)
        
    #Funciones de comando para los botones        
    def cmdVerGr(self):
        if self.verGrilla:
            self.quitar(self.canvas.Grilla)
            self.verGrilla = False
        else:
            self.agregar(self.canvas.Grilla)
            self.verGrilla = True
        
    def cmdVerCapa(self):
        self.canvas.capas.switch_layer(LAYER_COLISIONES,LAYER_FONDO)
        
    def cmdVerRegla(self):
        if self.verRegla:
            self.quitar(self.canvas.ReglaX)
            self.quitar(self.canvas.ReglaY)
            self.quitar(self.ReglaHandler)
            self.verRegla = False
            for linea in self.canvas.guias:
                linea.visible = False
        else:
            self.agregar(self.canvas.ReglaX)
            self.agregar(self.canvas.ReglaY)
            self.agregar(self.ReglaHandler)
            self.verRegla = True
            for linea in self.canvas.guias:
                linea.visible = True
   
    def update(self):        
        if G.HabilitarTodo:
            if not self.canvas.ScrollX.enabled: self.canvas.ScrollX.enabled = True
            if not self.canvas.ScrollY.enabled: self.canvas.ScrollY.enabled = True
            if not self.BtnVerCapa.enabled: self.BtnVerCapa.serHabilitado()
            if not self.BtnVerGr.enabled: self.BtnVerGr.serHabilitado()
            if not self.BtnVerRegla.enabled: self.BtnVerRegla.serHabilitado()
        else:
            if not self.canvas.ScrollX.enabled: self.canvas.ScrollX.enabled = False
            if not self.canvas.ScrollY.enabled: self.canvas.ScrollY.enabled = False
            if not self.BtnVerCapa.enabled: self.BtnVerCapa.serDeshabilitado()
            if not self.BtnVerGr.enabled: self.BtnVerGr.serDeshabilitado()
            if not self.BtnVerRegla.enabled: self.BtnVerRegla.serDeshabilitado()
        self.dirty = 1
        
class _grilla(BaseWidget):
    def __init__(self,parent,x,y,w,h,**opciones):
        super().__init__(**opciones)
        self.x,self.y = x,y
        self.parent = parent
        self.focusable = False
        self.nombre = self.parent.nombre+'._grilla'
        self.FONDO = self._crear(w,h)
        self.clip = Rect(0,0,15*C,15*C)
        self.image = self.FONDO.subsurface(self.clip)
        self.rect = self.FONDO.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _crear(w,h):
        marco = Rect(0,0,w,h)
        base = Surface(marco.size)
        _color = (100,200,100)
        for i in range(1*C,32*C,C):
            draw.line(base, _color, (i,marco.top), (i,marco.bottom),1)
            draw.line(base, _color, (marco.left,i), (marco.right,i),1)
        base.set_colorkey((0,0,0))
        
        return base
    
    def scroll(self,dx,dy):
        self.clip.y += dy
        self.clip.x += dx
        try:
            self.image.set_clip(self.clip)
            self.image = self.FONDO.subsurface(self.clip)
        except:
            self.clip.y -= dy
            self.clip.x -= dx
        
class BaseRegla(BaseWidget):
    pressed = False
    def __init__(self,parent,x,y,**opciones):
        super().__init__(**opciones)        
        self.x,self.y = x,y
        self.parent = parent
    
    @staticmethod
    def unaLinea(x,y,w,h):
        img = Surface((w,h))
        img.fill((120,255,255))
        spr = DirtySprite()
        spr.image = img
        spr.rect = spr.image.get_rect(topleft=(x,y))
        spr.dirty = 2
        return spr
        
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            self.linea = self.unaLinea(*self.lin)
            self.parent.guias.add(self.linea)
    
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
            self.parent.guias.add(self.linea)

    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()

    def onMouseOver(self):
        if self.pressed:
            self.moverLinea()

class ReglaH(BaseRegla):
    
    def __init__(self,parent,x,y,w,**opciones):
        super().__init__(parent,x,y,**opciones)
        self.nombre = self.parent.nombre+'.ReglaH'
        self.FONDO = self.crear(w)
        self.lin = 0,-2,self.parent.Tw,1
        self.w,self.h = w,self.FONDO.get_height()
        self.clip = Rect(0,0,15*C+1,self.h)
        self.image = self.FONDO.subsurface(self.clip)
        self.rect = self.image.get_rect(topleft =(self.x,self.y))
    
    @staticmethod
    def crear(w):
        fuente = font.SysFont('verdana',8)
        regla = Surface((w,C//2))
        regla.fill((255,255,255),(1,1,w-2,14))
        j = -1
        for i in range(1,31):
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

    def moverLinea(self):
        x,y = self.parent.getRelMousePos()
        self.linea.rect.y = y
    
    def scroll(self,dx):
        self.clip.x += dx
        try:
            self.image.set_clip(self.clip)
            self.image = self.FONDO.subsurface(self.clip)
        except:
            self.clip.x -= dx

class ReglaV(BaseRegla):
    def __init__(self,parent,x,y,h,**opciones):
        super().__init__(parent,x,y,**opciones)
        self.nombre = self.parent.nombre+'.ReglaV'
        self.FONDO = self.crear(h)
        self.lin = -2,0,1,self.parent.Th
        self.w,self.h = self.FONDO.get_width(),h
        self.clip = Rect(0,0,self.w,15*C+1)
        self.image = self.FONDO.subsurface(self.clip)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def crear(h):
        fuente = font.SysFont('verdana',8)
        regla = Surface((C//2,h))
        regla.fill((255,255,255),(1,1,14,h-2))
        
        j = -1
        for i in range(1,31):
            j+=1
            draw.line(regla,(0,0,0),(0,i*C),(C//2,i*C))
            digitos = [i for i in str(j*C)]
            gy = 0
            for d in range(len(digitos)):
                render = fuente.render(digitos[d],True,(0,0,0),(255,255,255))
                dy = (i-1)*C+gy+1
                regla.blit(render,(4,dy))
                gy += 9
    
        return regla
        
    def moverLinea(self):
        x,y = self.parent.getRelMousePos()
        self.linea.rect.x = x
    
    def scroll(self,dy):
        self.clip.y += dy
        try:
            self.image.set_clip(self.clip)
            self.image = self.FONDO.subsurface(self.clip)
        except:
            self.clip.y -= dy
    
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
        self.linX = -1,0,1,self.parent.Th
        self.linY = 0,-1,self.parent.Tw,1
    
    @staticmethod
    def _crear():
        imagen =  Surface((16,16))
        imagen.fill((255,255,255),(1,1,14,14))
        draw.line(imagen,(0,0,0),(0,10),(15,10))
        draw.line(imagen,(0,0,0),(10,0),(10,15))
        return imagen
    
    @staticmethod
    def unaLinea(x,y,w,h):
        img = Surface((w,h))
        img.fill((120,255,255))
        spr = DirtySprite()
        spr.image = img
        spr.rect = spr.image.get_rect(topleft=(x,y))
        spr.dirty = 2
        return spr
    
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            self.lineaX = self.unaLinea(*self.linX)
            self.lineaY = self.unaLinea(*self.linY)
            self.parent.guias.add(self.lineaX,self.lineaY)
    
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
            self.parent.guias.add(self.lineaX,self.lineaY)
    
    def onMouseIn(self):
        super().onMouseIn()
        self.ToggleSel(True)
    
    def onMouseOut(self):
        self.ToggleSel(False)
        if not self.pressed:
            super().onMouseOut()
    
    def onMouseOver(self):
        if self.pressed:
            self.moverLineas()
    
    def ToggleSel(self,select):
        if select:
            draw.line(self.image,(125,255,255),(1,10),(15,10))
            draw.line(self.image,(125,255,255),(10,1),(10,15))
        else:
            draw.line(self.image,(0,0,0),(0,10),(15,10))
            draw.line(self.image,(0,0,0),(10,0),(10,15))
    
    def moverLineas(self):
        x,y = self.parent.getRelMousePos()
        self.lineaX.rect.x = x
        self.lineaY.rect.y = y