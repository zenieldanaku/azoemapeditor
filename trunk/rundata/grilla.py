from widgets import BaseWidget, Scroll, Boton
from pygame import Surface,Rect,draw,font
from globales import GLOBALES as G
from renderer import Renderer
from constantes import *
import os

class grilla(BaseWidget):
    x,y,w,h = 0,0,0,0
    ScrollX = None
    ScrollY = None
    ver_posiciones = False
    ver_grilla = True
    _imagen = None
    
    def __init__(self):
        super().__init__()
        self.x,self.y, = (2*C)+2,2*C
        self.w,self.h = 15*C,15*C
        self.nombre = 'grilla'
        self.image = self.dibujar_base(self.w,self.h)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        
        self.ScrollX = Scroll((17*C)+8, self.y, 1/2*C, self.h, self)
        self.ScrollY = Scroll(self.x, (17*C)+8, self.w, 1/2*C, self)
        self.BtnVerPos = Boton(3,17*C+2,'Grilla.BtnVerPos',self.cmdVerPos,'V')
        self.BtnVerGr = Boton(C+1,17*C+2,'Grilla.BtnVerGr',self.cmdVerGr,'Gr')
        self.BtnVerCapa = Boton(17*C+3,17*C+4,'Grilla.BtnVerCapa',self.cmdVerCapa,'Cp')
        
        Renderer.addWidget(self)
        Renderer.addWidget(self.ScrollX)
        Renderer.addWidget(self.ScrollY)
        Renderer.addWidget(self.BtnVerPos,3)
        Renderer.addWidget(self.BtnVerGr,3)
        Renderer.addWidget(self.BtnVerCapa,3)
    
    # Funciones que dibujan la base, el marco, la grilla y las posiciones
    def dibujar_base(self,w,h):
        imagen = Surface((w,h))
        imagen.fill(gris)
        draw.rect(imagen, negro, (0,0,w-1,h-1), 2)
        return imagen
    
    def dibujar_marco(self):
        draw.rect(self.image, negro, (0,0,self.w-1,self.h-1), 2)
    
    def dibujar_grilla(self):
        marco = Rect(2,2,self.w-5,self.h-5)
        for i in range(1*C,16*C,C):
            draw.line(self.image, blanco, (i,marco.top), (i,marco.bottom),1)
            draw.line(self.image, blanco, (marco.left,i), (marco.right,i),1)
    
    def dibujar_posiciones(self):
        pos = -1
        fuente = font.SysFont('verdana',8)            
        for y in range(0,self._imagen.get_height()//32):
            for x in range(0,self._imagen.get_width()//32):    
                pos += 1
                render = fuente.render(str(pos),True,blanco)
                self.image.blit(render,(x*C+2,y*C+2))
    
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
    
    #Otras funciones importantes
    def sobreimponer_imagen(self,imagen):
        '''Impone la imagen cargada como fondo sobre la base gris'''
        self._imagen = imagen.copy()
        if imagen.get_width() > self.w or imagen.get_height() > self.h:
            imagen = imagen.subsurface((0,0,self.w,self.h))
        self.image = imagen.copy()
        self.dibujar_marco()
    
    def update(self):
        if G.IMG_actual == 'Fondo':
            if G.IMG_fondo != None:
                self.sobreimponer_imagen(G.IMG_fondo)
        elif G.IMG_actual == 'Colisiones':
            if G.IMG_colisiones != None:
                self.sobreimponer_imagen(G.IMG_colisiones)
        else: #G.IMG_actual == ''
            self.image = self.dibujar_base(self.w,self.h)
        
        if self.ver_grilla:
            self.dibujar_grilla()
        if self.ver_posiciones:
            self.dibujar_posiciones()
        
        self.dirty = 1