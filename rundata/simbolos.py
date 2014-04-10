from pygame import Rect,Surface,draw,mouse
from pygame.sprite import LayeredDirty
from widgets import Marco, BaseWidget
from renderer import Renderer
from colores import color
from constantes import *
from globales import SharedFunctions as shared

class PanelSimbolos(Marco):
    simbolos = None
    def __init__(self,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = color('sysElmFace')

        super().__init__(18*C-1,2*C,6*C,16*C-1,**opciones)
        self.nombre = 'panel_simbolos'
        self.simbolos = LayeredDirty()
        self.PrevArea = area_prev(self,self.x+3,self.y+10*C-2,self.w-6,6*C)
        ejemplo = Simbolo(self.PrevArea,16,16)
        self.PrevArea.agregarSimbolo(ejemplo)
        
class area_prev(Marco):
    simbolos = None
    def __init__(self,parent,x,y,w,h,**opciones):
        if 'colorGrilla' not in opciones:
            opciones['colorGrilla'] = (150,200,200)
        super().__init__(x,y,w,h,False,**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.AreaPrev'
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        grilla = self.opciones['colorGrilla']
        self.image = self._dibujar_grilla(self._biselar(self.image,sombra,luz),grilla)
        self.area = Rect(self.x+2,self.y+2,self.w-4,self.h-18)
        self.simbolos = LayeredDirty()
        
    @staticmethod
    def _dibujar_grilla(imagen,color):
        w,h = imagen.get_size()
        marco = Rect(0,0,w-2,h-2)
        for i in range(1*C,6*C,C):
            draw.line(imagen, color, (i,marco.top), (i,marco.bottom))
            draw.line(imagen, color, (marco.left,i), (marco.right,i))
        return imagen
    
    def agregarSimbolo(self,simbolo):
        simbolo.rect.x += self.area.x
        simbolo.rect.y += self.area.y

        if simbolo not in self.simbolos:
            self.simbolos.add(simbolo)
        self.agregar(simbolo)

class Simbolo (BaseWidget):
    pressed = False
    enArea = True
    copiar = False
    def __init__(self,parent,w,h,**opciones):
        super().__init__(**opciones)
        self.x,self.y = 0,0
        self.w,self.h = w,h
        self.parent = parent
        self.nombre = self.parent.nombre+'.Simbolo.'+'ejemplo'
        self.image = Surface((self.w,self.h))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
            if self.copiar:
                shared.copiar(self)
                shared.pegar('Grilla.Canvas')
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
    
    def onMouseOver(self):
        x,y = mouse.get_pos()
        dx = x-self.w//2
        dy = y-self.h//2
        self.enArea = self.parent.area.collidepoint(dx,dy)
        if self.pressed:
            if self.enArea:
                self.mover(dx,dy)
            elif x-self.rect.x < 0:
                self.copiar = True
        
    def mover(self,dx=0,dy=0):
        self.rect.x = dx
        self.rect.y = dy
        self.x,self.y = dx,dy
    
    def copy(self):
        copia = Simbolo(self.parent,self.w,self.h)
        return copia