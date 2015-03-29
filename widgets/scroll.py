from pygame import Rect,Surface,mouse,draw
from pygame.sprite import LayeredDirty
from . import BaseWidget, Boton
from globales import color, C

class _baseScroll(BaseWidget):
    nombre = ''
    parent = None
    cursor = None
    BtnPos = None # derecha, o abajo
    BtnNeg = None # izquierda, o arriba
    componentes = None # LayeredDirty
    velocidad = 2
    def __init__(self,parent,x,y,w,h):
        super().__init__()
        self.parent = parent
        self.layer = self.parent.layer +1
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.image = self._crear(self.w,self.h)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.componentes = LayeredDirty()
        self.dirty = 1
    
    def _crear(self,w,h):
        imagen = Surface((w,h))
        imagen.fill(color('sysScrBack'))
        return imagen
    
    def getRelMousePos(self):
        abs_x,abs_y = mouse.get_pos()
        dx = abs_x-self.x
        dy = abs_y-self.y
        
        return dx,dy
    
    def get_component(self):
        x,y = self.getRelMousePos()
        if self.componentes.get_sprites_at((x,y)) != []:
            return self.componentes.get_sprites_at((x,y))[-1]
        return self
        
    def onMouseDown(self,button):
        if button == 1:
            item = self.get_component()
            if item != self:
                item.onMouseDown(button)
            #else:
            #    self.cursor.pressed = True
    
    def onMouseUp(self,button):
        if button == 1:
            item = self.get_component()
            if item != self:
                item.onMouseUp(button)
            #else:
            #    self.cursor.pressed = False
    
    def onMouseIn(self):
        super().onMouseIn()
        item = self.get_component()
        if item != self:
            super().onMouseOut()
            item.onMouseIn()
        
    def onMouseOver(self):
        #if self.cursor.pressed:
        #    self.cursor.onMouseOver()
        #else:
        item = self.get_component()
        if item != self:
            item.onMouseOver()
        
    #def onMouseOut(self):
    #    if not self.cursor.pressed:
    #        super().onMouseOut()
    
    #def setCursorSpeed(self,velocidad):
    #    self.cursor.velocidad = velocidad
    
    def update(self):
        self.tamanio_cursor()
        self.image.fill(color('sysScrBack'))
        self.componentes.update()
        self.cursor.enabled = self.enabled
        self.cursor.visible = self.enabled
        self.componentes.draw(self.image)
        self.dirty = 1

class ScrollV(_baseScroll):
    def __init__(self,parent,x,y,w=1/2*C):
        super().__init__(parent,x,y,w,parent.h)
        self.nombre = self.parent.nombre+'.ScrollV'
        self.area = Rect(0,0,self.w,self.h-12*2)
        self.BtnPos = _btnVer(self,self.h-12,'abajo')
        self.BtnNeg = _btnVer(self,0,'arriba')
        self.cursor = CursorV(self,parent,0,12,1/2*C)
        self.componentes.add(self.BtnNeg,self.BtnPos,self.cursor)

    def tamanio_cursor(self):
        doc_h = self.parent.doc_h
        win_h = self.h
        h = int(win_h/(doc_h/win_h))
        if h == win_h:
            h = 0
        
        self.cursor.actualizar_tamanio(self.cursor.w,h)
        
    def moverCursor(self,dy):
        self.cursor.mover(dy)

class ScrollH(_baseScroll):
    def __init__(self,parent,x,y,h=1/2*C):
        super().__init__(parent,x,y,parent.w,h)
        self.nombre = self.parent.nombre+'.ScrollH'
        self.area = Rect(0,0,self.w-12*2,self.h)
        self.BtnPos = _btnHor(self,self.w-12,'derecha')
        self.BtnNeg = _btnHor(self,0,'izquierda')
        self.cursor = CursorH(self,parent,12,0,1/2*C)
        self.componentes.add(self.BtnNeg,self.BtnPos,self.cursor)
        
    def tamanio_cursor(self):
        doc_w = self.parent.doc_w
        win_w = self.w
        w = int(win_w/(doc_w/win_w))
        if w == win_w:
            w = 0
        
        self.cursor.actualizar_tamanio(w,self.cursor.h)
    
    def moverCursor(self,dx):
        self.cursor.mover(dx)

class _baseCursor(BaseWidget):
    parent = None
    pressed = False
    minX,minY = 0,0
    maxX,maxY = 0,0
    dx,dy = 0,0
    
    def __init__(self,parent,x,y,w,h):
        super().__init__()
        self.parent = parent
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.crear(w,h)
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.pressed = False
        self.dirty = 1
    
    def crear(self,w,h):
        cF,cL,cS = color('sysElmFace'),color('sysElmLight'),color('sysElmShadow')
        self.image = self._biselar(self._agregar_barras(self._crear(w,h,cF),cL,cS),cL,cS)
    
    def _arrastrar(self):
        abs_x,abs_y = mouse.get_pos()
        new_x,new_y = abs_x-self.x,abs_y-self.y
        
        dx = new_x-self.px
        dy = new_y-self.py
        
        return dx,dy
    
    @staticmethod
    def _crear(w,h,color):
        imagen = Surface((w,h)) # crear la base absoluta
        imagen.fill(color)
        return imagen
    
    def actualizar_tamanio(self,new_w,new_h):
        self.w,self.h = new_w,new_h
        self.crear(new_w,new_h)
        self.rect.size = new_w,new_h
        self.maxX = self.parent.w-self.w-self.parent.BtnPos.w
        self.maxY = self.parent.h-self.h-self.parent.BtnPos.h
    
    def onMouseDown(self,button):
        if button == 1:
            x,y = mouse.get_pos()
            self.px = x-self.x
            self.py = y-self.y
            self.pressed = True
        
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
    
    def update(self):
        self.dx,self.dy = 0,0
        self.dirty = 1

