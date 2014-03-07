from pygame import Rect,Surface,mouse,draw
from . import BaseWidget, Boton
from renderer import Renderer
from constantes import *

class _baseScroll(BaseWidget):
    nombre = ''
    parent = None
    cursor = None
    BtnPos = None # derecha, o abajo
    BtnNeg = None # izquierda, o arriba
    def __init__(self,parent,x,y,w,h):
        super().__init__()
        self.parent = parent
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.image = self._crear(self.w,self.h)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.dirty = 2

    def _crear(self,w,h):
        imagen = Surface((w,h))
        imagen.fill([205]*3)
        return imagen
    
    def onMouseDown(self,button):
        if button == 1:
            self.cursor.pressed = True
    
    def onMouseOut(self):
        if not self.cursor.pressed:
            super().onMouseOut()
    
    def update(self):
        self.dirty = 1

class ScrollV(_baseScroll):
    def __init__(self,parent,x,y,w,h):
        super().__init__(parent,x,y,w,h)
        self.nombre = self.parent.nombre+'.ScrollV'
        self.cursor = CursorV(self,self.x,self.y+self.h//2,1/2*C,1/2*C)
        self.BtnPos = _btnVer(self,self.x,self.y+self.h-12,'abajo')
        self.BtnNeg = _btnVer(self,self.x,self.y,'arriba')
        Renderer.addWidget(self.cursor,3)
        Renderer.addWidget(self.BtnPos,10)
        Renderer.addWidget(self.BtnNeg,10)

class ScrollH(_baseScroll):
    def __init__(self,parent,x,y,w,h):
        super().__init__(parent,x,y,w,h)
        self.nombre = self.parent.nombre+'.ScrollH'
        self.cursor = CursorH(self,self.x+self.w//2,self.y,1/2*C,1/2*C)
        self.BtnPos = _btnHor(self,self.x+self.w-12,self.y,'derecha')
        self.BtnNeg = _btnHor(self,self.x,self.y,'izquierda')
        Renderer.addWidget(self.cursor,3)
        Renderer.addWidget(self.BtnPos,10)
        Renderer.addWidget(self.BtnNeg,10)
        
class _baseCursor(BaseWidget):
    parent = None
    pressed = False
    def __init__(self,parent,x,y,w,h):
        super().__init__()
        self.parent = parent
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.image = self._crear(self.w,self.h)
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.pressed = False
        self.dirty = 1
        
    def _crear(self,w,h):
        imagen = Surface((w,h)) # crear la base absoluta
        # definir los colores. 
        mod = 40 # Se usa para modificar todos los colores a la vez
        c0 = [125+mod]*3 # base constantes.gris
        c1 = [150+mod]*3 # base constantes.gris_claro_bisel
        c2 = [100+mod]*3 # base constantes.gris_oscuro_bisel
        
        # colorear el fondo
        imagen.fill(c0)
        
        #agregar lineas de biselado
        draw.line(imagen, c2, (0,h-2),(w-1,h-2), 2) # inferior
        draw.line(imagen, c2, (w-2,h-2),(w-2,0), 2) # derecha
        draw.lines(imagen, c1, 0, [(w-2,0),(0,0),(0,h-4)]) #superior,izquierda
        
        # función de subclase: agregar barras H o V según corresponda.
        imagen = self.agregar_barras(imagen,w,h,c1,c2)
        return imagen

    def OnMouseDown(self,button):
        if button == 1:
            self.pressed = True

class CursorH(_baseCursor):
    def __init__(self,parent,x,y,w,h):
        super().__init__(parent,x,y,w,h)
        self.nombre = parent.nombre+'.CursorH'
        Renderer.addWidget(self,3)
        
    def agregar_barras(self,imagen,w,h,c1,c2):
        '''Agrega 6 barritas de "agarre" verticales'''
        for i in range(-3,3,1):
            if i%2 != 0: color = c1
            else: color = c2
            draw.line(imagen,color,(w//2+i,2),(w//2+i,h-4))
        return imagen

class CursorV(_baseCursor):
    def __init__(self,parent,x,y,w,h):
        super().__init__(parent,x,y,w,h)
        self.nombre = parent.nombre+'.CursorV'
        
    def agregar_barras(self,imagen,w,h,c1,c2):
        '''Agrega 6 barritas de "agarre" horizontales'''
        for i in range(-3,3,1):
            if i%2 != 0: color = c1
            else: color = c2
            draw.line(imagen,color,(2,h//2+i),(w-4,h//2+i))
        return imagen

class _baseBtn(BaseWidget):
    nombre = ''
    parent = None
    
    def __init__(self,parent,x,y):
        super().__init__()
        self.parent = parent
        self.x,self.y = x,y
        self.dirty = 1
    
    def _biselar(self,imagen,c1,c2):
        imagen = imagen.copy()
        w,h = imagen.get_size()
        draw.line(imagen, c1, (0,h-2),(w-1,h-2), 2) # inferior
        draw.line(imagen, c1, (w-2,h-2),(w-2,0), 2) # derecha
        draw.lines(imagen, c2, 0, [(w-2,0),(0,0),(0,h-4)]) #superior,izquierda
        return imagen
    
    def serDeselegido(self):
        self.image = self.img_uns
        self.dirty = 1
    
    def serPresionado(self):
        self.image = self.img_pre
        self.dirty = 1
        
    def OnMouseDown(self,dummy):
        print(self.nombre,'OnMouseDown')
        self.serPresionado()
        self.dirty = 1
    
    def onMouseUp(self,dummy):
        print(self.nombre,'OnMouseUp')
        self.serDeselegido()
        self.dirty = 1

class _btnVer(_baseBtn):
    def __init__(self,parent,x,y,orientacion):
        super().__init__(parent,x,y)
        self.w,self.h = 1/2*C,12
        self.nombre = self.parent.nombre+'.Btn.'+orientacion
        self.img_pre = self._biselar(self._crear(self.w,self.h,orientacion),[190]*3,[140]*3)
        self.img_uns = self._biselar(self._crear(self.w,self.h,orientacion),[140]*3,[190]*3)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    
    def _crear(self,w,h,orientacion):
        imagen = Surface((w,h))
        imagen.fill(([165]*3))
        
        if orientacion == 'arriba':
            points = [[3,h-4],[w//2-1,2],[w-5,h-4]]
        elif orientacion == 'abajo':
            points = [[3,4],[w//2-1,h-4],[w-5,4]]
        
        draw.polygon(imagen, ([70]*3), points)
        return imagen
    
class _btnHor(_baseBtn):
    def __init__(self,parent,x,y,orientacion):
        super().__init__(parent,x,y)
        self.w,self.h = 12,1/2*C
        self.nombre = self.parent.nombre+'.Btn.'+orientacion
        self.img_pre = self._biselar(self._crear(self.w,self.h,orientacion),[190]*3,[140]*3)
        self.img_uns = self._biselar(self._crear(self.w,self.h,orientacion),[140]*3,[190]*3)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    
    def _crear(self,w,h,orientacion):
        imagen = Surface((w,h))
        imagen.fill(([165]*3))
        
        if orientacion == 'derecha':
            points = [[4,3],[w-4,h//2-1],[4,h-5]]
        elif orientacion == 'izquierda':
            points = [[w-5,3],[3,h//2-1],[w-5,h-5]]
        
        draw.polygon(imagen, ([70]*3), points)
        return imagen