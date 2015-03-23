from widgets import BaseWidget
from pygame import Surface, mouse

class BaseLinea (BaseWidget):
    pressed = False
    locked = False
    def __init__(self,parent,idx,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.LineaGuia'
        self.layer = self.parent.layer +1
        self.idx = idx
        self.x,self.y = self.parent.x,self.parent.y
        self.base_x,self.base_y = self.x,self.y
        #self.max_x,self.max_y = self.parent.Tw,self.parent.Th
        
        self.image = self._crear(self.w,self.h)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _crear(w,h):
        img = Surface((w,h))
        img.fill((120,255,255))
        return img
        
    def onMouseDown(self,button):
        self.pressed = True
        
    def onMouseUp(self,button):
        self.pressed = False
      
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
        
    def update(self):
        if self.pressed and not self.locked:
            self.desplazar()
        
        self.dirty = 1
    
class LineaGuiaX(BaseLinea):
    def __init__(self,parent,idx,**opciones):
        self.w = parent.Tw
        self.h = 1
        super().__init__(parent,idx,**opciones)
        self.nombre += '.W:'+str(self.idx)
        
    def desplazar(self):
        x,y = mouse.get_pos()
        if y > self.base_y:
            self.rect.y = y
    
    def actualizar_tamanio(self,nuevotamanio):
        self.w = nuevotamanio
        self.image = self._crear(self.w,self.h)
        
class LineaGuiaY(BaseLinea):
    def __init__(self,parent,idx,**opciones):
        self.w = 1
        self.h = parent.Th
        super().__init__(parent,idx,**opciones)
        self.nombre += '.H:'+str(self.idx)
        
    def desplazar(self):
        x,y = mouse.get_pos()
        if x > self.base_x:
            self.rect.x = x
    
    def actualizar_tamanio(self,nuevotamanio):
        self.h = nuevotamanio
        self.image = self._crear(self.w,self.h)