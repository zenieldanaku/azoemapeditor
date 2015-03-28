from pygame.sprite import LayeredDirty
from pygame import Surface,draw
from . import BaseWidget
from globales import color, EventHandler

class Marco(BaseWidget):
    contenido = None
    indexes = []
    doc_w = None
    doc_h = None
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
        
        EventHandler.addWidget(self,self._layer)
        
        if borde:self.image = self._biselar(self.image,
                color(self.opciones.get('colorLuz','sysElmLight')),
                color(self.opciones.get('colorSombra','sysElmShadow')))
    
    def reubicar_en_ventana(self, dx, dy):
        for widget in self.contenido:
            widget.reubicar_en_ventana(dx, dy)
        super().reubicar_en_ventana(dx, dy)
        
    def agregar(self,objeto, layer=1):
        self.contenido.add(objeto)
        EventHandler.addWidget(objeto,self._layer+layer)
    
    def quitar(self,objeto):
        if objeto in self.contenido:
            self.contenido.remove(objeto)
            EventHandler.delWidget(objeto)
        else:
            raise IndexError('El objeto '+objeto.nombre+' no pertenece a este marco')
    
    def limpiar(self):
        for objeto in self.contenido:
            self.quitar(objeto)
    
    def cerrar(self):
        EventHandler.delWidget(self)
    
    def devolver(self,objeto):
        if objeto in self.contenido:
            raise IndexError('El objeto '+objeto.nombre+' no pertenece a este marco')
        else:
            for sprite in self.contenido.sprites():
                if sprite == objeto:
                    return sprite
    
    def __contains__(self,item):
        if item in self.contenido:
            return True
        else:
            return False
    
    def onDestruction(self):
        for widget in self.contenido:
            self.quitar(widget)
            if hasattr(widget,'tooltip'):
                if widget.tooltip is not None:
                    EventHandler.delWidget(widget.tooltip)