class CursorH(_baseCursor):
    def __init__(self,parent,scrollable,x,y,w,h=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = parent.nombre+'.CursorH'
        self.scrollable = scrollable
        self.rel_rect = Rect((0,0),(self.w,2))
        
    @staticmethod
    def _agregar_barras(imagen,c1,c2):
        '''Agrega 6 barritas de "agarre" verticales'''
        w,h = imagen.get_size()
        for i in range(-4,3,1):
            if i%2 != 0: color = c1
            else: color = c2
            draw.line(imagen,color,(w//2+i,2),(w//2+i,h-4))
        return imagen
    
    def actualizar_tamanio(self,new_w,new_h):
        super().actualizar_tamanio(new_w,new_h)
        self.rel_rect.w = new_w
        
    def mover(self,dx):
        if self.parent.area.contains(self.rel_rect.move(dx,0)):
            self.rect.x += dx
            self.rel_rect.x += dx
            self.x += dx
            #self.mover_scrollable(dx)
    
    #def mover_scrollable(self,dx):
    #    
    #    doc_w = self.parent.parent.doc_w
    #    win_w = self.parent.w
    #    self_w = self.w # representa el ancho de la pantalla #480
    #    area_w = self.parent.area.w #es el ancho del doc. #1024
    #    print(doc_w,win_w,self_w,area_w)
    #    re = self_w*area_w/doc_w
    #    
    #    #print(self.w)
    #    self.scrollable.scroll(dx = re)
        pass
        
    def update(self):
        super().update()
        if self.pressed:
            dx,dy = self._arrastrar()
            if dx != 0:
                self.mover(dx)

class CursorV(_baseCursor):
    def __init__(self,parent,scrollable,x,y,h,w=1/2*C):
        super().__init__(parent,x,y,w,h)
        self.nombre = parent.nombre+'.CursorV'
        self.scrollable = scrollable
        self.rel_rect = Rect((0,0),(2,self.h))
    
    @staticmethod
    def _agregar_barras(imagen,c1,c2):
        '''Agrega 6 barritas de "agarre" horizontales'''
        w,h = imagen.get_size()
        for i in range(-4,3,1):
            if i%2 != 0: color = c1
            else: color = c2
            draw.line(imagen,color,(2,h//2+i),(w-4,h//2+i))
        return imagen
    
    def actualizar_tamanio(self,new_w,new_h):
        super().actualizar_tamanio(new_w,new_h)
        self.rel_rect.h = new_h
        
    def mover(self,dy):
        if self.parent.area.contains(self.rel_rect.move(0,dy)):
            self.rect.y += dy
            self.rel_rect.y += dy
            self.y += dy
            #self.scrollable.scroll(dy=dy)
    
    def update(self):
        super().update()
        if self.pressed:
            dx,dy = self._arrastrar()
            if dy != 0:
                self.mover(dy)
                
class _baseBtn(BaseWidget):
    nombre = ''
    parent = None
    pressed = False
    
    def __init__(self,parent,x,y,orientacion):
        super().__init__()
        self.parent = parent
        self.pressed = False
        self.orientacion = orientacion
        self.x,self.y = x,y
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        self.img_pre = self._biselar(self._crear(self.w,self.h,self.orientacion),sombra,luz)
        self.img_uns = self._biselar(self._crear(self.w,self.h,self.orientacion),luz,sombra)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.nombre = self.parent.nombre+'.Btn.'+self.orientacion
        self.dirty = 1
    
    def serDeselegido(self):
        self.image = self.img_uns
    
    def serPresionado(self):
        self.image = self.img_pre
        self.pressed = True
        
    def onMouseDown(self,dummy):
        if self.enabled:
            self.serPresionado()
    
    def onMouseUp(self,dummy):
        self.pressed = False
        self.serDeselegido()
    
    def update(self):
        if self.pressed:
            self.serPresionado()
        self.enabled = self.parent.enabled
        self.dirty = 1

class _btnVer(_baseBtn):
    def __init__(self,parent,y,orientacion):
        self.w,self.h = parent.w,12
        super().__init__(parent,0,y,orientacion)
    
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
        dy = self.parent.velocidad
        if self.orientacion == 'arriba':
            self.parent.parent.scroll(0,-dy)
        elif self.orientacion == 'abajo':
            self.parent.parent.scroll(0,+dy)

class _btnHor(_baseBtn):
    def __init__(self,parent,x,orientacion):
        self.w,self.h = 12,parent.h
        super().__init__(parent,x,0,orientacion)
    
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
        dx = self.parent.velocidad
        if self.orientacion == 'izquierda':
            self.parent.parent.scroll(-dx,0)
        elif self.orientacion == 'derecha':
            self.parent.parent.scroll(+dx,0)