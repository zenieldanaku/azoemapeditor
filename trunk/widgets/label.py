from libs.textrect import render_textrect
from pygame import font,Rect,Surface
from colores import color
from . import BaseWidget
from constantes import *

class Label (BaseWidget):
    texto = ''
    
    def __init__(self,parent,nombre,x,y,texto = '',**opciones):
        if 'colorTexto' not in opciones:
            opciones['colorTexto'] = 'sysElmText'
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysElmFace'
        # algo más custom.. esta bien así?
        if 'Fuente' not in opciones:
            opciones['Fuente'] = 'Verdana'
        if 'fontSize' not in opciones:
            opciones['fontSize'] = 14
        
        super().__init__(**opciones)
        self.fuente = font.SysFont(opciones['Fuente'],opciones['fontSize'])
        self.x,self.y = x,y
        self.parent = parent
        self.nombre = self.parent.nombre+'.Label'+nombre
        if texto == '':
            self.w,self.h = self.fuente.size(self.texto)
            self.image = Surface((self.w,self.h))
            self.rect = self.image.get_rect(topleft = (self.x,self.y))
        else:
            self.setText(texto)
        
    def setText(self,texto,fgcolor=None,bgcolor=None):
        if fgcolor == None:
            fgcolor = color(self.opciones.get('colorTexto','sysElmText'))
        if bgcolor == None:
            bgcolor = color(self.opciones.get('colorFondo','sysElmFace'))
        w,h = self.fuente.size(texto)
        rect = Rect(self.x,self.y,w,h+1)
        self.image = render_textrect(texto,self.fuente,rect,fgcolor,bgcolor)
        self.rect = self.image.get_rect(topleft= (self.x,self.y))
        self.w,self.h = self.image.get_size()
        