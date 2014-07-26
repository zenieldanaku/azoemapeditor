from .simboloVirtual import SimboloVirtual
from .simboloBase import SimboloBase
from globales import EventHandler
from widgets import ContextMenu
from pygame import mouse

class MetaSimbolo(SimboloBase):
    '''Metaclass para no repetir onMouseOver'''
    
    def onMouseOver(self):
        if self.pressed:
            pos = mouse.get_pos()
            dx,dy = self._arrastrar()
            if dx != 0 or dy != 0:
                self.copia = SimboloVirtual(self,self.image.copy(),pos,self.data)
                EventHandler.setFocus(self.copia)
                self.pressed = False
        else:
            pass #showTooltip()

class SimboloSimple (MetaSimbolo):
    copiar = False
    
    def __init__(self,parent,data,**opciones):
        super().__init__(parent,data,**opciones)
        self.image = self._imagen.copy()
        self.context = ContextMenu(self)

class SimboloMultiple(MetaSimbolo):
    def __init__(self,parent,data,**opciones):
        self.images = self.cargar_anims(data['imagenes'],['S','I','D'])
        data['image'] = self.images['Sabajo']
        super().__init__(parent,data,**opciones)
        self.image = self._imagen.copy()
        
        cmds = [
            {'nom':"Arriba",'cmd':lambda:self.cambiar_imagen('arriba')},
            {'nom':"Abajo",'cmd':lambda:self.cambiar_imagen('abajo')},
            {'nom':"Izquierda",'cmd':lambda:self.cambiar_imagen('izquierda')},
            {'nom':"Derecha",'cmd':lambda:self.cambiar_imagen('derecha')}]
        
        self.context = ContextMenu(self,cmds)
    
    def cambiar_imagen(self,direccion):
        self.image = self.images['S'+direccion]
        self.data['image'] = self.image
    
    @staticmethod
    def cargar_anims(spritesheet,seq,alpha=False):
        dicc,keys = {},[]
        dires = ['abajo','arriba','izquierda','derecha']
        
        for L in seq:
            for D in dires:
                keys.append(L+D)
        
        for key in keys:
            dicc[key] = spritesheet[keys.index(key)]
            
        return dicc

