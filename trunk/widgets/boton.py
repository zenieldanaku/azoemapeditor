from libs.textrect import render_textrect
from pygame import font,Rect,draw,Surface, Color 
from . import BaseWidget
from colores import color
from globales import Resources as r, GLOBALES as G
import os.path

class Boton(BaseWidget):
    comando = None
    presionado = False
    def __init__(self,parent,x,y,nombre,cmd,scr,descripcion='', **opciones):
        opciones = self._opcionesPorDefault(opciones)
        super().__init__(**opciones)
        self.x,self.y = x,y
        self.w,self.h = self.opciones['w'],self.opciones['h']
        self.parent = parent
        self.nombre = self.parent.nombre+'.Boton.'+nombre
        self.comando = cmd
        self.descripcion = descripcion
        
        colorFondo   = color(self.opciones['colorFondo'])
        colorTexto   = color(self.opciones['colorText'])
        colorSText   = color(self.opciones['colorSelect'])
        colorDText   = color(self.opciones['colorDisabled'])
        colorBLuz    = color(self.opciones['colorBordeLuz'])
        colorBSombra = color(self.opciones['colorBordeSombra'])
            
        self.img_uns = self._biselar(self._crear(scr, colorTexto, colorFondo,self.w,self.h),colorBLuz,colorBSombra)
        self.img_sel = self._biselar(self._crear(scr, colorSText, colorFondo,self.w,self.h),colorBLuz,colorBSombra)
        self.img_pre = self._biselar(self._crear(scr, colorSText, colorFondo,self.w,self.h),colorBSombra,colorBLuz)
        self.img_dis = self._biselar(self._crear(scr, colorDText, colorFondo,self.w,self.h),colorBLuz,colorBSombra)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _opcionesPorDefault(opciones):
        if 'colorBordeSombra' not in opciones:
            opciones['colorBordeSombra'] = 'sysElmShadow'
        if 'colorBordeLuz' not in opciones:
            opciones['colorBordeLuz'] = 'sysElmLight'
        if 'colorSelect' not in opciones:
            opciones['colorSelect'] = Color(125,255,255)
        if 'colorText' not in opciones:
            opciones['colorText'] = 'sysElmText'
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysElmFace'
        if 'colorDisabled'not in opciones:
            opciones['colorDisabled'] = 'sysDisText'
        if 'w' not in opciones:
            opciones['w'] = 28
        if 'h' not in opciones:
            opciones['h'] = 25
        
        return opciones
    
    @staticmethod
    def  _crear(scr, color_texto, color_fondo,w,h):
        _rect = Rect(-1,-1,w,h)
        if type (scr) == str:
            if os.path.isfile(scr):
                img = r.cargar_imagen(scr)
                render = Surface((img.get_width()+3,img.get_height()+4))
                render.fill(color_fondo)
                render.blit(img,(1,1))
            else:
                fuente = font.SysFont('verdana',16)
                try:
                    render = render_textrect(scr,fuente,_rect,color_texto,color_fondo,1)
                except:
                    img = fuente.render(scr,True,color_texto,color_fondo)
                    render = Surface((img.get_width()+6,img.get_height()+4))
                    render.fill(color_fondo)
                    rect_render = render.get_rect()
                    rect_img = img.get_rect(centerx=rect_render.centerx,centery=rect_render.centery-1)
                    render.blit(img,rect_img)                    
        elif type (scr) == Surface:
            if scr.get_width() < w or scr.get_height() < h:
                render = Surface((scr.get_width()+3,scr.get_height()+3))
                render.fill(color_fondo)
                render.blit(scr,(1,1))
            else:
                raise ValueError('la imagen scr es mayor que el tamaño especificado')
        return render
    
    def serElegido(self):
        if self.enabled:
            self.image = self.img_sel
    
    def serDeselegido(self):
        if self.enabled:
            self.image = self.img_uns
            self.presionado = False
    
    def serPresionado(self):
        if self.enabled:
            self.image = self.img_pre
            self.presionado = True
    
    def serDeshabilitado(self):
        if self.enabled:
            self.image = self.img_dis
            self.enabled = False
    
    def serHabilitado(self):
        if not self.enabled:
            self.image = self.img_uns
            self.enabled = True
    
    def onMouseIn(self):
        super().onMouseIn()
        self.serElegido()

    def onMouseOut(self):
        super().onMouseOut()
        self.serDeselegido()
        
    def onMouseDown(self,button):
        if button == 1:
            if self.hasMouseOver:
                self.serPresionado()
    
    def onMouseUp(self, dummy):
        if self.hasMouseOver and self.enabled:
            self.serElegido()
            self.comando()
    
    def onMouseOver(self):
        if self.enabled:
            G.estado = self.descripcion