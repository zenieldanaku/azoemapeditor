from libs.textrect import render_textrect
from pygame import font,Rect,draw,Surface
from . import BaseWidget
from colores import color, cian_claro

class Boton(BaseWidget):
    comando = None
    presionado = False
    def __init__(self,parent,x,y,nombre,cmd,scr,descripcion='', **opciones):
        if 'colorBordeSombra' not in opciones:
            opciones['colorBordeSombra'] = 'sysElmShadow'
        if 'colorBordeLuz' not in opciones:
            opciones['colorBordeLuz'] = 'sysElmLight'
        super().__init__(**opciones)
        self.x,self.y = x,y
        self.parent = parent
        self.nombre = self.parent.nombre+'.Boton.'+nombre
        self.comando = cmd
        self.descripcion = descripcion
        
        colorFondo = color(opciones.get('colorFondo', 'sysElmFace'))
        
        #TODO: cambiar medidas fijas a opciones[w] y opciones[h] 
        self.rect = Rect(x,y,28,25)
        
        self.img_uns = self._crear(scr, color(opciones.get('colorText', 'sysElmText')), colorFondo)
        self.img_sel = self._crear(scr,cian_claro, colorFondo)
        
        self.opciones['colorBordeSombra'], self.opciones['colorBordeLuz'] = self.opciones['colorBordeLuz'], self.opciones['colorBordeSombra']
        self.img_pre = self._crear(scr,cian_claro, colorFondo)
        self.opciones['colorBordeSombra'], self.opciones['colorBordeLuz'] = self.opciones['colorBordeLuz'], self.opciones['colorBordeSombra']
        
        self.image = self.img_uns
        self._dibujarBorde()
    
    def  _crear(self, scr, color_texto, color_fondo):
        if type (scr) == str:
            fuente = font.SysFont('verdana',16)
            render = render_textrect(scr,fuente,self.rect,color_texto,color_fondo,1)
        elif type (scr) == Surface:
            render = scr.copy()
        
        #esto es para reutilizar dibujarBorde con las 3 imagenes
        dummy = lambda:None
        dummy.image=render
        dummy.rect=self.rect
        dummy.opciones=self.opciones
        Boton._dibujarBorde(dummy)
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