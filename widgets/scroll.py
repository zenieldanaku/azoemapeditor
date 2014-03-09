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

    def _crear(self,w,h):
        imagen = Surface((w,h))
        # [205]*3
        imagen.fill(color('sysScrBack'))
        return imagen
    
    def onMouseDown(self,button):
        if button == 1:
            self.cursor.pressed = True
    
    def onMouseOut(self):
        if not self.cursor.pressed:
            super().onMouseOut()
    
    def moverCursor(self,x=0,y=0):
        self.cursor.rect.move_ip(x,y)
    
    def setCursorSpeed(self,velocidad):
        self.cursor.velocidad = velocidad
    
    def update(self):
        self.cursor.enabled = self.enabled
        self.dirty = 1

class ScrollV(_baseScroll):
    def __init__(self,parent,x,y,h,w=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = self.parent.nombre+'.ScrollV'
        self.cursor = CursorV(self,self.x,self.y+12,1/2*C)
        self.BtnPos = _btnVer(self,self.x,self.y+self.h-12,'abajo')
        self.BtnNeg = _btnVer(self,self.x,self.y,'arriba')
        Renderer.addWidget(self.cursor,3)
        Renderer.addWidget(self.BtnPos,4)
        Renderer.addWidget(self.BtnNeg,4)
    
    def moverCursor(self,dy):
        if 0 <= dy <= self.cursor.maxY-1:
            super().moverCursor(y=dy)
            return True
        return False

class ScrollH(_baseScroll):
    def __init__(self,parent,x,y,w,h=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = self.parent.nombre+'.ScrollH'
        self.cursor = CursorH(self,self.x+12,self.y,1/2*C)
        self.BtnPos = _btnHor(self,self.x+self.w-12,self.y,'derecha')
        self.BtnNeg = _btnHor(self,self.x,self.y,'izquierda')
        Renderer.addWidget(self.cursor,3)
        Renderer.addWidget(self.BtnPos,4)
        Renderer.addWidget(self.BtnNeg,4)
    
    def moverCursor(self,dx):
        if 0 <= dx <= self.cursor.maxX-1:
            super().moverCursor(x=dx)
            return True
        return False

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
        self.image = self._crear(self.w,self.h)
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.pressed = False
        self.dirty = 1
        
    def _crear(self,w,h):
        imagen = Surface((w,h)) # crear la base absoluta
        
        # definir los colores. 
        c0 = color('sysElmFace') 
        c1 = color('sysElmLight') 
        c2 = color('sysElmShadow') 
        
        # colorear el fondo
        imagen.fill(c0)
        
        #agregar lineas de biselado
        draw.line(imagen, c2, (0,h-2),(w-1,h-2), 2) # inferior
        draw.line(imagen, c2, (w-2,h-2),(w-2,0), 2) # derecha
        draw.lines(imagen, c1, 0, [(w-2,0),(0,0),(0,h-4)]) #superior,izquierda
        
        # función de subclase: agregar barras H o V según corresponda.
        imagen = self.agregar_barras(imagen,w,h,c1,c2)
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
    def __init__(self,parent,x,y,w,h=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = parent.nombre+'.CursorH'
        self.minX = int(parent.x+self.w+4)
        self.maxX = parent.x+parent.w-19
        
    def agregar_barras(self,imagen,w,h,c1,c2):
        '''Agrega 6 barritas de "agarre" verticales'''
        for i in range(-4,3,1):
            if i%2 != 0: color = c1
            else: color = c2
            draw.line(imagen,color,(w//2+i,2),(w//2+i,h-4))
        return imagen
    
    def onMouseOver(self):
        if self.pressed:
            x,y = mouse.get_pos()
            if self.minX <= x <= self.maxX:
                self.rect.x = x-8
                self.parent.parent.slcX = (x-(self.parent.x)-20)*1.23
        
class CursorV(_baseCursor):
    def __init__(self,parent,x,y,h,w=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = parent.nombre+'.CursorV'
        self.minY = int(parent.y+self.h+4)
        self.maxY = parent.y+parent.h-19
        
    def agregar_barras(self,imagen,w,h,c1,c2):
        '''Agrega 6 barritas de "agarre" horizontales'''
        for i in range(-4,3,1):
            if i%2 != 0: color = c1
            else: color = c2
            draw.line(imagen,color,(2,h//2+i),(w-4,h//2+i))
        return imagen
    
    def onMouseOver(self):
        if self.pressed:
            x,y = mouse.get_pos()
            if self.minY <= y <= self.maxY:
                self.rect.y = y-8
                self.parent.parent.slcY = (y-(self.parent.y)-20)*1.23
                
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
    
    def _biselar(self,imagen,c1,c2):
        imagen = imagen.copy()
        w,h = imagen.get_size()
        draw.line(imagen, c1, (0,h-2),(w-1,h-2), 2) # inferior
        draw.line(imagen, c1, (w-2,h-2),(w-2,0), 2) # derecha
        draw.lines(imagen, c2, 0, [(w-2,0),(0,0),(0,h-4)]) #superior,izquierda
        return imagen
    
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
        self.img_pre = self._biselar(self._crear(self.w,self.h,self.orientacion),luz,sombra)
        self.img_uns = self._biselar(self._crear(self.w,self.h,self.orientacion),sombra,luz)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    
    def _crear(self,w,h,orientacion):
        imagen = Surface((w,h))
        imagen.fill(color('sysElmFace'))
        
        if orientacion == 'arriba':
            points = [[3,h-4],[w//2-1,2],[w-5,h-4]]
        elif orientacion == 'abajo':
            points = [[3,4],[w//2-1,h-4],[w-5,4]]
        
        # [70]*3
        draw.polygon(imagen, color('sysScrArrow'), points)
        return imagen
    
    def serPresionado(self):
        super().serPresionado()
        dy = self.parent.cursor.velocidad
        if self.orientacion == 'arriba':
            if self.parent.moverCursor(dy= -dy):
                self.parent.parent.slcY -= dy*1.23
        elif self.orientacion == 'abajo':
            if self.parent.moverCursor(dy= +dy):
                self.parent.parent.slcY += dy*1.23

class _btnHor(_baseBtn):
    def __init__(self,parent,x,y,orientacion):
        super().__init__(parent,x,y)
        self.w,self.h = 12,1/2*C
        self.orientacion = orientacion
        self.nombre = self.parent.nombre+'.Btn.'+self.orientacion
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        self.img_pre = self._biselar(self._crear(self.w,self.h,self.orientacion),luz,sombra)
        self.img_uns = self._biselar(self._crear(self.w,self.h,self.orientacion),sombra,luz)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    
    def _crear(self,w,h,orientacion):
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
            if self.parent.moverCursor(dx= -dx):
                self.parent.parent.slcX -= dx*1.23
        elif self.orientacion == 'derecha':
            if self.parent.moverCursor(dx= +dx):
                self.parent.parent.slcX += dx*1.23

