from globales import EventHandler, Sistema as Sys
from .simboloBase import SimboloBase
from pygame import PixelArray, mouse

class SimboloVirtual(SimboloBase):    
    def __init__(self,parent,imagen,pos,data,**opciones):
        _rect = imagen.get_rect(center=pos)
        self.datos = data
        data = {'nombre':'Virtual',
                'image':imagen,'pos':_rect.topleft}
        super().__init__(parent,data,**opciones)
        self.image = self._crear_transparencia(self._imagen)
        if not self.nombre in EventHandler.widgets:
            EventHandler.addWidget(self,20)
        self.pressed = True
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
            
    def onMouseOver(self):
        if self.pressed:
            x,y = mouse.get_pos()
            self.rect.center=(x,y)
        
    def onMouseUp(self,button):
        self.pressed = False
        Sys.copiar(self)
        x,y = mouse.get_pos()
        widget = EventHandler.getWidget('Grilla.Canvas')
        if widget.rect.collidepoint((x,y)):
            Sys.pegar(widget.nombre)
    
    def copy(self):
        self.datos['rect'] = self.rect.copy()
        self.copiar = False
        return self.datos
    
    def update(self):
        if self.pressed:
            self.dirty = 1
        else:
            EventHandler.delWidget(self)