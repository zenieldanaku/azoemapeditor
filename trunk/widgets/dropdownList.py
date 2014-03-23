from . import BaseWidget, Entry, BaseOpcion
from .menu import _Opcion
from renderer import Renderer
from pygame import Surface,draw, Rect,font
from pygame.sprite import LayeredDirty,DirtySprite
from libs.textrect import render_textrect
from colores import color
from constantes import *

class DropDownList(BaseWidget):
    def __init__(self,parent,nombre,x,y,w,lista,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.DropDownList.'+nombre
        self.layer = self.parent.layer +1
        self.x,self.y = x,y
        self.items = LayeredDirty()
        self.entry = Entry(self,nombre,self.x,self.y-2,w-19,'')
        self.w,self.h = w,self.entry.h
        self.flecha = _Flecha(self,self.x+self.w-18,self.y-2,18,self.h)
        self.rect = Rect(self.x,self.y,self.w,self.h)
        self.lista = self.crearLista(lista)
        self.visible = 0 # no es que sea invisible, es que no tiene imagen
        self.dirty = 1
        Renderer.addWidget(self.entry,self.layer+1)      
        Renderer.addWidget(self.flecha,self.layer+1)
        
        self.ItemActual = ''
    
    def crearLista(self,opciones):        
        alto,h = 0,0
        for n in range(len(opciones)):
            nom = opciones[n]
            dy = self.y+self.h+(n*h)-20
            opcion = _Opcion(self,nom,self.x+1,dy,self.w-21)
            h = opcion.image.get_height()
            self.items.add(opcion)
            
        for op in self.items:
            Renderer.addWidget(op,self.layer+2)
    
    def setText(self,texto):
        self.entry.setText(texto)
        # acá podría stripearse el texto, si fuera onda Archivo de mapa (*.json)
        # extrayendo solo el .json
        self.ItemActual = texto
    
    def onFocusOut(self):
        for item in self.items:
            item.visible = False
            item.enabled = False
    
    def onDestruction(self):
        Renderer.delWidget(self.entry)
        Renderer.delWidget(self.flecha)

class _Flecha(BaseWidget):
    def __init__(self,parent,x,y,w,h):
        super().__init__()
        self.parent = parent
        self.nombre = parent.nombre+'.flecha'
        self.x,self.y = x,y
        self.w,self.h = w,h
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        self.img_pre = self._biselar(self._crear(self.w,self.h),luz,sombra)
        self.img_uns = self._biselar(self._crear(self.w,self.h),sombra,luz)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    def _crear(self,w,h):
        imagen = Surface((w,h))
        imagen.fill(color('sysElmFace'))
        points = [[4,6],[w//2-1,h-8],[w-6,6]]
        draw.polygon(imagen, color('sysScrArrow'), points)
        return imagen
    
    @staticmethod
    def _biselar(imagen,c1,c2):
        imagen = imagen.copy()
        w,h = imagen.get_size()
        draw.line(imagen, c1, (0,h-2),(w-1,h-2), 2) # inferior
        draw.line(imagen, c1, (w-2,h-2),(w-2,0), 2) # derecha
        draw.lines(imagen, c2, 0, [(w-2,0),(0,0),(0,h-4)]) #superior,izquierda
        return imagen
    
    def showList(self):
        for item in self.parent.items:
            item.visible = True
            item.enabled = True
    
    def onMouseDown(self,dummy):
        self.image = self.img_pre
        self.showList()
    
    def onMouseUp(self,dummy):
        self.image = self.img_uns

class _Opcion(BaseOpcion):
    command = None
    
    def __init__(self,parent,nombre,x,y,w=0):
        super().__init__(parent,nombre,x,y,w)
        self.texto = nombre
        self.visible = False
        self.enabled = False

    def devolverTexto(self):
        self.parent.setText(self.texto)
    
    def onMouseDown(self,button):
        self.parent.onFocusOut()
        self.devolverTexto()
        
    def onFocusOut(self):
        super().onFocusOut()
        self.enabled=False
        
    def onMouseIn(self):
        if self.enabled:
            super().onMouseIn()
            self.image = self.img_sel
            self.onFocusIn()
    
    def onMouseOut(self):
        super().onMouseOut()
        self.image = self.img_des