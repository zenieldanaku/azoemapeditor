from .basewidget import BaseWidget
from libs.textrect import render_textrect
from pygame import Rect,font,mouse
from constantes import *

class Boton (BaseWidget):
    nombre = ''
    img_uns = None
    img_sel = None
    img_pre = None
    isSelected = False
    direcciones = {}
    
    def __init__(self,w,h,nombre='',texto='',imagen=None):
        super().__init__()
        self.direcciones = {}
        self.nombre = nombre
        sel,pre,uns = self._crear(w,h,texto,imagen)
        self.img_sel = sel
        self.img_pre = pre
        self.img_uns = uns
        self.image = self.img_uns
        self.rect = self.image.get_rect()
    
    def _crear(self,alto,ancho,texto='',imagen=None):        
        rect = Rect((0,0),((ancho)-6,alto-6))
        
        cnvs_pre = Surface(((ancho)+6,alto+6))
        cnvs_pre.fill(self.bg_cnvs)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        
        fnd_pre = self.crear_inverted_canvas(ancho,alto) # !
        fnd_uns = self.crear_canvas(ancho,alto) # !
        
        for i in range(round(((ancho)+6)/3)):
            #linea punteada horizontal superior
            draw.line(cnvs_sel,self.font_high_color,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(cnvs_sel,self.font_high_color,(i*7,alto+4),((i*7)+5,alto+4),2)
        
        for i in range(round((alto+6)/3)):
            #linea punteada vertical derecha
            draw.line(cnvs_sel,self.font_high_color,(0,i*7),(0,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(cnvs_sel,self.font_high_color,(ancho+4,i*7),(ancho+4,(i*7)+5),2)
        
        cnvs_sel.blit(fnd_uns,(3,3))
        cnvs_uns.blit(fnd_uns,(3,3))
        cnvs_pre.blit(fnd_pre,(3,3))
        
        if texto:
            font_se = font.SysFont('verdana', 16, bold = True)
            font_un = font.SysFont('verdana', 16)
            
            btn_sel = render_textrect(texto,font_se,rect,self.font_high_color,self.bg_cnvs,1)
            btn_uns = render_textrect(texto,font_un,rect,self.font_none_color,self.bg_cnvs,1)
        
        elif imagen:
            btn_sel = imagen
            btn_uns = imagen
        
        cnvs_uns.blit(btn_uns,(6,6))
        cnvs_sel.blit(btn_sel,(6,6))
        cnvs_pre.blit(btn_sel,(6,6))
        
        return cnvs_sel,cnvs_pre,cnvs_uns

    def serPresionado (self):
        self.image = self.img_pre
        self.isSelected = True
        self.dirty = 1
    
    def serElegido(self):
        self.image = self.img_sel
        self.isSelected = True
        self.dirty = 1
        
    def serDeselegido(self):
        self.image = self.img_uns
        self.isSelected = False
        self.dirty = 1
    
    def __repr__(self):
        return self.nombre+' _boton DirtySprite'