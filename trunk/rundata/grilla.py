from widgets import BaseWidget, ScrollH, ScrollV, Boton
from pygame.sprite import DirtySprite, LayeredDirty
from pygame import Surface,Rect,draw,font,K_SPACE
from globales import GLOBALES as G
from renderer import Renderer
from constantes import *
from colores import color
import os

class grilla(BaseWidget):
    x,y,w,h = 0,0,0,0
    ScrollX = None
    ScrollY = None
    BtnVerPos = None
    BtnVerGr = None
    BtnVerCapa = None
    ver_posiciones = False
    ver_grilla = True
    _imagen = None
    slcX = 0 # slc = Slicing, el "recorte" que se le hace a una imagen
    slcY = 0 # cuyas dimensiones sean mayores a 480x480 (las de la grilla)
    capas = None
    hayCambios = False
    def __init__(self):
        super().__init__()
        self.x,self.y, = 2*C+15,2*C+15
        self.w,self.h = 15*C,15*C
        self.nombre = 'Grilla'
        self.image = self.dibujar_base(self.w,self.h)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.capas = LayeredDirty()
        
        self.ScrollX = ScrollH(self,self.x, self.y+self.h, self.w)
        self.ScrollY = ScrollV(self,self.x+self.w, self.y, self.h)
        self.BtnVerPos = Boton(self,3,17*C+2,'BtnVerPos',self.cmdVerPos,'V')
        self.BtnVerGr = Boton(self,C+1,17*C+2,'BtnVerGr',self.cmdVerGr,'Gr')
        self.BtnVerCapa = Boton(self,3,16*C+8,'BtnVerCapa',self.cmdVerCapa,'Cp')
        
        self.ScrollX.enabled = False
        self.ScrollY.enabled = False
        
        Renderer.addWidget(self)
        Renderer.addWidget(self.ScrollX)
        Renderer.addWidget(self.ScrollY)
        Renderer.addWidget(self.BtnVerPos,3)
        Renderer.addWidget(self.BtnVerGr,3)
        Renderer.addWidget(self.BtnVerCapa,3)
    
    # Funciones que dibujan la base, el marco, la grilla y las posiciones
    def dibujar_base(self,w,h):
        imagen = Surface((w,h))
        imagen.fill(color('sysElmFace'))
        draw.rect(imagen, color('sysBoxBorder'), (0,0,w-1,h-1), 2)
        return imagen
    
    def dibujar_marco(self):
        draw.rect(self.image, color('sysBoxBorder'), (0,0,self.w-1,self.h-1), 2)
    
    def crear_grilla(self,imagen):
        w = imagen.get_width()
        h = imagen.get_height()
        marco = Rect(2,2,w-5,h-5)
        base = Surface(marco.size)
        for i in range(1*C,16*C,C):
            draw.line(base, color('sysBoxBack'), (i,marco.top), (i,marco.bottom),1)
            draw.line(base, color('sysBoxBack'), (marco.left,i), (marco.right,i),1)
        base.set_colorkey(negro)
        
        grilla = DirtySprite()
        grilla.image = base
        grilla.rect = grilla.image.get_rect()
        return grilla
    
    def crear_posiciones(self,imagen):
        pos = -1
        fuente = font.SysFont('verdana',8)
        if self._imagen != None:
            w = imagen.get_width()
            h = imagen.get_height()
            base = Surface((w,h))
            
            for y in range(0,h//32):
                for x in range(0,w//32):    
                    pos += 1
                    render = fuente.render(str(pos),True,blanco,negro)
                    base.blit(render,(x*C+2,y*C+2))
            base.set_colorkey(color('sysElmText'))
        
        posis = DirtySprite()
        posis.image = base
        posis.rect = posis.image.get_rect()
        return posis
    
    def crear_fondo (self,imagen):
        fondo = DirtySprite()
        fondo.image = imagen
        fondo.rect = fondo.image.get_rect()
        return fondo
        
    #Funciones de comando para los botones
    def cmdVerPos(self):
        if G.IMG_actual != '':
            self.ver_posiciones = not self.ver_posiciones
    def cmdVerGr(self):
        self.ver_grilla = not self.ver_grilla
    def cmdVerCapa(self):
        if G.IMG_actual == 'Fondo':
            G.IMG_actual = 'Colisiones'
        elif G.IMG_actual == 'Colisiones':
            G.IMG_actual = 'Fondo'
    
    # Event bindings
    
    #Otras funciones importantes
    def sobreimponer_imagen(self,imagen):
        '''Impone la imagen cargada como fondo sobre la base gris'''
        self._imagen = imagen.copy()
        if imagen.get_width() > self.w or imagen.get_height() > self.h:
            imagen = imagen.subsurface(self.slcX,self.slcY,self.w,self.h)
            self.habilitarScrolls()
        self.image = imagen.copy()
        self.dibujar_marco()
    
    def cargar_imagen(self,imagen):
        self._imagen = self.crear_fondo(imagen)
        self.grilla = self.crear_grilla(imagen)
        self.posiciones = self.crear_posiciones(imagen)
    
    def habilitarScrolls(self):
        self.ScrollX.enabled = True
        self.ScrollY.enabled = True
    
    def scroll(self,dx=0,dy=0):
        self.slcX += dx*1.23
        self.slcY += dy*1.23
    
    def huboCambios(self,hay):
        if G.IMG_actual == 'Fondo':
            if G.IMG_fondo != None:
                if self._imagen != None:
                    self.cargar_imagen(G.IMG_fondo)
                    hay = True
                else:hay = False
        elif G.IMG_actual == 'Colisiones':
            if G.IMG_colisiones != None:
                if self._imagen != None:
                    self.cargar_imagen(G.IMG_colisiones)
                    hay = True
                else:hay = False
        return hay
    
    def update(self):
        #self.hayCambios = self.huboCambios(self.hayCambios)
        #if self.hayCambios:
        #    print(self._imagen,self.grilla,self.posiciones)
        #    print('cambiar')
        if G.IMG_actual == 'Fondo':
            if G.IMG_fondo != None:
                self.sobreimponer_imagen(G.IMG_fondo)
        elif G.IMG_actual == 'Colisiones':
            if G.IMG_colisiones != None:
                self.sobreimponer_imagen(G.IMG_colisiones)
        else: #G.IMG_actual == ''
            self.image = self.dibujar_base(self.w,self.h)
        #if self.ver_grilla:
        #    self.dibujar_grilla()
        #if self.ver_posiciones:
        #    self.dibujar_posiciones()
        
        self.dirty = 1