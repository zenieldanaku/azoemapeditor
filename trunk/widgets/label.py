from libs.textrect import render_textrect
from pygame import font,Rect
from . import BaseWidget
from constantes import *

class Label (BaseWidget):
    texto = ''
    
    def __init__(self,texto='',size=14,color=(0,0,0)):
        self.texto = texto
        fuente = font.SysFont('verdana',size)
        w,h = fuente.size(self.texto)
        rect = Rect(-1,-1,w,h+1)
        self.image = render_textrect(texto,fuente,rect,color,gris)
        self.rect = self.image.get_rect()