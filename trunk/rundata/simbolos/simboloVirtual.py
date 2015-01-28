from globales import EventHandler, Sistema as Sys
from .simboloBase import SimboloBase
from pygame import PixelArray, mouse
from widgets import Alerta

class SimboloVirtual(SimboloBase):
    copiar = False
    def __init__(self,parent,imagen,pos,data,**opciones):
        x,y,z = pos
        rot = 0
        if 'rot' in data:
            rot = data['rot']
        _rect = imagen.get_rect(center=(x,y))
        self.datos = data
        data = {'nombre':'Virtual',
                'image':imagen,'pos':[_rect.x,_rect.y,z,rot]}
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
        if self.datos['colisiones'] == None:
            Sys.DiagBox = Alerta('El símbolo '+self.datos['nombre']+' carece de un mapa de colisiones. ¿Desea continuar de todos modos?')
        else:
            self.copy()
            
    def copy(self):
        x,y = mouse.get_pos()
        widget = EventHandler.getWidget('Grilla.Canvas')
        if widget.rect.collidepoint((x,y)):
            self.datos['rect'] = self.rect.copy()
            widget.colocar_tile(self.datos)
            EventHandler.delWidget(self)
    
    def update(self):
        if self.pressed:
            self.dirty = 1
        elif self.copiar:
            self.copy()
            