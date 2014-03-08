from pygame.sprite import LayeredDirty
from pygame import Surface,draw
from . import BaseWidget
import colores
from renderer import Renderer

class Marco(BaseWidget):
    contenido = None
    indexes = []
    def __init__(self,x,y,w,h,borde=True,**opciones):
        self.contenido = LayeredDirty()
        super().__init__(**opciones)
        self.w, self.h = w,h
        self.x, self.y = x,y
        self.image = Surface((w,h))
        
        self.image.fill(colores.color(opciones.get('colorFondo', 'sysElmFace')))
        self.rect = self.image.get_rect(topleft=(x,y))
        
        Renderer.addWidget(self)
        
        if borde:
            #draw.rect(self.image,colores.color(opciones.get('colorBorde', 'sysElmShadow')) ,(0,0,w-2,h-2),2)
            self._dibujarBorde()
        
        #cuando va a tener contenido si acaba de inicializarse?
        #if len(self.contenido) != 0:
        #    self.contenido.draw(self.image)
    
    def agregar(self,objeto, layer=1):
        self.contenido.add(objeto)
        Renderer.addWidget(objeto,self._layer+layer)
    
    def quitar(self,objeto):
        if objeto in self.contenido:
            self.contenido.remove(objeto)
            Renderer.delWidget(objeto)
        else:
            raise IndexError('El objeto no pertenece a este marco')
    
    def devolver(self,objeto):
        if objeto in self.contenido:
            raise IndexError('El objeto no pertenece a este marco')
        else:
            for sprite in self.contenido.sprites():
                if sprite == objeto:
                    return sprite