from pygame import Rect,Surface,mouse,draw
from . import BaseWidget, Boton
from renderer import Renderer
from colores import color
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
        self.dirty = 1
    
    def onDestruction(self):
        Renderer.delWidget(self.cursor)
        Renderer.delWidget(self.BtnPos)
        Renderer.delWidget(self.BtnNeg)

    def _crear(self,w,h):
        imagen = Surface((w,h))
        imagen.fill(color('sysScrBack'))
        return imagen
    
    def onMouseDown(self,button):
        if button == 1:
            self.cursor.pressed = True
    
    def onMouseOut(self):
        if not self.cursor.pressed:
            super().onMouseOut()
    
    def setCursorSpeed(self,velocidad):
        self.cursor.velocidad = velocidad
    
    def update(self):
        self.cursor.enabled = self.enabled
        self.dirty = 1

class ScrollV(_baseScroll):
    def __init__(self,parent,x,y,h,w=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = self.parent.nombre+'.ScrollV'
        self.BtnPos = _btnVer(self,self.x,self.y+self.h-12,'abajo')
        self.BtnNeg = _btnVer(self,self.x,self.y,'arriba')
        self.cursor = CursorV(self,parent,self.x,self.y+12,1/2*C)
        Renderer.addWidget(self.BtnPos,4)
        Renderer.addWidget(self.BtnNeg,4)
        Renderer.addWidget(self.cursor,3)

class ScrollH(_baseScroll):
    def __init__(self,parent,x,y,w,h=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = self.parent.nombre+'.ScrollH'
        self.BtnPos = _btnHor(self,self.x+self.w-12,self.y,'derecha')
        self.BtnNeg = _btnHor(self,self.x,self.y,'izquierda')
        self.cursor = CursorH(self,parent,self.x+12,self.y,1/2*C)
        Renderer.addWidget(self.BtnPos,4)
        Renderer.addWidget(self.BtnNeg,4)
        Renderer.addWidget(self.cursor,3)

class _baseCursor(BaseWidget):
    parent = None
    pressed = False
    minX,minY = 0,0
    maxX,maxY = 0,0
    velocidad = 2
    def __init__(self,parent,x,y,w,h):
        super().__init__()
        self.parent = parent
        self.x,self.y = x,y
        self.w,self.h = w,h
        cF,cL,cS = color('sysElmFace'),color('sysElmLight'),color('sysElmShadow') 
        self.image = self._biselar(self._agregar_barras(self._crear(w,h,cF),cL,cS),cL,cS)
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.pressed = False
        self.dirty = 1
    
    @staticmethod
    def _crear(w,h,color):
        imagen = Surface((w,h)) # crear la base absoluta
        imagen.fill(color)
        return imagen

    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
    
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
    
    def update(self):
        self.visible = self.enabled
        self.dirty = 1
        
class CursorH(_baseCursor):
    def __init__(self,parent,scrollable,x,y,w,h=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = parent.nombre+'.CursorH'
        self.scrollable = scrollable
        self.minX = int(parent.x+parent.BtnNeg.w)
        self.maxX = parent.x+parent.w-self.w-parent.BtnPos.w
        self.relX = 0
        
    @staticmethod
    def _agregar_barras(imagen,c1,c2):
        '''Agrega 6 barritas de "agarre" verticales'''
        w,h = imagen.get_size()
        for i in range(-4,3,1):
            if i%2 != 0: color = c1
            else: color = c2
            draw.line(imagen,color,(w//2+i,2),(w//2+i,h-4))
        return imagen
    
    def onMouseOver(self):
        if self.pressed:
            x,y = mouse.get_pos()
            dx = x-self.rect.x-8
            self.mover(dx)
    
    def mover(self,dx):
        x = self.rect.x+dx
        if self.minX <= x <= self.maxX:
            self.rect.x = x
            self.scrollable.scroll(dx=dx)
        
class CursorV(_baseCursor):
    def __init__(self,parent,scrollable,x,y,h,w=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = parent.nombre+'.CursorV'
        self.scrollable = scrollable
        self.minY = int(parent.y+parent.BtnNeg.h)
        self.maxY = parent.y+parent.h-self.h-parent.BtnPos.h
        self.relY = 0
    
    @staticmethod
    def _agregar_barras(imagen,c1,c2):
        '''Agrega 6 barritas de "agarre" horizontales'''
        w,h = imagen.get_size()
        for i in range(-4,3,1):
            if i%2 != 0: color = c1
            else: color = c2
            draw.line(imagen,color,(2,h//2+i),(w-4,h//2+i))
        return imagen
    
    def onMouseOver(self):
        if self.pressed:
            x,y = mouse.get_pos()
            dy = y-self.rect.y-8
            self.mover(dy)
    
    def mover(self,dy):
        y = self.rect.y+dy
        if self.minY <= y <= self.maxY:
            self.rect.y = y
            self.scrollable.scroll(dy=dy)
                
class _baseBtn(BaseWidget):
    nombre = ''
    parent = None
    pressed = False
    
    def __init__(self,parent,x,y):
        super().__init__()
        self.parent = parent
        self.pressed = False
        self.x,self.y = x,y
        self.dirty = 1
    
    def serDeselegido(self):
        self.image = self.img_uns
        self.pressed = False
    
    def serPresionado(self):
        self.image = self.img_pre
        self.pressed = True
        
    def onMouseDown(self,dummy):
        if self.enabled:
            self.serPresionado()
    
    def onMouseUp(self,dummy):
        self.serDeselegido()
    
    def onMouseOver(self):
        if self.pressed:
            self.serPresionado()
    
    def update(self):
        self.enabled = self.parent.enabled
        self.dirty = 1
    
class _btnVer(_baseBtn):
    def __init__(self,parent,x,y,orientacion):
        super().__init__(parent,x,y)
        self.w,self.h = 1/2*C,12
        self.orientacion = orientacion
        self.nombre = self.parent.nombre+'.Btn.'+self.orientacion
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        self.img_pre = self._biselar(self._crear(self.w,self.h,self.orientacion),sombra,luz)
        self.img_uns = self._biselar(self._crear(self.w,self.h,self.orientacion),luz,sombra)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    
    @staticmethod
    def _crear(w,h,orientacion):
        imagen = Surface((w,h))
        imagen.fill(color('sysElmFace'))
        
        if orientacion == 'arriba':
            points = [[3,h-4],[w//2-1,2],[w-5,h-4]]
        elif orientacion == 'abajo':
            points = [[3,4],[w//2-1,h-4],[w-5,4]]

        draw.polygon(imagen, color('sysScrArrow'), points)
        return imagen
    
    def serPresionado(self):
        super().serPresionado()
        dy = self.parent.cursor.velocidad
        if self.orientacion == 'arriba':
            self.parent.cursor.mover(-dy)
        elif self.orientacion == 'abajo':
            self.parent.cursor.mover(+dy)

class _btnHor(_baseBtn):
    def __init__(self,parent,x,y,orientacion):
        super().__init__(parent,x,y)
        self.w,self.h = 12,1/2*C
        self.orientacion = orientacion
        self.nombre = self.parent.nombre+'.Btn.'+self.orientacion
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        self.img_pre = self._biselar(self._crear(self.w,self.h,self.orientacion),sombra,luz)
        self.img_uns = self._biselar(self._crear(self.w,self.h,self.orientacion),luz,sombra)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    
    @staticmethod
    def _crear(w,h,orientacion):
        imagen = Surface((w,h))
        imagen.fill(color('sysElmFace'))
        
        if orientacion == 'derecha':
            points = [[4,3],[w-4,h//2-1],[4,h-5]]
        elif orientacion == 'izquierda':
            points = [[w-5,3],[3,h//2-1],[w-5,h-5]]
        
        draw.polygon(imagen, color('sysScrArrow'), points)
        return imagen
    
    def serPresionado(self):
        super().serPresionado()
        dx = self.parent.cursor.velocidad
        if self.orientacion == 'izquierda':
            self.parent.cursor.mover(-dx)
        elif self.orientacion == 'derecha':
            self.parent.cursor.mover(+dx)

