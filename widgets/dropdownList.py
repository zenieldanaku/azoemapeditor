from . import BaseWidget, Entry, BaseOpcion
from pygame import Surface,draw, Rect,font, mouse
from pygame.sprite import LayeredDirty,DirtySprite
from libs.textrect import render_textrect
from colores import color
from constantes import *

class DropDownList(BaseWidget):
    componentes = None # LayeredDirty
    def __init__(self,parent,nombre,x,y,w,lista,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.DropDownList.'+nombre
        self.layer = self.parent.layer +1
        self.x,self.y = x,y
        self.componentes = LayeredDirty()
        self.entry = Entry(self,nombre,0,0,w-18)
        self.w,self.h = w,self.entry.h
        self.flecha = _Flecha(self,18)
        self.collapsedRect = Rect(self.x,self.y,self.w,self.h)
        self.rect = self.collapsedRect
        self.componentes.add(self.flecha,self.entry)
        self.image = Surface((self.w,self.crearLista(lista)+2))
        self.image.fill((255,0,0)) #fill with some transparent
        self.image.set_colorkey((255,0,0)) # color
        self.openRect = Rect((self.x,self.y),self.image.get_size())
        self.dirty = 1
        self.ItemActual = ''
    
    def crearLista(self,opciones):        
        alto,h = 0,0
        for n in range(len(opciones)):
            nom = opciones[n]
            dy = self.h+(n*h)-19
            opcion = _Opcion(self,nom,4,dy,self.w-23)
            opcion.layer = self.layer +50
            h = opcion.image.get_height()-1
            alto += h
            self.componentes.add(opcion)
        return alto
    
    def setText(self,texto):
        self.entry.setText(texto)
        # acá podría stripearse el texto, si fuera onda Archivo de mapa (*.json)
        # extrayendo solo el .json
        self.ItemActual = texto
    
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
    
    def onMouseUp(self,button):
        if button == 1:
            item = self.get_component()
            if item != self:
                item.onMouseUp(button)
    
    def onMouseIn(self):
        item = self.get_component()
        if item != self:
            for opcion in self.componentes:
                if isinstance(opcion,_Opcion):
                    opcion.onMouseOut()
            item.onMouseIn()

    def showItems(self):
        for item in self.componentes:
            if isinstance(item,_Opcion):
                item.visible = True
                item.enabled = True
        self.rect = self.openRect
    
    def hideItems(self):
        for item in self.componentes:
            if isinstance(item,_Opcion):
                item.visible = False
                item.enabled = False
        self.rect = self.collapsedRect
    
    def update(self):
        self.image.fill((255,0,0)) #clear with transparent color
        self.componentes.update()
        self.componentes.draw(self.image)
        self.dirty = 2

class _Flecha(BaseWidget):
    def __init__(self,parent,w,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = parent.nombre+'.flecha'
        self.w,self.h = w,self.parent.h
        self.x,self.y = self.parent.w-self.w,0
        cF,cB = color('sysScrArrow'),color('sysElmFace') # cFlecha,cBackground
        cL,cS = color('sysElmLight'),color('sysElmShadow') # cLuz,cSombra
        self.img_pre = self._biselar(self._crear(self.w,self.h,cF,cB),cS,cL)
        self.img_uns = self._biselar(self._crear(self.w,self.h,cF,cB),cL,cS)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _crear(w,h,cFlecha,cFondo):
        imagen = Surface((w,h))
        imagen.fill(cFondo)
        points = [[4,7],[w//2-1,h-9],[w-6,7]]
        draw.polygon(imagen,cFlecha,points)
        return imagen
      
    def onMouseDown(self,dummy):
        self.image = self.img_pre
        self.parent.showItems()
    
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
        self.parent.hideItems()
            
    def update(self):
        if self.hasMouseOver:
            self.image = self.img_sel
        else:
            self.image = self.img_des
            
        self.dirty = 1