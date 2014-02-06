from .basewidget import BaseWidget
from constantes import *
from pygame import Surface,draw
from pygame.sprite import LayeredDirty

class Marco(BaseWidget):
    contenido = None
    indexes = []
    def __init__(self,x,y,w,h,borde=True):
        self.contenido = LayeredDirty()
        super().__init__()
        self.image = Surface((w,h))
        self.image.fill(gris)
        self.rect = self.image.get_rect(topleft=(x,y))
        if borde:
            draw.rect(self.image,negro,(0,0,w-2,h-2),2)
        
        if len(self.contenido) != 0:
            self.contenido.draw(self.image)
    
    def agregar(self,objeto):
        self.contenido.add(objeto)
    
    def quitar(self,objeto):
        if objeto in self.contenido:
            self.contenido.remove(objeto)
        else:
            raise IndexError('El objeto no pertenece a este marco')
    
    def devolver(self,objeto):
        if objeto in self.contenido:
            raise IndexError('El objeto no pertenece a este marco')
        else:
            for sprite in self.contenido.sprites():
                if sprite == objeto:
                    return sprite