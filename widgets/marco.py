from pygame.sprite import LayeredDirty
from pygame import Surface,draw
from . import BaseWidget
from colores import color
from renderer import Renderer

class Marco(BaseWidget):
    contenido = None
    indexes = []
    def __init__(self,x,y,w,h,borde=True,**opciones):
        self.contenido = LayeredDirty()
        super().__init__(**opciones)
        self.layer += 1
        self.w, self.h = w,h
        self.x, self.y = x,y
        self._layer = self.layer
        self.image = Surface((self.w, self.h))
        self.image.fill(color(opciones.get('colorFondo', 'sysElmFace')))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        Renderer.addWidget(self,self._layer)
        
        if borde:self.image = self._biselar(self.image,
                color(self.opciones.get('colorLuz','sysElmLight')),
                color(self.opciones.get('colorSombra','sysElmShadow')))
            
    def agregar(self,objeto, layer=1):
        self.contenido.add(objeto)
        Renderer.addWidget(objeto,self._layer+layer)
    
    def quitar(self,objeto):
        if objeto in self.contenido:
            self.contenido.remove(objeto)
            Renderer.delWidget(objeto)
        else:
            raise IndexError('El objeto '+objeto.nombre+' no pertenece a este marco')
    
    def devolver(self,objeto):
        if objeto in self.contenido:
            raise IndexError('El objeto '+objeto.nombre+' no pertenece a este marco')
        else:
            for sprite in self.contenido.sprites():
                if sprite == objeto:
                    return sprite
    
    def onDestruction(self):
        for widget in self.contenido:
            self.quitar(widget)