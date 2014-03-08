from libs.textrect import render_textrect
from pygame import font,Rect,draw
from . import BaseWidget
from colores import color, cian_claro

class Boton(BaseWidget):
    comando = None
    presionado = False
    def __init__(self,x,y,nombre,cmd,texto,descripcion='', **opciones):
        if 'colorBordeSombra' not in opciones:
            opciones['colorBordeSombra'] = 'sysElmShadow'
        if 'colorBordeLuz' not in opciones:
            opciones['colorBordeLuz'] = 'sysElmLight'
        super().__init__(**opciones)
        self.x,self.y = x,y
        self.nombre = nombre
        self.comando = cmd
        self.descripcion = descripcion
        
        colorFondo = color(opciones.get('colorFondo', 'sysElmFace'))
        
        #TODO: cambiar medidas fijas a opciones[w] y opciones[h] 
        self.rect = Rect(x,y,28,25)
        
        self.img_uns = self._crear(texto, color(opciones.get('colorText', 'sysElmText')), colorFondo)
        self.img_sel = self._crear(texto,cian_claro, colorFondo)
        
        self.opciones['colorBordeSombra'], self.opciones['colorBordeLuz'] = self.opciones['colorBordeLuz'], self.opciones['colorBordeSombra']
        self.img_pre = self._crear(texto,cian_claro, colorFondo)
        self.opciones['colorBordeSombra'], self.opciones['colorBordeLuz'] = self.opciones['colorBordeLuz'], self.opciones['colorBordeSombra']
        
        self.image = self.img_uns
        self._dibujarBorde()
    
    def  _crear(self, texto, color_texto, color_fondo):
        fuente = font.SysFont('verdana',16)
        render = render_textrect(texto,fuente,self.rect,color_texto,color_fondo,1)
        
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
    
    def update(self):
        self.dirty = 1
        
    def onMouseIn(self):
        super().onMouseIn()
        self.serElegido()

    def onMouseOut(self):
        super().onMouseOut()
        self.serDeselegido()
        
    def onMouseDown(self,button):
        if button == 1:
            self.serPresionado()
    
    def onMouseUp(self, dummy):
        self.serElegido()
        if self.presionado:
            self.comando()

    def __repr__(self):
        return 'Boton '+self.nombre