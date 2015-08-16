from globales import Sistema as Sys
from azoe import EventHandler
from .simboloBase import SimboloBase
from pygame import PixelArray, mouse
from azoe.widgets import Alerta

class SimboloVirtual(SimboloBase):
    copiar = False
    x,y = 0,0
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
            EventHandler.addWidget(self)
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
        self.x,self.y = mouse.get_pos()
        if self.datos['colisiones'] is None:
            texto = 'El símbolo '+self.datos['nombre']+' carece de un mapa de colisiones.\n¿Desea continuar de todos modos?'
            copiar = self.copy
            eliminar = lambda:EventHandler.delWidget(self)
            
            Sys.DiagBox = Alerta(texto, copiar,eliminar)
        else:
            self.copiar = True
            
    def copy(self):
        x,y = self.x,self.y
        widget = EventHandler.getWidget('Grilla.Canvas')
        if widget.rect.collidepoint((x,y)):
            self.datos['rect'] = self.rect.copy()
            self.datos['original'] = True
            widget.colocar_tile(self.datos)
            EventHandler.delWidget(self)
    
    def update(self):
        if self.pressed:
            self.dirty = 1
        elif self.copiar:
            self.copy()