from libs.textrect import render_textrect
from pygame import font,Rect,draw,Surface, Color 
from . import BaseWidget
from colores import color

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
        colorBLuz    = color(self.opciones['colorBordeLuz'])
        colorBSombra = color(self.opciones['colorBordeSombra'])
            
        self.img_uns = self._biselar(self._crear(scr, colorTexto, colorFondo,self.w,self.h),colorBLuz,colorBSombra)
        self.img_sel = self._biselar(self._crear(scr, colorSText, colorFondo,self.w,self.h),colorBLuz,colorBSombra)
        self.img_pre = self._biselar(self._crear(scr, colorSText, colorFondo,self.w,self.h),colorBSombra,colorBLuz)
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
        if 'w' not in opciones:
            opciones['w'] = 28
        if 'h' not in opciones:
            opciones['h'] = 25
        return opciones
    
    @staticmethod
    def  _crear(scr, color_texto, color_fondo,w,h):
        _rect = Rect(-1,-1,w,h)
        if type (scr) == str:
            fuente = font.SysFont('verdana',16)        
            render = render_textrect(scr,fuente,_rect,color_texto,color_fondo,1)
        elif type (scr) == Surface:
            if scr.get_widht() > w or scr.get_height() > h:
                render = scr.copy()
        return render
    
    def serElegido(self):
        self.image = self.img_sel
    
    def serDeselegido(self):
        self.image = self.img_uns
        self.presionado = False
    
    def serPresionado(self):
        self.image = self.img_pre
        self.presionado = True
    
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
        if self.hasMouseOver:
            self.serElegido()
            self.comando()